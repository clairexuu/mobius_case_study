"""
utils.py

## LICENSE Information ##

Copyright © 2025 David Lowry-Duda <david@lowryduda.com>

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import ctypes
import os


dldlib = ctypes.CDLL(os.path.abspath('../mobius_code/mobius.so'))
dldmobius = dldlib.mobius
dldmobius.argtypes = [ctypes.c_longlong]


def encode_integer(val, base=1000, digit_sep=" "):
    """integer -> Int2Int format"""
    if val == 0:
        return '+ 0'
    sgn = '+' if val >= 0 else '-'
    val = abs(val)
    r = []
    while val > 0:
        r.append(str(val % base))
        val = val//base
    r.append(sgn)
    r.reverse()
    return digit_sep.join(r)


def encode_integer_array(x, base=1000):
    """integers -> Int2Int format"""
    return f'V{len(x)} ' + " ".join(encode_integer(int(z), base) for z in x)


def primes_up_to(X):
    """
    A basic implementation of Eratosthenes.
    """
    arr = [True] * (X + 1)
    arr[0] = arr[1] = False
    primes = []
    for p in range(X + 1):
        if arr[p]:  # is prime
            primes.append(p)
            for j in range(p*p, X + 1, p):
                arr[j] = False
    return primes


def mobius_up_to(X):
    """
    Eratosthenes-like way to compute mobius.
    """
    arr = [1] * (X + 1)
    arr[0] = 0
    ps = primes_up_to(X)
    for p in ps:
        for j in range(p, X + 1, p):
            arr[j] *= -1
        for j in range(p*p, X + 1, p*p):
            arr[j] = 0
    return arr


primes_100 = primes_up_to(542)


def wheel_mobius(n):
    """
    Mobius using wheel-type factorization in pure python.
    """
    if n < 1:
        return 0
    if n == 1:
        return 1
    ret = 1
    if n % 2 == 0:
        ret *= -1
        n //= 2
    if n % 2 == 0:
        return 0
    if n % 3 == 0:
        ret *= -1
        n //= 3
    if n % 3 == 0:
        return 0
    if n % 5 == 0:
        ret *= -1
        n //= 5
    if n % 5 == 0:
        return 0

    incs = [4, 2, 4, 2, 4, 6, 2, 6]
    p = 7
    i = 0
    limit = int(n**.5 + 1)
    while p <= limit:
        if n % p == 0:
            ret *= -1
            n //= p
            limit = int(n**.5 + 1)
        if n % p == 0:
            return 0
        p += incs[i]
        i = (i + 1) % len(incs)
    if n > 1:
        ret *= -1
    return ret


def shuffle_and_create(fname, ntrain=900_000, ntest=100_000):
    """
    Shuffle a datafile and separate into separate testing and training files.
    Uses pure Python with tqdm for progress bars.
    """
    import random

    try:
        from tqdm import tqdm
        has_tqdm = True
    except ImportError:
        has_tqdm = False

    if not fname.endswith(".txt"):
        raise ValueError("Incorrect filename assumption.")
    name = fname[:-4]  # remove ".txt"

    # Read all lines
    print("Reading data...")
    with open(f"{name}.txt", 'r') as f:
        if has_tqdm:
            # Count lines first for progress bar
            print("Counting lines...")
            num_lines = sum(1 for _ in f)
            f.seek(0)
            lines = list(tqdm(f, total=num_lines, desc="Loading lines", unit="lines"))
        else:
            lines = f.readlines()
            print(f"  Loaded {len(lines):,} lines")

    # Shuffle
    print("Shuffling...")
    if has_tqdm:
        random.shuffle(lines)
        print(f"  Shuffled {len(lines):,} lines")
    else:
        random.shuffle(lines)
        print(f"  Shuffled {len(lines):,} lines")

    # Write shuffled file
    print("Writing shuffled data...")
    with open(f"{name}.shuf.txt", 'w') as f:
        if has_tqdm:
            for line in tqdm(lines, desc="Writing shuffled", unit="lines"):
                f.write(line)
        else:
            f.writelines(lines)
            print(f"  Wrote {len(lines):,} lines")

    # Write training data
    print("Making training data...")
    with open(f"{name}.txt.train", 'w') as f:
        if has_tqdm:
            for line in tqdm(lines[:ntrain], desc="Writing train", unit="lines"):
                f.write(line)
        else:
            f.writelines(lines[:ntrain])
            print(f"  Wrote {ntrain:,} training samples")

    # Write testing data
    print("Making testing data...")
    with open(f"{name}.txt.test", 'w') as f:
        if has_tqdm:
            for line in tqdm(lines[-ntest:], desc="Writing test", unit="lines"):
                f.write(line)
        else:
            f.writelines(lines[-ntest:])
            print(f"  Wrote {ntest:,} testing samples")

    print("Done!")
