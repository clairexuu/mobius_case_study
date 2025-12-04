/*
 * liouville.cpp
 *
 * This is a very simple cpp script to evaluate the Liouville function using
 * wheel factorization. This is wrapped in C-style linkage so that it can be
 * called by a python module via ctypes.
 *
 *
 * // LICENSE INFORMATION //
 *
 * Copyright © 2025 David Lowry-Duda <david@lowryduda.com>
 *
 * MIT License
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
 * DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
 * OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

extern "C" {

int liouville(long long n) {
  if (n < 1) { return 0; }
  if (n == 1) { return 1; }
  int omega = 0;

  while (n % 2 == 0) { omega++; n/=2; }
  while (n % 3 == 0) { omega++; n/=3; }
  while (n % 5 == 0) { omega++; n/=5; }

  long long incs[] = {4, 2, 4, 2, 4, 6, 2, 6};
  int i = 0;
  long long p = 7;

  while (p*p <= n) {
    while (n % p == 0) { omega++; n /= p; }
    p += incs[i];
    i = (i + 1) % 8;
  }
  if (n > 1) { omega++; }
  return (omega % 2 == 0) ? 1 : -1;
}

}
