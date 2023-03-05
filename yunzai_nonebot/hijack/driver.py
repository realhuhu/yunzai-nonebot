import asyncio
from pathlib import Path
from typing import Callable, Union, Awaitable, Set, Type, Dict, TYPE_CHECKING

import nonebot
from nonebot.log import logger
from nonebot.config import Env, Config
from nonebot.internal.driver import Driver
from nonebot.adapters.onebot import V11Bot, V12Bot
from omegaconf import OmegaConf

from yunzai_nonebot.utils import Servicer

HOOK_FUNC = Union[Callable[[], None], Callable[[], Awaitable[None]]]


class GRPCDriver(Driver):

    def __init__(self, config: Config):
        super().__init__(Env(), config)
        self.startup_funcs: Set[HOOK_FUNC] = set()
        self.shutdown_funcs: Set[HOOK_FUNC] = set()
        self.servicer = Servicer(self.handler, config)

    @property
    def type(self) -> str:
        return "grpc_driver"

    @property
    def logger(self):
        return logger

    def run(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.serve())
        except KeyboardInterrupt:
            logger.info("已强制退出Py服务器")
            loop.run_until_complete(self.servicer.server.stop(0))

    def on_startup(self, func: HOOK_FUNC) -> HOOK_FUNC:
        self.startup_funcs.add(func)
        return func

    def on_shutdown(self, func: HOOK_FUNC) -> HOOK_FUNC:
        self.shutdown_funcs.add(func)
        return func

    async def serve(self):
        logger.info("开机中..")
        await self.servicer.server.start()

        if self.config.dict().get("shutdown_check") is not False:
            logger.info("检查与更新插件资源...")
            await self.startup()

        await asyncio.sleep(2)
        logger.info("Py服务器已开机(Py started)")
        try:
            await self.servicer.server.wait_for_termination()
        except asyncio.exceptions.CancelledError:
            if self.config.dict().get("shutdown_check") is not False:
                logger.info("关机检查...")
                await self.shutdown()
            logger.info("已关机")

    async def startup(self):
        for handler in self.startup_funcs:
            if asyncio.iscoroutinefunction(handler):
                await handler()
            else:
                handler()

    async def shutdown(self):
        for handler in self.shutdown_funcs:
            if asyncio.iscoroutinefunction(handler):
                await handler()
            else:
                handler()

    async def handler(self, self_id: str):
        event_handlers = []
        adapter_v11, adapter_v12 = self._adapters.values()
        self_id_v11=self_id+"v11"
        self_id_v12=self_id+"v12"
        async for request in await self.servicer.connections[self_id]:
            print(request)
            await asyncio.gather(*[handler(request) for handler in event_handlers])


def hijack_driver(config_path: Path):
    fields = Config.__dict__["__fields__"]
    yaml = dict(OmegaConf.load(config_path))
    for k, v in yaml.items():
        if field := fields.get(k):
            yaml[k] = field.default.__class__(v)
    logger.info(yaml)
    config = Config.parse_obj(yaml)
    driver = GRPCDriver(config)
    nonebot._driver = driver
    return driver
