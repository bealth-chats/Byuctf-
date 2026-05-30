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
        print(chunk, end='')

    n_match = re.search(r'n = (\d+)', data)
    c_match = re.search(r'c = (\d+)', data)
    e_match = re.search(r'e = ([0-9\^]+)', data)

    if not (n_match and c_match and e_match):
        print("Could not parse n, c, or e")
        return

    n = int(n_match.group(1))
    c = int(c_match.group(1))
    e_str = e_match.group(1)

    exps = [int(x) for x in e_str.split('^')]

    print(f"Factoring n...")
    factors = factor_n(n)
    print(f"Factors: {factors}")

    phi_n = 1
    for f in factors:
        phi_n *= (f - 1)

    print(f"phi(n) = {phi_n}")

    print(f"Evaluating tower...")
    E = eval_tower(exps, phi_n)
    print(f"E = {E}")

    D = pow(E, -1, phi_n)
    print(f"D = {D}")

    m = pow(c, D, n)
    print(f"m = {m}")

    s.sendall((str(m) + '\n').encode('utf-8'))

    response = s.recv(4096).decode('utf-8')
    print(response)

if __name__ == '__main__':
    solve()
