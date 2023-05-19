from utils import string_exception

from asyncio import BaseEventLoop, CancelledError, Future, gather, Queue, sleep as asleep
from inspect import iscoroutine
from logging import getLogger
from typing import Coroutine, Iterable, Union


class BackgroundQueue():
    def __init__(self) -> None:
        self._queue = Queue()
        self.logger = getLogger("backgroundqueue")
        self.task = None

    def start(
        self,
        loop: BaseEventLoop
    ):
        self.task = loop.create_task(self.run_task())

    async def run_task(self):
        while True:
            try:
                if self._queue.empty():
                    await asleep(0.1)
                    continue

                task = await self._queue.get()
                if iscoroutine(task):
                    await task
                    continue

                try:
                    await gather(*task)
                except TypeError:
                    pass
                except CancelledError as exc:
                    raise exc
                except Exception as exc:
                    self.logger.error(string_exception(exc))
            except CancelledError:
                return

    async def add_task(
        self,
        task: Union[Coroutine, Iterable[Coroutine]]
    ):
        await self._queue.put(task)

    async def stop(self):
        if self.task is None:
            return
        if not self.task.cancelled():
            self.task.cancel()
