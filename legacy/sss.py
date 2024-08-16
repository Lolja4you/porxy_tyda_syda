from scapy.all import *

ip = IP(dst='192.168.1.89')
SYN = TCP(sport=8081, dport=8080, flags='S', seq=10)
SYNACK = sr1(ip/SYN)
my_ack = SYNACK.seq + 1
ACK = TCP(sport=8081, dport=8080, flags='A', seq=11, ack=my_ack)
send(ip/ACK)
payload = 'SEND TCP'
PUSH = TCP(sport=8081, dport=8080, flags='PA', seq=11, ack=my_ack)
send(ip/PUSH/payload)