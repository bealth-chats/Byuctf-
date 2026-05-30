# Stereotyped Message Attack CTF Writeup

**Flag:** `byuctf{cuz_st3r30typ3s_hurt_92de04}`

Here is a step-by-step, simple explanation of how we found the hidden flag for this challenge!

## 1. The Setup
When we open the challenge files, we are presented with a cryptographic puzzle. We have a locked box (an encrypted message) and the public details of the lock (`N` and `e`), along with the locked message itself (`c`). This uses a very famous encryption method called **RSA**.

Normally, RSA is incredibly secure. If it is set up correctly, it would take supercomputers billions of years to guess what is inside our locked box.

## 2. The Clue
However, we have a massive clue! We know almost exactly what the message inside the box says.

The python code used to lock the box (`enc.py`) shows us that the secret message starts with a very long, predictable sentence:
> *"Congrats on making it all the way here. If you're looking at this challenge you obviously know a lot, just find the flag: "*

Right after that long sentence is our unknown, secret flag.

## 3. The Weakness
Because the encryption used a very small public exponent (`e = 3`) and because we already know a huge chunk of the message, the lock is broken.

We can use a powerful mathematical trick known as **Coppersmith's Stereotyped Message Attack**.

Think of it like playing a game of *Wheel of Fortune* or *Hangman*. If a puzzle has 150 letters and you already know 120 of them, it becomes very easy to guess the remaining few letters. In the world of cryptography, because we know so much of the message and the lock's "settings" were weak, advanced math allows us to automatically calculate the missing letters without having to guess them one by one.

## 4. The Solution
To crack the puzzle, we wrote a Python script using some advanced math tools.

Since we didn't know exactly how long the secret flag was (how many missing letters there were), our script just tried every possible length one by one. For each length (e.g., 15 letters, 16 letters, etc.), the script asked the math tool: *"If the flag is this long, can you fill in the blanks using Coppersmith's attack?"*

## 5. The Result
We ran our script, and it quickly tested different lengths. When it guessed that the flag was exactly 35 characters long, the math perfectly aligned, and the lock popped open.

The script successfully revealed the missing piece of the message: `byuctf{cuz_st3r30typ3s_hurt_92de04}`.