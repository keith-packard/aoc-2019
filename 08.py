#!/usr/bin/snek

string = input()
string_pos = 0

def getc():
    global string_pos, string
    while string_pos < len(string):
        c = string[string_pos]
        string_pos += 1
        if '0' <= c and c <= '9':
            return c
    return None

def ungetc():
    global string_pos
    string_pos -= 1

def at_end():
    if getc() is None:
        return True
    ungetc()

layer_width = 25
layer_height = 6
layer_size = layer_width * layer_height

def read_layer():
    layer = ""
    for i in range(layer_size):
        layer += getc()
    return layer

def match(layer, c):
    count = 0
    for l in layer:
        if c == l:
            count += 1
    return count

def find_layer():
    min_zeros = None
    min_ones_times_twos = None
    while not at_end():
        layer = read_layer()
        zeros = match(layer, '0')
        if min_zeros is None or zeros < min_zeros:
            min_zeros = zeros
            ones = match(layer, '1')
            twos = match(layer, '2')
            min_ones_times_twos =  ones * twos
    return min_ones_times_twos

def merge(over, under):
    result = ""
    for i in range(len(over)):
        if over[i] == '2':
            result += under[i]
        else:
            result += over[i]
    return result

def merge_layers():
    result = None
    while not at_end():
        under = read_layer()
        if result:
            result = merge(result, under)
        else:
            result = under
    return result

def show_image(layer):
    for y in range(layer_height):
        for x in range(layer_width):
            if layer[y * layer_width + x] == '0':
                print(' ', end='')
            else:
                print(layer[y * layer_width + x], end='')
        print()

print("part a", find_layer())
string_pos = 0
show_image(merge_layers())
