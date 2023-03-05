import inspect
from typing import Optional, Type, Tuple, Any

from nonebot import logger
from nonebot.exception import SkippedException
from nonebot.adapters.onebot import V11Bot, V12Bot, V11Event, V12Event
from nonebot.internal.params import BotParam, EventParam

from .bot import OneBot
from .event import OneEvent


class OneBotParam(BotParam):
    async def _solve(self, bot: OneBot, **kwargs: Any) -> Any:
        checker = self.extra.get("checker")
        if not checker or checker.type_ == V11Bot:
            return bot.v11

        return bot.v12

    async def _check(self, bot: OneBot, **kwargs: Any) -> None:
        if checker := self.extra.get("checker"):
            if checker.type_ not in (V11Bot, V12Bot):
                logger.error("py-plugin只支持OneBot V11和OneBot V12的插件")
                raise SkippedException


class OneEventParam(EventParam):
    async def _solve(self, event: OneEvent, **kwargs: Any) -> Any:
        checker = self.extra.get("checker")
        if not checker or checker.type_ == V11Event:
            return event.v11

        return event.v12

    async def _check(self, bot: OneBot, **kwargs: Any) -> None:
        if checker := self.extra.get("checker"):
            if checker.type_ not in (V11Event, V12Event):
                logger.error("py-plugin只支持OneBot V11和OneBot V12的插件")
                raise SkippedException


def hijack_params():
    pass
