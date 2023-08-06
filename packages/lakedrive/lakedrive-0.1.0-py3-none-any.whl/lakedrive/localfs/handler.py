import os
import stat
import time
import logging
import asyncio

from typing import List, AsyncIterator

from lakedrive.core.executors import run_async_threadpool
from lakedrive.localfs.files import get_files_recursive

from lakedrive.core.helpers import split_in_chunks
from lakedrive.core.objects import FileObject
from lakedrive.core.objects import StreamObject
from lakedrive.core.handlers import ObjectStoreHandler


logger = logging.getLogger(__name__)


class LocalFileHandler(ObjectStoreHandler):
    def __init__(
        self,
        storage_target: str,
        stream_chunk_size: int = 1024 * 128,
        read_threads_per_worker: int = 160,
        write_threads_per_worker: int = 8,
    ):
        super().__init__(
            storage_target,
            stream_chunk_size,
            read_threads_per_worker,
            write_threads_per_worker,
        )
        self.support.list_directories = True

    async def __ainit__(self):
        return self

    async def storage_target_exists(
        self, raise_on_noperm: bool = True, raise_on_exist_nodir: bool = True
    ) -> bool:
        """Check if storage target exists, and can be used as such"""
        try:
            fp = os.lstat(self.storage_target)
            if not stat.S_ISDIR(fp.st_mode):
                if raise_on_exist_nodir is True:
                    raise FileExistsError(
                        f"{self.storage_target} exists, but not a directory"
                    )
                return False

            if (
                raise_on_noperm is True
                and os.access(self.storage_target, os.R_OK | os.W_OK | os.W_OK) is False
            ):
                raise PermissionError(
                    f"{self.storage_target} exists, but has no rwx permission set"
                )
            return True
        except FileNotFoundError:
            pass
        except PermissionError:
            if raise_on_noperm is True:
                raise
        return False

    async def create_storage_target(self, mode: int = 0o755) -> str:
        """Ensure storage target exists (create if needed), and is a directory with
        sufficient (read,write and execute) permissions for current user."""
        try:
            if (
                await self.storage_target_exists(
                    raise_on_noperm=True, raise_on_exist_nodir=True
                )
                is False
            ):
                os.makedirs(self.storage_target, mode)
        except PermissionError:
            raise PermissionError(f"No permission to create: {self.storage_target}")
        except FileExistsError:
            raise
        return self.storage_target

    async def _write_file(
        self,
        stream_object: StreamObject,
    ) -> None:
        """Read incoming chunks (async stream), and write the chunks to a file.
        Important: function assumes directory already exists!

        If mtime is given, set this via os.utime() explicitly
        (modification time may require backdating when kept same as source)"""
        name = stream_object.file.name
        mtime = stream_object.file.mtime
        stream_in = stream_object.data
        filepath = "/".join([self.storage_target, name])
        with open(filepath, "wb") as stream_out:
            async for chunk in stream_in:
                stream_out.write(chunk)
        if mtime > 0:
            os.utime(filepath, (int(time.time()), mtime))

    async def write_file(
        self,
        file_object: FileObject,
        stream_in: AsyncIterator,
    ) -> None:
        # TODO: CHECK IF PATH EXISTS
        stream_object = StreamObject(
            file=file_object,
            data=stream_in,
        )
        return await self._write_file(stream_object)

    async def _read_file(self, filepath: str) -> AsyncIterator:
        """Read file in chunks of fixed size, until all parts are read"""
        with open(f"{self.storage_target}/{filepath}", "rb") as stream:
            while True:
                chunk = stream.read(self.stream_chunk_size)
                if chunk:
                    yield chunk
                else:
                    break

    async def read_file(
        self,
        file_object: FileObject,
    ) -> AsyncIterator:
        async for chunk in self._read_file(file_object.name):
            yield chunk

    async def list_contents(
        self,
        checksum: bool = False,
        skip_hidden: bool = False,
        filter_str: str = "",
    ) -> List[FileObject]:
        """Get list of files that are contained in location.

        Optional:
          checksum: add checksum per file
          skip_hidden: skips files or directories starting with "."

        return as list of FileObjects"""
        self.object_list = get_files_recursive(
            self.storage_target,
            list_directories=self.support.list_directories,
            checksum=checksum,
            skip_hidden=skip_hidden,
        )
        if filter_str:
            self.filter_list(filter_str)
        return self.object_list

    async def read_batch(
        self,
        file_objects: List[FileObject],
        stream_chunk_size: int = (1024 * 256),
        threads_per_worker: int = 0,
    ) -> AsyncIterator:
        """Divided list of file objects in smaller fixed-size batches,
        every time this function is called a new batch of files are returned"""
        if threads_per_worker < 1:
            threads_per_worker = self.read_threads_per_worker
        self.stream_chunk_size = stream_chunk_size

        # split in batches
        # skip files ending with "/" as there are assumed to be directories
        batches = split_in_chunks(
            [fo for fo in file_objects if fo.name[-1] != "/"], threads_per_worker
        )

        for batch in batches:
            yield [
                StreamObject(
                    file=file_object,
                    data=self._read_file(file_object.name),
                    chunk_size=stream_chunk_size,
                )
                for file_object in batch
            ]

    async def write_batch(self, source_handler, file_objects: List[FileObject]) -> None:
        """Write the given list of files in batches.

        All directories are created first, underlying _write_file() function calls
        can then safely assume the target directory to be present.

        This functions works in tandem with a read_batch() function. Files are
        split in read_batch(), then read and written through a loop in this function."""
        # on local filesystem, directories must be created first
        if source_handler.support.list_directories is True:
            # get directories from source (i.e. "files" ending with a "/")
            directories = [
                ("/".join([self.storage_target, fo.name]), fo.mtime)
                for fo in file_objects
                if fo.name[-1] == "/"
            ]
        else:
            # Get directories from source.
            # there is no mtime, plug in 0 to keep default (current time)
            directories = [
                ("/".join([self.storage_target, os.path.dirname(fo.name)]), 0)
                for fo in file_objects
            ]

        # create (empty) directories -- must be in hierarchical order
        directories_sorted = sorted(set(directories), reverse=True)
        last_leaf = ""
        for directory, _ in directories_sorted:
            # skip if directory is part of last created leaf
            if f"{directory}/" not in last_leaf:
                os.makedirs(directory, exist_ok=True)
                last_leaf = directory

        if not last_leaf:
            # no (sub) directories created. Ensure at least target exists
            await self.create_storage_target()

        threads_per_worker = min(
            source_handler.read_threads_per_worker, self.write_threads_per_worker
        )
        # fo_batches = await source_handler.read_batch(
        stream_objects_batched = source_handler.read_batch(
            file_objects, threads_per_worker=threads_per_worker
        )

        async for batch in stream_objects_batched:
            await asyncio.gather(
                *[self._write_file(stream_object) for stream_object in batch]
            )

        await source_handler.soft_cleanup()
        # ensure directory have correct mtime -- must be in order,
        # and after copying files to keep original mtime
        for directory, mtime in directories_sorted:
            if mtime > 0:
                os.utime(directory, (int(time.time()), mtime))

    async def delete_batch(self, file_objects: List[FileObject]) -> None:
        """Delete a batch of files in one call. First all files are deleted,
        and than directories using the os system calls"""
        # delete all (reg)files first
        await run_async_threadpool(
            os.unlink,
            [
                ("/".join([self.storage_target, fo.name]),)
                for fo in file_objects
                if fo.name[-1] != "/"
            ],
        )
        # (empty) directories must be unlinked in order due to possible hiearchy
        directories_sorted = sorted(
            [
                "/".join([self.storage_target, fo.name])
                for fo in file_objects
                if fo.name[-1] == "/"
            ],
            reverse=True,
        )
        for directory in directories_sorted:
            os.rmdir(directory)

    async def delete_storage_target(self) -> None:
        """Delete storage target.
        Note: function will fail if directory is not emptied before"""
        if (
            await self.storage_target_exists(
                raise_on_noperm=True, raise_on_exist_nodir=False
            )
            is False
        ):
            return
        os.rmdir(self.storage_target)
