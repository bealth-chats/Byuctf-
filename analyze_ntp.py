from scapy.all import rdpcap, UDP, NTP

packets = rdpcap('GLaDOS_Network.pcapng')
for i, pkt in enumerate(packets):
    if pkt.haslayer(UDP) and pkt[UDP].dport == 123: # NTP port
        print(f"Packet {i}: {pkt.summary()}")
        if pkt.haslayer(NTP):
            print(f"NTP details:")
            print(pkt[NTP].show())
