# Liouville Function Support

This repository now supports the Liouville function λ(n) in addition to the Möbius function μ(n).

## Mathematical Definition

The Liouville function λ(n) returns (-1)^Ω(n) where Ω(n) is the total number of prime factors of n (counted with multiplicity).

**Key Properties:**
- λ(n) ∈ {-1, 1} (never returns 0, unlike μ(n))
- λ(1) = 1
- λ(p^k) = (-1)^k for prime p
- λ is completely multiplicative: λ(ab) = λ(a)λ(b)

**Examples:**
```
λ(1) = 1
λ(2) = -1       (one factor)
λ(4) = 1        (2² has two factors)
λ(6) = 1        (2×3 has two factors)
λ(8) = -1       (2³ has three factors)
λ(12) = -1      (2²×3 has three factors)
```


**JUST DO THIS TO RUN**
**Just generate and shuffle data:**
```bash
cd src/run_int2int_scripts
make data ENCODING=interCRT100 FUNCTION=liouville
```

## Implementation

### C++ Implementation
`src/mobius_code/liouville.cpp` - Fast wheel factorization implementation

### Python Wrapper
`src/scripts/utils.py` contains:
- `dldliouville` - ctypes wrapper for C++ implementation
- `wheel_liouville` - pure Python implementation

### Tests
`src/mobius_code/liouville_test.py` - Unit tests

Run tests with:
```bash
cd src/mobius_code
make test_liouville
```

## Usage

### Compile the Liouville Library
```bash
cd src/mobius_code
make liouville.so
```

### Generate Training Data
```bash
cd src/scripts
python generate_datafiles.py \
    --encoding interCRT100 \
    --dataset_type natural \
    --function liouville \
    --num_samples 1000000 \
    --seed 42
```

Or using make:
```bash
make good_data ENCODING=interCRT100 DATASET_TYPE=natural FUNCTION=liouville
```

### Generate Corrupted Data
```bash
python generate_corrupted_datafiles.py --function liouville
```

Or using make:
```bash
make corrupted_data FUNCTION=liouville
```

### Training Commands

**Generate data and train (GPU):**
```bash
cd src/run_int2int_scripts
make run ENCODING=interCRT100 FUNCTION=liouville
```

**Generate data and train (CPU):**
```bash
cd src/run_int2int_scripts
make run-cpu ENCODING=interCRT100 FUNCTION=liouville
```

**Just generate and shuffle data:**
```bash
cd src/run_int2int_scripts
make data ENCODING=interCRT100 FUNCTION=liouville
```

**Train on existing data:**
```bash
cd src/run_int2int_scripts
make train ENCODING=interCRT100 FUNCTION=liouville
```

## Command Line Arguments

All data generation scripts now accept `--function` argument:
- `--function mobius` (default) - Generate Möbius function data
- `--function liouville` - Generate Liouville function data

## Output Files

### Möbius (default):
- `mu_<encoding>_<dataset_type>.txt`
- `musq_<encoding>_<dataset_type>.txt`

### Liouville:
- `lambda_<encoding>_<dataset_type>.txt`
- `lambdasq_<encoding>_<dataset_type>.txt`

Note: λ²(n) = 1 for all n ≥ 1 (since λ(n) ∈ {-1, 1})

## Differences from Möbius

| Property | Möbius μ(n) | Liouville λ(n) |
|----------|-------------|----------------|
| Range | {-1, 0, 1} | {-1, 1} |
| Zero values | Yes (squared factors) | No |
| Factor counting | Distinct primes only | All prime factors |
| Multiplicativity | Multiplicative | Completely multiplicative |
| ML difficulty | 3-class classification | Binary classification |

## Expected Performance

Training models on the Liouville function may be slightly easier than Möbius because:
1. Binary classification ({-1, 1}) instead of 3-class ({-1, 0, 1})
2. No special "squared factor" detection required
3. More balanced class distribution (~50/50 split)

However, the model still needs to learn prime factorization patterns, making it a challenging task.
