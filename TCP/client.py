import socket

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client_socket.connect(("127.0.0.1", 8080))

# Receive any fixed msg from the server
response = client_socket.recv(1024)

if response:
    print("Server:", response.decode())

while True:
    # Send data to server
    msg = input('Write Message: ')
    client_socket.send(msg.encode())

    # Receive response from server
    response = client_socket.recv(1024)
    print("Server:", response.decode())

    if msg == 'Bye':
        break

client_socket.close()