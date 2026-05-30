import sys
from fpylll import IntegerMatrix, LLL
from Crypto.Util.number import bytes_to_long, long_to_bytes
import sympy

sys.set_int_max_str_digits(100000)

with open('output.txt', 'r') as f:
    lines = f.read().strip().split('\n')
    N = int(lines[0].split(' = ')[1])
    e = int(lines[1].split(' = ')[1])
    c = int(lines[2].split(' = ')[1])

prefix_str = b"Congrats on making it all the way here. If you're looking at this challenge you obviously know a lot, just find the flag: "
print(f"Prefix length: {len(prefix_str)}")

def solve_coppersmith(L):
    # A is the prefix shifted by L bytes
    A = bytes_to_long(prefix_str) * (256**L)

    # Coefficients of f(x)
    a3 = 1
    a2 = 3 * A
    a1 = 3 * A**2
    a0 = A**3 - c

    # We want to find x such that |x| < X
    X = 256**L

    # Let's try dimension 4
    dim = 4
    B = IntegerMatrix(dim, dim)

    B[0, 0] = N

    B[1, 0] = 0
    B[1, 1] = N * X

    B[2, 0] = 0
    B[2, 1] = 0
    B[2, 2] = N * X**2

    B[3, 0] = a0 % N
    B[3, 1] = (a1 % N) * X
    B[3, 2] = (a2 % N) * X**2
    B[3, 3] = X**3

    # Apply LLL
    M = LLL.reduction(B)

    # The first row gives a polynomial with small coefficients
    poly_coeffs = [M[0, i] // (X**i) for i in range(dim)]

    # Reverse to get decreasing powers of x
    poly_coeffs = poly_coeffs[::-1]

    x = sympy.Symbol('x')
    f_x = sum([poly_coeffs[i] * x**(dim - 1 - i) for i in range(dim)])

    roots = sympy.roots(f_x, x)

    for r in roots:
        if r.is_integer:
            root_val = int(r)
            if root_val > 0 and root_val < X:
                flag = long_to_bytes(root_val)
                if b'byuctf{' in flag:
                    print(f"Found flag! {flag}")
                    return True
    return False

for L in range(15, 60):
    print(f"Testing length {L}...")
    if solve_coppersmith(L):
        break
