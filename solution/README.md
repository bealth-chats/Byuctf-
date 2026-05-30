# Pickle Rick ELF Challenge Write-Up

## Description
"I turned my ELF binary into a pickle, Morty! Note: not related to the python pickle library"

## Solution

**1. Analyzing the File**
First, looking at `pickled.txt`, it contains a massive sequence of only two words: "rick" and "pickle". Because there are exactly two unique words, this strongly suggests a binary encoding where one word represents `0` and the other represents `1`.

**2. Decoding the Binary**
We can write a simple Python script to read the words, map them to binary digits, and pack them into bytes (8 bits).

If we try mapping `rick -> 0` and `pickle -> 1`, we get a series of bytes. However, when we inspect the file that comes out, it is not recognized as a valid ELF file (which the description told us it should be).

**3. Finding the XOR Key**
Every ELF file starts with a specific sequence of 4 "magic" bytes: `\x7fELF` (in hex: `7f 45 4c 46`).

When we look at the first 4 bytes of our decoded file, we see they are `18 22 2b 21` in hex.
If we compare them, we can see they are XOR encoded:
* `0x18 ^ 0x7f = 0x67`
* `0x22 ^ 0x45 = 0x67`
* `0x2b ^ 0x4c = 0x67`
* `0x21 ^ 0x46 = 0x67`

We've found our XOR key! The file was encoded with a single-byte XOR key of `0x67`.

**4. Reconstructing the ELF and Getting the Flag**
We can update our Python script (`solve.py`) to decode the binary, apply the XOR key (`0x67`), and save it to an executable file.

Running `solve.py` generates `out.elf`. We then make it executable (`chmod +x out.elf`) and run it (`./out.elf`), which prints the flag:

`byuctf{1m_p1ckl3_r1111ck!}`
