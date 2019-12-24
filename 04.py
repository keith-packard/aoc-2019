#!/usr/bin/snek

def digits(a):
    d = [a % 10]
    a //= 10
    while a:
        d = [a % 10] + d
        a //= 10
    return d
    
def has_double(ds):
    prev = None
    for d in ds:
        if prev == d:
            return True
        prev = d
    return False

def has_double_not_triple(ds):
    prev = None
    count = 0
    for d in ds:
        if prev == d:
            count += 1
        else:
            if count == 1:
                return True
            count = 0
        prev = d
    if count == 1:
        return True
    return False

def increasing(ds):
    prev = None
    for d in ds:
        if prev and prev > d:
            return False
        prev = d
    return True

def match_a(a):
    ds = digits(a)
    return has_double(ds) and increasing(ds)

def matches_a(s, e):
    m = 0
    for a in range(s, e + 1):
        if match_a(a):
            m += 1
    return m

def match_b(a):
    ds = digits(a)
    return has_double_not_triple(ds) and increasing(ds)

def matches_b(s, e):
    m = 0
    for a in range(s, e + 1):
        if match_b(a):
            m += 1
    return m

print("matches_a", matches_a(372037, 905157))
print("matches_b", matches_b(372037, 905157))
