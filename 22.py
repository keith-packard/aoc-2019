#!/usr/bin/snek

def deal_into_new_stack(deck):
    return deck[::-1]

def cut(deck, pos):
    if pos == 0:
        return deck
    return deck[pos:] + deck[:pos]

def deal_with_increment(deck, n):
    result = [0] * len(deck)
    for i in range(len(deck)):
        result[(i * n) % len(deck)] = deck[i]
    return result

def make_deck(n):
    deck = [0] * n
    for i in range(n):
        deck[i] = i
    return deck

def do_line(deck, line):
    if line[:3] == 'cut':
        return cut(deck, int(line[4:]))
    if line[:19] == 'deal with increment':
        return deal_with_increment(deck, int(line[20:]))
    if line[:19] == 'deal into new stack':
        return deal_into_new_stack(deck)
    assert False

def get_lines():
    lines = []
    while True:
        line = input()
        if line == 'done' or line is None:
            break
        lines += [line]
    return lines

def do_lines(deck, lines):
    for line in lines:
        deck = do_line(deck, line)
    return deck

def fun_deal_into_new_stack():
    return (-1, -1)

def fun_cut(pos):
    return (1, -pos)

def fun_deal_with_increment(n):
    return (n, 0)

def fun_line(line):
    if line[:3] == 'cut':
        return fun_cut(int(line[4:]))
    if line[:19] == 'deal with increment':
        return fun_deal_with_increment(int(line[20:]))
    if line[:19] == 'deal into new stack':
        return fun_deal_into_new_stack()
    assert False

#
#
#

def inverse(n, l):

    # return n ** (l - 2)

    pow = l - 2
    r = 1
    while pow:
        if pow & 1:
            r = (r * n) % l
        n = (n * n) % l
        pow >>= 1
    return r

#
# g = f⁻¹
#
def fun_invert(f, l):
    #
    # y = f[0] * x + f[1]
    #
    # (y - f[1]) * 
    #
    # y * f[0]⁻¹ - f[1] * f[0]⁻¹
    #
    i = inverse(f[0], l)
    print("inverse of %d is %d (mod %d)" % (f[0], i, l))
    return (i, (-f[1] * i) % l)
    

# g(f(x))
#
# ga * (fa * x + fb) + gb
#
# ga * fa * x + ga * fb + gb
#

def fun_compose(g,f, l):
    return ((g[0] * f[0]) % l, (g[0] * f[1] + g[1]) % l)

def fun_pow(f, n, l):
    r = (1, 0)
    while n > 0:
        if n & 1:
            r = fun_compose(f, r, l)
        f = fun_compose(f,f, l)
        n >>= 1
    return r

def fun_lines(lines, l):
    f = (1, 0)
    for line in lines:
        g = fun_line(line)
        f = fun_compose(g, f, l)

    return f

def eval(f, x, l):
    return (f[0] * x + f[1]) % l

def do_fun(f, deck):
    result = [0] * len(deck)
    for i in range(len(deck)):
        result[eval(f, i, len(deck))] = deck[i]
    return result

def run_fun(deck, lines, n):
    f = fun_lines(lines, len(deck))
    f = fun_pow(f, n, len(deck))
    fi = fun_invert(f, len(deck))
    print("f(x) = %d * x + %d" % f)
    print("fi(x) = %d * x + %d" % fi)
    sdeck = do_fun(f, deck)
    ndeck = do_fun(fi, sdeck)
    assert ndeck == deck
    print(sdeck)

def run_old(deck, lines, n):
    for i in range(n):
        deck = do_lines(deck, lines)
    print(deck)

lines = get_lines()

#run_old(make_deck(11), lines, 997)
#run_fun(make_deck(11), lines, 997)
l = 119315717514047
t = 101741582076661
fi = fun_invert(fun_lines(lines, l), l)
fit = fun_pow(fi, t, l)
p = 2020
s = eval(fit, p, l)
print("pos %d has val %d" % (p, s))
