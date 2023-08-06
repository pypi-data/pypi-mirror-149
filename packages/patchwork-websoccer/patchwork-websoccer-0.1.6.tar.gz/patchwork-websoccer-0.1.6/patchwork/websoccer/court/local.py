# -*- coding: utf-8 -*-
import asyncio
from typing import Iterable

from patchwork.websoccer.court.base import BaseCourt


class LocalCourt(BaseCourt):
    """
    Local memory court.

    For testing and debug purposes only! Local court keeps all data in local memory.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._queue: asyncio.Queue
        self._loop_task: asyncio.Task

    async def _start(self) -> bool:
        self._queue = asyncio.Queue()
        self._loop_task = asyncio.create_task(self._loop())
        return True

    async def _stop(self) -> bool:
        self._loop_task.cancel()
        try:
            await self._loop_task
        except asyncio.CancelledError:
            pass

        return True

    async def _loop(self):
        while True:
            task = await self._queue.get()
            await self.forward_task(task)
            self._queue.task_done()

    async def _subscribe(self, queue_names: Iterable[str]):
        pass

    async def _unsubscribe(self, queue_names: Iterable[str]):
        pass

    async def publish(self, task):
        await self._queue.put(task)
