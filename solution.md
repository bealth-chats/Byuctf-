# CTF Write-up: Corrupted Cores

## Challenge Description
"The scientists were always hanging cores on me to regulate my behavior. I've heard voices all my life. But now I hear the voice of a conscience, and it's terrifying, because for the first time it's my voice."

Hints provided:
1. The voices may not belong to a single identity.
2. The arp packets are not part of this challenge.

## Analysis
The pcap file `GLaDOS_Network.pcapng` contains network traffic with four different flags corresponding to four different Portal-themed challenges.

By analyzing the network traffic, we discovered four distinct flags:
1. **TCP HTTP Traffic**: `byuctf{Th3_C4k3_!s_4_L!3_HTC56zeE}` found in a base64 encoded HTTP Cookie (`cake`). This corresponds to the "There will be cake" challenge.
2. **ICMP Data Payloads**: `byuctf{Turr3t_R3d3mpt!0n_L!n3s_4r3_N0t_R!d3s}` found by concatenating the raw data payloads of ICMP echo-request packets. This corresponds to the "Are you still there?" challenge.
3. **NTP (UDP) Payloads**: `byuctf{S0_My_P4r4d0x_!d34_D!dnt_W0rk}` found by extracting and decoding the specific hidden bytes within the NTP payloads. This corresponds to the "Alright. Paradox time" challenge.
4. **ICMP Source IPs**: `byuctf{Th3_P4rt_Wh3r3_H3_K!lls_Y0u}` found by interpreting the octets of multiple ICMP source IP addresses as ASCII characters to form a base64 string, which is then decoded.

## The Solution
The description hints at "Corrupted Cores", and specifically mentions that "the voices may not belong to a single identity."

In networking, an "identity" often refers to an IP address or MAC address. In the case of the fourth flag, it is constructed by taking the Source IP addresses of multiple ICMP echo-request packets and mapping their octets directly to ASCII characters to form a base64 string, which is then decoded to yield the flag. Because the flag is spread across multiple different source IP addresses (identities), this perfectly matches the challenge hint.

Furthermore, the decoded string refers to "The part where he kills you", a famous chapter/achievement in Portal 2 involving Wheatley, a corrupted core.

**Flag:** `byuctf{Th3_P4rt_Wh3r3_H3_K!lls_Y0u}`