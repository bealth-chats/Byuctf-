from scapy.all import rdpcap, ICMP, Raw

packets = rdpcap('GLaDOS_Network.pcapng')
flag = ""
for pkt in packets:
    if pkt.haslayer(ICMP) and pkt[ICMP].type == 8 and pkt.haslayer(Raw): # echo-request
        flag += pkt[Raw].load.decode('utf-8')

print(f"Flag from ICMP payload: {flag}")
