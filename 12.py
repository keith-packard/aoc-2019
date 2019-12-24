#!/usr/bin/snek

def sgn(x):
    if x < 0: return -1
    if x > 0: return 1
    return 0

def gravity(a,b):
    for i in range(3):
        d = sgn(b[i] - a[i])
        a[i+3] += d
        b[i+3] -= d

def velocity(a):
    for i in range(3):
        a[i] += a[i+3]

def all_gravity(moons):
    for i in range(len(moons)):
        for j in range(i+1, len(moons)):
            gravity(moons[i], moons[j])

def all_velocity(moons):
    for i in range(len(moons)):
        velocity(moons[i])

def motion(moons):
    all_gravity(moons)
    all_velocity(moons)

def abs(a):
    if a < 0:
        return -a
    return a

def potential(moon):
    return abs(moon[0]) + abs(moon[1]) + abs(moon[2])

def kinetic(moon):
    return abs(moon[3]) + abs(moon[4]) + abs(moon[5])

def energy_moon(moon):
    return potential(moon) * kinetic(moon)

def energy_moons(moons):
    sum = 0
    for m in moons:
        print('energy for %r' % (m,))
        sum += energy_moon(m)
    return sum

def is_num(c):
    if '0' <= c and c <= '9':
        return True
    if '-' == c:
        return True
    return False

def read_moon():
    line = input()
    if line == 'done' or line is None:
        return None
    moon = []
    p = 0
    for i in range(3):
        while not is_num(line[p]):
            p += 1
        q = p + 1
        while is_num(line[q]):
            q += 1
        moon += [int(line[p:q])]
        p = q + 1
    return moon + [0,0,0]

def read_moons():
    moons = []
    while True:
        moon = read_moon()
        if moon is None:
            break
        moons += [moon]
    return moons

def print_moon(moon):
    print("pos=<x=%d, y=%d, z=%d>, vel=<x=%d, y=%d, z=%d>" % moon)

def print_moons(label, moons):
    print(label)
    for m in moons:
        print_moon(m)

def step_moons(moons, steps):
    for s in range(steps):
        motion(moons)
    print_moons("After %d steps:" % steps, moons)
    print("Energy: %d" % energy_moons(moons))

moons = read_moons()
print_moons("start", moons)

step_moons(moons, 1000)
