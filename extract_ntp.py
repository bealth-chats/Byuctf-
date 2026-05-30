from scapy.all import rdpcap, UDP

packets = rdpcap('GLaDOS_Network.pcapng')
for i, pkt in enumerate(packets):
    if pkt.haslayer(UDP):
        # Dump the UDP payload directly
        print(f"UDP payload length: {len(pkt[UDP].payload)}")
        payload = bytes(pkt[UDP].payload)
        print(payload.hex())
