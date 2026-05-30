from scapy.all import rdpcap, UDP

# Read the pcap file
packets = rdpcap('GLaDOS_Network.pcapng')

# Filter for NTP packets (UDP port 123)
ntp_packets = [p for p in packets if UDP in p and (p[UDP].sport == 123 or p[UDP].dport == 123)]

print(f"Found {len(ntp_packets)} NTP packets.")

for i, p in enumerate(ntp_packets):
    print(f"Packet {i}: {bytes(p[UDP].payload)}")
