from scapy.all import rdpcap, TCP, UDP

pcap = rdpcap('GLaDOS_Network.pcapng')

tcp_payloads = []
udp_payloads = []

for pkt in pcap:
    if TCP in pkt:
        payload = bytes(pkt[TCP].payload)
        if payload and payload not in tcp_payloads:
            tcp_payloads.append(payload)
    if UDP in pkt:
        payload = bytes(pkt[UDP].payload)
        if payload and payload not in udp_payloads:
            udp_payloads.append(payload)

for p in tcp_payloads:
    if b'byuctf' in p:
        print("TCP:", p)

for p in udp_payloads:
    if b'byuctf' in p:
        print("UDP:", p)
