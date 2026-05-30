# There will be cake - CTF Writeup

## Challenge Description
The Enrichment Center is required to remind you that all test subject activity will be logged, analyzed, and stored for scientific purposes.
"Cake and grief counseling will be available at the conclusion of the test."

**Hint:** what is a baked treat similar to a cake that you can find on almost any website?

## Solution

This challenge gives us a hint about a "baked treat similar to a cake that you can find on almost any website". This is a clever reference to web **cookies**! On the internet, a cookie is a small piece of data sent from a website and stored on the user's computer by the user's web browser while the user is browsing.

We are also provided with a file named `GLaDOS_Network.pcapng`. This is a network capture file, which is basically a recording of the network traffic (like web requests) that happened over a period of time.

1. **Searching the Capture File:**
   We can look through the raw text of this recording to see if we can find any cookies being sent. We can do this using a tool called `strings`, which extracts all the readable text from a file, and then filter it for the word "cookie" using `grep`.

   Running `strings GLaDOS_Network.pcapng | grep -i "cookie"` reveals the following line:
   ```
   Cookie: cake=Ynl1Y3Rme1RoM19DNGszXyFzXzRfTCEzX0hUQzU2emVFfQ==
   ```

2. **Decoding the Cookie:**
   We see a cookie named `cake`! Its value is a string of characters: `Ynl1Y3Rme1RoM19DNGszXyFzXzRfTCEzX0hUQzU2emVFfQ==`.

   This string ends with `==` and uses a mix of uppercase letters, lowercase letters, and numbers. This is a telltale sign that the text is encoded using **Base64**. Base64 is a way to represent data (like text or images) using only 64 common characters, making it safe to transmit over different systems.

3. **Finding the Flag:**
   To read what the cookie actually says, we need to decode the Base64 string back into normal text.

   Decoding `Ynl1Y3Rme1RoM19DNGszXyFzXzRfTCEzX0hUQzU2emVFfQ==` using a Base64 decoder gives us our flag:

   ```
   byuctf{Th3_C4k3_!s_4_L!3_HTC56zeE}
   ```

And there we have it! We found the flag hidden in a web cookie inside the network traffic recording.
