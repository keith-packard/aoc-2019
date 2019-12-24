#!/usr/bin/snek

def abs(a):
    if a < 0:
        return -a
    return a

def gcd(a,b):
    a = abs(a)
    b = abs(b)
    while True:
        if a == 0:
            return b
        if b == 0:
            return a
        t = b % a
        b = a
        a = t

def read():
    y = 0
    a = []
    while True:
        line = input()
        if line == 'done' or line == None:
            break
        for x in range(len(line)):
            if line[x] == '#':
                a += [(x,y)]
        y += 1
    return a

def blocks(s, a, b):
    if a == b:
        return False
    if a == s:
        return False
    adx = a[0] - s[0]
    ady = a[1] - s[1]
    ag = gcd(adx, ady)
    bdx = b[0] - s[0]
    bdy = b[1] - s[1]
    bg = gcd(bdx, bdy)
#    print("a %d,%d (%d,%d) b %d,%d (%d,%d)" % (adx, ady, adx/ag, ady/ag, bdx, bdy, bdx/bg, bdy/bg))
    if adx/ag == bdx/bg and ady/ag == bdy/bg:
        if ag < bg:
            return True
    return False

def blocked(station, asteroid, field):
    for a in field:
        if a != asteroid and blocks(station, a, asteroid):
#            print("%r blocks %r" % (a, asteroid))
            return True
    return False

def unblocked(station, field):
    result = 0
    for u in field:
        if u != station and not blocked(station, u, field):
            result += 1
    return result

def swap(field, i, j):
    t = field[i]
    field[i] = field[j]
    field[j] = t

def qsort(a, p, r):
    if p >= r:
        return

    # partition
    pivot = p + random.randrange(p-r)

    swap(a, pivot, r)

    x = a[r]
    q = p
    for j in range(p, r):
        if x[2] > a[j][2] or (x[2] == a[j][2] and x[3] > a[j][3]):
            swap(a, q, j)
            q += 1
    swap(a, q, r)
    qsort(a, p, q-1)
    qsort(a, q+1, r)

def sort(field, station):
    with_angle = []

    # Add angle to each element
    for f in field:
        if f == station:
            continue
        dx = f[0] - station[0]
        dy = f[1] - station[1]
        angle = math.atan2(dy, dx) / math.pi * 180
        # rotate by 90 degrees so that 0 is 'up'
        #
        angle += 90
        if angle < 0:
            angle += 360
        with_angle += [(f[0], f[1], angle, math.sqrt(dx*dx + dy*dy))]

    qsort(with_angle, 0, len(with_angle) - 1)
    return with_angle

def best(field):
    max_see = 0
    max_pos = None
    for s in field:
        u = unblocked(s, field)
#        print("from %r see %r" % (s, u))
        if u > max_see:
            max_see = u
            max_pos = s
    return (max_pos, max_see)

def vaporize(a, count):
    angle = None
    i = 0
    while True:
        save = []
        while len(a) > 0:
            if a[0][2] == angle:
                save += [a[0]]
            else:
                i += 1
                print("%d: %r" % (i, a[0]))
                if i == count:
                    return a[0]
            angle = a[0][2]
            del a[0]
        a = save

field = read()

b = best(field)

print("best", b)

with_angle = sort(field, b[0])

print("200th", vaporize(with_angle, 200))

exit(0)
