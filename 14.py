#!/usr/bin/snek

import math

def is_num(c):
    if '0' <= c and c <= '9':
        return True
    if '-' == c:
        return True
    return False

def is_let(c):
    if 'a' <= c and c <= 'z':
        return True
    if 'A' <= c and c <= 'Z':
        return True
    return False


def read_line():
    line = input()
    if line == 'done' or line is None:
        return None
    state = 0
    p = 0
    r = []
    while p < len(line):
        while not is_num(line[p]):
            p += 1
        q = p + 1
        while is_num(line[q]):
            q += 1
        num = int(line[p:q])

        p = q
        while not is_let(line[p]):
            p += 1
        q = p + 1
        while q < len(line) and is_let(line[q]):
            q += 1

        let = line[p:q]
        r += [(num, let)]

        p = q
    return [r[:-1], r[-1:]]

def read_lines():
    reactions = []
    while  True:
        r = read_line()
        if r is None:
            break
        reactions += [r]
    return reactions

reactions = read_lines()

def find_eqn(reactions, product):
    for r in reactions:
        if r[1][0][1] == product:
            return r
    return None

def times(terms, count):
    prod = []
    for t in terms:
        prod += [(t[0] * count, t[1])]
    return prod

def plus(a_s, b_s):
    result = a_s[:]
    for b in b_s:
        for ri in range(len(result)):
            a = result[ri]
            if b[1] == a[1]:
                result[ri] = (a[0] + b[0], a[1])
                break
        else:
            result += [b]
    return result

def balance(lhs, rhs):
    li = 0
    ri = 0
    while li < len(lhs) and ri < len(rhs):
        l = lhs[li]
        r = rhs[ri]
        if l[1] == r[1]:
            if l[0] > r[0]:
                lhs[li] = (l[0] - r[0], l[1])
                del rhs[ri]
                li += 1
                ri = 0
            elif r[0] > l[0]:
                rhs[ri] = (r[0] - l[0], r[1])
                del lhs[li]
                ri = 0
            else:
                del rhs[ri]
                del lhs[li]
                ri = 0
        else:
            ri += 1
            if ri == len(rhs):
                ri = 0
                li += 1

def print_terms(t):
    for li in range(len(t) - 1):
        print("%f %s, " % t[li], end='')
    print("%f %s" % t[len(t)-1], end='')

def print_reaction(r):
    print_terms(r[0])
    print(" => ", end='')
    print_terms(r[1])
    print()

def print_reactions(reactions):
    for r in reactions:
        print_reaction(r)

def solve(reactions, nfuel):
    eqn = find_eqn(reactions, 'FUEL')
    lhs = times(eqn[0], nfuel)
    rhs = times(eqn[1], nfuel)
    while True:
        for i in range(len(lhs)):
            need = lhs[i]
            sub = find_eqn(reactions, need[1])
            if sub is not None:
                break
        else:
            break
        get = sub[1][0]
        count = math.ceil(need[0] / get[0])

        add = times(sub[0], count)

        del lhs[i]
        lhs = plus(lhs, add)

        extra = get[0] * count - need[0]
        if extra > 0:
            rhs = plus(rhs, [(extra, need[1])])
        balance(lhs, rhs)
    return lhs[0][0]

def most_for(reactions, max_ore):
    nfuel = 1
    while True:
        n_ore = solve(reactions, nfuel)
        if n_ore == max_ore:
            return nfuel
        if n_ore > max_ore:
            break
        nfuel *= 2
    lo = nfuel // 2
    hi = nfuel
    while lo < hi:
        m = (lo + hi) // 2
        n_ore = solve(reactions, m)
        if n_ore == max_ore:
            return m
        if n_ore > max_ore:
            hi = m
        else:
            lo = m + 1
    if solve(reactions, lo) > max_ore:
        lo -= 1
    return lo
        

#print_reactions(reactions)
#exit(0)
print("ore %f nfuel 1" % solve(reactions, 1))

nfuel = most_for(reactions, 1e12)

print("ore %f nfuel %f" % (1e12, nfuel))
