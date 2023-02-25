import socket
import time

# Define ip, ports, max packet size and congestion control variables
server_port = 1234
ip = "127.0.0.1"
client_port = 5000
max_Size = 1024
timeout = 2
max_Retries = 4

# Create a UDP socket to connect to the server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, client_port))

# "Handshake" with the server
message = "Handshake"
sock.sendto(message.encode('utf-8'), (ip, server_port))

# Receive list of queries from the server
while True:
    try:
        data, server_address = sock.recvfrom(max_Size)
        print(f"Received from server {server_address}: {data.decode('utf-8')}")
        sock.sendto("ACK".encode("utf-8"), (ip, server_port))
        break
    except socket.timeout:
        print("Timeout while waiting for queries")

# Send queries to the server
query_num = 1  # Query serial number
while True:
    sock.settimeout(timeout)
    query_name = input("Choose query to use, or type nothing to stop: ")
    query_name = query_name + "|" + str(query_num)
    retries = 0
    while retries < max_Retries:
        start_time = time.time()  # Measure the start time of transmission
        sock.sendto("ACK".encode("utf-8"), (ip, server_port))
        sock.sendto(query_name.encode('utf-8'), (ip, server_port))

        try:
            data, address = sock.recvfrom(max_Size)
            data = data.decode('utf-8')
            if data == "ACK":
                break
            if data == "Timed out":
                break
        except socket.timeout:
            pass  # Retry if timeout occurs

        end_time = time.time()  # Measure the end time of transmission
        rtt = end_time - start_time  # Calculate the RTT
        if rtt < 0.5 * timeout:
            timeout *= 0.9  # Increase the transmission rate
        else:
            timeout *= 1.2  # Decrease the transmission rate

        retries += 1
    query_num += 1
    if "nothing" in query_name:
        print("Closing connection...")
        break
    if retries == max_Retries:
        print("Maximum number of retries reached, closing connection...")
        break
    elif data == "Timed out":
        print("Server timed out, closing connection...")
        break
    else:
        print(f"Received from server {server_address}: {data}")

sock.close()
