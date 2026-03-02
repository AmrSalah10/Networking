import asyncio
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
_logger = logging.getLogger(__name__)

RESPONSES = {
    "How are you?": "I am good",
    "How is your day?": "Very good"
}
CLIENT_IDLE_TIMEOUT_SECONDS = 30

active_clients = {}

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    port = addr[1]
    active_clients[addr] = writer
    
    _logger.info(f"Connection established with Client on Address: {addr} | Total active: {len(active_clients)}")
    
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
            _logger.info(f"Client ({port}): {msg}")

            if msg == 'Bye':
                writer.write(b"See you next time")
                await writer.drain()
                break

            # Send Response
            writer.write(RESPONSES.get(msg, "I don't understand you").encode())
            await writer.drain()

        except asyncio.TimeoutError:
            writer.write(b"You are dissconected")
            await writer.drain()
            _logger.info(f"Client ({port}) timed out after {CLIENT_IDLE_TIMEOUT_SECONDS}s of inactivity")
            break
        except (ConnectionResetError, ConnectionAbortedError):
            _logger.info(f"Client ({port})) disconnected")
            break

    # remove active client
    active_clients.pop(addr)

    writer.close()
    await writer.wait_closed()

    _logger.info(f"Connection closed with Client on Address: {addr} | Total active: {len(active_clients)}")

async def start_server():
    # Create socket
    # Bind the socket to the address
    server = await asyncio.start_server(handle_client, "127.0.0.1", 8080)

    _logger.info("Server is Running on port 8080")

    async with server:
        await server.serve_forever()
            

if __name__ == '__main__':
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        _logger.info("Server Closed")
