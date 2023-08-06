import asyncio
import concurrent

from typing import Callable, List, Tuple, Any


async def run_async_threadpool(
    function: Callable, arguments_list: List[Tuple], max_workers: int = 8
) -> None:
    """Run process on multiple threads"""
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
        loop = asyncio.get_running_loop()
        futures = [
            loop.run_in_executor(pool, function, *args) for args in arguments_list
        ]
        await asyncio.gather(*futures, return_exceptions=False)


def sync_to_async(*args: Tuple[Any]) -> None:
    async_function, *f_args = args
    asyncio.run(async_function(*tuple(f_args)))


async def run_async_processpool(
    function: Callable,
    arguments_list: List[Tuple[Callable, List]],
    max_workers: int = 2,
) -> None:
    """Run async process on multiple processors"""
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as pool:
        loop = asyncio.get_running_loop()
        futures = [
            loop.run_in_executor(pool, sync_to_async, *((function,) + args))
            for args in arguments_list
        ]
        await asyncio.gather(*futures, return_exceptions=False)
