import asyncio
from collections import defaultdict
from typing import AsyncGenerator, Any, Dict

import grpc

from yunzai_nonebot.rpc import hola_pb2_grpc, hola_pb2
from yunzai_nonebot.utils.queue import AsyncQueue


class Pipe(hola_pb2_grpc.Pipe):
    def __init__(self, server: grpc.Server):
        self.server = server
        self.connections: Dict[int] = defaultdict(asyncio.Future)

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
        user_id = (await request_iterator.__anext__()).user_id
        if not self.connections[user_id].done():
            self.connections[user_id].set_result(request_iterator)

        asyncio.run_coroutine_threadsafe(self.handler(user_id), asyncio.get_event_loop())

        async for i in AsyncQueue(f"result{user_id}"):
            yield hola_pb2.Response(response=i)

    async def handler(self, user_id: int):
        queue = AsyncQueue(f"result{user_id}")
        async for i in await self.connections[user_id]:
            i: hola_pb2.Request
            await queue.put(i.request)
            await asyncio.sleep(1)
            await queue.put(2 * i.request)


def create_servicer(config: Dict[str, Any]):
    server: grpc.Server = grpc.aio.server(
        options=[
            ('grpc.max_send_message_length', 256 * 1024 * 1024),
            ('grpc.max_receive_message_length', 256 * 1024 * 1024),
        ]
    )
    server.add_insecure_port(f'{config.get("host") or "127.0.0.1"}:{config.get("port") or 50052}')
    servicer = Pipe(server)
    hola_pb2_grpc.add_PipeServicer_to_server(servicer, server)
    return servicer
