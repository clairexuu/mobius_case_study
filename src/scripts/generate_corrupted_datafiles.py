"""
generate_corrupted_datafiles.py - make datafiles for Int2Int

This also makes datafiles with incorrect values at the primes 2 and 3.

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

from utils import dldmobius, dldliouville, encode_integer, primes_100


def make_line(input_func, output_func, n):
    return input_func(n) + "\t" + output_func(n) + "\n"


def make_correct_input(n):
    ret = []
    count = len(primes_100)
    ret.append(f"V{2*count}")
    for p in primes_100:
        ret.append(encode_integer(n % p))
        ret.append(encode_integer(p))
    return ' '.join(ret)


def make_23_wrong_input(n):
    ret = []
    count = len(primes_100)
    ret.append(f"V{2*count}")
    for p in primes_100[:2]:
        ret.append(encode_integer(random.randint(0, p-1)))
        ret.append(encode_integer(p))
    for p in primes_100[2:]:
        ret.append(encode_integer(n % p))
        ret.append(encode_integer(p))
    return ' '.join(ret)


def make_23_only_right_input(n):
    ret = []
    count = len(primes_100)
    ret.append(f"V{2*count}")
    for p in primes_100[:2]:
        ret.append(encode_integer(n % p))
        ret.append(encode_integer(p))
    for p in primes_100[2:]:
        ret.append(encode_integer(random.randint(0, p-1)))
        ret.append(encode_integer(p))
    return ' '.join(ret)


def make_p_random_input_func(q):
    def inner(n):
        ret = []
        count = len(primes_100)
        ret.append(f"V{2*count}")
        for p in primes_100:
            if p != q:
                ret.append(encode_integer(n % p))
                ret.append(encode_integer(p))
            else:
                ret.append(encode_integer(random.randint(0, p-1)))
                ret.append(encode_integer(p))
        return ' '.join(ret)
    return inner


def make_output_mu(n):
    return str(dldmobius(n))


def make_output_musq(n):
    return str(dldmobius(n)**2)


def make_output_lambda(n):
    return str(dldliouville(n))


def make_output_lambdasq(n):
    return str(dldliouville(n)**2)


def main():
    parser = argparse.ArgumentParser(
        description='Generate corrupted datafiles for testing'
    )
    parser.add_argument(
        '--function',
        type=str,
        default='mobius',
        choices=['mobius', 'liouville'],
        help='Arithmetic function to compute'
    )
    args = parser.parse_args()

    if args.function == 'mobius':
        output_func = make_output_mu
        output_func_sq = make_output_musq
        prefix = 'mu'
    elif args.function == 'liouville':
        output_func = make_output_lambda
        output_func_sq = make_output_lambdasq
        prefix = 'lambda'

    outdir = "../../input/"
    seen = set()
    with (
        open(outdir + f"{prefix}_only23_correct.txt", "w", encoding="utf8") as f23,
        open(outdir + f"{prefix}sq_only23_correct.txt", "w", encoding="utf8") as fsq23,
        open(outdir + f"{prefix}_2_random.txt", "w", encoding="utf8") as f2hat,
        open(outdir + f"{prefix}sq_2_random.txt", "w", encoding="utf8") as fsq2hat,
        open(outdir + f"{prefix}_p_3_random.txt", "w", encoding="utf8") as f3hat,
        open(outdir + f"{prefix}sq_p_3_random.txt", "w", encoding="utf8") as fsq3hat,
        open(outdir + f"{prefix}_23_random.txt", "w", encoding="utf8") as f23hat,
        open(outdir + f"{prefix}sq_23_random.txt", "w", encoding="utf8") as fsq23hat,
        open(outdir + f"{prefix}_true.txt", "w", encoding="utf8") as ftrue,
        open(outdir + f"{prefix}sq_true.txt", "w", encoding="utf8") as fsqtrue,
    ):
        while len(seen) < 10**5:
            n = random.randint(2, 10**13)
            if n in seen:
                continue
            seen.add(n)
            f23.write(make_line(make_23_only_right_input, output_func, n))
            fsq23.write(make_line(make_23_only_right_input, output_func_sq, n))
            f2hat.write(make_line(make_p_random_input_func(2), output_func, n))
            fsq2hat.write(make_line(make_p_random_input_func(2), output_func_sq, n))
            f3hat.write(make_line(make_p_random_input_func(3), output_func, n))
            fsq3hat.write(make_line(make_p_random_input_func(3), output_func_sq, n))
            f23hat.write(make_line(make_23_wrong_input, output_func, n))
            fsq23hat.write(make_line(make_23_wrong_input, output_func_sq, n))
            ftrue.write(make_line(make_correct_input, output_func, n))
            fsqtrue.write(make_line(make_correct_input, output_func_sq, n))


if __name__ == "__main__":
    print("Making good and corrupt datafiles in ../../input")
    main()
    print("Done")
