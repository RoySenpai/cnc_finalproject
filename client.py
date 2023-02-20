import socket
import binascii
import struct
from random import randint
from scapy.all import get_if_raw_hwaddr, conf
from time import sleep

hw = get_if_raw_hwaddr(conf.iface)[1]
xid = randint(0, 0xFFFFFFFF)


class DHCPDiscover:
    def __init__(self, xid, hw):
        self.TransactionID = struct.pack("!L", xid)
        self.macInBytes = hw

    def DHCP(self): #DHCP header packet
        op = '\x01'
        HwType = '\x01'
        HwAddrLen = '\x06'
        HopC = '\x00'
        TransactionID = self.TransactionID
        NumOfSec = '\x00\x00'
        Flags_B_Res = '\x00\x00'
        ciaddr = '\x00\x00\x00\x00'
        yiaddr = '\x00\x00\x00\x00'
        siaddr = '\x00\x00\x00\x00'
        giaddr = '\x00\x00\x00\x00'
        chwaddr = self.macInBytes
        chwpadding = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        srchostname = '\x00' * 64
        bootfilename = '\x00' * 128
        magic_cookie = '\x63\x82\x53\x63' # not sure if this is needed
        msg_type = '\x35\x01\x01' #DHCP message type
        end = '\xff'
        packet = op+HwType+HwAddrLen+HopC+TransactionID+NumOfSec+Flags_B_Res+ciaddr+yiaddr+siaddr+giaddr+chwaddr+chwpadding+srchostname+bootfilename+magic_cookie+msg_type+end
        return packet
    def dhcp_req(self):
        op = '\x01'
        HwType = '\x01'
        HwAddrLen = '\x06'
        HopC = '\x00'
        TransactionID = self.TransactionID
        NumOfSec = '\x00\x00'
        Flags_B_Res = '\x00\x00'
        ciaddr = '\x00\x00\x00\x00'
        yiaddr = '\x00\x00\x00\x00'
        siaddr = '\x00\x00\x00\x00'
        giaddr = '\x00\x00\x00\x00'
        chwaddr = self.macInBytes
        chwpadding = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        srchostname = '\x00' * 64
        bootfilename = '\x00' * 128
        magic_cookie = '\x63\x82\x53\x63'  # not sure if this is needed
        msg_type = '\x35\x01\x01'  # DHCP message type
        clientID = '\x3d\x07\x01' + self.macInBytes
        req_addr = '\x32\x04' + socket.inet_aton('127.0.0.1')
        serverID = '\x36\x04' + socket.inet_aton('127.0.0.1')
        par_req_list = '\x37\x03\x03\x01\x06'
        end = '\xff'
        packet2 = op+HwType+HwAddrLen+HopC+TransactionID+NumOfSec+Flags_B_Res+ciaddr+yiaddr+siaddr+giaddr+chwaddr+chwpadding+srchostname+bootfilename+magic_cookie+msg_type+clientID+req_addr+serverID+par_req_list+end
        return packet2


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
obj = DHCPDiscover(xid, hw)
packet = obj.DHCP()
req = obj.dhcp_req()

s.sendto(packet, ("127.0.0.1", 67))
print("discover sent")
sleep(1)
s.sendto(req, ("127.0.0.1", 67))
print("request sent")




