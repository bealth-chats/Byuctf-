from scapy.all import rdpcap, ICMP, Ether, IP, UDP, Raw
import base64

packets = rdpcap('GLaDOS_Network.pcapng')

# Find MAC addresses and try to build a flag
macs = []
for pkt in packets:
    if pkt.haslayer(Ether):
        mac = pkt[Ether].src
        if mac not in macs:
            macs.append(mac)
        mac = pkt[Ether].dst
        if mac not in macs:
            macs.append(mac)

print(f"Unique MACs: {macs}")

# Check ICMP echo requests IPs
ips = []
for pkt in packets:
    if pkt.haslayer(ICMP) and pkt[ICMP].type == 8: # echo-request
        ips.append(pkt[IP].src)
b64_str = ""
for ip in ips:
    parts = ip.split('.')
    for p in parts:
        b64_str += chr(int(p))
print(f"ICMP IPs as characters: {b64_str}")
try:
    print(f"Decoded: {base64.b64decode(b64_str).decode('utf-8')}")
except Exception as e:
    pass

# Check ICMP echo requests payload
for pkt in packets:
    if pkt.haslayer(ICMP) and pkt.haslayer(Raw):
        print(f"ICMP payload: {pkt[Raw].load}")
