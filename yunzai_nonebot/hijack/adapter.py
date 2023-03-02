from typing import TYPE_CHECKING, Any

from nonebot.adapters.onebot import (
    V11Adapter as BaseV11Adapter,
    V12Adapter as BaseV12Adapter
)

from .driver import GRPCDriver


class V11Adapter(BaseV11Adapter):
    def __init__(self, driver: GRPCDriver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.connections=


def hijack_adapter():
    return V11Adapter, 2
