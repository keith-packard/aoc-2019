#!/usr/bin/snek

orbits = []

def count_orbits(p):
    count = 0
    while True:
        for o in orbits:
            if o[1] == p:
                count += 1
                p = o[0]
                break
        else:
            break
    return count

def path(p):
    ph = []
    while True:
        for o in orbits:
            if o[1] == p:
                p = o[0]
                ph += [p]
                break
        else:
            break
    return ph

def common(p1, p2):
    o1 = len(p1) - 1
    o2 = len(p2) - 1
    while o1 >= 0 and o2 >= 0 and p1[o1] == p2[o2]:
        o1 -= 1
        o2 -= 1
    return p1[o1+1:]

def split_orbit(line):
    found = False
    for i in range(len(line)):
        if line[i] == ')':
            return (line[:i], line[i+1:])
    return None
    
def read_orbits():
    global orbits
    orbits = []
    while  True:
        line = input('')
        if line is None or line == 'done':
            break
        orbits += [split_orbit(line)]
    return orbits

def total_orbits():
    total = 0
    for o in orbits:
        total += count_orbits(o[1])
    return total
    

read_orbits()
#print("total orbits %d" % total_orbits())

you_path = path('YOU')
san_path = path('SAN')
com_path = common(you_path, san_path)
print("common %r" % (com_path,))
total_len = len(you_path) + len(san_path) - len(com_path) * 2
print("distance %d" % total_len)
