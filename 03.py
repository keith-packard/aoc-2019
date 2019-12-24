#!/usr/bin/snek

# Given a string motion description, compute a tuple with (dx, dy)

def move(elt):
    dist = int(elt[1:])
    if elt[0] == 'R':
        return (dist, 0)
    if elt[0] == 'L':
        return (-dist, 0)
    if elt[0] == 'U':
        return (0, dist)
    if elt[0] == 'D':
        return (0, -dist)
    assert(false)

def min(a,b):
    if a < b:
        return a
    return b

def max(a,b):
    if a > b:
        return a
    return b

def abs(a):
    if a < 0:
        return -a
    return a

# Given two points, generate a line
# ((x1, y1), (x2, y2))
# such that x1 <= x2 and y1 <= y2

def line(pt1, pt2):
    return ((min(pt1[0], pt2[0]),
             min(pt1[1], pt2[1])),
            (max(pt1[0], pt2[0]),
             max(pt1[1], pt2[1])))

#
# Return true if a line is vertical, else horizontal

def vertical(l):
    return l[0][0] == l[1][0]

# l1 is vertical. return whether it's x value is in l2's x range

def xbetween(l1, l2):
    return l2[0][0] <= l1[0][0] and l1[0][0] <= l2[1][0]

# l1 is horizontal. return whether it's y value is in l2's y range

def ybetween(l1, l2):
    return l2[0][1] <= l1[0][1] and l1[0][1] <= l2[1][1]

# Return the intersection of two lines as a tuple, None if they
# do not intersect

def intersect(l1, l2):
    v1 = vertical(l1)
    v2 = vertical(l2)
    if v1 == v2:
        if v1:
            if l1[0][0] == l2[0][0] and l1[0][1] <= l2[1][1] and l2[0][1] <= l1[1][1]:
                return (l1[0][0], max(l1[0][1], l2[0][1]))
        else:
            if l1[0][1] == l2[0][1] and l1[0][0] <= l2[1][0] and l2[0][0] <= l1[1][0]:
                return (max(l1[0][0], l2[0][0]), l1[0][1])
    else:
        if v1:
            if xbetween(l1, l2) and ybetween(l2, l1):
                return (l1[0][0], l2[0][1])
        else:
            if xbetween(l2, l1) and ybetween(l1, l2):
                return (l2[0][0], l1[0][1])
    return None

def get_path():
    pos = (0, 0)
    path=[pos]
    while True:
        line = input()
        if line == "done":
            break
        m = move(line)
        pos = (pos[0] + m[0], pos[1] + m[1])
        path += [pos]
    return path

def line_len(l):
    return abs(l[0][0] - l[1][0]) + abs(l[0][1] - l[1][1])

def intersects(patha, pathb):
    intersects = []
    preva = None
    lena = 0
    for posa in patha:
        if preva:
            linea = line(preva, posa)
            prevb = None
            lenb = 0
            for posb in pathb:
                if prevb:
                    lineb = line(prevb, posb)
                    i = intersect(linea, lineb)
                    if i and (i[0] != 0 or i[1] != 0):
                        plena = line_len(line(preva, i))
                        plenb = line_len(line(prevb, i))
                        i = i + (lena + plena, lenb + plenb)
                        print("line a", linea, "line b", lineb, "i", i)
                        intersects += [i]
                    lenb += line_len(lineb)
                prevb = posb
            lena += line_len(linea)
        preva = posa
    return intersects

def manhatten(pos):
    return abs(pos[0]) + abs(pos[1])

def min_point(points):
    m = None
    for p in points:
        d = manhatten(p)
        if not m or d < manhatten(m):
            m = p
    return (manhatten(m), m )

def min_index(points):
    m = None
    for p in points:
        if not m or (p[2] + p[3]) < (m[2] + m[3]):
            m = p
    return (m[2] + m[3], m)

patha = get_path()
pathb = get_path()

i = intersects(patha, pathb)

print("min intersect", min_point(i))
print("min index", min_index(i))
