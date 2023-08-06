import asyncio
from functools import wraps, partial
from typing import Any, Coroutine, TypeVar


def async_wrap(func):
    """
    Turn sync function to async.

    From
    ------------------
    https://dev.to/0xbf/turn-sync-function-to-async-python-tips-58nn
    """
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run


_ReturnType = TypeVar('_ReturnType')


def run_async(coroutine: Coroutine[Any, Any, _ReturnType]) -> _ReturnType:
    """
    Run async in sync.

    :param coroutine: A coroutine.
    """
    try:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coroutine)
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(coroutine)
