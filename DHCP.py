import socket

# Define parameters for ports and packet maximum size
MAX_BYTES = 1024
serverPort = 67
clientPort = 68


class DHCP_server(object):
    def server(self):
        print("DHCP server starting...\n")

        # Create a socket for the server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind(('0.0.0.0', serverPort))
        destination = ('255.255.255.255', clientPort)

        while 1:
            try:
                print("Waiting for a DHCP discovery...")
                data, address = s.recvfrom(MAX_BYTES)
                print("Received a DHCP discovery.")
                # print(data)

                print("Sending a DHCP offer...")
                data = DHCP_server.offer_get()
                s.sendto(data, destination)
                while 1:
                    try:
                        print("Waiting for a DHCP request...")
                        data, address = s.recvfrom(MAX_BYTES)
                        print("Received DHCP request.")
                        # print(data)

                        print("Sending a DHCP pack... \n")
                        data = DHCP_server.pack_get()
                        s.sendto(data, destination)
                        break
                    except:
                        raise
            except:
                raise

    def offer_get():

        op_Code = bytes([0x02])
        hw_Type = bytes([0x01])
        hw_Len = bytes([0x06])
        hops = bytes([0x00])
        XID = bytes([0x39, 0x03, 0xF3, 0x26])
        secs = bytes([0x00, 0x00])
        flags = bytes([0x00, 0x00])
        ciaddr = bytes([0x00, 0x00, 0x00, 0x00])
        yiaddr = bytes([0xC0, 0xA8, 0x01, 0x64])  # 192.168.1.100
        siaddr = bytes([0xC0, 0xA8, 0x01, 0x01])  # 192.168.1.1
        giaddr = bytes([0x00, 0x00, 0x00, 0x00])
        c_Hwaddr1 = bytes([0x00, 0x05, 0x3C, 0x04])
        c_Hwaddr2 = bytes([0x8D, 0x59, 0x00, 0x00])
        c_Hwaddr3 = bytes([0x00, 0x00, 0x00, 0x00])
        c_Hwaddr4 = bytes([0x00, 0x00, 0x00, 0x00])
        c_Hwaddr5 = bytes(192)
        magic_Cookie = bytes([0x63, 0x82, 0x53, 0x63])
        DHCP_Options1 = bytes([53, 1, 2])  # DHCP Offer
        DHCP_Options2 = bytes([1, 4, 0xFF, 0xFF, 0xFF, 0x00])  # 255.255.255.0 subnet mask
        DHCP_Options3 = bytes([3, 4, 0xC0, 0xA8, 0x01, 0x01])  # 192.168.1.1 router
        DHCP_Options4 = bytes([51, 4, 0x00, 0x01, 0x51, 0x80])  # 86400s(1 day) IP address lease time
        DHCP_Options5 = bytes([54, 4, 0xC0, 0xA8, 0x01, 0x01])  # DHCP server

        pack = op_Code + hw_Type + hw_Len + hops + XID + secs + flags + ciaddr + yiaddr + siaddr + giaddr + c_Hwaddr1 + c_Hwaddr2 + c_Hwaddr3 + c_Hwaddr4 + c_Hwaddr5 + magic_Cookie + DHCP_Options1 + DHCP_Options2 + DHCP_Options3 + DHCP_Options4 + DHCP_Options5

        return pack

    def pack_get():
        op_Code = bytes([0x02])
        hw_Type = bytes([0x01])
        hw_Len = bytes([0x06])
        hops = bytes([0x00])
        XID = bytes([0x39, 0x03, 0xF3, 0x26])
        secs = bytes([0x00, 0x00])
        flags = bytes([0x00, 0x00])
        ciaddr = bytes([0x00, 0x00, 0x00, 0x00])
        yiaddr = bytes([0xC0, 0xA8, 0x01, 0x64])
        siaddr = bytes([0xC0, 0xA8, 0x01, 0x01])
        giaddr = bytes([0x00, 0x00, 0x00, 0x00])
        c_Hwaddr1 = bytes([0x00, 0x05, 0x3C, 0x04])
        c_Hwaddr2 = bytes([0x8D, 0x59, 0x00, 0x00])
        c_Hwaddr3 = bytes([0x00, 0x00, 0x00, 0x00])
        c_Hwaddr4 = bytes([0x00, 0x00, 0x00, 0x00])
        c_Hwaddr5 = bytes(192)
        magic_Cookie = bytes([0x63, 0x82, 0x53, 0x63])
        DHCP_Options1 = bytes([53, 1, 5])  # DHCP ACK(value = 5)
        DHCP_Options2 = bytes([1, 4, 0xFF, 0xFF, 0xFF, 0x00])  # 255.255.255.0 subnet mask
        DHCP_Options3 = bytes([3, 4, 0xC0, 0xA8, 0x01, 0x01])  # 192.168.1.1 router
        DHCP_Options4 = bytes([51, 4, 0x00, 0x01, 0x51, 0x80])  # 86400s(1 day) IP address lease time
        DHCP_Options5 = bytes([54, 4, 0xC0, 0xA8, 0x01, 0x01])  # DHCP server

        pack = op_Code + hw_Type + hw_Len + hops + XID + secs + flags + ciaddr + yiaddr + siaddr + giaddr + c_Hwaddr1 + c_Hwaddr2 + c_Hwaddr3 + c_Hwaddr4 + c_Hwaddr5 + magic_Cookie + DHCP_Options1 + DHCP_Options2 + DHCP_Options3 + DHCP_Options4 + DHCP_Options5

        return pack


if __name__ == '__main__':
    dhcp_server = DHCP_server()
    dhcp_server.server()
