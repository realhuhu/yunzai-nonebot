from nonebot.adapters.onebot import (
    V11Bot as BaseV11Bot,
    V12Bot as BaseV12Bot,
)
from nonebot.message import handle_event


class V11Bot(BaseV11Bot):
    def handle_event(self, event) -> None:
        pass
