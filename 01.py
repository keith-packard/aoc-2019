#!/usr/bin/snek

def fuel(mass):
    f = mass // 3 - 2
    if f < 0:
        return 0
    return f

def allfuel(mass):
    total = 0
    while True:
        f = fuel(mass)
        if f == 0:
            break
        total += f
        mass = f
    return total

def fuels():
    total = 0
    alltotal = 0
    count = 0
    while True:
        i = input("mass? ")
        if not i:
            break
        mass = int(i)
        count += 1
        total += fuel(mass)
        alltotal += allfuel(mass)
    print("count %d total %d alltotal %d" % (count, total, alltotal))

fuels()
