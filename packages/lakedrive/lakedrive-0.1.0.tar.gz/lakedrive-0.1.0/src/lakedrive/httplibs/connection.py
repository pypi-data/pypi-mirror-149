import re
import ssl
import socket
import asyncio
import logging

from codecs import StreamReader, StreamWriter
from typing import AsyncIterator, Tuple

from .objects import HttpResponse


TIMEOUT_READ = 10


logger = logging.getLogger(__name__)


def parse_header_line(line: str) -> Tuple[str, str]:
    if not re.match("^[-a-zA-Z0-9]*: ?.*", line):
        raise ValueError("Invalid header line")

    key, value = line.split(":", 1)
    return key.lower().strip(" "), value.strip(" ")


class HttpConnection:
    """Manage an HTTP connection"""

    def __init__(self, connection_args, thread_no):
        self.connection_args = connection_args
        self.thread_no = thread_no
        self.open = False
        self.ssl_context = None

        self.connection = None
        # self.reader = None
        # self.writer = None

    def _verify_connection(self):
        """Verify if http_connection is open by checking read/write state"""
        if not self.connection:
            return False
        reader, writer = self.connection
        peer_info = writer.get_extra_info("peername")
        if peer_info is None:
            return False
        if reader.at_eof():
            return False
        return True

    async def _new_connection(self) -> Tuple[StreamReader, StreamWriter]:
        """Open a new http connection"""
        self.ssl_context = ssl.create_default_context(
            ssl.Purpose.SERVER_AUTH,
        )

        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

        # only validated ipv4, should implement and use ipv6 if possible
        connection_args_ipv4 = [
            ca for ca in self.connection_args if ca["family"] == socket.AF_INET
        ]
        self.connection = await asyncio.open_connection(
            **connection_args_ipv4[0], ssl=self.ssl_context
        )
        return self.connection

    async def get_connection(self) -> Tuple[StreamReader, StreamWriter]:
        if self._verify_connection() is False:
            return await self._new_connection()
        return self.connection

    async def write(self, data) -> Tuple[StreamReader, StreamWriter]:
        _, writer = await self.get_connection()

        writer.write(data)
        await writer.drain()
        return self.connection

    async def yield_response(self, reader):
        try:
            response = await asyncio.wait_for(reader.readuntil(), TIMEOUT_READ)
            return response.decode("latin1").rstrip()
        except asyncio.IncompleteReadError:
            logger.error(
                f"Connection IncompleteReadError,threadno:{str(self.thread_no)}"
            )
            raise
        except asyncio.TimeoutError:
            logger.error(f"Connection TimeoutError,threadno:{str(self.thread_no)}")
            raise

    async def get_response_headers(self):
        reader, _ = await self.get_connection()

        status_line = await self.yield_response(reader)
        if not re.match("^HTTP/[1-9].[0-9]* [1-5][0-9]{2} ", status_line):
            # invalid http response
            raise asyncio.IncompleteReadError(b"", None)

        response_dict = {"status_code": int(status_line.split(" ")[1])}

        while True:
            try:
                key, value = parse_header_line(await self.yield_response(reader))
            except ValueError:
                break
            response_dict[key] = value

        return HttpResponse(response_dict)

    async def get_response_headers_safe(self) -> HttpResponse:
        error_msg = ""
        try:
            http_response = await self.get_response_headers()
        except asyncio.IncompleteReadError:
            error_msg = "IncompleteReadError"
        except asyncio.TimeoutError:
            error_msg = "TimeoutError"

        if error_msg:
            http_response = HttpResponse({"status_code": 408}, error_msg=error_msg)
        elif http_response and http_response.headers.get("connection", "") != "close":
            # connection can be re-used - skip close
            return http_response

        await self.close()
        return http_response

    async def read_content(self, stream, content_lenght) -> AsyncIterator[bytes]:
        chunk_size = 1024 * 1024
        remaining = content_lenght
        while True:
            try:
                if remaining <= 0:
                    break
                if remaining <= chunk_size:
                    chunk_size = remaining
                    remaining = 0
                else:
                    remaining -= chunk_size
                chunk = await stream.readexactly(chunk_size)
                yield chunk
            except Exception as error:
                logger.error(str(error))
                raise asyncio.IncompleteReadError(b"", None)

    async def read_chunks(self, stream) -> AsyncIterator[bytes]:
        """Read chunks from chunked response."""
        while True:
            try:
                line = (await stream.readline()).rstrip()
                chunk_size = int(line, 16)
                if not chunk_size:
                    # read last CRLF
                    await stream.readline()
                    break
                chunk = await stream.readexactly(chunk_size + 2)
                yield chunk[:-2]
            except Exception as error:
                logger.error(str(error))
                raise asyncio.IncompleteReadError(b"", None)

    async def execute(self, query: bytes, retries: int = 3) -> HttpResponse:
        error_msg = ""
        while retries > 0:
            retries -= 1
            await self.write(query)
            http_response = await self.get_response_headers_safe()
            if not http_response.error_msg:
                # assume success
                return http_response
            # store last error message
            error_msg = http_response.error_msg

        # failed (retries depleted)
        await self.close()
        return HttpResponse({"status_code": 408}, error_msg=error_msg)

    async def close_stream(self, stream) -> None:
        stream.close()
        await stream.wait_closed()

    async def close(self):
        """Close connection if active/ open"""
        if self._verify_connection() is True:
            _, writer = self.connection
            await self.close_stream(writer)
