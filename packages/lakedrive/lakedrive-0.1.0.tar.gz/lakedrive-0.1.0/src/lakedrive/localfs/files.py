from __future__ import annotations
import os
import stat

from lakedrive.core.helpers import utc_offset

from typing import List
from lakedrive.core.objects import FileObject
from lakedrive.core.helpers import file_md5sum

from lakedrive.core.objects import HashTuple


def md5_hash_tuple(filepath: str) -> HashTuple:
    return HashTuple(algorithm="md5", value=file_md5sum(filepath))


def get_files_recursive(
    directory: str,
    relpath: str = "",
    list_directories: bool = True,
    checksum: bool = False,
    skip_hidden: bool = False,
) -> List[FileObject]:
    """Return list files_objects from a from a directory, and all sub-directories
    that are found within it (recursive search).

    Optional:
    - calculate checksum (md5)
    - skip hidden files and directories (starting with ".")"""
    if not os.path.exists(directory):
        return []

    skip_mark = "." if skip_hidden is True else ""
    files = {
        name: os.lstat("/".join([directory, name]))
        for name in os.listdir(directory)
        if name[0] != skip_mark
    }

    # st_mtime is based on system time, deduct offset to get UTC time
    _utc_offset = utc_offset()

    file_objects: List[FileObject] = []
    for name, st in files.items():
        relpath_name = "/".join(filter(None, [relpath, name]))
        if stat.S_ISREG(st.st_mode):
            file_objects.append(
                FileObject(
                    name=relpath_name,
                    bytes=int(st.st_size),
                    mtime=int(st.st_mtime) - _utc_offset,
                    hash=(
                        lambda: md5_hash_tuple("/".join([directory, name]))
                        if checksum
                        else None
                    )(),
                    tags=b"",
                )
            )
        elif stat.S_ISDIR(st.st_mode):
            if list_directories is True:
                file_objects.append(
                    FileObject(
                        name=f"{relpath_name}/",
                        bytes=0,
                        mtime=int(st.st_mtime),
                        hash=None,
                        tags=b"",
                    )
                )
            new_directory = "/".join([directory, name])
            file_objects += get_files_recursive(
                new_directory,
                list_directories=list_directories,
                relpath=relpath_name,
                checksum=checksum,
                skip_hidden=skip_hidden,
            )

    return file_objects
