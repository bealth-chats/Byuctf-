# CTF Write-up: Corrupted Cores

This is a step-by-step guide on how to solve the "Corrupted Cores" network forensics challenge.

## 1. Understanding the Goal

We are given a file named `GLaDOS_Network.pcapng`. Think of this file as a recording of a digital conversation (network traffic) between different computers. Our goal is to find a secret piece of text known as a "flag" hidden somewhere within this recording.

The flag will look like this: `byuctf{some_secret_text}`.

We also have a description and some hints:
> "The scientists were always hanging cores on me to regulate my behavior. I've heard voices all my life. But now I hear the voice of a conscience, and it's terrifying, because for the first time it's my voice."
> **Hint 1:** the voices may not belong to a single identity
> **Hint 2:** the arp packets are not part of this challenge.

## 2. Exploring the Network Recording

When we open the recording (using tools like Wireshark or scripts), we see different types of network messages being sent back and forth. This recording actually contains *four* different flags, each belonging to a different challenge. We need to find all of them and figure out which one belongs to "Corrupted Cores."

Here is what we discovered by looking closely at the different types of messages:

*   **Web Traffic (HTTP):** One computer was sending website requests. Hidden inside a "cookie" (a small piece of data websites use to remember you) was a secret code. When decoded, it revealed the flag: `byuctf{Th3_C4k3_!s_4_L!3_HTC56zeE}`. This clearly belongs to a different challenge called "There will be cake".
*   **Time Requests (NTP):** Computers often ask each other for the current time. Inside these specific time requests, extra secret letters were hidden. Putting them together spelled out: `byuctf{S0_My_P4r4d0x_!d34_D!dnt_W0rk}`. This matches the challenge "Alright. Paradox time".
*   **Ping Messages (ICMP Payloads):** Computers "ping" each other to check if they are online. Inside the extra data area of these pings, we found pieces of text. When combined, they formed: `byuctf{Turr3t_R3d3mpt!0n_L!n3s_4r3_N0t_R!d3s}`. This matches the challenge "Are you still there?".

## 3. Finding the Final Flag

We are left with one final place to look, which must hold the flag for "Corrupted Cores". Let's look at the remaining "Ping" (ICMP) messages, but this time, let's look at *who* is sending them.

Normally, a ping comes from one computer with one specific address (an IP address, like a digital phone number). However, in this recording, a series of pings are coming from **many different, fake IP addresses**.

For example, the pings came from:
*   `89.110.108.49`
*   `89.51.82.109`
*   `101.49.82.111`
*   ...and so on.

Let's look at Hint 1 again: *"the voices may not belong to a single identity"*.
In networking, an "identity" is an IP address! The fact that the secret is split across many different IP addresses perfectly matches this hint.

## 4. Decoding the Secret

To get the flag, we take those fake IP addresses and look at the numbers they are made of. In computers, numbers can represent letters (for example, the number 89 represents the letter 'Y', 110 is 'n', 108 is 'l', and 49 is '1').

If we convert all the numbers from those fake IP addresses into characters, we get a jumbled string of text:
`Ynl1Y3Rme1RoM19QNHJ0X1doM3IzX0gzX0shbGxzX1kwdX0A`

This text is encoded using a common method called Base64 (which is like a secret decoder ring). When we decode this Base64 text, it finally reveals our hidden flag:

**`byuctf{Th3_P4rt_Wh3r3_H3_K!lls_Y0u}`**

*Fun fact: This flag text "The part where he kills you" is a reference to a chapter in the game Portal 2 featuring Wheatley, who is a "Corrupted Core"!*