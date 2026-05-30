from scapy.all import rdpcap, ICMP

pcap = rdpcap('GLaDOS_Network.pcapng')

for pkt in pcap:
    if ICMP in pkt:
        # Let's print the payload
        try:
            payload = bytes(pkt[ICMP].payload)
            if payload:
                print(payload)
        except Exception as e:
            pass
