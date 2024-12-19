import sys
import re
from itertools import product

# from z3 import *


file = open(sys.argv[1]).read()
state, program = file.strip().split("\n\n")

a, b, c = list(map(int, re.findall(r"\d+", state)))
program = list(map(int, re.findall(r"\d+", program)))
outs = []

idx = 0
while True:
    vals = program[idx : idx + 2]
    if len(vals) != 2:
        break

    op, operand = vals
    combo = [(0), (1), (2), (3), a, b, c, None][operand]
    match op:
        case 0:
            a = int(a / (2 ** (combo)))
        case 1:
            b = b ^ operand
        case 2:
            b = combo % 8
        case 3:
            if a:
                idx = operand
                continue
        case 4:
            b = b ^ c
        case 5:
            outs.append(str(combo % 8))
        case 6:
            b = int(a / (2 ** (combo)))
        case 7:
            c = int(a / (2 ** (combo)))
        case _:
            raise Exception
    idx += 2

print(",".join(outs))


for init_a_coefs in product("01234567", repeat=16):
    init_a = a = int("".join(init_a_coefs), 8)
    b=c=0
    outs = []
    idx = 0
    while True:
        vals = program[idx : idx + 2]
        if len(vals) != 2:
            break

        op, operand = vals
        combo = [(0), (1), (2), (3), a, b, c, None][operand]
        match op:
            case 0:
                a = int(a / (2 ** (combo)))
            case 1:
                b = b ^ operand
            case 2:
                b = combo % 8
            case 3:
                if a:
                    idx = operand
                    continue
            case 4:
                b = b ^ c
            case 5:
                outs.append(str(combo % 8))
            case 6:
                b = int(a / (2 ** (combo)))
            case 7:
                c = int(a / (2 ** (combo)))
            case _:
                raise Exception
        idx += 2

    if outs == program:
        print(init_a_coefs, init_a)
        break
