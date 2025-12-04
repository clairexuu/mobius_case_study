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

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False

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
        '--dataset_type',
        type=str,
        default='natural',
        choices=['natural', 'cheat', 'non_cheat'],
        help='Dataset type: natural (for train/test split), cheat (test only), non_cheat (test only)'
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
        help='Number of training samples (only used for natural dataset)'
    )
    parser.add_argument(
        '--ntest',
        type=int,
        default=100000,
        help='Number of test samples'
    )
    parser.add_argument(
        '--function',
        type=str,
        default='mobius',
        choices=['mobius', 'liouville'],
        help='Arithmetic function to process'
    )

    args = parser.parse_args()

    # Set function-specific prefixes
    if args.function == 'mobius':
        prefix = 'mu'
        prefix_sq = 'musq'
    elif args.function == 'liouville':
        prefix = 'lambda'
        prefix_sq = 'lambdasq'

    # Create encoding-specific subdirectory with dataset type
    encoding_dir = os.path.join(args.input_dir, f"input_dir_{args.encoding}_{args.dataset_type}")
    os.makedirs(encoding_dir, exist_ok=True)

    # Generate filenames based on encoding and dataset type
    base_func = f"{prefix}_{args.encoding}"
    base_func_sq = f"{prefix_sq}_{args.encoding}"

    # Add dataset type suffix
    func_filename = os.path.join(encoding_dir, f"{base_func}_{args.dataset_type}.txt")
    func_sq_filename = os.path.join(encoding_dir, f"{base_func_sq}_{args.dataset_type}.txt")

    print(f"Shuffling and splitting data with encoding: {args.encoding}")
    print(f"Function: {args.function}")
    print(f"Dataset type: {args.dataset_type}")

    # All dataset types: create train/test split
    print(f"  Training samples: {args.ntrain}")
    print(f"  Test samples: {args.ntest}")

    # Process function files
    if os.path.exists(func_filename):
        print(f"\nProcessing: {func_filename}")
        shuffle_and_create(func_filename, args.ntrain, args.ntest)
    else:
        print(f"Warning: {func_filename} not found!")

    # Process function squared files
    if os.path.exists(func_sq_filename):
        print(f"\nProcessing: {func_sq_filename}")
        shuffle_and_create(func_sq_filename, args.ntrain, args.ntest)
    else:
        print(f"Warning: {func_sq_filename} not found!")

    print("\nDone!")


if __name__ == "__main__":
    main()
