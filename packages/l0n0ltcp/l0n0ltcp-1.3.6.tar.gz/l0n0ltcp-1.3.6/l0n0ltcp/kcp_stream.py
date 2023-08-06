import asyncio
import socket
import time
from typing import Dict, Tuple
from l0n0lkcp.ikcp import Ikcp


class KcpEndPoint:
    def __init__(self,
                 owner,
                 sock: socket.socket,
                 conv: int,
                 id: int,
                 addr: Tuple[str, int],
                 loop=asyncio.get_event_loop(),
                 timeout_time=60 * 1000,
                 kcp_interval: int = 0.01,
                 nodelay: int = 0, interval: int = 100, resend: int = 0, nc: int = 0) -> None:
        u'''
        ### 最快: nodelay(1, 20, 2, 1)
        * nodelay: 0表示关闭nodelay(默认值), 1:开启
        * interval: 内部更新时间间隔（单位：毫秒）(默认100ms)
        * resend: 开启或关闭快速重传 0:关闭（默认） 1: 开启
        * nc: 是否开启拥塞控制 0:关闭(默认) 1:开启
        '''
        self._owner = owner
        self.sock = sock
        self.conv = conv
        self.id = id
        self.addr = addr
        self.loop = loop
        self.kcp_interval = kcp_interval
        self.timeout_time = timeout_time
        self._timeout = False
        self._buffer = bytearray()
        self._closed = False
        self._exception = None
        self._read_future = None
        self._read_target_size = 0
        self._update_timestamp = 0
        self._input_timestamp = 0
        self._kcp = Ikcp(conv, lambda
                         data, size: self.sock.sendto(data[:size], self.addr))
        self._kcp.nodelay(nodelay, interval, resend, nc)
        self.loop.call_later(self.kcp_interval, self._update_kcp)

    def _check_timeout(self, current_time=None):
        current_time = current_time or int(time.time() * 1000)
        if self._input_timestamp != 0 and current_time - self._input_timestamp >= self.timeout_time:
            self.set_exception(Exception("Kcp Endpoint Time out"))

    def __repr__(self):
        info = ['KcpEndPoint']
        if self._buffer:
            info.append(f'{len(self._buffer)} bytes')
        if self._read_future:
            info.append(f'read_future={self._read_future!r}')
        if self._read_target_size:
            info.append(f'read_target_size={self._read_target_size!r}')
        if self._exception:
            info.append(f'exception={self._exception!r}')
        if self._kcp:
            info.append(f'transport={self._kcp!r}')
        return '<{}>'.format(' '.join(info))

    def _cancel_read_future(self):
        read_future = self._read_future
        if read_future is not None:
            self._read_future = None
            if not read_future.done():
                read_future.cancel()

    def _update_kcp(self):
        if self.is_closing() or self._exception:
            return
        try:
            current_time = int(time.time() * 1000)
            self._check_timeout(current_time)
            if self._exception is not None:
                return

            if self._update_timestamp == 0:
                elapse = 0
            else:
                elapse = current_time - self._update_timestamp
            self._update_timestamp = current_time

            # 更新KCP状态
            self._kcp.update(elapse)

            # 接收kcp数据
            msg_data, lens = self._kcp.recv()
            if lens < -1:
                self.close()
                return

            if lens > 0:
                # 将数据放到read_buffer
                self._buffer.extend(msg_data[:lens])
                # 检查是否有需要返回的future
                if self._read_future and not self._read_future.done() \
                        and len(self._buffer) >= self._read_target_size:
                    data = self._get_exact_data(self._read_target_size)
                    self._read_future.set_result(data)
            # 调用下一次循环
            self.loop.call_later(self.kcp_interval, self._update_kcp)
            return
        except Exception as e:
            self.set_exception(e)
        # 关闭
        self._closed = True
        self._cancel_read_future()

    def exception(self):
        return self._exception

    def set_exception(self, e):
        self._exception = e
        if self._read_future is not None and not self._read_future.done():
            self._read_future.set_exception(e)

    def close(self):
        self._closed = True
        if self._owner is not None:
            self._owner.on_endpoint_close(self)
        if self._read_future is not None and not self._read_future.done():
            self._read_future.cancel()

    def is_closing(self):
        return self._closed

    async def drain(self):
        if self._closed:
            return
        self._kcp.flush()

    async def read(self, n=-1):
        if self._closed:
            self.set_exception(Exception("Kcp Endpoint Closed"))
        self._check_timeout()
        if self._exception is not None:
            raise self._exception
        if n == 0:
            return b''
        if n < 0:
            data = bytes(self._buffer)
            self._buffer.clear()
            return data
        if len(self._buffer) == 0:
            self._read_future = self.loop.create_future()
            self._read_target_size = 0
            await self._read_future
        data = bytes(self._buffer[:n])
        del self._buffer[:n]
        await asyncio.sleep(0, loop=self.loop)
        return data

    def _get_exact_data(self, n):
        if n == 0:
            return b''
        buffer_len = len(self._buffer)
        if buffer_len == n:
            data = bytes(self._buffer)
            self._buffer.clear()
            return data
        elif buffer_len > n:
            data = bytes(self._buffer[:n])
            del self._buffer[:n]
            return data

    def at_eof(self):
        return False

    def write(self, data: bytes):
        if self._closed:
            self.set_exception(Exception("Kcp Endpoint Closed"))
        self._check_timeout()
        if self._exception is not None:
            raise self._exception
        self._kcp.send(data)

    async def readexactly(self, n):
        if n < 0:
            raise ValueError('read size can not be less than zero')
        if self._exception is not None:
            raise self._exception
        data = self._get_exact_data(n)
        if data:
            return data
        self._read_future = self.loop.create_future()
        self._read_target_size = n
        return await self._read_future

    def input(self, data):
        self._kcp.input(data)
        self._input_timestamp = int(time.time() * 1000)


