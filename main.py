import sys
import asyncio
import signal
# import socket

from utils.logger import logger


def signal_handler(sig, frame):
    # перехватывает ctrl+c
    logger.info('Proxy is Stopped.')
    sys.exit(0)

def write_log_file(*content, prt=False):
    if prt:
        if len(content[0]) < 100:
            logger.info(*content)
        else:
            logger.info("This message is too long not print in cmd but will store at log.txt.")
    if type(content[0]) == bytes:
        content = b" ".join(content)
    else:
        content = bytes(" ".join(content), encoding="utf-8")
    with open("log.txt", "ab") as f:
        f.write(content + b"\n")

class Proxy:
    def __init__(self):
        self.ip = "0.0.0.0"
        self.port = 8080
        logger.info(f"Proxy Server Is Start on {self.ip}:{self.port}, See log.txt get log.")
        logger.info("Press Ctrl+C to Stop.")
        signal.signal(signal.SIGINT, signal_handler)

    async def handle_client(self, reader, writer):
        """_summary_
        Args:
            reader (_type_): Это объект, который предоставляет методы для асинхронного чтения данных из сокета. 
                позволяет асинхронно читать данные, полученные от клиента или сервера.
            writer (_type_): Это объект, который предоставляет методы для асинхронной записи данных в сокет. 
                позволяет асинхронно отправлять данные клиенту или серверу.
        """
        client_addr = writer.get_extra_info('peername') # get_extra_info получи информацию; 'peername' о том к кому подключен
        logger.info(f"Connected by {client_addr}")      ## выводит к кому подключен    
                
        # код ищет dst находит положение :// а потом вычленяет url dst\src
        request = await reader.read(4096)
        request = request.decode(encoding="utf-8")
        first_line = request.split("\r\n")[0]
        url = first_line.split(" ")[1]
        http_pos = url.find("://")        
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos + 3):]


        webserver = ""
        port = -1
        port_pos = temp.find(":")
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)
        if port_pos == -1 or webserver_pos < port_pos:
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int(temp[(port_pos + 1):])
            webserver = temp[:port_pos]
        logger.info("Browser Request:")
        # write_log_file(request)
        
        try:
            server_reader, server_writer = await asyncio.open_connection(webserver, port)
        except Exception as e:
            logger.error("Failed to connect to %s:%s: %s", webserver, port, e)
            writer.close()
            return
        
        if port == 443:
            writer.write(b"HTTP/1.1 200 Connection established\r\n\r\n")
            await writer.drain()
            await asyncio.gather(
                self.forward_data(reader, server_writer),
                self.forward_data(server_reader, writer)
            )
        else:
            server_writer.write(request.encode())
            await server_writer.drain()
            logger.info("Website Host Result:")
            while True:
                data = await server_reader.read(4096)
                if not data:
                    break
                writer.write(data)
                await writer.drain()
                # write_log_file(data)
                
        server_writer.close()
        await server_writer.wait_closed()
        
        writer.close()
        await writer.wait_closed()

    async def forward_data(self, reader, writer):
        while True:
            data = await reader.read(4096)
            if not data:
                break
            
            writer.write(data)
            await writer.drain()

    async def start(self):
        server = await asyncio.start_server(self.handle_client, self.ip, self.port)
        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    proxy = Proxy()
    asyncio.run(proxy.start())