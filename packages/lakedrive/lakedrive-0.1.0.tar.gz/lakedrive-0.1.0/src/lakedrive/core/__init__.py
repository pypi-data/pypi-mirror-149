import re
import asyncio

from typing import List, Dict

from .objects import FileObject

from .handlers import SchemeError
from lakedrive.localfs.handler import LocalFileHandler
from lakedrive.s3.handler import S3Handler


def get_scheme_handler(location: str, credentials: Dict[str, str] = {}):
    if re.match("^s3://", location):
        return asyncio.run(S3Handler(location, credentials=credentials).__ainit__())
    elif not re.match("^[-a-zA-Z0-9]*://", location):
        return asyncio.run(LocalFileHandler(location).__ainit__())
    else:
        raise SchemeError(f"unsupported scheme: {location}")


def search_contents(
    location: str = ".",
    checksum: bool = False,
    skip_hidden: bool = False,
    filter_str: str = "",
) -> List[FileObject]:
    handler = get_scheme_handler(location)
    return asyncio.run(
        handler.list_contents(
            checksum=checksum, skip_hidden=skip_hidden, filter_str=filter_str
        )
    )