class KcpServer:
    def __init__(self,
                 conv: int,
                 sock: socket.socket,
                 client_connected_cb,
                 read_max_size=65535,
                 timeout_time=60 * 1000,
                 loop: asyncio.BaseEventLoop = asyncio.get_event_loop(),
                 kcp_loop_interval: float = 0.01,
                 nodelay: int = 0, interval: int = 100,
                 resend: int = 0, nc: int = 0) -> None:
        self._conv = conv
        self._sock = sock
        self._loop = loop
        self._kcp_loop_interval = kcp_loop_interval
        self._nodelay = nodelay
        self._interval = interval
        self._resend = resend
        self._nc = nc
        self._client_connected_cb = client_connected_cb
        self._read_max_size = read_max_size
        self._timeout_time = timeout_time
        self._serving_task = None
        self._max_id = 0

    def _gen_id(self):
        self._max_id = (self._max_id + 1) % 0x7FFFFFFF
        return self._max_id

    def on_endpoint_close(self, endpoint: KcpEndPoint):
        target_id = f"{endpoint.addr[0]}{endpoint.addr[1]}"
        if self._endpoints.get(target_id):
            del self._endpoints[target_id]

    def get_loop(self):
        return self._loop

    def is_serving(self):
        return self._serving_task is not None \
            and not self._serving_task.cancelled() \
            and not self._serving_task.done()

    async def _serve_loop(self):
        self._endpoints: Dict[str, KcpEndPoint] = {}
        while True:
            try:
                data, addr = self._sock.recvfrom(self._read_max_size)
                target_id = f"{addr[0]}{addr[1]}"
                target_endpoint = self._endpoints.get(target_id)
                if target_endpoint is None:
                    id = self._gen_id()
                    target_endpoint = KcpEndPoint(
                        self,
                        self._sock,
                        self._conv,
                        id,
                        addr,
                        self._loop,
                        self._timeout_time,
                        self._kcp_loop_interval,
                        self._nodelay,
                        self._interval,
                        self._resend,
                        self._nc)
                    self._endpoints[target_id] = target_endpoint
                    self._loop.create_task(
                        self._client_connected_cb(target_endpoint, target_endpoint))
                target_endpoint.input(data)
            except:
                pass
            await asyncio.sleep(0.0001, loop=self._loop)

    async def start_serving(self):
        if self.is_serving():
            return
        self._serving_task = self._loop.create_task(self._serve_loop())

    def close(self):
        endpoints = self._endpoints
        if endpoints is None:
            return
        self._endpoints = None

        for endpoint in endpoints.values():
            endpoint.close()

        self._sock.close()

        if (self._serving_forever_fut is not None
                and not self._serving_forever_fut.done()):
            self._serving_forever_fut.cancel()
            self._serving_forever_fut = None

    async def serve_forever(self):
        if self._serving_forever_fut is not None:
            raise RuntimeError(
                f'serveris already being awaited on serve_forever()')
        await self.start_serving()
        self._serving_forever_fut = self._loop.create_future()
        try:
            await self._serving_forever_fut
        except asyncio.exceptions.CancelledError:
            try:
                self.close()
            finally:
                raise
        finally:
            self._serving_forever_fut = None

# 考虑到 A -> B 的包 socket.recvfrom 后的 addr （ip,port)可能不一样，所以kcp可能不能这样用，所以先废弃
async def start_server(conv: int,
                       client_connected_cb: callable,
                       host=None, port=None,
                       loop=asyncio.get_event_loop(),
                       timeout_time=60 * 1000,
                       kcp_loop_interval=0.01,
                       nodelay=1, interval=20, resend=3, nc=1):
    '''
    开启UDP的KCP服务器
    * conv: 相同的conv的客户端服务器才能通信
    * client_connected_cb: 当有新的udp ip和端口进入的时候
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(0)
    s.bind((host, port))
    return KcpServer(conv, s, client_connected_cb, timeout_time=timeout_time, loop=loop,
                     kcp_loop_interval=kcp_loop_interval,
                     nodelay=nodelay, interval=interval, resend=resend, nc=nc)


async def open_connection(conv: int,
                          host=None, port=None,
                          loop=asyncio.get_event_loop(),
                          timeout_time=60 * 1000,
                          kcp_loop_interval=0.01,
                          nodelay=1, interval=20, resend=3, nc=1):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(0)
    reader = KcpEndPoint(None, s, conv, 0, (host, port), loop, timeout_time,
                         kcp_interval=kcp_loop_interval,
                         nodelay=nodelay, interval=interval, resend=resend, nc=nc)
    writer = reader
    return reader, writer
