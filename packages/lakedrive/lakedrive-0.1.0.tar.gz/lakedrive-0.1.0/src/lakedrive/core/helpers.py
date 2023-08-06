import hashlib

from datetime import datetime
from typing import Iterator


def compute_md5sum(file_bytes: bytes) -> str:
    """Compute md5sum from array of bytes"""
    return hashlib.md5(file_bytes).hexdigest()


def file_md5sum(filepath: str) -> str:
    md5_hash = hashlib.md5()
    with open(filepath, "rb") as stream:
        md5_hash.update(stream.read())
    return md5_hash.hexdigest()


def splitlist(a, n) -> Iterator:
    k, m = divmod(len(a), n)
    return (
        a[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)]
        for i in range(min(len(a), n))
    )


def split_in_chunks(input_list, length):
    """Split input_list into new lists of max length"""
    return [input_list[i : i + length] for i in range(0, len(input_list), length)]


def utc_offset() -> int:
    """Calculate offset in seconds to UTC time
    positive means ahead of UTC time, negative means behind UTC time"""
    return round((datetime.now() - datetime.utcnow()).total_seconds())
