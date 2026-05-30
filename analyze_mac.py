from scapy.all import rdpcap, ICMP, Ether

packets = rdpcap('GLaDOS_Network.pcapng')
for pkt in packets:
    if pkt.haslayer(ICMP) and pkt[ICMP].type == 8: # echo-request
        print(f"Source MAC: {pkt[Ether].src}, Source IP: {pkt['IP'].src}")
