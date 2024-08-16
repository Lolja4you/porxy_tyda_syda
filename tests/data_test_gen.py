import asyncio
from scapy.all import IP, TCP, send
from utils.logger import logger
from route_table import RouteTable
import random

class PacketGenerator:
    def __init__(self, route_table = RouteTable()):
        self.route_table = route_table
        self.ip_pool = ['192.168.1.{}'.format(i) for i in range(1, 255)]

    async def generate_packets(self):
        while True:
            # Генерация случайных данных для имитации пакетов
            src = random.choice(self.ip_pool)
            dst = random.choice(self.ip_pool)
            while src == dst:
                dst = random.choice(self.ip_pool)

            packet = IP(src=src, dst=dst) / TCP(dport=80, flags='A')

            self.route_table.cycle_route(src=packet[IP].src, dst=packet[IP].dst)
            
            await asyncio.sleep(1)  # Задержка для имитации реального перехвата пакетов

    # async def process_packet(self, packet):
    #     if IP in packet and TCP in packet:
    #         if packet[IP].src == '192.168.1.95' and packet[IP].dst == 'rutube.moms':
    #             packet[IP].ttl = 50
    #             packet[TCP].flags = 'A'
    #             send(packet, verbose=0)

    #         elif packet[IP].src == 'rutube.moms' and packet[IP].dst == '192.168.1.95':
    #             packet[IP].ttl = 50
    #             packet[TCP].flags = 'A'
    #             send(packet, verbose=0)
    #             self.route_table.add_route(src=packet[IP].src, dst=packet[IP].dst)

