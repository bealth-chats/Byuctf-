from scapy.all import rdpcap

packets = rdpcap('GLaDOS_Network.pcapng')
print(f"Total packets: {len(packets)}")
for i, pkt in enumerate(packets[:50]):
    print(pkt.summary())
