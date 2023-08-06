import socket
import logging
from io import BytesIO
from urllib.parse import urlparse
from typing import Dict, List, Any, AsyncIterator


logger = logging.getLogger(__name__)


async def bytestream_to_bytes(stream_in: AsyncIterator) -> bytes:
    stream_out = BytesIO()
    async for chunk in stream_in:
        stream_out.write(chunk)
    return stream_out.getvalue()


def headers_to_string(headers: Dict[str, str]) -> str:
    headers_str = ""
    for key, value in headers.items():
        headers_str += f"{key}: {value}\r\n"
    return headers_str


def get_connection_args(url_string: str) -> List[Dict[str, Any]]:
    logger.debug(f"Parsing url: {url_string}")
    url = urlparse(url_string)

    assert url.hostname != ""
    assert url.scheme in ["https", "http"]

    if url.port:
        port = url.port
    elif url.scheme == "http":
        port = 80
    else:
        port = 443

    tcp_addresses = [
        (addr[0], addr[4][0])
        for addr in socket.getaddrinfo(url.hostname, port)
        if addr[2] == 6
    ]

    return [
        {
            "host": address,
            "port": port,
            "family": family,
            "proto": 6,
            "flags": socket.AI_NUMERICHOST | socket.AI_NUMERICSERV,
            "server_hostname": url.hostname,
        }
        for family, address in tcp_addresses
    ]
