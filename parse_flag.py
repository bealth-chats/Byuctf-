from scapy.all import rdpcap, UDP

# Read the pcap file
packets = rdpcap('GLaDOS_Network.pcapng')

# Filter for NTP packets (UDP port 123)
ntp_packets = [p for p in packets if UDP in p and (p[UDP].sport == 123 or p[UDP].dport == 123)]

flag = ""
for p in ntp_packets:
    payload = bytes(p[UDP].payload)
    # The bytes seem to be in positions 19, 27, 35, 43
    # Look at the previous output:
    # b'#\x02\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\x00\x00\x01eS\xf1b\x00\x00\x00\x00eS\xf1y\x00\x00\x00\x00eS\xf1u\x00\x00\x00\x00eS\xf1c\x00\x00\x00\x00'
    # b is at 19
    # y is at 27
    # u is at 35
    # c is at 43
    if len(payload) >= 44:
        c1 = payload[19]
        c2 = payload[27]
        c3 = payload[35]
        c4 = payload[43]
        if c1 != 0: flag += chr(c1)
        if c2 != 0: flag += chr(c2)
        if c3 != 0: flag += chr(c3)
        if c4 != 0: flag += chr(c4)

print("Flag:", flag)
