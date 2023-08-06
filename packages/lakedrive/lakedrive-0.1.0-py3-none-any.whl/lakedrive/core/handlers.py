from __future__ import annotations
from dataclasses import dataclass

from lakedrive.core.list_filter import apply_search_filter_str


@dataclass
class StorageSupportFlags:
    # should be False by default. Only True for local fs. For object stores
    # it may be useful to show virtual dirs in certain cases (e.g. syncing
    # localfs to S3 including empty dirs, but not as default behavior.
    list_directories: bool = False


class SchemeError(Exception):
    """Custom Exception, raise on unknown scheme"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return str(self.message)


class ObjectStoreHandler:
    def __init__(
        self,
        storage_target: str,
        stream_chunk_size: int,
        read_threads_per_worker: int,
        write_threads_per_worker: int,
    ):
        self.storage_target = storage_target
        self.stream_chunk_size = stream_chunk_size
        self.read_threads_per_worker = read_threads_per_worker
        self.write_threads_per_worker = write_threads_per_worker

        self.support = StorageSupportFlags()
        self.object_list = []

    def filter_list(self, filter_str: str) -> None:
        if self.object_list:
            self.object_list = apply_search_filter_str(filter_str, self.object_list)

    async def soft_cleanup(self):
        """Optional function used for some, but not all, handlers.
        example use-case: wait for network connections to close"""
        pass
