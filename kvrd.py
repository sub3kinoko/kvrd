import os
import subprocess
import fcntl
import linux
import socket
import binascii

DESTIP = "52.68.118.158"

NIC1 = "enp0s25"
NIC2 = "ppp0"

tun = os.open('/dev/net/tun', os.O_RDWR)
ifr = linux.ifreq(name=b'tun0', flags=linux.IFF_NO_PI|linux.TUN_TUN_DEV)
fcntl.ioctl(tun, linux.TUNSETIFF, ifr)

subprocess.check_call('sudo ifconfig tun0 192.168.120.1 netmask 255.255.255.0 up', shell=True)

sock1 = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
sock1.setsockopt(socket.SOL_SOCKET, 25, str(NIC1 + '\0').encode('utf-8'))

sock2 = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
sock2.setsockopt(socket.SOL_SOCKET, 25, str(NIC2 + '\0').encode('utf-8'))

while True:
  data = os.read(tun, 1500)
#  print(binascii.hexlify(data))

  if int.from_bytes(data[0:1], 'big') >> 4 == 4:
    print("Sending on " + NIC1)
    d = bytearray(data)
    d[10:12] = [0,0]
    d[12:16] = [0,0,0,0]
    d[16:20] = socket.inet_aton(DESTIP)
    d[26:28] = [0,0]
    sock1.sendto(d, (DESTIP, 0))
    print(binascii.hexlify(d))

  data = os.read(tun, 1500)
#  print(binascii.hexlify(data))

  if int.from_bytes(data[0:1], 'big') >> 4 == 4:
    print("Sending on " + NIC2)
    d = bytearray(data)
    d[10:12] = [0,0]
    d[12:16] = [0,0,0,0]
    d[16:20] = socket.inet_aton(DESTIP)
    d[26:28] = [0,0]
    sock2.sendto(d, (DESTIP, 0))
    print(binascii.hexlify(d))

