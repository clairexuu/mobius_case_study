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


from utils import dldmobius, encode_integer, primes_100


def make_line(inputfunc, outputfunc, n):
    return inputfunc(n) + "\t" + outputfunc(n) + "\n"


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


# Encoding format registry
ENCODING_FORMATS = {
    'interCRT100': make_input_interCRT100,
    'CRT100': make_input_CRT100,
    'interCRT100_with_n': make_input_interCRT100_with_n,
    'CRT100_with_stats': make_input_CRT100_with_stats,
}


def make_output_mu(n):
    return str(dldmobius(n))


def make_output_musq(n):
    return str(dldmobius(n)**2)


def get_output_filename(encoding_format, task):
    """
    Generate output filename based on encoding format and task.
    """
    # Keep legacy filenames for interCRT100 (backward compatibility)
    if encoding_format == 'interCRT100':
        return f"{task}_modp_and_p.txt"
    else:
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

    args = parser.parse_args()

    # Set random seed if provided
    if args.seed is not None:
        random.seed(args.seed)
        print(f"Random seed set to: {args.seed}")

    # Create encoding-specific subdirectory
    encoding_dir = os.path.join(args.output_dir, f"input_dir_{args.encoding}")
    os.makedirs(encoding_dir, exist_ok=True)

    # Get encoding function
    input_encoder = ENCODING_FORMATS[args.encoding]

    # Generate filenames
    mu_filename = os.path.join(encoding_dir, get_output_filename(args.encoding, "mu"))
    musq_filename = os.path.join(encoding_dir, get_output_filename(args.encoding, "musq"))

    print(f"Generating {args.num_samples} samples with encoding: {args.encoding}")
    print(f"Integer range: [{args.min_value}, {args.max_value}]")
    print(f"Output files:")
    print(f"  - {mu_filename}")
    print(f"  - {musq_filename}")

    seen = set()
    with (
        open(mu_filename, "w", encoding="utf8") as mufile,
        open(musq_filename, "w", encoding="utf8") as musqfile,
    ):
        while len(seen) < args.num_samples:
            n = random.randint(args.min_value, args.max_value)
            if n in seen:
                continue
            seen.add(n)
            mufile.write(make_line(input_encoder, make_output_mu, n))
            musqfile.write(make_line(input_encoder, make_output_musq, n))

            # Progress indicator
            if len(seen) % 100000 == 0:
                print(f"  Generated {len(seen):,} samples...")

    print(f"Done! Generated {args.num_samples:,} samples.")
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


if __name__ == "__main__":
    main()
