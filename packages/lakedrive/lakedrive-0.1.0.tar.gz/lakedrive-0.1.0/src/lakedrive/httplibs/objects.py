from typing import Dict, Union


class HttpResponse:
    def __init__(
        self,
        headers: Dict[str, Union[str, int]],
        body: bytes = b"",
        error_msg: str = "",
    ):
        self.status_code = int(headers.get("status_code", 503))
        self.headers = headers
        self.body = body
        self.error_msg = error_msg


class HttpResponseError(Exception):
    """Exceptions related to HttpResponse"""

    def __init__(self, http_response: HttpResponse):
        message = f"{http_response.error_msg} ({str(http_response.status_code)})"
        super().__init__(message)

        self.message = message

    def __str__(self):
        return str(self.message)
