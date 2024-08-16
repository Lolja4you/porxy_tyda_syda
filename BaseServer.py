import socket
from utils.logger import logger

class Server:
    def __init__(self, HOST='0.0.0.0', PORT='8080'):
        self.HOST = HOST
        self.PORT = PORT
        self.is_running_sock = False
        self._socket = socket.socket()
    
    def start_backend(self):
        try:
            self._socket.bind((self.HOST, self.PORT))
            self._socket.listen(1)
            logger.info(f"Server open on {self.HOST}:{self.PORT}")
        except socket.error as e:
            logger.error(f"{e}")
            
    def start_client(self):
        try:
            logger.info(f"Server is listen {self.HOST}:{self.PORT}")
            self._socket.connect((self.HOST, self.PORT))
        except socket.error as e:
            logger.error(f"{e}")

    def send(self, message): 
        logger.info(message.encode())
        byte_code_msg =  message.encode()
        self._socket.send(byte_code_msg)

    def listen(self):        
        conn, addr = self._socket.accept()
        logger.info(f"Connection from {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            logger.info(f"{addr} {data.decode('UTF-8')}")
            # self.send(conn, data.decode('UTF-8'))
        conn.close()

    def stop(self):
        self._socket.close()

def up_server(arg):
    split_arg = arg.split()
    if split_arg[0] == 'client':
        split_addres = split_arg[1].split(":")
        HOST, PORT = split_addres[0], split_addres[1]
        client = Server(HOST, int(PORT))
        client.start_client()
        while True:
            client.send(str(input('> ')))
            
    elif split_arg[0] == 'back':
        split_addres = split_arg[1].split(":")
        HOST, PORT = split_addres[0], split_addres[1]
        backend = Server(HOST, int(PORT))
        backend.start_backend()
        while True:
            backend.listen()
    else:
        logger.error(f"Not avalibal configurations server {split_arg}")


if __name__ == '__main__':
    try:
        up_server(str(input("config > ")))
    except KeyboardInterrupt:
        exit






'''
async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    logger.info(f"Client connected: {addr}")

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break
            message = data.decode()
            logger.info(f"Received message from {addr}: {message}")

            # Echo back the received data
            writer.write(data)
            await writer.drain()
    except Exception as e:
        logger.error(f"Error handling client {addr}: {e}")
    finally:
        logger.info(f"Client disconnected: {addr}")
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 8080)
    addr = server.sockets[0].getsockname()
    logger.info(f"Serving on {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":

    
    asyncio.run(main())
'''