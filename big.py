#!/usr/bin/snek

import random

def big_string(b):
    return b[0] + b[:0:-1]

def big_equal(a,b):
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True

def big_uless(a,b):
    if len(a) > len(b):
        return False
    if len(a) < len(b):
        return True
    for i in range(len(a)-1,0,-1):
        if a[i] < b[i]:
            return True
        if a[i] > b[i]:
            return False
    return False

def big_less(a,b):
    if a[0] == b[0]:
        if a[0] == '-':
            return big_uless(b,a)
        return big_uless(a,b)
    if a[0] == '-':
        return True
    return False

def big_uplus(a,b,sign):
    r = sign
    carry = 0
    if len(a) < len(b):
        t = b
        b = a
        a = t
    for i in range(1,len(b)):
        c = carry + ord(a[i]) + int(b[i])
        carry = 0
        while c > ord('9'):
            carry += 1
            c -= 10
        r += chr(c)
    for i in range(len(b), len(a)):
        c = carry + ord(a[i])
        carry = 0
        while c > ord('9'):
            carry += 1
            c -= 10
        r += chr(c)
    while carry > 0:
        c = carry + ord('0')
        carry = 0
        while c > ord('9'):
            carry += 1
            c -= 10
        r += chr(c)
    return r

def big_uminus(a,b,sign):
    r = sign
    borrow = 0
    assert len(a) >= len(b)
    for i in range(1,len(b)):
        c = ord(a[i]) - int(b[i]) - borrow
        borrow = 0
        while c < ord('0'):
            borrow += 1
            c += 10
        r += chr(c)
    for i in range(len(b), len(a)):
        c = ord(a[i]) - borrow
        borrow = 0
        while c < ord('0'):
            borrow += 1
            c += 10
        r += chr(c)
    assert borrow == 0
    i = len(r)
    while i > 3 and r[i-1] == '0':
        i -= 1
    if i < len(r):
        r = r[:i]
    if r == '-0':
        return '+0'
    return r

def change_sign(sign):
    if sign == '-':
        return '+'
    return '-'

def big_plus(a,b):
    if a[0] == b[0]:
        return big_uplus(a, b, a[0])
    sign = a[0]
    if big_uless(b,a):
        return big_uminus(a, b, sign)
    return big_uminus(b, a, change_sign(sign))

def big_minus(a,b):
    if a[0] == b[0]:
        sign = a[0]
        if big_uless(b,a):
            return big_uminus(a, b, sign)
        return big_uminus(b, a, change_sign(sign))
    return big_uplus(a, b, a[0])

def big_utimes(a,b,sign):
    r = None
    pos = sign
    for bi in range(1,len(b)):
        p = pos
        pos += "0"
        carry = 0
        for ai in range(1,len(a)):
            n = (ord(a[ai]) - ord('0')) * (ord(b[bi]) - ord('0')) + carry
            carry = n // 10
            n %= 10
            p += chr(n + ord('0'))
        while carry:
            n = carry % 10
            carry //= 10
            p += chr(n + ord('0'))
        if r:
            r = big_uplus(r, p, sign)
        else:
            r = p
    return r

def big_times(a,b):
    if a == "+0" or b == "+0":
        return "+0"
    sign = '+'
    if a[0] != b[0]:
        sign = '-'
    return big_utimes(a,b,sign)

def int_to_big(i):
    if i < 0:
        r = "-"
        i = -i
    else:
        r = "+"
    while True:
        r += chr(ord('0') + i % 10)
        i //= 10
        if i == 0:
            break
    return r

def string_to_big(s):
    if s[0] == '-' or s[0] == '+':
        return s[0] + s[:0:-1]
    return '+' + s[::-1]

def big_to_int(b):
    i = 0
    f = 1
    sign = None
    for c in b:
        if sign is None:
            sign = 1
            if c == '-':
                sign = -1
        else:
            i += f * (ord(c) - ord('0'))
            f *= 10
    return i * sign

def big_check(describe, got, want):
    if big_to_int(got) != want:
        print("FAIL: %s %s != %d" % (describe, big_string(got), want))

def big_test(a,b):
    if a < b:
        t = a
        a = b
        b = t

    big_a = int_to_big(a)
    big_b = int_to_big(b)

    big_check("%d + %d" % (a, b), big_plus(big_a, big_b), a+b)

    big_check("%d - %d" % (a, b), big_minus(big_a, big_b), a-b)

    big_check("%d * %d" % (a, b), big_times(big_a, big_b), a*b)

def randint():
    return random.randrange(10000) - 5000

if True:
    random.seed(12)
    for i in range(20000):
        a = randint()
        b = randint()
        big_test(a,b)
