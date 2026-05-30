# Incontinent - CTF Writeup

## The Challenge
We were given an executable program (`incontinent_dist`) and a remote server address (`chals.cyberjousting.com:1366`). The description told us that the flag was located on the remote server and hinted at needing to find a "leaky" behavior in the program to get it.

## The Problem (Vulnerability)
When interacting with the program, it asks for a message and then repeats it back to us:

```
I've got the flag securely locked up, anything you want to say to it?
You said:
[Our Input]
```

However, the program has a small flaw in how it handles our input. In computer memory, text is usually followed by a special "stop sign" (a null byte) to tell the computer where the text ends. If the program forgets to add this stop sign or if we fill the memory buffer completely so there is no room for it, the computer keeps reading memory until it accidentally finds another stop sign.

This means it might read and show us secret information (like the flag) that happens to be sitting right next to our message in the computer's memory! This is called an **Out-of-Bounds Read** or **Information Leak**.

## The Solution
To test this, we sent a message that was exactly the right size to fill the program's expected space, preventing it from adding the "stop sign".

After some trial and error on the remote server, we discovered that sending exactly **32 characters** (like 32 'A's) filled the space perfectly. When the program tried to repeat our message, it kept reading past the 32 'A's and spilled the flag that was sitting right next to it!

### Step-by-Step Exploit
1. We used a simple Python script to connect to the remote server `chals.cyberjousting.com` on port `1366`.
2. We waited for the program's initial greeting.
3. We sent a string of 32 'A's (`AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA`).
4. The server responded with our 'A's, immediately followed by the hidden flag because it didn't know where our text stopped!

The server output looked like this:
```
You said: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
yuctf{incontinent_is_one_of_my_favorite_words_lol}
```

The flag is: `byuctf{incontinent_is_one_of_my_favorite_words_lol}`
