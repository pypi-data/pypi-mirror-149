import asyncio
import sys
import os

filepath = os.path.split(__file__)[0]
sys.path.append(".")

from .tcp_simple_proto import TcpSimpleProto
from .trans_callback import TransServerCallback, TransLocalServerCallback, TransServerClientCallback
from .tcp_server import TcpServer
from .socks5_callback import Socks5ServerCallback
from .socks5_proto import Socks5ServerProto
from .tcp_proto_base import TcpProtoBase
from .sym_enc_chacha20 import SymEncChaCha20

server = TcpServer('0.0.0.0', 12344,
                   Socks5ServerCallback(),
                   Socks5ServerProto(),
                   loop=asyncio.get_event_loop())
server.start()

server2 = TcpServer('0.0.0.0', 12343,
                    TransServerCallback('127.0.0.1', 12344, SymEncChaCha20("123456")),
                    TcpSimpleProto(),loop=asyncio.get_event_loop())
server2.start()

server3 = TcpServer('0.0.0.0', 12345,
                    TransLocalServerCallback('127.0.0.1', 12343, SymEncChaCha20("123456")),
                    TcpProtoBase(),
                    loop=asyncio.get_event_loop())
server3.start()

asyncio.get_event_loop().run_forever()
