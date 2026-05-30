from scapy.all import rdpcap, ICMP, IP
import base64

packets = rdpcap('GLaDOS_Network.pcapng')
ips = []
for pkt in packets:
    if pkt.haslayer(ICMP) and pkt[ICMP].type == 8: # echo-request
        ips.append(pkt[IP].src)

b64_str = ""
for ip in ips:
    parts = ip.split('.')
    for p in parts:
        b64_str += chr(int(p))

print(f"Base64: {b64_str}")
try:
    print(f"Decoded: {base64.b64decode(b64_str).decode('utf-8')}")
except Exception as e:
    print(f"Decode error: {e}")
