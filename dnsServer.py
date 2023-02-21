import socket

# create a socket for the dns server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', 9999))

while True:
    # receive domain name from the client
    domain_name, client_address = sock.recvfrom(1024)
    domain_name = domain_name.decode('utf-8')

    # resolve domain name to its IP address using Google Public DNS server
    try:
        address_info = socket.getaddrinfo(domain_name, 80, socket.AF_INET, socket.SOCK_STREAM)
        ip_address = address_info[0][4][0]
        sock.sendto(ip_address.encode('utf-8'), client_address)
    except socket.gaierror:
        sock.sendto("Could not find IP address for this domain".encode('utf-8'), client_address)

sock.close()