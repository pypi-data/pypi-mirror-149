import asyncio
import logging

from typing import List, Dict, Callable, Any

from .objects import FileObject, FileUpdate

from lakedrive.core import get_scheme_handler
from .executors import run_async_processpool
from .handlers import ObjectStoreHandler
from .helpers import splitlist


logger = logging.getLogger(__name__)


def list_contents(
    location: str = ".", checksum: bool = False, skip_hidden: bool = False
) -> List[FileObject]:
    handler = get_scheme_handler(location)
    return asyncio.run(
        handler.list_contents(checksum=checksum, skip_hidden=skip_hidden)
    )


def get_rsync_update(
    objects_source: List[FileObject],
    objects_target: List[FileObject],
    params: Dict[str, bool],
) -> List[FileUpdate]:

    checksum = params.get("checksum", False)
    skip_newer_on_target = params.get("skip_newer_on_target", False)
    delete_extraneous = params.get("delete_extraneous", False)

    if checksum is True:
        # skip based on checksum, not mtime (or size)
        objects_in_source = {(obj.name, obj.hash): obj for obj in objects_source}
        hashkeys_in_target = set([(obj.name, obj.hash) for obj in objects_target])
        hashkeys_in_source = set(objects_in_source.keys())
        copy_keys = hashkeys_in_source.difference(hashkeys_in_target)
        copy_to_target = set([objects_in_source[key] for key in copy_keys])

    else:
        copy_to_target = set(objects_source).difference(set(objects_target))

    if checksum is False and skip_newer_on_target is True:
        # skip based on mod-time (unless skipped based on md5sum)
        filetimes_on_target = {obj.name: obj.mtime for obj in objects_target}
        # skip objects that exist on target, and have a newer mtime
        skippable_objects = [
            obj
            for obj in copy_to_target
            if obj.name in filetimes_on_target
            and obj.mtime < filetimes_on_target[obj.name]
        ]

        # substract skippable objects
        copy_to_target = copy_to_target.difference(skippable_objects)

    if delete_extraneous is True:
        # delete files found on target, but not on source
        objects_in_target = {obj.name: obj for obj in objects_target}
        keys_in_source = set([obj.name for obj in objects_source])
        keys_in_target = set(objects_in_target.keys())

        delete_keys = keys_in_target.difference(keys_in_source)
        delete_from_target = [objects_in_target[key] for key in delete_keys]
    else:
        delete_from_target = []

    return [
        FileUpdate(action="copy", files=list(copy_to_target)),
        FileUpdate(action="delete", files=list(delete_from_target)),
    ]


def target_from_source(
    target_function: Callable,
    source_handler: Callable,
    object_list: List[Any],
    max_workers: int = 2,
) -> None:
    if not object_list:
        return

    arguments_list = [
        (source_handler, chunk) for chunk in splitlist(object_list, max_workers * 1)
    ]
    asyncio.run(
        run_async_processpool(target_function, arguments_list, max_workers=max_workers)
    )


def execute_rsync_update(
    source_handler: ObjectStoreHandler,
    target_handler: ObjectStoreHandler,
    file_update: FileUpdate,
):

    if file_update.action == "copy":
        workers = 1
        target_from_source(
            target_handler.write_batch,
            source_handler,
            file_update.files,
            max_workers=workers,
        )
        return
    if file_update.action == "delete":
        asyncio.run(target_handler.delete_batch(file_update.files))
        return

    raise ValueError(f"Invalid action: {str(file_update.action)}")


def rsync_paths(
    source: str, target: str, dry_run: bool = False, params: Dict[str, bool] = {}
) -> None:

    skip_hidden = params.get("skip_hidden", False)
    checksum = params.get("checksum", False)

    objects_source = list_contents(
        location=source, checksum=checksum, skip_hidden=skip_hidden
    )
    objects_target = list_contents(
        location=target, checksum=checksum, skip_hidden=skip_hidden
    )
    update_list = get_rsync_update(objects_source, objects_target, params=params)

    if dry_run is False:
        # execute
        for file_update in update_list:
            execute_rsync_update(
                get_scheme_handler(source), get_scheme_handler(target), file_update
            )
    # else:
    #     # print(update[0])
    #     for file_update in update_list:
    #         if not file_update.files:
    #             continue
    #         if file_update.action == "copy":
    #             pass
    #         elif file_update.action == "delete":
    #             print("Deleting:")
    #             print(file_update.files)
