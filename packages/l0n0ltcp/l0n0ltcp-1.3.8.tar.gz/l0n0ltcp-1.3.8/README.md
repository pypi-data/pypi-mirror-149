# 主要就是封装了一下asyncio 的网络

# 实例1 一个tcp server
```python
from l0n0ltcp.tcp_server import TcpServer
from l0n0ltcp.json_handler import JsonHandler, json_rpc
from l0n0ltcp.tcp_simple_proto import TcpSimpleProto

# TcpSimpleProto简介
# 3 byte(后面的数据包大小size) + 4byte(控制字段，可自定义) + (size - 4)的数据

# JsonHandler 简介

# Json handler 会将 数据解析为一个json对象
# 格式为{"name": 函数名, args: 参数列表, serial_id: 调用ID}
# 然后根据 name 获取函数，将 [会话ID] 和 args 传递给 获取的函数 然后调用
# 函数的返回值 会被发送回调用方

# json_rpc简介
# json_rpc 用于调用远程的函数
# 原理：
# 1.如果调用有返回值： json_rpc(send_msg, "remote_func", [123,321])
# 第一步： 发送 {"name": "remote_func", "args": [123,321], "serial_id": 1}
# 第二步： 生成一个future 放到一个dict里面 futures[serial_id] = future, 等待返回值
# 第三步： 接收方（比如JsonHandler）收到后 执行 "remote_func"。
#         发送返回值 {"name": 1, "args": "返回数据" }
# 第四步： 调用方接收到返回数据， 根据 fu = futures.get(name) 获取到 等待的future。
#           fu.set_result(args) 
# 第五步： 获取到结果
# 2.如果没有返回值
# 发送 {"name": "remote_func", "args": [123,321]}



# TCP handler
g_msg_handler = JsonHandler() # 函数对象，也可以是一个  **[异步函数]**
def tcp_handle(func):  # tcp handler装饰器
    g_msg_handler.regist_handler(func)
    return func


@tcp_handle
async def remote_func(session_id, a, b):
    print(a, b)
    return {"aaa":"bbb"}


loop = asyncio.get_event_loop()
g_tcp_server = TcpServer("0.0.0.0",             # 监听地址
                         12345,                 # 监听端口
                         g_msg_handler,         # 用来处理数据的【异步】函数
                         TcpSimpleProto(),      # 用来解析包的对象
                         1,                     # 心跳时间间隔
                         5,                     # 当有~次心跳检测没有检测到数据包，就认定为该链接已经断开。
                         loop)                  # asyncio loop
```

## 如何自定义协议
```python
import struct
from l0n0ltcp.tcp_proto_base import TcpProtoBase, StreamReader

class TcpSimpleProto(TcpProtoBase):
    def make_heart_msg(self) -> bytes:
        return b"\x00\x00\x00"

    def build_msg(self, data: bytes) -> bytes:
        data_len = len(data) + 4
        size = data_len & 0xFFFF
        count = (data_len >> 16) & 0xFF
        header = struct.pack("!HBI", size, count, 0)
        return header + data

    async def read_msg(self, reader: StreamReader):
        header = await reader.readexactly(3)
        size, count = struct.unpack("!HB", header)
        size = (count << 16) | size
        if size <= 0:
            return
        return await reader.readexactly(size)
```

## 穿越GFW

```
1.服务器执行
usage: l0n0ltranssocks5 [-h] listenhost listenport password sock5port

创建SOCKS5服务器,并使用加密通道代理

positional arguments:
  listenhost  监听host
  listenport  监听端口
  password    密钥
  sock5port   socks5监听端口(并不需要再启动一个socks5,自动启动一个socks5)

optional arguments:
  -h, --help  show this help message and exit

2.本地主机执行 
usage: l0n0ltransclient [-h] serverhost serverport localhost localport password

创建本地代理服务器

positional arguments:
  serverhost  服务器监听host
  serverport  服务器监听端口
  localhost   本地服务host
  localport   本地服务端口
  password    密钥

optional arguments:
  -h, --help  show this help message and exit
```

## socks5 服务器
### 代码
```python
from l0n0ltcp.tcp_server import TcpServer
from l0n0ltcp.socks5_callback import Socks5ServerCallback
from l0n0ltcp.socks5_proto import Socks5ServerProto
server = TcpServer('0.0.0.0', 1080,
                   Socks5ServerCallback(),
                   Socks5ServerProto(),
                   loop=asyncio.get_event_loop())
server.start()
asyncio.get_event_loop().run_forever()
```
### 命令行
```
usage: l0n0lsocks5 [-h] listenhost listenport

创建SOCKS5服务器(目前仅支持CONNECT命令)

positional arguments:
  listenhost  监听host
  listenport  监听端口

optional arguments:
  -h, --help  show this help message and exit
```

## 加密信道

### 代码
```python
from l0n0ltcp.tcp_simple_proto import TcpSimpleProto
from l0n0ltcp.trans_callback import TransServerCallback, TransLocalServerCallback
from l0n0ltcp.tcp_server import TcpServer
from l0n0ltcp.tcp_proto_base import TcpProtoBase
from l0n0ltcp.sym_enc_chacha20 import SymEncChaCha20
# 远端服务器
serverremote = TcpServer('0.0.0.0', 12343,
                    TransServerCallback('baidu.com', 443, SymEncChaCha20("123")),
                    TcpSimpleProto(),loop=asyncio.get_event_loop())
serverremote.start()

# 本地服务器
serverlocal = TcpServer('0.0.0.0', 12345,
                    TransLocalServerCallback('127.0.0.1', 12343, SymEncChaCha20("123")),
                    TcpProtoBase(),
                    loop=asyncio.get_event_loop())
serverlocal.start()

asyncio.get_event_loop().run_forever()

# 访问 localhost:12345 相当于访问 baidu.com 443 中间的过程是chacha20加密的
```

### 命令行
```
1.服务器
usage: l0n0ltransserver [-h] listenhost listenport password targethost targetport

创建加密信道服务器

positional arguments:
  listenhost  监听host
  listenport  监听端口
  password    密钥
  targethost  要代理的host
  targetport  要代理的端口

optional arguments:
  -h, --help  show this help message and exit

2.客户端
usage: l0n0ltransclient [-h] serverhost serverport localhost localport password

创建本地代理服务器

positional arguments:
  serverhost  服务器监听host
  serverport  服务器监听端口
  localhost   本地服务host
  localport   本地服务端口
  password    密钥

optional arguments:
  -h, --help  show this help message and exit
```
