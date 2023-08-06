import socket
import sys
from impacket import ImpactDecoder, ImpactPacket


if sys.platform == "win32":
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    s.bind(("192.168.1.57", 0))
    s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    while True:
        data = s.recvfrom(65535)
        ip_decoder = ImpactDecoder.IPDecoder()
        ip_packet = ip_decoder.decode(data)
        print(ip_packet.get_ip_address())
        
if sys.platform == "linux":
    # s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x1234))
    s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0X0800))
    s.bind(("eth0", 0))
    # s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    while True:
        data = s.recvfrom(1024)
        print(data)