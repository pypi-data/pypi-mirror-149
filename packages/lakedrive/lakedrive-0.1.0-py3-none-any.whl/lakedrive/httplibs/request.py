import ssl
import logging
import asyncio
import hashlib

from typing import ByteString, List, Callable, AsyncIterator

from gzip import decompress as gzip_decompress
from zlib import decompress as zlib_decompress

from lakedrive.core.objects import StreamObject

from .connection import HttpConnection
from .helpers import headers_to_string, bytestream_to_bytes
from .objects import HttpResponse

logger = logging.getLogger(__name__)


def update_http_response_body(http_response: HttpResponse, body: bytes) -> HttpResponse:
    content_encoding = http_response.headers.get("content-encoding", "")
    if not content_encoding:
        http_response.body = body
    elif content_encoding == "gzip":
        http_response.body = gzip_decompress(body)
    elif content_encoding == "deflated":
        http_response.body = zlib_decompress(body)
    return http_response


class HttpRequest:
    """"""

    def __init__(self, config, connections=2):
        self.ssl_context = ssl.create_default_context(
            ssl.Purpose.SERVER_AUTH,
        )
        self.config = config
        self.connections = connections
        self.locks = [asyncio.Lock() for _ in range(connections)]
        self.http_connections = [
            HttpConnection(config.connection_args, thread_no)
            for thread_no in range(connections)
        ]

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        """Exit context"""
        logger.debug("Closing connections")
        await self.close_connections()

    async def close_connections(self):
        """Closing all connections"""
        await asyncio.gather(*[conn.close() for conn in self.http_connections])

    async def head(
        self, http_class: Callable, resource: str = "", parameter_str: str = "", tid=0
    ):
        http_connection = http_class(self.config)
        headers = http_connection.generate_headers(resource, parameter_str, "HEAD")
        query = "\r\n".join(
            [
                f"HEAD /{http_connection.request_url} HTTP/1.1",
                headers_to_string(headers),
                "",
            ]
        )

        thread_no = tid % self.connections

        async with self.locks[thread_no]:
            http_conn = self.http_connections[thread_no]
            http_response = await http_conn.execute(query.encode())

        return http_response

    async def get(
        self, http_class: Callable, resource: str = "", parameter_str: str = "", tid=0
    ):
        http_connection = http_class(self.config)
        headers = http_connection.generate_headers(resource, parameter_str, "GET")

        thread_no = tid % self.connections

        query = "\r\n".join(
            [
                f"GET /{http_connection.request_url} HTTP/1.1",
                headers_to_string(headers),
                "",
            ]
        )

        async with self.locks[thread_no]:
            http_conn = self.http_connections[thread_no]

            reader, _ = await http_conn.write(query.encode())
            http_response = await http_conn.get_response_headers()
            if http_response.headers.get("connection", "").lower() == "close":
                await http_conn.close()
            else:
                content_length = int(http_response.headers.get("content-length", 0))
                try:
                    body = b""
                    if content_length > 0:
                        async for chunk in http_conn.read_content(
                            reader, content_length
                        ):
                            body += chunk
                    else:
                        async for chunk in http_conn.read_chunks(reader):
                            body += chunk
                    if body:
                        http_response = update_http_response_body(http_response, body)

                except asyncio.IncompleteReadError:
                    http_response = HttpResponse(
                        {"status_code": 408}, error_msg="IncompleteReadError"
                    )

        return http_response

    async def put(
        self,
        http_class: Callable,
        resource: str,
        parameter_str: str = "",
        body=b"",
        content_length: int = 0,
        tid: int = 0,
    ):
        http_connection = http_class(self.config)
        thread_no = tid % self.connections

        headers = http_connection.generate_headers(
            resource,
            parameter_str,
            "PUT",
            payload_hash=hashlib.sha256(body).hexdigest(),
        )
        headers["content-length"] = (
            str(len(body)) if content_length <= 0 else str(content_length)
        )

        query = "\r\n".join(
            [
                f"PUT /{http_connection.request_url} HTTP/1.1",
                headers_to_string(headers),
                "",
            ]
        )

        async with self.locks[thread_no]:
            http_conn = self.http_connections[thread_no]
            http_response = await http_conn.execute(query.encode() + body, retries=3)

        return http_response

    async def upstream(
        self, http_class: Callable, stream_object: StreamObject, thread_id=0
    ):
        """a set of HTTP connections, uses (cooperative)
        multi-tasking to minize time spent waiting on I/O,"""
        file_object = stream_object.file
        content_length = file_object.bytes

        # if chunk_size is unknown, must write directly
        # small files can be written directly
        if (
            stream_object.chunk_size == 0
            or content_length < stream_object.chunk_size
            or content_length < (1024 * 10)
        ):
            body = await bytestream_to_bytes(stream_object.data)
            return await self.put(
                http_class,
                file_object.name,
                body=body,
                content_length=content_length,
                tid=thread_id,
            )

        http_connection = http_class(self.config)
        thread_no = thread_id % self.connections

        headers = http_connection.generate_headers_streaming(
            file_object.name, content_length, stream_object.chunk_size
        )
        query = "\r\n".join(
            [
                f"PUT /{http_connection.request_url} HTTP/1.1",
                headers_to_string(headers),
                "",
            ]
        )

        buffered_chunks: List[ByteString] = []
        content_length_buffered = 0
        retries_left = 3

        async with self.locks[thread_no]:
            http_conn = self.http_connections[thread_no]

            while retries_left > 0:
                retries_left -= 1
                _, writer = await http_conn.write(query.encode())

                (
                    success,
                    content_length_buffered,
                    buffered_chunks,
                ) = await http_connection.write_http_stream(
                    writer,
                    stream_object.data,
                    content_length_buffered=content_length_buffered,
                    buffered_chunks=buffered_chunks,
                )

                if success is True:
                    http_response = await http_conn.get_response_headers_safe()
                    if not http_response.error_msg:
                        logger.debug(f"Succesful upload for {file_object.name}")
                        break

        return http_response

    async def downstream(
        self, http_class: Callable, resource: str = "", thread_id=0
    ) -> AsyncIterator:
        http_connection = http_class(self.config)
        headers = http_connection.generate_headers(resource, "", "GET")

        thread_no = thread_id % self.connections
        query = "\r\n".join(
            [
                f"GET /{http_connection.request_url} HTTP/1.1",
                headers_to_string(headers),
                "",
            ]
        )

        async with self.locks[thread_no]:
            http_conn = self.http_connections[thread_no]
            reader, _ = await http_conn.write(query.encode())

            http_response = await http_conn.get_response_headers_safe()
            content_lenght = int(http_response.headers.get("content-length", 0))

            try:
                if content_lenght > 0:
                    async for chunk in http_conn.read_content(reader, content_lenght):
                        yield chunk
                else:
                    async for chunk in http_conn.read_chunks(reader):
                        yield chunk
            except asyncio.IncompleteReadError:
                return

    async def delete(self, http_class: Callable, resource: str = "", thread_id=0):
        http_connection = http_class(self.config)
        headers = http_connection.generate_headers(resource, "", "DELETE")
        thread_no = thread_id % self.connections

        query = "\r\n".join(
            [
                f"DELETE /{http_connection.request_url} HTTP/1.1",
                headers_to_string(headers),
                "",
            ]
        )

        async with self.locks[thread_no]:
            http_conn = self.http_connections[thread_no]
            http_response = await http_conn.execute(query.encode())

        return http_response
