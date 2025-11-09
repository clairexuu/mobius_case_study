"""
shuffle_datafiles.py


## LICENSE Information ##

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
import argparse
import os
from utils import shuffle_and_create


def main():
    parser = argparse.ArgumentParser(
        description='Shuffle and split datafiles into train/test sets'
    )
    parser.add_argument(
        '--encoding',
        type=str,
        default='interCRT100',
        help='Encoding format (must match the format used in generate_datafiles.py)'
    )
    parser.add_argument(
        '--input_dir',
        type=str,
        default='../../input/',
        help='Input directory containing data files'
    )
    parser.add_argument(
        '--ntrain',
        type=int,
        default=900000,
        help='Number of training samples'
    )
    parser.add_argument(
        '--ntest',
        type=int,
        default=100000,
        help='Number of test samples'
    )

    args = parser.parse_args()

    # Create encoding-specific subdirectory
    encoding_dir = os.path.join(args.input_dir, f"input_dir_{args.encoding}")
    os.makedirs(encoding_dir, exist_ok=True)

    # Generate filenames based on encoding
    # Keep legacy filenames for interCRT100 (backward compatibility)
    if args.encoding == 'interCRT100':
        mu_filename = os.path.join(encoding_dir, "mu_modp_and_p.txt")
        musq_filename = os.path.join(encoding_dir, "musq_modp_and_p.txt")
    else:
        mu_filename = os.path.join(encoding_dir, f"mu_{args.encoding}.txt")
        musq_filename = os.path.join(encoding_dir, f"musq_{args.encoding}.txt")

    print(f"Shuffling and splitting data with encoding: {args.encoding}")
    print(f"  Training samples: {args.ntrain}")
    print(f"  Test samples: {args.ntest}")

    # Process mu files
    if os.path.exists(mu_filename):
        print(f"\nProcessing: {mu_filename}")
        shuffle_and_create(mu_filename, args.ntrain, args.ntest)
    else:
        print(f"Warning: {mu_filename} not found!")

    # Process musq files
    if os.path.exists(musq_filename):
        print(f"\nProcessing: {musq_filename}")
        shuffle_and_create(musq_filename, args.ntrain, args.ntest)
    else:
        print(f"Warning: {musq_filename} not found!")

    print("\nDone!")


if __name__ == "__main__":
    main()
