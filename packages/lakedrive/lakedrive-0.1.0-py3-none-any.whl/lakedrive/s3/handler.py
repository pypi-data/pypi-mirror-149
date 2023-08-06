import os
import logging

from typing import List, Dict, AsyncIterator
from lakedrive.s3.objects import S3Bucket

from .bucket import bucket_create, bucket_delete, bucket_validate, bucket_list
from .files import (
    get_file,
    get_file_batched,
    put_file,
    put_file_batched,
    delete_file_batched,
)

from lakedrive.core.objects import FileObject, StreamObject
from lakedrive.core.handlers import ObjectStoreHandler

logger = logging.getLogger(__name__)


class S3HandlerError(Exception):
    """Exceptions called by S3Handler"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return str(self.message)


class S3Handler(ObjectStoreHandler):
    def __init__(
        self,
        storage_target: str,
        credentials: Dict[str, str] = {},
        stream_chunk_size: int = 1024 * 256,
        read_threads_per_worker: int = 8,
        write_threads_per_worker: int = 4,
    ):
        super().__init__(
            storage_target,
            stream_chunk_size,
            read_threads_per_worker,
            write_threads_per_worker,
        )

        self.support.list_directories = True

        self.aws_credentials = credentials
        self.s3_client = None

        self.bucket_path = self.storage_target.split("s3://")[-1].split("/")
        self.prefix = "/".join(self.bucket_path[1:])

    async def __ainit__(self):
        await self._set_bucket()
        return self

    def _get_aws_credentials(self):
        if not self.aws_credentials:
            self.aws_credentials = {
                "access_id": os.environ["AWS_ACCESS_KEY_ID"],
                "secret_key": os.environ["AWS_SECRET_ACCESS_KEY"],
            }
        return self.aws_credentials

    def _get_bucket(self, raise_not_found: bool = True):
        try:
            if self.bucket:
                if self.bucket.exists is False:
                    if raise_not_found is True:
                        raise S3HandlerError(f"Bucket not found: {self.storage_target}")
                return self.bucket
        except AttributeError:
            pass
        raise S3HandlerError(f"Bucket not initialized: {self.storage_target}")

    async def _set_bucket(
        self, raise_not_found: bool = False, raise_no_permission: bool = False
    ):
        self.bucket = await bucket_validate(
            self.bucket_path[0],
            self._get_aws_credentials(),
            raise_not_found=raise_not_found,
            raise_no_permission=raise_no_permission,
        )
        assert isinstance(self.bucket, S3Bucket)
        return self.bucket

    async def storage_target_exists(
        self, raise_on_noperm: bool = True, raise_on_exist_nodir: bool = True
    ) -> bool:
        """Check if storage target exists, and can be used as such"""
        try:
            if await self._set_bucket(raise_no_permission=True, raise_not_found=True):
                return True
        except FileNotFoundError:
            pass
        except PermissionError:
            if raise_on_noperm is True:
                raise PermissionError(f"{self.storage_target} denied access")
        return False

    async def create_storage_target(self, mode: int = 0o755) -> str:
        """Ensure storage target exists (create if needed), and is a directory with
        sufficient (read,write and execute) permissions for current user."""
        try:
            self.bucket = await bucket_create(
                self.bucket_path[0], self._get_aws_credentials(), check_exist=True
            )
        except PermissionError:
            raise
        except FileExistsError:
            raise
        return self.storage_target

    async def write_file(
        self,
        file_object: FileObject,
        stream_in: AsyncIterator,
    ) -> None:
        return await put_file(
            self._get_bucket(),
            StreamObject(file=file_object, data=stream_in),
            self._get_aws_credentials(),
        )

    async def read_file(
        self,
        file_object: FileObject,
    ) -> AsyncIterator:
        bucket = self._get_bucket()
        stream_objects = get_file(bucket, self._get_aws_credentials(), file_object)
        async for stream_object in stream_objects:
            async for chunk in stream_object.data:
                yield chunk

    async def list_contents(
        self,
        checksum: bool = False,
        skip_hidden: bool = False,
        filter_str: str = "",
    ) -> List[FileObject]:
        bucket = self._get_bucket(raise_not_found=False)
        if bucket.exists is False:
            return []

        self.object_list, prefix_list = await bucket_list(
            bucket,
            self._get_aws_credentials(),
            prefixes=[self.prefix],
            checksum=checksum,
            skip_hidden=skip_hidden,
        )
        if filter_str:
            self.filter_list(filter_str)
        return self.object_list

    async def cleanup(self):
        if self.s3_client:
            await self.s3_client.close_connections()

    async def read_batch(
        self,
        file_objects: List[FileObject],
        stream_chunk_size: int = (1024 * 256),
        threads_per_worker: int = 0,
    ) -> AsyncIterator:
        bucket = self._get_bucket()
        async for batch in get_file_batched(
            bucket,
            self._get_aws_credentials(),
            file_objects,
        ):
            yield batch

    async def write_batch(self, source_handler, file_objects: List[FileObject]) -> None:
        # throughput is based on weakest link
        threads_per_worker = min(
            source_handler.read_threads_per_worker, self.write_threads_per_worker
        )

        stream_objects_batched = source_handler.read_batch(
            file_objects,
            stream_chunk_size=self.stream_chunk_size,
            threads_per_worker=threads_per_worker,
        )
        await put_file_batched(
            self._get_bucket(),
            self._get_aws_credentials(),
            stream_objects_batched,
            threads_per_worker=threads_per_worker,
        )

    async def delete_batch(self, file_objects: List[FileObject]) -> None:
        """Delete a batch of files in one call"""
        bucket = self._get_bucket(raise_not_found=False)
        if bucket.exists is True:
            pathnames = [fo.name for fo in file_objects]
            await delete_file_batched(
                bucket,
                self._get_aws_credentials(),
                pathnames,
            )

    async def delete_storage_target(self) -> None:
        """Delete storage target.
        Note: function will fail if directory is not emptied before"""
        bucket = self._get_bucket(raise_not_found=False)
        if bucket.exists is True:
            await bucket_delete(
                bucket,
                self._get_aws_credentials(),
            )
