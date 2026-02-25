import socket

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client_socket.connect(("127.0.0.1", 8080))

# Send data to server
client_socket.send(b"Hello From Client")

# Receive response from server
response = client_socket.recv(1024)
print("Server:", response.decode())

client_socket.close()