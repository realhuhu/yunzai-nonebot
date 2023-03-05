from typing import Any

from nonebot import Bot
from nonebot.adapters.onebot import V11Adapter, V12Adapter
from .driver import GRPCDriver


class OneAdapter(V11Adapter, V12Adapter):
    def __init__(self, driver: GRPCDriver, **kwargs: Any):
        super().__init__(driver, **kwargs)

    @classmethod
    def get_name(cls) -> str:
        return "OneAdapter"

    async def _call_api(self, bot: Bot, api: str, **data: Any) -> Any:
        pass


def hijack_adapter():
    return OneAdapter
