import asyncio
from collections import defaultdict
from typing import Dict, AsyncGenerator, Any

import grpc
from nonebot.config import Config

from yunzai_nonebot.rpc import hola_pb2_grpc, hola_pb2
from yunzai_nonebot.utils import AsyncQueue


class Servicer(hola_pb2_grpc.Pipe):
    def __init__(self, handler, config: Config):
        self.connections: Dict[str, asyncio.Future] = defaultdict(asyncio.Future)
        self.handler = handler
        self.server: grpc.Server = grpc.aio.server(
            options=[
                ('grpc.max_send_message_length', 256 * 1024 * 1024),
                ('grpc.max_receive_message_length', 256 * 1024 * 1024),
            ]
        )
        hola_pb2_grpc.add_PipeServicer_to_server(self, self.server)
        self.server.add_insecure_port(f'{config.host}:{config.port}')

    async def Option(
            self,
            request: hola_pb2.OptionCode,
            context: grpc.ServicerContext,
            **kwargs
    ):
        code = request.code
        if code == 1:
            await self.server.stop(0)

        return hola_pb2.OptionCode(code=code)

    async def Channel(
            self,
            request_iterator: AsyncGenerator[hola_pb2.Request, Any],
            context: grpc.ServicerContext,
            **kwargs
    ):
        self_id = (await request_iterator.__anext__()).self_id
        if not self.connections[self_id].done():
            self.connections[self_id].set_result(request_iterator)
        asyncio.run_coroutine_threadsafe(self.handler(self_id), asyncio.get_event_loop())

        async for i in AsyncQueue(f"result{self_id}"):
            yield hola_pb2.Response(response=i)
