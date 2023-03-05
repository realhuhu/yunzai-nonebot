from typing import Union, Any

from nonebot.message import handle_event
from nonebot.adapters.onebot import V11Bot, V12Bot
from nonebot.internal.adapter import Event, Message, MessageSegment

from .adapter import OneAdapter


class OneBot(V11Bot, V12Bot):
    def __init__(self, adapter: OneAdapter, self_id: str):
        super().__init__(adapter, self_id)
        self.v11 = V11Bot(adapter, self_id)
        self.v12 = V12Bot(adapter, self_id, "yunzai")

        self.v11.call_api = self.v12.call_api = self.call_api

    async def send(self, event: Event, message: Union[str, Message, MessageSegment], **kwargs: Any) -> Any:
        pass

    async def handle_event(self, event: Event) -> None:
        await handle_event(self, event)

    async def call_api(self, api: str, **data) -> Any:
        print(data)
