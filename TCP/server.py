import socket
from concurrent.futures import ThreadPoolExecutor

RESPONSES = {
    "How are you?": "I am good",
    "How is your day?": "Very good"
}
CLIENT_IDLE_TIMEOUT_SECONDS = 30

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address
server_socket.bind(("127.0.0.1", 8080))
print("Server is Running on port 8080")

server_socket.listen(5)

def handle_client(client_socket, addr):
    port = addr[1]
    client_socket.settimeout(CLIENT_IDLE_TIMEOUT_SECONDS)

    # each client connection loop  
    while True:
        try:
            # Receive client msg
            msg = client_socket.recv(1024)

            # no message from client (not active)
            if not msg:
                break
            
            msg = msg.decode().strip()
            print("Client (%s):"%port, msg)

            if msg == 'Bye':
                client_socket.send(b"See you next time")
                break

            # Send Response
            client_socket.send(RESPONSES.get(msg, "I don't understand you").encode())

        except socket.timeout:
            print(f"Client ({port}) timed out after {CLIENT_IDLE_TIMEOUT_SECONDS}s of inactivity")
            break
        except ConnectionResetError:
            print('Client (%s) disconnected' %port)
            break

    client_socket.close()    
    print('Connection closed with Client on Address:', addr)

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

