from __future__ import annotations

import abc
import asyncio

from typing import List
from asyncio import Task

from ..config import RunningConfig
from ..exceptions import NotifierDeliveryException


class NotifierInterface(metaclass=abc.ABCMeta):

    def __init__(self):
        self.tasks: List[Task] = []

    async def join(self):
        # await asyncio.gather(*self.tasks)
        await asyncio.wait(self.tasks)

    @classmethod
    @abc.abstractmethod
    async def open(cls, config: RunningConfig) -> NotifierInterface:
        ...

    @abc.abstractmethod
    async def notify(self, message: dict) -> None or NotifierDeliveryException:
        ...

__all__ = ("NotifierInterface", )
