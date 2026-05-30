from scapy.all import rdpcap, UDP, Raw

packets = rdpcap('GLaDOS_Network.pcapng')
for i, pkt in enumerate(packets):
    if pkt.haslayer(UDP):
        print(f"Packet {i} (UDP): dport={pkt[UDP].dport}, sport={pkt[UDP].sport}")
        if pkt.haslayer(Raw):
            print(f"Raw data: {pkt[Raw].load}")
