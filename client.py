import socket
import uuid

# Define variables for ports and packet maximum size
max_Size = 1024
server_DHCPPort = 67
client_DHCPPort = 68
port = 20159
ip = "127.0.0.1"


class DHCP_client(object):
    def client(self):
        # Create a socket for the client and send a discovery pacakge in a broadcast
        print("[DHCP] DHCP Client is starting...\n")
        destination = ('<broadcast>', server_DHCPPort)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(('0.0.0.0', client_DHCPPort))

        print("[DHCP] Sending DHCP discovery.")
        data = DHCP_client.get_Discover()
        sock.sendto(data, destination)

        data, address = sock.recvfrom(max_Size)
        print("[DHCP] Received DHCP offers.")

        print("[DHCP] Sending DHCP request.")
        data = DHCP_client.get_Request()
        sock.sendto(data, destination)

        data, address = sock.recvfrom(max_Size)
        print("[DHCP] Received DHCP pack.\n")
        sock.close()

    def get_Discover():
        # DHCP message format for discovery package
        op_Code = bytes([0x01])                                 # Type - Request (1 byte)
        hw_Type = bytes([0x01])                                 # Hardware type - Ethernet (1 byte)
        hw_Len = bytes([0x06])                                  # MAC address length
        hops = bytes([0x00])                                    # Hops (1 byte)
        XID = bytes([0x39, 0x03, 0xF3, 0x26])                   # Transaction ID (4 bytes)
        secs = bytes([0x00, 0x00])                              # Seconds elapsed (2 bytes)
        flags = bytes([0x00, 0x00])                             # Flags (2 bytes)
        ciaddr = bytes([0x00, 0x00, 0x00, 0x00])                # Client IP address (4 bytes)
        yiaddr = bytes([0x00, 0x00, 0x00, 0x00])                # Your IP address (4 bytes)
        siaddr = bytes([0x00, 0x00, 0x00, 0x00])                # Server IP address (4 bytes)
        giaddr = bytes([0x00, 0x00, 0x00, 0x00])                # Gateway IP address (4 bytes)
        c_Hwaddr1 = bytes([0x00, 0x05, 0x3C, 0x04])             # Client hardware address (4 bytes)
        c_Hwaddr2 = bytes([0x8D, 0x59, 0x00, 0x00])             # Client hardware address (4 bytes)
        c_Hwaddr3 = bytes([0x00, 0x00, 0x00, 0x00])             # Client hardware address (4 bytes) - Unused
        c_Hwaddr4 = bytes([0x00, 0x00, 0x00, 0x00])             # Client hardware address (4 bytes) - Unused
        c_Hwaddr5 = bytes(192)                                  # Zero padding (192 bytes)
        magic_Cookie = bytes([0x63, 0x82, 0x53, 0x63])          # Magic cookie (4 bytes)
        DHCP_Options1 = bytes([53, 1, 1])                       # DHCP message type - Discover (3 bytes)
        DHCP_Options2 = bytes([50, 4, 192, 168, 1, 100])        # Requested IP address (6 bytes)
        END_packet = bytes([0xFF])                              # End of packet (1 byte) - Always 0xFF

        pack = op_Code + hw_Type + hw_Len + hops + XID + secs + flags + ciaddr + yiaddr + siaddr + giaddr + c_Hwaddr1 + c_Hwaddr2 + c_Hwaddr3 + c_Hwaddr4 + c_Hwaddr5 + magic_Cookie + DHCP_Options1 + DHCP_Options2 + END_packet

        return pack

    def get_Request():
        # DHCP message format
        op_Code = bytes([0x01])                                 # Type - Request (1 byte)
        hw_Type = bytes([0x01])                                 # Hardware type - Ethernet (1 byte)
        hw_Len = bytes([0x06])                                  # MAC address length
        hops = bytes([0x00])                                    # Hops (1 byte)
        XID = bytes([0x39, 0x03, 0xF3, 0x26])                   # Transaction ID (4 bytes)
        secs = bytes([0x00, 0x00])                              # Seconds elapsed (2 bytes)
        flags = bytes([0x00, 0x00])                             # Flags (2 bytes)
        ciaddr = bytes([0, 0, 0, 0])                            # Client IP address (4 bytes)
        yiaddr = bytes([0, 0, 0, 0])                            # Your IP address (4 bytes)
        siaddr = bytes([0, 0, 0, 0])                            # Server IP address (4 bytes)
        giaddr = bytes([0, 0, 0, 0])                            # Gateway IP address (4 bytes)
        c_Hwaddr1 = bytes([0x00, 0x05, 0x3C, 0x04])             # Client hardware address (4 bytes)
        c_Hwaddr2 = bytes([0x8D, 0x59, 0x00, 0x00])             # Client hardware address (4 bytes)
        c_Hwaddr3 = bytes([0x00, 0x00, 0x00, 0x00])             # Client hardware address (4 bytes) - Unused
        c_Hwaddr4 = bytes([0x00, 0x00, 0x00, 0x00])             # Client hardware address (4 bytes) - Unused
        c_Hwaddr5 = bytes(192)                                  # Zero padding (192 bytes)
        magic_Cookie = bytes([0x63, 0x82, 0x53, 0x63])          # Magic cookie (4 bytes)
        DHCP_Options1 = bytes([53, 1, 3])                       # DHCP message type - Request (3 bytes)
        DHCP_Options2 = bytes([50, 4, 192, 168, 1, 100])        # Requested IP address (6 bytes)
        DHCP_Options3 = bytes([54, 4, 192, 168, 1, 1])          # Server IP address (6 bytes)
        END_packet = bytes([255])                               # End of packet (1 byte) - Always 0xFF

        pack = op_Code + hw_Type + hw_Len + hops + XID + secs + flags + ciaddr + yiaddr + siaddr + giaddr + c_Hwaddr1 + c_Hwaddr2 + c_Hwaddr3 + c_Hwaddr4 + c_Hwaddr5 + magic_Cookie + DHCP_Options1 + DHCP_Options2 + DHCP_Options3 + END_packet

        return pack


