import socket

# Define ip, port and max packet size
server_port = 1234
ip = "127.0.0.1"
client_Port = 5000
max_Size = 1024

# Create UDP socket to connect to server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, client_Port))

# "Handshake" with the server
message = "Hand shake"
sock.sendto(message.encode('utf-8'), (ip, server_port))

# Receive list of queries from the server
while True:
    try:
        data, server_address = sock.recvfrom(max_Size)
        print(f"Received from server {server_address}: {data.decode('utf-8')}")
        break
    except socket.timeout:
        print("Timeout while waiting for queries")

# Send queries to the server
while True:
    query_name = input("Choose query to use, or type nothing to stop: ")
    sock.sendto("ACK".encode("utf-8"), (ip, server_port))
    sock.sendto(query_name.encode('utf-8'), (ip, server_port))

    if query_name == "nothing":
        break
    data, address = sock.recvfrom(max_Size)
    data = data.decode('utf-8')
    
    if data == "Timed out":
        print("Server timed out, closing connection...")
        break
        
    if data != "ACK":  # if server didn't return ACK for the first time, try to send again
        sock.sendto("ACK".encode("utf-8"), (ip, server_port))
        sock.sendto(query_name.encode('utf-8'), (ip, server_port))
        data, address = sock.recvfrom(max_Size)
        data = data.decode('utf-8')
        if data != "ACK":  # if server didn't return ACK for the second time, close the connection.
            print("Didn't receive Ack from server for the second time, closing connection...")
            break
# Close socket
sock.close()
