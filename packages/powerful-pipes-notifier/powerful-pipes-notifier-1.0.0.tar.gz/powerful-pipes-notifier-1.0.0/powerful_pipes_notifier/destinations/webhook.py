from __future__ import annotations

import abc
import asyncio

import aiohttp as aiohttp

from aiohttp import ClientConnectorError
from powerful_pipes import async_report_exception

from ..config import RunningConfig
from .interface import NotifierInterface
from ..exceptions import NotifierDeliveryException


class HTTPNotifier(NotifierInterface):

    def __init__(self, config: RunningConfig):
        super().__init__()

        self.debug = config.debug
        self.timeout = config.timeout
        self.webhook_url = config.destination_uri
        self.max_concurrency = config.max_concurrency

        self._queue = asyncio.Queue()

        # Start consumer
        self.tasks.append(
            asyncio.create_task(self.consumer())
        )

    @classmethod
    async def open(cls, config: RunningConfig) -> NotifierInterface:
        return cls(config)

    async def notify(self, message: dict) -> None or NotifierDeliveryException:
        await self._queue.put(message)

    @abc.abstractmethod
    async def consumer(self):
        ...


class WebhookNotifier(HTTPNotifier):

    async def consumer(self):

        sem = asyncio.Semaphore(self.max_concurrency)

        while True:
            # Get a "work item" out of the queue.
            message = await self._queue.get()

            await sem.acquire()

            self.tasks.append(asyncio.create_task(
                self._notify_webhook_(message, sem, self._queue)
            ))


    async def _notify_webhook_(
            self,
            data: dict,
            sem: asyncio.Semaphore,
            queue: asyncio.Queue
    ):

        timeout = aiohttp.ClientTimeout(total=self.timeout)

        ex = None
        message = None

        try:
            async with aiohttp.ClientSession(
                    # json_serialize=orjson.dumps,
                    timeout=timeout
            ) as ses:

                async with ses.post(
                        url=self.webhook_url,
                        json=data,
                        headers={"User-Agent": "Notifier/1.0"}
                ) as resp:

                    if resp.status == 403:
                        message = "Webhook: Unauthorized. Invalid webhook token"
                        ex = resp.reason

                    elif resp.status != 200:
                        message = "Webhook: remote web server return an error"
                        ex = await resp.text()

        except ClientConnectorError as e:
            message = "Server is not reachable"
            ex = e

        except asyncio.TimeoutError as e:
            message = "Webhook: server connection timeout"
            ex = e

        except Exception as e:
            message = "Webhook: Unknown error"
            ex = e

        if ex:
            if self.debug:
                print(f"Webhook error: {message}")

            await async_report_exception(data, ex, message)

        else:
            if self.debug:
                print("Webhook done")

        # await asyncio.sleep(5)

        queue.task_done()
        sem.release()

class WebSocketNotifier(HTTPNotifier):


    async def consumer(self):
        timeout = aiohttp.ClientTimeout(total=self.timeout)

        try:
            async with aiohttp.ClientSession(
                    # json_serialize=orjson.dumps,
                    timeout=timeout
            ) as session:

                async with session.ws_connect(self.webhook_url) as ws:
                    while True:
                        # Get a "work item" out of the queue.
                        data = await self._queue.get()

                        await ws.send_json(data)

        except ClientConnectorError as e:
            message = "Server is not reachable"
            ex = e

        except asyncio.TimeoutError as e:
            message = "Webhook: server connection timeout"
            ex = e

        except Exception as e:
            message = "Webhook: Unknown error"
            ex = e

        if ex:
            if self.debug:
                print(f"Webhook error: {message}")

            await async_report_exception(None, ex, message)



__all__ = ("WebhookNotifier", "WebSocketNotifier")