def dns_client():
    # create a socket for the dns client
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('localhost', 9999))

    domain_Name = input('[DNS] Enter domain name: ')

    # send the domain name entered by user to the dns server
    sock.send(domain_Name.encode('utf-8'))

    # receive the IP address response from the dns server
    ip_Address = sock.recv(max_Size).decode('utf-8')

    print('[DNS] IP Address:', ip_Address)
    sock.close()


def app_client_TCP():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    list_of_Queries = sock.recv(max_Size).decode("utf-8")
    print(list_of_Queries)
    while True:
        query = input("[SQL] Please enter the name of the query you wish to use or the word nothing to stop the loop: ")
        sock.send(bytes(query, "utf-8"))
        if query == "nothing":
            print("[SQL] Closing connection...")
            break
        result = sock.recv(max_Size).decode("utf-8")
        print(f"[SQL] Received result from server: {result}")
    sock.close()


if __name__ == '__main__':
    print("\n    Client Multipurpose Application;  Copyright (C) 2023  Roy Simanovich and Yuval Yurzdichinsky\n"
		 "This program comes with ABSOLUTELY NO WARRANTY.\n"
		 "This is free software, and you are welcome to redistribute it\n"
		 "under certain conditions; see `LICENSE' for details.\n")

    while True:
        print("\nWhat would you like to do?")
        print("1. Simulate DHCP (Discover, Offer, Request, Ack)")
        print("2. DNS Query (UDP & TCP)")
        print("3. Application Client (TCP)")
        print("4. Exit")

        choice = input("Enter your choice: ")

        match choice:
            case '1':
                # Starts the DHCP client
                dhcp_client = DHCP_client()
                dhcp_client.client()

            case '2':
                # Starts the DNS client
                dns_client()

            case '3':
                # Starts the app client
                app_client_TCP()

            case '4':
                print("Exiting...")
                break

            case _:
                print("Invalid choice. Please try again.")

