# Data Encoding Formats

This document describes the data encoding formats for the Möbius function dataset.


### 1. `interCRT100` (Default)
**Interleaved Chinese Remainder Theorem encoding with 100 primes**

- **Format:** `[n mod p₁, p₁, n mod p₂, p₂, ..., n mod p₁₀₀, p₁₀₀]`
- **Vector length:** 200
- **Primes used:** First 100 primes (2, 3, 5, ..., 541)
- **Example:** For n=12345:
  ```
  V200 + 1 + 2 + 0 + 3 + 0 + 5 + 4 + 7 ...
       ╰─┬─╯ ╰─┬─╯ ╰─┬─╯ ╰─┬─╯
      n%2  p=2  n%3  p=3  n%5  p=5  n%7  p=7
  ```


### 2. `CRT100`
**Standard Chinese Remainder Theorem encoding**

- **Format:** `[n mod p₁, n mod p₂, ..., n mod p₁₀₀]`
- **Vector length:** 100
- **Primes used:** First 100 primes (2, 3, 5, ..., 541)
- **Example:** For n=12345:
  ```
  V100 + 1 + 0 + 0 + 4 + 3 + 8 + 3 + 14 ...
       ╰─┬─╯ ╰─┬─╯ ╰─┬─╯ ╰─┬─╯
       n%2   n%3   n%5   n%7
  ```

### 3. `interCRT100_with_n`
**Interleaved CRT encoding with original number appended**

- **Format:** `[n mod p₁, p₁, n mod p₂, p₂, ..., n mod p₁₀₀, p₁₀₀, n]`
- **Vector length:** 201
- **Primes used:** First 100 primes plus the original number
- **Example:** For n=12345:
  ```
  V201 + 1 + 2 + 0 + 3 + ... + 12 345
       ╰─┬─╯ ╰─┬─╯          ╰─────┬─────╯
       CRT encoding           original n
  ```
