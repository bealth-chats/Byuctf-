# Multi-Prime RSA Power Tower Challenge Write-Up

## The Challenge Overview

In this Capture The Flag (CTF) challenge, we are presented with a variation of standard encryption called "multi-prime RSA". The server gives us a math puzzle with three pieces of information:
1. **$n$ (The Modulus):** A massive number that defines the boundaries of our math.
2. **$c$ (The Ciphertext):** The encrypted, secret message we want to read.
3. **$E$ (The Exponent):** The encryption key used to lock the message. However, instead of a normal number, it's an unimaginably large "power tower" (like $37^{59^{91\dots}}$)!

Our goal is to figure out the original message ($m$) from these numbers within a 1-second time limit, which means we have to automate our solution.

---

## Step 1: Exploit the Weakness (Breaking apart $n$)

In standard RSA encryption, the security relies on the number $n$ being the product of two incredibly large prime numbers, making it practically impossible to break apart into its factors. But the challenge description gives us a massive hint: *"each factor of $n$ is at most $2^{16}$"*.

$2^{16}$ is exactly $65,536$. This means all the prime numbers multiplied together to create $n$ are actually relatively small! We can write a quick computer script to try dividing $n$ by all prime numbers up to $65,536$. Because computers are so fast, this instantly breaks $n$ apart and reveals all 25 of its prime factors.

## Step 2: Calculate $\phi(n)$

To decrypt RSA, we need a special mathematical value called Euler's Totient Function, often written as $\phi(n)$ ("phi" of n). This value essentially tells us how many numbers are "co-prime" to $n$, which is a necessary step for reversing the encryption mathematically.

Because we successfully found all the prime factors of $n$ in Step 1, calculating $\phi(n)$ is straightforward! The formula says we just subtract 1 from each prime factor and multiply them all together:
$\phi(n) = (p_1 - 1) \times (p_2 - 1) \times \dots \times (p_{25} - 1)$

## Step 3: Taming the Power Tower

We need to find out what our giant power tower exponent ($E$) evaluates to. The problem is that a number like $37^{59^{91\dots}}$ is so unfathomably large that all the computers on Earth combined could never calculate it directly.

Thankfully, advanced math comes to the rescue! According to a rule called Euler's Theorem, when dealing with exponents in this kind of "clock arithmetic" (modular arithmetic), we don't need to know the massive number itself—we only need to know what it is *modulo* $\phi(n)$ (the remainder when dividing by $\phi(n)$).

Since $E$ is a tower of exponents, we apply Euler's Theorem repeatedly. To shrink an exponent modulo $m$, we calculate the *next* level up the tower modulo $\phi(m)$, and so on, recursively going up the tower. This instantly shrinks the massive, impossible power tower down to a manageable, bite-sized number. We now have our effective encryption exponent!

## Step 4: Decrypt the Message

Now we have our standard RSA components: we know $\phi(n)$ and we know the effective encryption key.

1. We find the secret decryption key ($D$) by calculating the "modular inverse" of our effective encryption key.
2. We decrypt the ciphertext using the standard RSA decryption formula: $m = c^D \pmod n$.

## Step 5: Profit!

We take the decrypted message ($m$) and immediately send it back to the server. Because we used an automated Python script, all this complex math happens in a fraction of a second. The server verifies our answer, sees it is correct, and rewards us with the flag!

**The Flag:**
`byuctf{eulers_phi_phunction_is_a_phun_phunction}`

---

### The Python Solution Script
If you are curious about the technical implementation, here is the complete python script used to quickly connect to the server, do all the math, and retrieve the flag:

```python
import socket
import re
import math

def get_primes(n_max):
    is_prime = [True] * (n_max + 1)
    p = 2
    primes = []
    while p <= n_max:
        if is_prime[p]:
            primes.append(p)
            for i in range(p * p, n_max + 1, p):
                is_prime[i] = False
        p += 1
    return primes

primes_up_to_2_16 = get_primes(2**16)

def factor_n(n):
    factors = []
    for p in primes_up_to_2_16:
        if p * p > n:
            break
        if n % p == 0:
            factors.append(p)
            while n % p == 0:
                n //= p
    if n > 1:
        factors.append(n)
    return factors

def phi(n):
    res = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            res -= res // p
        p += 1
    if n > 1:
        res -= res // n
    return res

def exact_tower(tower):
    if not tower: return 1
    if len(tower) == 1: return tower[0]
    exp = exact_tower(tower[1:])
    if exp == float('inf'): return float('inf')
    if exp * math.log10(tower[0]) > 3000:
        return float('inf')
    return tower[0] ** exp

def eval_tower(tower, m):
    if m == 1:
        return 0
    if not tower:
        return 1
    if len(tower) == 1:
        return tower[0] % m

    exact = exact_tower(tower)
    if exact != float('inf') and exact < m:
        return exact % m

    base = tower[0]
    phim = phi(m)
    exponent_mod = eval_tower(tower[1:], phim)
    return pow(base, exponent_mod + phim, m)

def solve():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('chals.cyberjousting.com', 1359))

    data = ""
    while "What is m?" not in data:
        chunk = s.recv(4096).decode('utf-8')
        if not chunk:
            break
        data += chunk

    n_match = re.search(r'n = (\d+)', data)
    c_match = re.search(r'c = (\d+)', data)
    e_match = re.search(r'e = ([0-9\^]+)', data)

    n = int(n_match.group(1))
    c = int(c_match.group(1))
    e_str = e_match.group(1)

    exps = [int(x) for x in e_str.split('^')]

    factors = factor_n(n)

    phi_n = 1
    for f in factors:
        phi_n *= (f - 1)

    E = eval_tower(exps, phi_n)
    D = pow(E, -1, phi_n)
    m = pow(c, D, n)

    s.sendall((str(m) + '\n').encode('utf-8'))

    response = s.recv(4096).decode('utf-8')
    print("Server Response:\n", response.strip())

if __name__ == '__main__':
    solve()
```
