#!/usr/bin/snek

orig_program = []
program = []

input_index = 0
input_source = (5,)

def op_input():
    global input_index
    global input_source
    i = input_source[input_index]
    input_index += 1
    return i

def param_mode(opcode, param):
    return (opcode // (10 ** (param + 1))) % 10

def param(opcode, param, op):
    mode = param_mode(opcode, param)
    if mode == 0:
        return program[op]
    elif mode == 1:
        return op
    assert False

def eval(ip):
    global program
    print("%d: %d" % (ip, program[ip]), end='')
    opcode = program[ip]
    op = opcode % 100
    if op == 1:
        op1 = param(opcode, 1, program[ip+1])
        op2 = param(opcode, 2, program[ip+2])
        op3 = program[ip+3]
        print(" %d = %d(%d) + %d(%d) (%d)" % (op3, op1, program[ip+1], op2, program[ip+2], op1 + op2))
        program[op3] = op1 + op2
        return ip + 4
    elif op == 2:
        op1 = param(opcode, 1, program[ip+1])
        op2 = param(opcode, 2, program[ip+2])
        op3 = program[ip+3]
        print(" %d = %d(%d) * %d(%d) (%d)" % (op3, op1, program[ip+1], op2, program[ip+2], op1 * op2))
        program[op3] = op1 * op2
        return ip + 4
    elif op == 3:
        op1 = program[ip+1]
        print(" %d" % op1)
        program[op1] = op_input()
        return ip +  2
    elif op == 4:
        op1 = param(opcode, 1, program[ip+1])
        print(" %d" % op1)
        print('op4', op1)
        return ip + 2
    elif op == 5:
        op1 = param(opcode, 1, program[ip+1])
        op2 = param(opcode, 2, program[ip+2])
        print(" %d != 0 → %d" % (op1, op2))
        if op1:
            return op2
        return ip + 3
    elif op == 6:
        op1 = param(opcode, 1, program[ip+1])
        op2 = param(opcode, 2, program[ip+2])
        print(" %d == 0 → %d" % (op1, op2))
        if op1 == 0:
            return op2
        return ip + 3
    elif op == 7:
        op1 = param(opcode, 1, program[ip+1])
        op2 = param(opcode, 2, program[ip+2])
        op3 = program[ip+3]
        print(" %d = %d(%d) < %d(%d) (%d)" % (op3, op1, program[ip+1], op2, program[ip+2], op1 < op2))
        if op1 < op2:
            program[op3] = 1
        else:
            program[op3] = 0
        return ip  + 4
    elif op == 8:
        op1 = param(opcode, 1, program[ip+1])
        op2 = param(opcode, 2, program[ip+2])
        op3 = program[ip+3]
        print(" %d = %d(%d) < %d(%d) (%d)" % (op3, op1, program[ip+1], op2, program[ip+2], op1 == op2))
        if op1 == op2:
            program[op3] = 1
        else:
            program[op3] = 0
        return ip  + 4
    elif op == 99:
        print(" done")
        return None
    assert False

def run():
    global program, orig_program
    ip = 0
    program = orig_program[:]
    while True:
        ip = eval(ip)
        if ip is None:
            break
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
        program += [val]

def read():
    global program
    while True:
        line = input('')
        if not line or line == 'done':
            break
        scanline(line)
    print("program %r" % (program,))

def search(target):
    global program
    for noun in range(100):
        for verb in range(100):
            if run(noun, verb) == target:
                show(noun, verb, target)
                return

read()
orig_program = program[:]
run()
