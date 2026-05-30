from scapy.all import rdpcap, TCP, Raw

packets = rdpcap('GLaDOS_Network.pcapng')
for pkt in packets:
    if pkt.haslayer(TCP) and pkt.haslayer(Raw):
        print(f"TCP Payload ({pkt.summary()}):")
        try:
            print(pkt[Raw].load.decode('utf-8'))
        except:
            print(pkt[Raw].load)
        print("-" * 50)
