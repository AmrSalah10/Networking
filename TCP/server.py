import socket
from concurrent.futures import ThreadPoolExecutor

RESPONSES = {
    "How are you?": "I am good",
    "How is your day?": "Very good"
}

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address
server_socket.bind(("127.0.0.1", 8080))
print("Server is Running on port 8080")

server_socket.listen(5)

def handle_client(client_socket, addr):
    port = addr[1]

    # each client connection loop  
    while True:
        # Receive client msg
        msg = client_socket.recv(1024).decode()
        print("Client (%s):"%port, msg)

        # Close connection
        if msg == 'Bye':
            client_socket.send(b"See you next time")
            client_socket.close()
            break

        # Send Response
        client_socket.send(RESPONSES.get(msg, "I don't understand you").encode())

    print('Connection closed with Client on Address: ', addr)

def start_server():
    with ThreadPoolExecutor(5) as exec:
        while True:
            # Accept client connection
            client_socket, addr = server_socket.accept()
            
            print('Connection established with Client on Address: ', addr)
            
            # fixed message
            client_socket.send(b"""
                I am a simple server please choose your message:
                    1- How are you?
                    2- How is your day?
                    3- Bye (to close the connection)
            """)

            exec.submit(handle_client, client_socket, addr)
            

if __name__ == '__main__':
    start_server()