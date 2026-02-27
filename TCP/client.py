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
    try:
        # Send data to server
        msg = input('Write Message: ').strip()

        # Don't send empty payloads; they'd keep both sides waiting.
        if not msg:
            print("Please type a message (or 'Bye' to close).")
            continue

        client_socket.send(msg.encode())

        # Receive response from server
        response = client_socket.recv(1024)

        # server not responding
        if not response:
            print("Server disconnected")
            break

        print("Server:", response.decode())

        if msg == 'Bye':
            break
    
    except (ConnectionResetError, ConnectionAbortedError):
        print("Server disconnected")
        break
    except KeyboardInterrupt:
        print("You are disconnected")
        break

# close the connection
client_socket.close()
