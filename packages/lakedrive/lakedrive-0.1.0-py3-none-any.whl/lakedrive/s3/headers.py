from __future__ import unicode_literals

import hmac
import hashlib
import datetime

from urllib.parse import quote, urlparse
from dataclasses import dataclass, field
from typing import ByteString, Dict, List, Tuple, Any, OrderedDict

from lakedrive.httplibs.helpers import get_connection_args
from lakedrive.config import HTTP_BASE_HEADERS

from .objects import S3Bucket


CRLF = "\r\n"


def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def to_base16(n: int):
    """Convert base10 number to base16"""
    hex_chars = "0123456789ABCDEF"
    return "0" if not n else to_base16(n // 16).lstrip("0") + hex_chars[n % 16]


def hash_nobytes():
    return hashlib.sha256(b"").hexdigest()


@dataclass(frozen=True)
class S3ConnectConfiguration:
    bucket: S3Bucket
    credentials: Dict[str, str]
    headers: Dict[str, str] = field(default_factory=dict)
    connection_args: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self):
        if not self.headers:
            object.__setattr__(self, "headers", dict(HTTP_BASE_HEADERS))
        object.__setattr__(
            self, "connection_args", get_connection_args(self.bucket.endpoint_url)
        )


class S3Connect:
    def __init__(self, config: S3ConnectConfiguration):
        self.connection_args = config.connection_args
        self.credentials = config.credentials
        self.bucket = config.bucket
        self.bucket_url = self.bucket.endpoint_url
        self.base_headers = dict(config.headers)
        # self.session_token = kwargs.get('session_token')
        # if self.session_token:
        #     headers['x-amz-security-token'] = self.session_token

        self.initialize()

    def initialize(self):
        self.now = datetime.datetime.utcnow()
        self.dateStamp = self.now.strftime("%Y%m%d")
        self.credential_scope = f"{self.dateStamp}/{self.bucket.region}/s3/aws4_request"

        self._generate_signing_key()
        self.seed_signature = ""

        self.stream_chunk_size = 0
        self.stream_content_length = 0

        self.request_url = ""

    def _generate_signing_key(self):
        kDate = sign(
            ("AWS4" + self.credentials["secret_key"]).encode("utf-8"), self.dateStamp
        )
        kRegion = sign(kDate, self.bucket.region)
        kService = sign(kRegion, "s3")
        self.signing_key = sign(kService, "aws4_request")

        self.headers = {}

    def _get_canonical_headers(self, headers: Dict[str, str]) -> OrderedDict[str, str]:
        """
        https://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-streaming.html#example-signature-calculations-streaming
        """
        include_hdrs = set({"host", "content-type", "date", "x-amz-*"})
        canonical_headers_dict: OrderedDict = OrderedDict()
        # aws requires the header items to be sorted
        for hdr, val in sorted(headers.items()):
            if hdr in include_hdrs or (
                hdr.startswith("x-amz-") and not hdr == "x-amz-client-context"
            ):
                if hdr not in canonical_headers_dict:
                    canonical_headers_dict[hdr] = []
                canonical_headers_dict[hdr].append(val)
        return canonical_headers_dict

    def generate_headers(
        self,
        resource: str,
        query_string: str,
        method: str,
        headers: Dict[str, str] = {},
        payload_hash: str = "UNSIGNED-PAYLOAD",
    ) -> Dict:
        """

        Implementation based on the following AWS documentation:
        https://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html
        https://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-streaming.html
        """
        if not headers:
            headers = dict(self.base_headers)
        headers["x-amz-date"] = self.now.strftime("%Y%m%dT%H%M%SZ")
        headers["x-amz-content-sha256"] = payload_hash

        # Step 2: Create canonical URI--the part of the URI from domain to query
        endpoint_parsed = urlparse(self.bucket.endpoint_url)

        # canonical_uri = amz_cano_path(resource, self.service)
        canonical_uri = quote(resource, safe="/")

        # if endpoint includes a path, add this to canonical_uri
        # ensure begin and end "/" is stripped of
        endpoint_path = endpoint_parsed.path.strip("/")
        if endpoint_path:
            if canonical_uri:
                canonical_uri = "/".join([endpoint_path, canonical_uri])
            else:
                # canonical uri cant start with "/"
                canonical_uri = endpoint_path

        # Step 3: Create the canonical headers and signed headers. Header names
        # must be trimmed and lowercase, and sorted in code point order from
        # low to high. Note trailing \n in canonical_headers.
        # signed_headers is the list of headers that are being included
        # as part of the signing process. For requests that use query strings,
        # only "host" is included in the signed headers.
        # Flatten cano_headers dict to string and generate signed_headers
        headers["host"] = endpoint_parsed.netloc.split(":")[0]

        # print("Bucket:", self.bucket_url, "Host:", headers["host"])
        canonical_headers_dict = self._get_canonical_headers(headers)
        canonical_headers_str = ""
        for header in canonical_headers_dict:
            canonical_headers_str += (
                f"{header}:{','.join(sorted(canonical_headers_dict[header]))}\n"
            )
        signed_headers = ";".join(canonical_headers_dict.keys())

        # AWS handles "extreme" querystrings differently to urlparse
        # (see post-vanilla-query-nonunreserved test in aws_testsuite)
        _query_string_parts = [
            tuple(q.split("=", 1)) for q in sorted(query_string.split("&")) if q
        ]
        query_string_safe = "&".join(
            [f"{k}={quote(v, safe='')}" for k, v in _query_string_parts]
        )

        canonical_request = "\n".join(
            [
                method,
                f"/{canonical_uri}",
                query_string_safe,
                canonical_headers_str,
                signed_headers,
                payload_hash,
            ]
        )
        # print('### CANONICAL REQUEST ###\n', canonical_request, '\n######')
        # ************* 2: CREATE THE STRING TO SIGN*************
        algorithm = "AWS4-HMAC-SHA256"
        string_to_sign = "\n".join(
            [
                algorithm,
                headers["x-amz-date"],
                self.credential_scope,
                hashlib.sha256(canonical_request.encode("utf-8")).hexdigest(),
            ]
        )

        # ************* 3: CALCULATE THE SIGNATURE *************
        self.seed_signature = hmac.new(
            self.signing_key,
            string_to_sign.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        # ************* 4: ADD SIGNING INFORMATION TO THE REQUEST *************
        auth_header_str = ", ".join(
            [
                f'Credential={self.credentials["access_id"]}/{self.credential_scope}',
                f"SignedHeaders={signed_headers}",
                f"Signature={self.seed_signature}",
            ]
        )
        headers["Authorization"] = f"{algorithm} {auth_header_str}"

        self.headers = headers
        self.request_url = (
            f"{canonical_uri}?{query_string_safe}"
            if query_string_safe
            else canonical_uri
        )
        return headers

    def generate_headers_streaming(
        self,
        resource: str,
        content_length: int,
        chunk_size: int,
    ) -> Dict:
        headers = dict(self.base_headers)

        headers["x-amz-decoded-content-length"] = str(content_length)
        headers["Content-Encoding"] = "aws-chunked"

        if chunk_size < content_length:
            no_full_chunks = content_length // chunk_size
            chunk_size_remainder = content_length % chunk_size
            sig_hexlength = len(to_base16(chunk_size)) * no_full_chunks + 1
        else:
            no_full_chunks = 1
            chunk_size_remainder = 0
            sig_hexlength = len(to_base16(content_length)) * no_full_chunks + 1

        if chunk_size_remainder > 0:
            chunks_to_write = no_full_chunks + 2
            sig_hexlength += len(to_base16(chunk_size_remainder))
        else:
            chunks_to_write = no_full_chunks + 1

        body_length = (
            content_length
            + sig_hexlength
            + (len(";chunk-signature=" + CRLF * 2) + 64) * chunks_to_write
        )
        headers["Content-Length"] = str(body_length)

        self.stream_chunk_size = chunk_size
        self.stream_content_length = content_length
        return self.generate_headers(
            resource,
            "",
            "PUT",
            headers=headers,
            payload_hash="STREAMING-AWS4-HMAC-SHA256-PAYLOAD",
        )

    async def write_http_stream(
        self,
        writer,
        stream,
        content_length_buffered: int = 0,
        buffered_chunks: List[ByteString] = [],
    ) -> Tuple[bool, int, List[ByteString]]:
        # signature = self.seed_signature
        amz_date = self.headers["x-amz-date"]
        zero_hash = hash_nobytes()
        content_length_written = 0

        # re-write earlier buffered chunks
        if content_length_buffered > 0:
            chunk_buffer = buffered_chunks

            # print("Buffered chunks given:", content_length_buffered, buffered_chunks)
            for chunk in buffered_chunks:
                writer.write(chunk)
                await writer.drain()  # ensure not writing faster than data gets sent
            content_length_written += content_length_buffered
            # release memory from buffered chunks?
        else:
            chunk_buffer = []

        while True:
            try:
                chunk = bytes(await stream.__anext__())
            except StopAsyncIteration:
                # no more chunks to read, last upload is an empty chunk
                chunk = b""

            read_chunk_size = len(chunk)
            if read_chunk_size != self.stream_chunk_size:
                # if not last chunk, input size is invalid
                if (
                    content_length_written + read_chunk_size
                ) != self.stream_content_length:
                    raise Exception(
                        f"Chunk input length ({read_chunk_size}) un-expected size"
                    )

            # get hash and signature
            chunk_hash = hashlib.sha256(chunk).hexdigest()

            string_to_sign = "\n".join(
                [
                    "AWS4-HMAC-SHA256-PAYLOAD",
                    amz_date,
                    self.credential_scope,
                    self.seed_signature,
                    zero_hash,
                    chunk_hash,
                ]
            )
            self.seed_signature = hmac.new(
                self.signing_key,
                string_to_sign.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()

            sig = ";".join(
                [
                    f"{to_base16(read_chunk_size)}",
                    f"chunk-signature={self.seed_signature}{CRLF}",
                ]
            ).encode()

            data_ptr = memoryview(sig + chunk + CRLF.encode())
            chunk_buffer.append(data_ptr)

            try:
                writer.write(data_ptr)
                await writer.drain()  # ensure not writing faster than data gets sent
            except Exception as error:
                print(
                    "ERROR write_http_stream:",
                    "bytes-written=",
                    content_length_written,
                    read_chunk_size,
                    str(error),
                )
                content_length_written += read_chunk_size
                return (False, content_length_written, chunk_buffer)
                # raise(e)
            content_length_written += read_chunk_size

            if not chunk:
                # last chunk reached
                break

        if content_length_written != self.stream_content_length:
            raise Exception("Write failed, insufficient bytes written")

        return (True, content_length_written, chunk_buffer)
