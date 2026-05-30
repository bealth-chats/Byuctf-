# RSA Dreams - CTF Writeup

## The Challenge
We are given a zip file `rsa_dreams_dist.zip` which contains two files:
- `encrypt.py`: A Python script showing how the secret message (the "flag") was locked.
- `output.txt`: A text file containing the locked message (`c`), some numbers used for the lock (`n` and `e`), and a `hint`.

The description says: *"Did I give one too many hints????"*

## Understanding the Basics of the Lock (RSA)
This challenge uses a famous locking method called RSA. To understand how it works, imagine a padlock:
- You create the padlock by taking two huge, secret prime numbers, let's call them **`p`** and **`q`**.
- You multiply them together to get another number, **`n`** (so `n = p * q`).
- **`n`** is the public padlock. You can give this to anyone so they can lock messages and send them to you.
- However, to unlock the message, you *must* know the two secret starting numbers **`p`** and **`q`**.

It is very easy to multiply `p` and `q` to get `n`, but it is incredibly difficult to look at the massive number `n` and figure out what `p` and `q` were. Because of this, it is considered secure.

## The Weakness
When we look at the script `encrypt.py`, we see exactly how the `hint` was made:
**`hint = p + q`**

This is a critical mistake! We now have two pieces of a puzzle:
1. We know that `n` is `p * q`
2. We know the `hint` is `p + q`

Because we have these two math equations, we don't have to guess the secret numbers. We can use some basic algebra to figure them out!

If we take the second equation and say that `q` is the same as the `hint` minus `p`, we can put that into the first equation:
`n = p * (hint - p)`

Which becomes:
`n = (p * hint) - (p * p)`

We can rearrange this into a classic math problem called a quadratic equation:
`(p * p) - (hint * p) + n = 0`

## Solving the Puzzle
If you remember algebra from high school, you might remember the "quadratic formula" which helps you solve equations that look like `a*x^2 + b*x + c = 0`. We can use this exact formula to find our secret numbers `p` and `q`.

The formula looks like this:
`p, q = (hint ± square_root(hint*hint - 4*n)) / 2`

## Writing the Code
Using this math, we can write a short computer script to do the heavy lifting, calculate `p` and `q`, and then use standard unlocking methods to reveal our secret message.

```python
import math

# These are the massive numbers from output.txt
n = 6452268004013779272669102227661703532150635430524568657091997086066784917218113937677647594597481724133073200003104968955173212323278046973034541033497147
e = 65537
c = 5074616349947930347771128443869249667723941019037011379843932659330729580197593522845748676276068149443504037403162962894625104017380398816152166168830833
hint = 161697499284577475400347684012866511237569864647822807778480533925514941939388

# Calculate the inside of the square root (hint squared minus 4*n)
inside_square_root = hint**2 - 4*n

# Find the square root of that number
square_root_result = math.isqrt(inside_square_root)

# Find our secret numbers p and q!
p = (hint + square_root_result) // 2
q = (hint - square_root_result) // 2

# Now that we have p and q, we can create the key to unlock the message
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi) # This is the private key

# Use the private key to unlock the secret message!
m = pow(c, d, n)

# Convert the unlocked numbers back into readable text
flag = m.to_bytes((m.bit_length() + 7) // 8, 'big').decode()
print("Flag:", flag)
```

## The Flag
Running the script gives us the decrypted, secret message!
**`byuctf{great_job_recovering_the_flag}`**
