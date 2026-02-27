import asyncio

RESPONSES = {
    "How are you?": "I am good",
    "How is your day?": "Very good"
}
CLIENT_IDLE_TIMEOUT_SECONDS = 30

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    port = addr[1]
    
    print('Connection established with Client on Address: ', addr)
    
    # fixed message
    writer.write(b"""
        I am a simple server please choose your message:
            1- How are you?
            2- How is your day?
            3- Bye (to close the connection)
    """)
    await writer.drain()

    # each client connection loop  
    while True:
        try:
            # Receive client msg
            msg = await asyncio.wait_for(
                reader.read(1024),
                timeout=CLIENT_IDLE_TIMEOUT_SECONDS
            )

            # no message from client (not active)
            if not msg:
                break
            
            msg = msg.decode().strip()
            print("Client (%s):"%port, msg)

            if msg == 'Bye':
                writer.write(b"See you next time")
                await writer.drain()
                break

            # Send Response
            writer.write(RESPONSES.get(msg, "I don't understand you").encode())
            await writer.drain()

        except asyncio.TimeoutError:
            writer.write(b"You are dissconected")
            writer.drain()
            print(f"Client ({port}) timed out after {CLIENT_IDLE_TIMEOUT_SECONDS}s of inactivity")
            break
        except (ConnectionResetError, ConnectionAbortedError):
            print('Client (%s) disconnected' %port)
            break

    writer.close()
    await writer.wait_closed()
    print('Connection closed with Client on Address:', addr)

async def start_server():
    # Create socket
    # Bind the socket to the address
    server = await asyncio.start_server(handle_client, "127.0.0.1", 8080)

    print("Server is Running on port 8080")

    async with server:
        await server.serve_forever()
            

if __name__ == '__main__':
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print("Server Closed")
