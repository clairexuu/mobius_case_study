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

    args = parser.parse_args()

    # Create encoding-specific subdirectory with dataset type
    encoding_dir = os.path.join(args.input_dir, f"input_dir_{args.encoding}_{args.dataset_type}")
    os.makedirs(encoding_dir, exist_ok=True)

    # Generate filenames based on encoding and dataset type
    base_mu = f"mu_{args.encoding}"
    base_musq = f"musq_{args.encoding}"

    # Add dataset type suffix
    mu_filename = os.path.join(encoding_dir, f"{base_mu}_{args.dataset_type}.txt")
    musq_filename = os.path.join(encoding_dir, f"{base_musq}_{args.dataset_type}.txt")

    print(f"Shuffling and splitting data with encoding: {args.encoding}")
    print(f"Dataset type: {args.dataset_type}")

    # All dataset types: create train/test split
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
