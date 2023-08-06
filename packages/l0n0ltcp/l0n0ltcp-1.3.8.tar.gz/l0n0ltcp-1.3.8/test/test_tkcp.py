import sys

sys.path.append("D:\l0n0ltcp")

import asyncio
from l0n0ltcp.tcp_server import TcpServer
from l0n0ltcp.tcp_proto_base import TcpProtoBase
from l0n0ltcp.tcp_callback_base import TcpCallbackBase
from l0n0lutils.async_runner import run
from l0n0lkcp.ikcp import load_clib
from ctypes.util import find_library
load_clib(find_library("kcp"))

class TestCb(TcpCallbackBase):
    async def on_connect(self, session):
        print("connected", session.id)

    async def on_msg(self, session, data: bytes):
        print(data)

    async def on_close(self, session):
        print("close", session.id)

class TestProto(TcpProtoBase):
    async def read_msg(self, session):
        data = await session.reader.read(4096)
        if len(data) <= 0:
            session.close()
        return data
    
    def make_heart_msg(self) -> bytes:
        return b''

    def build_msg(self, data: bytes) -> bytes:
        return data


loop = asyncio.get_event_loop()
server = TcpServer('0.0.0.0', 9999,  TestCb(), TestProto(), loop=loop)
server.use_kcp(123, 2000)
server.start()
run()
