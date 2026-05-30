from scapy.all import rdpcap, ICMP

pcap = rdpcap('GLaDOS_Network.pcapng')

for pkt in pcap:
    if ICMP in pkt:
        # Print only ICMP requests
        if pkt[ICMP].type == 8:
            payload = bytes(pkt[ICMP].payload)
            if payload:
                print(payload)
