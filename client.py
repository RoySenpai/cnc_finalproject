import socket


# Define variables for ports and packet maximum size
max_Size = 1024
server_DHCPPort = 67
client_DHCPPort = 68
port = 1234
ip = "127.0.0.1"


class DHCP_client(object):
    def client(self):
        # Create a socket for the client and send a discovery pacakge in a broadcast
        print("DHCP Client is starting...\n")
        destination = ('<broadcast>', server_DHCPPort)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(('0.0.0.0', client_DHCPPort))

        print("Sending DHCP discovery.")
        data = DHCP_client.get_Discover()
        sock.sendto(data, destination)

        data, address = sock.recvfrom(max_Size)
        print("Received DHCP offers.")

        print("Sending DHCP request.")
        data = DHCP_client.get_Request()
        sock.sendto(data, destination)

        data, address = sock.recvfrom(max_Size)
        print("Received DHCP pack.\n")
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


def dns_client():
    # create a socket for the dns client
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('localhost', 9999))

    domain_Name = input('Enter domain name: ')

    # send the domain name entered by user to the dns server
    sock.send(domain_Name.encode('utf-8'))

    # receive the IP address response from the dns server
    ip_Address = sock.recv(1024).decode('utf-8')

    print('IP Address:', ip_Address)
    sock.close()


def app_client_TCP():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    list_of_Queries = sock.recv(max_Size).decode("utf-8")
    print(list_of_Queries)
    while True:
        query = input("Please enter the name of the query you wish to use or the word nothing to stop the loop: ")
        sock.send(bytes(query, "utf-8"))
        if query == "nothing":
            break


if __name__ == '__main__':
    # Starts the DHCP client
    # dhcp_client = DHCP_client()
    # dhcp_client.client()

    # Starts the DNS client
    # dns_client()

    # Starts the app client
    app_client_TCP()
