from collections import namedtuple
from typing import List, Dict, NamedTuple, Optional, AsyncIterator

HashTuple = namedtuple("HashTuple", ["algorithm", "value"])


class FileObject(NamedTuple):
    name: str
    bytes: int
    hash: Optional[HashTuple]
    mtime: int
    tags: bytes


class StreamObject(NamedTuple):
    file: FileObject
    data: AsyncIterator
    chunk_size: int = 0


class FileUpdate(NamedTuple):
    action: str
    files: List[FileObject]
