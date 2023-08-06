import logging
import asyncio
from typing import AsyncIterator, List, Dict

from lakedrive.core.objects import FileObject, StreamObject
from lakedrive.core.helpers import split_in_chunks
from lakedrive.httplibs.request import HttpRequest

from .objects import S3Bucket
from .headers import S3ConnectConfiguration
from .headers import S3Connect


logger = logging.getLogger(__name__)


async def s3_batch_put(
    client: HttpRequest,
    batch: List[StreamObject],
) -> List[StreamObject]:
    """This function processes one batch of StreamObject items, and forwards
    each single item to a HTTP upstream client for execution.

    Return a list of failed items (or empy list if none failed),
    so failed items can be retried at a later time"""
    logger.debug(f"Uploading batch of {str(len(batch))} StreamObject items")

    responses = await asyncio.gather(
        *[
            client.upstream(
                S3Connect,
                stream_object,
                thread_id=thread_id,
            )
            for thread_id, stream_object in enumerate(batch)
        ],
        return_exceptions=True,
    )

    items_failed = []
    for item_no, http_response in enumerate(responses):
        filename = batch[item_no].file.name
        if http_response.status_code == 200:
            logger.info(f"Succesful upload: {filename}")
            continue
        items_failed.append(batch[item_no])
        http_error = f"{http_response.error_msg} ({str(http_response.status_code)})"
        logger.error(f"Failed upload: {filename},http_error={http_error})")

    return items_failed


async def s3_batch_delete(
    client: HttpRequest,
    batch: List[str],
) -> List[str]:
    """This function processes one batch of keynames, and forwards
    each single keyname to a HTTP client (HTTP DELETE) for execution.

    Return a list of failed items (or empy list if none failed),
    so failed items can be retried at a later time"""
    responses = await asyncio.gather(
        *[
            client.delete(
                S3Connect,
                keyname,
                thread_id=thread_id,
            )
            for thread_id, keyname in enumerate(batch)
        ]
    )

    items_failed = []
    for item_no, http_response in enumerate(responses):
        filename = batch[item_no]
        if http_response.status_code == 204:
            logger.info(f"Succesful delete: {filename}")
            continue
        items_failed.append(batch[item_no])
        http_error = f"{http_response.error_msg} ({str(http_response.status_code)})"
        logger.error(f"Failed delete: {filename},http_error={http_error})")

    return items_failed


async def put_file_batched(
    bucket: S3Bucket,
    credentials: Dict[str, str],
    stream_objects_batched: AsyncIterator,
    threads_per_worker: int = 4,
) -> None:
    """Put files on S3 bucket batch by batch. This function sets up a HTTP config,
    yields batches of StreamObject items and forwards this to an upload processor.

    read_batch_iterator yields a list of StreamObject items, which are forwarded to
    an (HTTP) upstream client. Size of each batch should (ideally) be a multiple of
    connections (i.e. if threads_per_worker == 4, batch == 4, 8, 12, 16, ... items)"""
    client = await HttpRequest(
        S3ConnectConfiguration(bucket, credentials),
        connections=threads_per_worker,
    ).__aenter__()

    try:
        async for batch in stream_objects_batched:
            items_remaining = await s3_batch_put(client, batch)
            if items_remaining:
                """log only for now -- to make retry working we need to implement
                a reset option in the StreamObject, to read data from start"""
                logging.error(
                    f"Not all items uploaded, items left:{str(len(items_remaining))}"
                )

    except Exception as exception:
        logger.error(f"Unexpected error uploading file-batch: {str(exception)}")
        if not await client.__aexit__(
            type(exception), exception, exception.__traceback__
        ):
            raise exception
    else:
        await client.__aexit__(None, None, None)


async def delete_file_batched(
    bucket: S3Bucket,
    credentials: Dict[str, str],
    keynames: List[str],
    max_connections_per_thread: int = 50,
) -> None:
    """Delete a list of files (by keyname) in a S3 bucket
    If an item delete fails, retry once"""
    if len(keynames) == 0:
        logger.info("Nothing to delete")
        # nothing to delete
        return

    no_connections = min(len(keynames), max_connections_per_thread)
    batches = split_in_chunks(keynames, no_connections)

    async with HttpRequest(
        S3ConnectConfiguration(bucket, credentials),
        connections=no_connections,
    ) as client:
        for batch in batches:
            items_remaining = await s3_batch_delete(client, batch)
            if not items_remaining:
                continue
            logger.warning(
                f"Not all items deleted, remaining: {str(len(items_remaining))}"
            )
            # retry once
            items_remaining = await s3_batch_delete(client, items_remaining)
            if items_remaining:
                logger.error(
                    f"Cant delete all items, remaining: {str(len(items_remaining))}"
                )
                logger.debug(f'Items failed: {",".join(items_remaining)}')


async def get_file_batched(
    bucket: S3Bucket,
    credentials: Dict[str, str],
    file_objects: List[FileObject],
    threads_per_worker: int = 16,
) -> AsyncIterator:
    """Get files a S3 bucket in batches of StreamObjects. Each StreamObject within a
    batch must also be consumed over iteration (connection is opened/ re-used) as
    data gets read from the source.


    At the end ensure all connections are closed off"""
    client = await HttpRequest(
        S3ConnectConfiguration(bucket, credentials),
        connections=min(threads_per_worker, 50),
    ).__aenter__()

    batches = split_in_chunks(file_objects, threads_per_worker)

    for batch in batches:
        yield [
            StreamObject(
                file=file_object,
                data=client.downstream(
                    S3Connect,
                    resource=file_object.name,
                    thread_id=thread_id,
                ),
            )
            for thread_id, file_object in enumerate(batch)
        ]
    # ensure connections get closed
    await client.__aexit__()


async def get_file(
    bucket: S3Bucket,
    credentials: Dict[str, str],
    file_object: FileObject,
) -> AsyncIterator:
    """Get a single file from a S3 bucket, return as a StreamObject iterator,
    iteration is required to open connection when data is consumed"""
    async with HttpRequest(
        S3ConnectConfiguration(bucket, credentials),
        connections=1,
    ) as client:
        stream_object = StreamObject(
            file=file_object,
            data=client.downstream(S3Connect, resource=file_object.name),
        )
        yield stream_object

    # client = await HttpRequest(
    #     S3ConnectConfiguration(bucket, credentials),
    #     connections=1,
    # ).__aenter__()
    # iterator = client.downstream(
    #     S3Connect,
    #     resource=file_object.name,
    # )
    # stream_object = StreamObject(
    #     file=file_object,
    #     data=iterator,
    # )
    # yield stream_object
    # await client.__aexit__()


async def put_file(
    bucket: S3Bucket,
    stream_object: StreamObject,
    credentials: Dict[str, str],
) -> None:
    """Upload a single file (StreamObject) to a S3 bucket"""
    async with HttpRequest(
        S3ConnectConfiguration(bucket, credentials),
        connections=1,
    ) as client:
        await s3_batch_put(client, [stream_object])
