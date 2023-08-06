# -*- coding: utf-8 -*-
import asyncio
from functools import cached_property
from typing import Union, Iterable

from patchwork.core import AsyncSubscriber, Task
from patchwork.core.config import SubscriberConfig

from patchwork.websoccer.court.base import BaseCourt


class PatchworkCourt(BaseCourt):

    class Config(BaseCourt.Config):
        subscriber: SubscriberConfig

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subscription = {}
        self._monitor_task: Union[asyncio.Task, None] = None

    @cached_property
    def subscriber(self) -> AsyncSubscriber:
        return self.settings.subscriber.instantiate(parent=self)

    async def _start(self) -> bool:
        self._monitor_task = asyncio.create_task(self._monitor())
        return True

    async def _stop(self) -> bool:
        if not self._monitor_task.done():
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass

        await self.subscriber.terminate()
        return True

    async def _monitor(self):
        sub_task: Union[asyncio.Task, None] = None
        loop_task: Union[asyncio.Task, None] = None

        while True:
            if not self.subscriber.is_running:
                await self.subscriber.run()

            if sub_task is None or sub_task.done():
                sub_task = asyncio.create_task(self.subscriber.state.wait_for(False))

            if loop_task is None or loop_task.done():
                loop_task = asyncio.create_task(self._loop())

            if not sub_task.done() and not loop_task.done():
                # all running
                self._wait_step = 0

            await asyncio.wait([
                sub_task,
                loop_task
            ], return_when=asyncio.FIRST_COMPLETED)

            self._wait_step = min(self._wait_step + 1, 3)
            wait_time = pow(10, self._wait_step)
            self.logger.warning(f"{self.__class__.__name__} degraded. "
                                f"Restarting in {wait_time} seconds ({self._wait_step} attempt)")
            await asyncio.sleep(wait_time)

    async def _loop(self):
        while True:
            if not self.subscriber.is_running:
                await self.subscriber.state.wait_for(True)

            try:
                task = await self.subscriber.get()
            except:
                continue

            try:
                commit = await self.forward_task(task)
            except Exception as e:
                self.logger.error(f"task forwarding error: {e.__class__.__name__}({e})", exc_info=True)
                commit = False

            if commit:
                await self.subscriber.commit(task)
            else:
                await self.subscriber.rollback(task)

    async def _subscribe(self, queue_names: Iterable[str]):
        if queue_names:
            await self.subscriber.subscribe(queue_names)
            self.logger.debug(f"subscribed on {', '.join(queue_names)}")

    async def _unsubscribe(self, queue_names: Iterable[str]):
        if queue_names:
            await self.subscriber.unsubscribe(queue_names)
            self.logger.debug(f"unsubscribed from {', '.join(queue_names)}")
