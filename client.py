import socket
import struct
from random import randint
from scapy.all import get_if_raw_hwaddr, conf
from time import sleep

hw = get_if_raw_hwaddr(conf.iface)[1]
xid = randint(0, 0xFFFFFFFF)


class DHCPDiscover:
    def __init__(self, xid, hw):
        self.TransactionID = struct.pack("!L", xid) #generate random transactionID
        self.macInBytes = hw

    def DHCP(self): #DHCP header packet
        op = b'\x01'
        HwType = b'\x01'
        HwAddrLen = b'\x01'
        HopC = b'\x00'
        TransactionID = self.TransactionID
        NumOfSec = b'\x00\x00'
        Flags_B_Res = b'\x00\x00'
        ciaddr = b'\x00\x00\x00\x00'
        yiaddr = b'\x00\x00\x00\x00'
        siaddr = b'\x00\x00\x00\x00'
        giaddr = b'\x00\x00\x00\x00'
        chwaddr = self.macInBytes
        chwpadding = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        srchostname = b'\x00' * 64
        bootfilename = b'\x00' * 128
        magic_cookie = b'\x63\x82\x53\x63'
        msg_type = b'\x35\x01\x01' #DHCP message type
        end = b'\xff'
        packet = op+HwType+HwAddrLen+HopC+TransactionID+NumOfSec+Flags_B_Res+ciaddr+yiaddr+siaddr+giaddr+chwaddr+chwpadding+srchostname+bootfilename+magic_cookie+msg_type+end
        return packet

    def dhcp_req(self): #request from DHCP server the desired IP address
        op = b'\x01'
        HwType = b'\x01'
        HwAddrLen = b'\x06'
        HopC = b'\x00'
        TransactionID = self.TransactionID
        NumOfSec = b'\x00\x00'
        Flags_B_Res = b'\x00\x00'
        ciaddr = b'\x00\x00\x00\x00'
        yiaddr = b'\x00\x00\x00\x00'
        siaddr = b'\x00\x00\x00\x00'
        giaddr = b'\x00\x00\x00\x00'
        chwaddr = self.macInBytes
        chwpadding = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        srchostname = b'\x00' * 64
        bootfilename = b'\x00' * 128
        magic_cookie = b'\x63\x82\x53\x63'
        msg_type = b'\x35\x01\x01'  # DHCP message type
        clientID = b'\x3d\x06\x01' + self.macInBytes
        req_addr = b'\x32\x04' + socket.inet_aton('0.0.0.0')
        serverID = b'\x36\x04' + socket.inet_aton('0.0.0.0')
        par_req_list = b'\x37\x05\x01\x03\x06\x0f\x1f'
        end = b'\xff'
        packet2 = op + HwType + HwAddrLen + HopC + TransactionID + NumOfSec + Flags_B_Res + ciaddr + yiaddr + siaddr + giaddr + chwaddr + chwpadding + srchostname + bootfilename + magic_cookie + msg_type + clientID + req_addr + serverID + par_req_list + end
        return packet2


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
obj = DHCPDiscover(xid, hw)
packet = obj.DHCP()
req = obj.dhcp_req()

s.sendto(packet, ("255.255.255.255", 67))
print("discover sent")
sleep(3)
s.sendto(req, ("255.255.255.255", 67))
print("request sent")




