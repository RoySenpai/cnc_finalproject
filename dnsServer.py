import socket

max_Size = 1024  # Message max size
ip = "127.0.0.1"
print("Starting dns server...")

# create a socket for the dns server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, 9999))

while True:
    # Receive domain name from the client
    domain_name, client_address = sock.recvfrom(max_Size)
    domain_name = domain_name.decode('utf-8')

    # resolve domain name to its IP address using google's public DNS server
    try:
        address_info = socket.getaddrinfo(domain_name, 80, socket.AF_INET, socket.SOCK_STREAM)
        ip_address = address_info[0][4][0]
        sock.sendto(ip_address.encode('utf-8'), client_address)
        print("sent IP to client successfully!")
    except socket.gaierror:
        sock.sendto("Could not find IP address for this domain".encode('utf-8'), client_address)
