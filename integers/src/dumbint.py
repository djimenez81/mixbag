#!/usr/bin/python
# module dumbint

# This module implements some basic algorithms that, for floats are well
# implemented already. But in this case, I need them implemented strictly with
# integer arithmetics.

# Copyright (c) 2017 David Jimenez.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#   - Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#   - Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#   - Neither the name of the <organization> nor the names of its contributors
#     may be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL DAVID JIMENEZ BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


def cubeRoot(N):
    return theRoot(N,3)


def squareRoot(N):
    return theRoot(N,2)


def theRoot(N,K):
    # Computes the floor of the K-th root of N, if N is not negative, and the
    # ceiling if N is negative. N and K need to be integers. It uses a simple
    # bisection-method approximation approach.
    LOW = 0
    if N < 0:
        HIGH = -N
        X = -N
    else:
        HIGH = N
        X = N
    NOW = HIGH//2
    while HIGH-LOW >2:
        if NOW**K > X:
            NEXT = (LOW+NOW)//2
            HIGH = NOW
        else:
            NEXT = (HIGH+NOW)//2
            LOW = NOW
        NOW = NEXT
    if NOW**K > X and X > N:
        return -LOW
    elif NOW**K > X:
        return LOW
    elif X > N:
        return -NOW
    else:
        return NOW


def gcd(N,M):
    # This method calculates the greater common denominator of N and M.
    if N < M:
        K = M
        M = N
        N = K
    K = N%M
    while K!=0:
        N = M
        M = K
        K = N%M
    return M


def factorization(N):
    # This finds the prime factorization of N.
    # Innefficient for numbers with big prime factors.
    primeFactors = []
    if N % 2 == 0:
        while N % 2 == 0:
            primeFactors.append(2)
            N //= 2
    d = 3
    while d * d < N:
        while N % d == 0:
            primeFactors.append(d)
            N //= d
        d += 2
    if N > 1:
        primeFactors.append(N)
    return primeFactors
    