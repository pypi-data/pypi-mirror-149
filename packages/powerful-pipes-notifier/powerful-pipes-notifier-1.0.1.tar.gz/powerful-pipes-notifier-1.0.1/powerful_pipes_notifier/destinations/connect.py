from __future__ import annotations

from .webhook import WebhookNotifier, WebSocketNotifier
from .interface import NotifierInterface
from ..exceptions import NotifierException
from ..config import RunningConfig

async def connect_destination(
        config: RunningConfig
) -> NotifierInterface or NotifierException:

    if config.destination_uri.startswith("http"):
        return await WebhookNotifier.open(config)

    elif config.destination_uri.startswith("ws"):
        return await WebSocketNotifier.open(config)

    else:
        raise NotifierException("Invalid destination URI")

__all__ = ("connect_destination", )
