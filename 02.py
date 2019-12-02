#!/usr/bin/snek

orig_program = []
program = []

def eval(ip):
    global program
    opcode = program[ip]
    if opcode == 1:
        op1 = program[ip+1]
        op2 = program[ip+2]
        op3 = program[ip+3]
        program[op3] = program[op1] + program[op2]
        return True
    elif opcode == 2:
        op1 = program[ip+1]
        op2 = program[ip+2]
        op3 = program[ip+3]
        program[op3] = program[op1] * program[op2]
        return True
    elif opcode == 99:
        return False
    else:
        return False

def run(noun, verb):
    global program, orig_program
    ip = 0
    program = orig_program[:]
    program[1] = noun
    program[2] = verb
    while eval(ip):
        ip += 4
    print("noun %d verb %d 100 * noun + verb %d output %d" % (noun, verb, 100 * noun + verb, program[0]))
    return program[0]

def index(s,c):
    i = 0
    for ch in s:
        if ch == c:
            return i
        i += 1
    return -1

def scanline(line):
    global program
    while line:
        i = index(line, ',')
        if i >= 0:
            val = int(line[:i])
            line = line[i+1:]
        else:
            val = int(line)
            line = None
        if len(program) > 27:
            assert program[27] == 27
        program += [val]

def read():
    global program
    while True:
        line = input("> ")
        if not line:
            break
        scanline(line)
    print("program %d" % (program,))

def search(target):
    global program
    for noun in range(100):
        for verb in range(100):
            if run(noun, verb) == target:
                return

read()
orig_program = program[:]
run(12, 2)
search(19690720)
