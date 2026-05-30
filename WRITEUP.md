# Are You Still There? Write-up

## The Challenge

We were provided with a network capture file (`GLaDOS_Network.pcapng`) and a description that included lyrics from the ending song of the video game Portal, "Still Alive".

The description also gave us a few important hints:
1. The PCAP file contains flags for 4 different challenges ("There will be cake", "Are you still there?", "Alright. Paradox time", and "Corrupted Cores").
2. The crucial hint: "how would you remotely check if a server is online?"

## The Solution

1. **Understanding the Hint**
   The hint is the key to solving this challenge. When you want to check if a computer or server is online and connected to the network, the most common tool used is the `ping` command.

   The `ping` command works by sending special network messages called **ICMP** (Internet Control Message Protocol) packets to the server. The server, if online, receives the message and sends an ICMP reply back.

2. **Analyzing the Network File**
   Knowing that we need to look for `ping` messages (ICMP packets), we can analyze the provided `GLaDOS_Network.pcapng` file. A PCAP file is just a recording of network traffic.

   We can use a network analysis tool or script to filter the traffic and only look at the ICMP packets.

3. **Extracting the Flag**
   If we look closely at the data (the "payload") carried inside these ICMP request packets, we notice that each packet carries a small piece of text.

   By extracting the text from each ICMP packet in order and combining them together, we get the hidden message:

   `byuctf{Turr3t_R3d3mpt!0n_L!n3s_4r3_N0t_R!d3s}`

   This matches the required flag format, giving us the solution to the challenge!