# CTF Write-up: GLaDOS Network - Alright. Paradox time

## Challenge Description
> To maintain a constant testing cycle, I simulate daylight at all hours and add adrenal vapor to your oxygen supply. So you may be confused about the passage of time. The point is, yesterday was your birthday. I thought you'd want to know.
> *The pcap file contains a flag for each of the following challenges: "There will be cake", "Are you still there?", "Alright. Paradox time", and "Corrupted Cores".
> If the flag you found doesn't work, then it most likely belongs to one of the other 3 challenges.
> Hint: What protocol is associated with time?

## Analysis and Solution

### Step 1: Understand the Hint
The description provides a major hint by focusing on the "passage of time" and explicitly asking: "What protocol is associated with time?". In computer networks, the protocol used for clock synchronization is **NTP** (Network Time Protocol), which operates over UDP port 123.

### Step 2: Analyze the PCAP File
We are given a network capture file named `GLaDOS_Network.pcapng`. Our first goal is to isolate the NTP traffic, as suggested by the hint. We can use a Python library called `scapy` to easily filter and inspect the packets.

### Step 3: Inspect the NTP Packets
By filtering out only the NTP packets from the capture, we find a sequence of 10 packets. When we look closely at the raw data (payload) inside these packets, we can spot a pattern.

The payload for the first packet looks like this:
```
b'#\x02\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\x00\x00\x01eS\xf1b\x00\x00\x00\x00eS\xf1y\x00\x00\x00\x00eS\xf1u\x00\x00\x00\x00eS\xf1c\x00\x00\x00\x00'
```

Notice the letters `b`, `y`, `u`, `c` scattered within the data. These are the starting letters of the flag format `byuctf{...}`.

### Step 4: Extract the Flag
The letters are embedded inside the NTP timestamp fields. By carefully observing the positions of the letters, we can see they are located at specific offsets within the payload (specifically at index 19, 27, 35, and 43).

We can write a simple Python script to automatically read all the NTP packets and extract the character at each of these positions:

```python
from scapy.all import rdpcap, UDP

# Read the capture file
packets = rdpcap('GLaDOS_Network.pcapng')

# Filter for NTP packets (UDP port 123)
ntp_packets = [p for p in packets if UDP in p and (p[UDP].sport == 123 or p[UDP].dport == 123)]

# Extract the hidden characters
flag = ""
for p in ntp_packets:
    payload = bytes(p[UDP].payload)
    if len(payload) >= 44:
        c1, c2, c3, c4 = payload[19], payload[27], payload[35], payload[43]
        if c1 != 0: flag += chr(c1)
        if c2 != 0: flag += chr(c2)
        if c3 != 0: flag += chr(c3)
        if c4 != 0: flag += chr(c4)

print("Flag:", flag)
```

Running this script reveals the hidden flag pieced together from the NTP packets!

### Flag
`byuctf{S0_My_P4r4d0x_!d34_D!dnt_W0rk}`