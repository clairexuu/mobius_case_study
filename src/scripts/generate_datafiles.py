"""
generate_datafiles.py - make mobius datafiles for Int2Int

NOTE: this implicitly assumes python3.10+. This could be made to work with
earlier version of python by using different context-manager syntax for opening
files.

## License Information ##

Copyright © 2025 David Lowry-Duda <david@lowryduda.com>

MIT License

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
import random
import argparse
import os

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    print("Note: Install tqdm for progress bar support: pip install tqdm")

from utils import dldmobius, dldliouville, encode_integer, primes_100


def make_line(inputfunc, outputfunc, n):
    return inputfunc(n) + "\t" + outputfunc(n) + "\n"


def generate_natural_number(min_val, max_val):
    """Generate a uniform random number between min_val and max_val."""
    return random.randint(min_val, max_val)


def generate_cheat_number(min_val, max_val):
    """
    Generate a number whose prime factors are all within the first 100 primes.

    Use logarithms to control the size more precisely.
    Target a specific log value and build the number incrementally.
    """
    import math

    # Target log range
    log_min = math.log(max(min_val, 2))
    log_max = math.log(max_val)

    # Pick a target log value
    target_log = random.uniform(log_min, log_max)

    # Build number by selecting primes and powers
    n = 1
    current_log = 0.0
    log_primes = [math.log(p) for p in primes_100]

    # Shuffle primes for randomness
    indices = list(range(len(primes_100)))
    random.shuffle(indices)

    # Add primes until we reach close to target
    for idx in indices:
        p = primes_100[idx]
        log_p = log_primes[idx]

        if current_log >= target_log:
            break

        # Calculate how many times we can use this prime
        remaining_log = target_log - current_log
        max_power = int(remaining_log / log_p)

        if max_power >= 1:
            # Use this prime with probability that decreases with size
            if random.random() < 0.5:  # 50% chance to use each applicable prime
                power = random.randint(1, min(max_power, 5))  # Limit to reasonable powers
                n *= p ** power
                current_log += power * log_p

    # Ensure n is in range
    if n < min_val:
        # Multiply by a small random product of primes
        while n < min_val and n < max_val // primes_100[0]:
            p = random.choice(primes_100[:10])  # Use smaller primes
            if n * p <= max_val:
                n *= p
            else:
                break

    if n > max_val:
        # Divide by random prime factors until in range
        for p in primes_100:
            while n > max_val and n % p == 0:
                n //= p

    # Final check
    if min_val <= n <= max_val:
        return n

    # Fallback: generate a simple product
    n = 1
    for p in random.sample(primes_100[:20], k=random.randint(3, 8)):
        n *= p
        if n > max_val:
            n //= p
            break

    return max(min_val, min(n, max_val))


def is_composed_only_of_first_100_primes(n):
    """Check if n has only prime factors within the first 100 primes."""
    for p in primes_100:
        while n % p == 0:
            n //= p
    return n == 1


def generate_non_cheat_number(min_val, max_val, max_attempts=10000):
    """
    Generate a number that has at least one prime factor outside the first 100 primes.

    Strategy: generate random numbers and check if they have a prime factor
    outside the first 100 primes.
    """
    for _ in range(max_attempts):
        n = random.randint(min_val, max_val)
        if not is_composed_only_of_first_100_primes(n):
            return n

    # Fallback: multiply a random number by a prime just outside the first 100
    # The 101st prime is 547
    return random.randint(min_val // 547, max_val // 547) * 547


# Encoding format implementations
def make_input_interCRT100(n):
    """
    Interleaved CRT encoding with 100 primes.
    Format: [n mod p1, p1, n mod p2, p2, ..., n mod p100, p100]
    """
    ret = []
    count = len(primes_100)
    ret.append(f"V{2*count}")
    for p in primes_100:
        ret.append(encode_integer(n % p))
        ret.append(encode_integer(p))
    return ' '.join(ret)


def make_input_CRT100(n):
    """
    Standard CRT encoding with 100 primes.
    Format: [n mod p1, n mod p2, ..., n mod p100]
    """
    ret = []
    count = len(primes_100)
    ret.append(f"V{count}")
    for p in primes_100:
        ret.append(encode_integer(n % p))
    return ' '.join(ret)


def make_input_interCRT100_with_n(n):
    """
    Interleaved CRT with n appended.
    Format: [n mod p1, p1, n mod p2, p2, ..., n mod p100, p100, n]
    """
    ret = []
    count = len(primes_100)
    ret.append(f"V{2*count + 1}")
    for p in primes_100:
        ret.append(encode_integer(n % p))
        ret.append(encode_integer(p))
    ret.append(encode_integer(n))
    return ' '.join(ret)


def make_input_CRT100_with_stats(n):
    """
    CRT encoding with proportion of primes dividing n and parity.
    Format: [n mod p1, n mod p2, ..., n mod p100, x, k, parity(x)]
    where x = distinct number of primes (among first 100) that divide n
          k = total number of primes (100)
          parity(x) = x mod 2 (0 for even, 1 for odd)
    """
    ret = []
    count = len(primes_100)

    # Count how many primes divide n
    num_dividing_primes = 0
    for p in primes_100:
        if n % p == 0:
            num_dividing_primes += 1

    # Calculate proportion x/k
    proportion = num_dividing_primes  # Numerator (will encode as x and k separately)
    total_primes = count  # Denominator
    parity = num_dividing_primes % 2  # 0 for even, 1 for odd

    # Vector length: 100 CRT values + proportion_numerator + proportion_denominator + parity
    ret.append(f"V{count + 3}")

    # Add CRT representation
    for p in primes_100:
        ret.append(encode_integer(n % p))

    # Add statistics
    ret.append(encode_integer(proportion))  # x (numerator)
    ret.append(encode_integer(total_primes))  # k (denominator)
    ret.append(encode_integer(parity))  # parity of x

    return ' '.join(ret)


def make_input_interCRT_sqfree(n):
    """
    New encoding format: [interleaving CRT | square free flag]
    Format: [n mod p1, p1, n mod p2, p2, ..., n mod p100, p100, sqfree_flag]
    where sqfree_flag = 1 if n is square-free, 0 otherwise (computed as μ²(n))

    Vector length: 200 (interleaved CRT) + 1 (sqfree) = 201
    """
    ret = []
    count = len(primes_100)

    # Vector length: 2*100 + 1 = 201
    ret.append(f"V{2*count + 1}")

    # Add interleaved CRT representation (without n at the beginning)
    for p in primes_100:
        ret.append(encode_integer(n % p))
        ret.append(encode_integer(p))

    # Add square-free flag: μ²(n) = 1 if square-free, 0 otherwise
    mu = dldmobius(n)
    sqfree_flag = mu * mu  # This is μ²(n): 1 if μ ≠ 0, else 0
    ret.append(encode_integer(sqfree_flag))

    return ' '.join(ret)


# Encoding format registry
ENCODING_FORMATS = {
    'interCRT100': make_input_interCRT100,
    'CRT100': make_input_CRT100,
    'interCRT100_with_n': make_input_interCRT100_with_n,
    'CRT100_with_stats': make_input_CRT100_with_stats,
    'interCRT_sqfree': make_input_interCRT_sqfree,
}


def make_output_mu(n):
    return str(dldmobius(n))


def make_output_musq(n):
    return str(dldmobius(n)**2)


def make_output_lambda(n):
    return str(dldliouville(n))


def make_output_lambdasq(n):
    return str(dldliouville(n)**2)


def get_output_filename(encoding_format, task):
    """
    Generate output filename based on encoding format and task.
    """
    return f"{task}_{encoding_format}.txt"


def main():
    parser = argparse.ArgumentParser(
        description='Generate Möbius function training data with different encoding formats'
    )
    parser.add_argument(
        '--encoding',
        type=str,
        default='interCRT100',
        choices=list(ENCODING_FORMATS.keys()),
        help='Encoding format for input data'
    )
    parser.add_argument(
        '--dataset_type',
        type=str,
        default='natural',
        choices=['natural', 'cheat', 'non_cheat'],
        help='Dataset type: natural (uniform random), cheat (only first 100 prime factors), non_cheat (at least one prime factor outside first 100)'
    )
    parser.add_argument(
        '--num_samples',
        type=int,
        default=1000000,
        help='Number of samples to generate'
    )
    parser.add_argument(
        '--min_value',
        type=int,
        default=2,
        help='Minimum value for random integers'
    )
    parser.add_argument(
        '--max_value',
        type=int,
        default=10**13,
        help='Maximum value for random integers'
    )
    parser.add_argument(
        '--output_dir',
        type=str,
        default='../../input/',
        help='Output directory for generated files'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        help='Random seed for reproducibility'
    )
    parser.add_argument(
        '--function',
        type=str,
        default='mobius',
        choices=['mobius', 'liouville'],
        help='Arithmetic function to compute'
    )

    args = parser.parse_args()

    # Set random seed if provided
    if args.seed is not None:
        random.seed(args.seed)
        print(f"Random seed set to: {args.seed}")

    # Select number generator based on dataset type
    if args.dataset_type == 'natural':
        generate_number = lambda: generate_natural_number(args.min_value, args.max_value)
    elif args.dataset_type == 'cheat':
        generate_number = lambda: generate_cheat_number(args.min_value, args.max_value)
    elif args.dataset_type == 'non_cheat':
        generate_number = lambda: generate_non_cheat_number(args.min_value, args.max_value)

    # Create encoding-specific subdirectory with dataset type
    encoding_dir = os.path.join(args.output_dir, f"input_dir_{args.encoding}_{args.dataset_type}")
    os.makedirs(encoding_dir, exist_ok=True)

    # Get encoding function
    input_encoder = ENCODING_FORMATS[args.encoding]

    # Select output functions based on arithmetic function
    if args.function == 'mobius':
        output_func = make_output_mu
        output_func_sq = make_output_musq
        task_prefix = 'mu'
    elif args.function == 'liouville':
        output_func = make_output_lambda
        output_func_sq = make_output_lambdasq
        task_prefix = 'lambda'

    # Generate filenames with dataset type suffix
    base_filename = get_output_filename(args.encoding, task_prefix)
    base_sq_filename = get_output_filename(args.encoding, f"{task_prefix}sq")

    # Add dataset type to filename (before .txt extension)
    output_filename = os.path.join(encoding_dir, base_filename.replace('.txt', f'_{args.dataset_type}.txt'))
    output_sq_filename = os.path.join(encoding_dir, base_sq_filename.replace('.txt', f'_{args.dataset_type}.txt'))

    # Check if files already exist
    if os.path.exists(output_filename) and os.path.exists(output_sq_filename):
        print(f"Data files already exist for {args.encoding} with dataset type {args.dataset_type} and function {args.function}:")
        print(f"  - {output_filename}")
        print(f"  - {output_sq_filename}")
        print("Skipping generation. Delete these files if you want to regenerate.")
        return

    print(f"Generating {args.num_samples} samples with encoding: {args.encoding}")
    print(f"Function: {args.function}")
    print(f"Dataset type: {args.dataset_type}")
    print(f"Integer range: [{args.min_value}, {args.max_value}]")
    print(f"Output files:")
    print(f"  - {output_filename}")
    print(f"  - {output_sq_filename}")

    seen = set()
    with (
        open(output_filename, "w", encoding="utf8") as outfile,
        open(output_sq_filename, "w", encoding="utf8") as outsqfile,
    ):
        if HAS_TQDM:
            # Use tqdm progress bar
            pbar = tqdm(total=args.num_samples, desc="Generating samples", unit="samples")
            while len(seen) < args.num_samples:
                n = generate_number()
                if n in seen:
                    continue
                seen.add(n)
                outfile.write(make_line(input_encoder, output_func, n))
                outsqfile.write(make_line(input_encoder, output_func_sq, n))
                pbar.update(1)
            pbar.close()
        else:
            # Fallback to simple progress messages
            while len(seen) < args.num_samples:
                n = generate_number()
                if n in seen:
                    continue
                seen.add(n)
                outfile.write(make_line(input_encoder, output_func, n))
                outsqfile.write(make_line(input_encoder, output_func_sq, n))

                # Progress indicator every 10,000 samples
                if len(seen) % 10000 == 0:
                    progress = 100 * len(seen) / args.num_samples
                    print(f"  Progress: {len(seen):,}/{args.num_samples:,} ({progress:.1f}%)")

    print(f"\nDone! Generated {args.num_samples:,} samples.")
    print(f"\nEncoding format details ({args.encoding}):")
    if args.encoding == 'interCRT100':
        print("  Format: [n mod p₁, p₁, n mod p₂, p₂, ..., n mod p₁₀₀, p₁₀₀]")
        print("  Vector length: 200")
    elif args.encoding == 'CRT100':
        print("  Format: [n mod p₁, n mod p₂, ..., n mod p₁₀₀]")
        print("  Vector length: 100")
    elif args.encoding == 'interCRT100_with_n':
        print("  Format: [n mod p₁, p₁, n mod p₂, p₂, ..., n mod p₁₀₀, p₁₀₀, n]")
        print("  Vector length: 201")
    elif args.encoding == 'CRT100_with_stats':
        print("  Format: [n mod p₁, n mod p₂, ..., n mod p₁₀₀, x, k, parity(x)]")
        print("  where x = number of primes dividing n, k = 100, parity = x mod 2")
        print("  Vector length: 103")
    elif args.encoding == 'interCRT_sqfree':
        print("  Format: [n mod p₁, p₁, n mod p₂, p₂, ..., n mod p₁₀₀, p₁₀₀, sqfree_flag]")
        print("  where sqfree_flag = μ²(n) = 1 if n is square-free, 0 otherwise")
        print("  Vector length: 201")


if __name__ == "__main__":
    main()
