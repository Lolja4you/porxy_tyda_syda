#!/usr/bin/python3
import logging
import asyncio
import colorlog
#from scapy.all import IP, TCP, send

logger = logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

# Создание форматтера с цветами для уровня логирования
formatter = colorlog.ColoredFormatter(
    '[%(asctime)s] %(log_color)s%(levelname)s: %(message)s',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    },
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Создание обработчика для консоли
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
logger.addHandler(console)


async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    logger.info(f"Client connected: {addr}")

    while True:
        data = await reader.read(1024)
        if not data:
            break
        message = data.decode()
        logger.info(f"Received message from {addr}: {message}")

        # Echo back the received data
        writer.write(data)
        await writer.drain()

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