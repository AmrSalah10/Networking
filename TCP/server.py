import socket

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address
server_socket.bind(("127.0.0.1", 8080))
print("Server is Running on port 8080")

server_socket.listen(5)

# Accept client connection
client_socket, addr = server_socket.accept()

# Receive client msg
msg = client_socket.recv(1024)
print("Client", msg.decode())

# Send Response
client_socket.send(b"Hello From Server")

# Close connection
client_socket.close()