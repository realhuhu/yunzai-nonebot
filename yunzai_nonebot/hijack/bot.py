import asyncio
from typing import Union, Any, TYPE_CHECKING

from nonebot.message import handle_event
from nonebot.adapters.onebot import V11Bot, V12Bot
from nonebot.internal.adapter import Bot, Event, Message, MessageSegment

from yunzai_nonebot.rpc.hola_pb2 import Event as GRPCEvent
from yunzai_nonebot.utils import to_v11, to_v12

if TYPE_CHECKING:
    from .adapter import OneAdapter


class OneBot(Bot):
    def __init__(self, adapter: "OneAdapter", self_id: str):
        super().__init__(adapter, self_id)
        self.v11 = V11Bot(adapter, self_id)
        self.v12 = V12Bot(adapter, self_id, "yunzai")

        self.v11.call_api = self.v12.call_api = self.call_api

    async def send(self, event: Event, message: Union[str, Message, MessageSegment], **kwargs: Any) -> Any:
        pass

    async def handle_event(self, event: GRPCEvent) -> None:
        await asyncio.gather(
            handle_event(self.v11, await to_v11(event)),
            handle_event(self.v12, await to_v12(event))
        )

    async def call_api(self, api: str, **data) -> Any:
        print(api, data)
