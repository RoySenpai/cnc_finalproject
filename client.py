import socket

# Define parameters for ports and packet maximum size
MAX_SIZE = 1024
server_Port = 67
client_Port = 68


class DHCP_client(object):
    def client(self):
        # Create a socket for the client and send a discovery pacakge in a broadcast
        print("DHCP Client starting...\n")
        destination = ('<broadcast>', server_Port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(('0.0.0.0', client_Port))

        print("Sending DHCP discovery.")
        data = DHCP_client.get_Discover()
        sock.sendto(data, destination)

        data, address = sock.recvfrom(MAX_SIZE)
        print("Received DHCP offers.")
        # print(data)

        print("Sending DHCP request.")
        data = DHCP_client.get_Request()
        sock.sendto(data, destination)

        data, address = sock.recvfrom(MAX_SIZE)
        print("Received DHCP pack.\n")
        # print(data)
        sock.close()

    def get_Discover():
        # DHCP message format
        op_Code = bytes([0x01])
        hw_Type = bytes([0x01])
        hw_Len = bytes([0x06])
        hops = bytes([0x00])
        XID = bytes([0x39, 0x03, 0xF3, 0x26])
        secs = bytes([0x00, 0x00])
        flags = bytes([0x00, 0x00])
        ciaddr = bytes([0x00, 0x00, 0x00, 0x00])
        yiaddr = bytes([0x00, 0x00, 0x00, 0x00])
        siaddr = bytes([0x00, 0x00, 0x00, 0x00])
        giaddr = bytes([0x00, 0x00, 0x00, 0x00])
        c_Hwaddr1 = bytes([0x00, 0x05, 0x3C, 0x04])
        c_Hwaddr2 = bytes([0x8D, 0x59, 0x00, 0x00])
        c_Hwaddr3 = bytes([0x00, 0x00, 0x00, 0x00])
        c_Hwaddr4 = bytes([0x00, 0x00, 0x00, 0x00])
        c_Hwaddr5 = bytes(192)
        magic_Cookie = bytes([0x63, 0x82, 0x53, 0x63])
        DHCP_Options1 = bytes([53, 1, 1])
        DHCP_Options2 = bytes([50, 4, 0xC0, 0xA8, 0x01, 0x64])

        pack = op_Code + hw_Type + hw_Len + hops + XID + secs + flags + ciaddr + yiaddr + siaddr + giaddr + c_Hwaddr1 + c_Hwaddr2 + c_Hwaddr3 + c_Hwaddr4 + c_Hwaddr5 + magic_Cookie + DHCP_Options1 + DHCP_Options2

        return pack

    def get_Request():
        # DHCP message format
        op_Code = bytes([0x01])
        hw_Type = bytes([0x01])
        hw_Len = bytes([0x06])
        hops = bytes([0x00])
        XID = bytes([0x39, 0x03, 0xF3, 0x26])
        secs = bytes([0x00, 0x00])
        flags = bytes([0x00, 0x00])
        ciaddr = bytes([0x00, 0x00, 0x00, 0x00])
        yiaddr = bytes([0x00, 0x00, 0x00, 0x00])
        siaddr = bytes([0x00, 0x00, 0x00, 0x00])
        giaddr = bytes([0x00, 0x00, 0x00, 0x00])
        c_Hwaddr1 = bytes([0x00, 0x0C, 0x29, 0xDD])
        c_Hwaddr2 = bytes([0x5C, 0xA7, 0x00, 0x00])
        c_Hwaddr3 = bytes([0x00, 0x00, 0x00, 0x00])
        c_Hwaddr4 = bytes([0x00, 0x00, 0x00, 0x00])
        c_Hwaddr5 = bytes(192)
        magic_Cookie = bytes([0x63, 0x82, 0x53, 0x63])
        DHCP_Options1 = bytes([53, 1, 3])
        DHCP_Options2 = bytes([50, 4, 0xC0, 0xA8, 0x01, 0x64])
        DHCP_Options3 = bytes([54, 4, 0xC0, 0xA8, 0x01, 0x01])

        pack = op_Code + hw_Type + hw_Len + hops + XID + secs + flags + ciaddr + yiaddr + siaddr + giaddr + c_Hwaddr1 + c_Hwaddr2 + c_Hwaddr3 + c_Hwaddr4 + c_Hwaddr5 + magic_Cookie + DHCP_Options1 + DHCP_Options2 + DHCP_Options3

        return pack

    def dns_client(query, server):
        # create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # send DNS query to server
        sock.sendto(query.encode('utf-8'), (server, 53))

        # receive DNS response from server
        data, address = sock.recvfrom(1024)

        # print DNS response
        print(data.decode('utf-8'))

        # close socket
        sock.close()


if __name__ == '__main__':
    dhcp_client = DHCP_client()
    dhcp_client.client()

    # create a socket for the dns client
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('localhost', 9999))

    domain_name = input('Enter domain name: ')

    # send the domain name entered by user to the dns server
    sock.send(domain_name.encode('utf-8'))

    # receive the IP address response from the dns server
    ip_address = sock.recv(1024).decode('utf-8')

    print('IP Address:', ip_address)

    sock.close()
