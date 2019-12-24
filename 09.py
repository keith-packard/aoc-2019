#!/usr/bin/snek

input_index = 0
input_source = (5,)

def op_input():
    global input_index
    global input_source
    i = input_source[input_index]
    input_index += 1
    return i

def 

def big_add(a,b):
    

def param_mode(opcode, param):
    return (opcode // (10 ** (param + 1))) % 10

def read(program, addr):
    if addr >= len(program):
        return 0
    return program[addr]

def write(program, addr, value):
    if addr >= len(program):
        if  value == 0:
            return
        program += [0] * ((addr + 1) - len(program))
    program[addr] = value

def param(state, opcode, param, op):
    mode = param_mode(opcode, param)
    if mode == 0:
        program = state['program']
        return read(program, op)
    elif mode == 1:
        return op
    elif mode == 2:
        rel_base = state['relative base']
        return read(program, op + rel_base)
    assert False

def addr(state, opcode, param, op):
    mode = param_mode(opcode, param)
    if mode == 0:
        return op
    elif mode == 2:
        rel_base = state['relative base']
        return op + rel_base
    assert False

def eval(state, ip):
    program = state['program']
    print("%d: %d" % (ip, program[ip]), end='')
    opcode = read(program, ip)
    op = opcode % 100
    if op == 1:
        op1 = param(state, opcode, 1, read(program, ip+1))
        op2 = param(state, opcode, 2, read(program, ip+2))
        op3 = addr (state, opcode, 3, read(program, ip+3))
        print(" %d = %d(%d) + %d(%d) (%d)" % (op3, op1, program[ip+1], op2, program[ip+2], op1 + op2))
        write(program, op3, op1 + op2)
        return ip + 4
    elif op == 2:
        op1 = param(state, opcode, 1, read(program, ip+1))
        op2 = param(state, opcode, 2, read(program, ip+2))
        op3 = addr (state, opcode, 3, read(program, ip+3))
        print(" %d = %d(%d) * %d(%d) (%d)" % (op3, op1, program[ip+1], op2, program[ip+2], op1 * op2))
        write(program, op3, op1 * op2)
        return ip + 4
    elif op == 3:
        op1 = addr (state, opcode, 1, read(program, ip+1))
        print(" %d" % op1)
        input = state['input']
        write(program, op1, input[0])
        del input[0]
        return ip + 2
    elif op == 4:
        op1 = param(state, opcode, 1, read(program, ip+1))
        print(" %d" % op1)
        state['output'] = op1
        return ip + 2
    elif op == 5:
        op1 = param(state, opcode, 1, read(program, ip+1))
        op2 = param(state, opcode, 2, read(program, ip+2))
        print(" %d != 0 → %d" % (op1, op2))
        if op1:
            return op2
        else:
            return ip + 3
    elif op == 6:
        op1 = param(state, opcode, 1, read(program, ip+1))
        op2 = param(state, opcode, 2, read(program, ip+2))
        print(" %d == 0 → %d" % (op1, op2))
        if op1 == 0:
            return op2
        else:
            return ip + 3
    elif op == 7:
        op1 = param(state, opcode, 1, read(program, ip+1))
        op2 = param(state, opcode, 2, read(program, ip+2))
        op3 = addr (state, opcode, 3, read(program, ip+3))
        print(" %d = %d(%d) < %d(%d) (%d)" % (op3, op1, program[ip+1], op2, program[ip+2], op1 < op2))
        if op1 < op2:
            write(program, op3, 1)
        else:
            write(program, op3, 0)
        return ip + 4
    elif op == 8:
        op1 = param(state, opcode, 1, read(program, ip+1))
        op2 = param(state, opcode, 2, read(program, ip+2))
        op3 = addr (state, opcode, 3, read(program, ip+3))
        print(" %d = %d(%d) < %d(%d) (%d)" % (op3, op1, program[ip+1], op2, program[ip+2], op1 == op2))
        if op1 == op2:
            write(program, op3, 1)
        else:
            write(program, op3, 0)
        return ip + 4
    elif op == 9:
        op1 = param(state, opcode, 1, read(program, ip+1))
        state['relative base'] += op1
        return ip + 2
    elif op == 99:
#        print(" done")
        return None
    assert False

def run(program, input):
    state = {
        'program' : program[:],
        'input' : input,
        'output' : None,
        'relative base': 0
        }
    ip = 0
    while True:
        ip = eval(state, ip)
        if ip is None:
            break
    return state['output']

def run_amp(program, phase):
    signal = 0
    for p in phase:
        signal = run(program, [p, signal])
    return signal

def add_input(state, input):
    state['input'] += [input]

def run_feedback(state, input):
    add_input(state, input)
    state['output'] = None
    ip = state['ip']
    while state['output'] is None:
        ip = eval(state, ip)
        if not ip:
            return None
    state['ip'] = ip
    return state['output']

def run_loop(program, phase):
    stage = []
    for p in phase:
        stage += [{
            'program': program[:],
            'ip': 0,
            'input': [p]
            }]
    amp = 0
    while stage[0]['ip'] is not None:
        for s in range(len(phase)):
            new_amp = run_feedback(stage[s], amp)
            if not new_amp:
                return amp
            amp = new_amp
    return amp

def opt_loop(program, phase):
    max_amp = 0
    max_phase = None
    while phase:
        amp = run_loop(program, phase)
        if amp is None:
            break
        if amp > max_amp:
            max_amp = amp
            max_phase = phase[:]
        phase = next_perm(phase)
    return (max_amp, max_phase)

def done(state):
    return state['ip'] is None

def index(s,c):
    i = 0
    for ch in s:
        if ch == c:
            return i
        i += 1
    return -1

def scanline(program, line):
    while line:
        i = index(line, ',')
        if i >= 0:
            val = int(line[:i])
            line = line[i+1:]
        else:
            val = int(line)
            line = None
        program += [val]
    return program

def read():
    program = []
    while True:
        line = input('')
        if not line or line == 'done':
            break
        program = scanline(program, line)
#    print("program %r" % (program,))
    return program

def search(target):
    global program
    for noun in range(100):
        for verb in range(100):
            if run(noun, verb) == target:
                show(noun, verb, target)
                return

def next_perm(a):
    k = None
    for i in range(len(a) - 1):
        if a[i] < a[i+1]:
            k = i
    if k is None:
        return None
    l = None
    for i in range(k+1, len(a)):
        if a[k] < a[i]:
            l = i
    t = a[k]
    a[k] = a[l]
    a[l] = t
    left = a[:k+1]
    right = a[:k:-1]
#    print("a %r left %r right %r" % (a, left, right))
    return left + right

def show_perm(a):
    while True:
        print(a)
        a = next_perm(a)
        if not a:
            break

orig_program = read()

def search_amp(program):
    phases = [0,1,2,3,4]
    max_output = 0
    while phases:
        output = run_amp(program, phases)
        if output > max_output:
            print("phases %r output %d" % (phases, output))
            max_output = output
        phases = next_perm(phases)
    return max_output

#output = opt_loop(orig_program, [5,6,7,8,9])
output = opt_loop(orig_program, [5,6,7,8,9])
#output = search_amp(orig_program)
print('output', output)
