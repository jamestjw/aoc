import sys
import math
import re
from collections import defaultdict
from itertools import zip_longest


def blockwise(t, size=2, fillvalue=None):
    it = iter(t)
    return zip_longest(*[it] * size, fillvalue=fillvalue)


file = open(sys.argv[1]).read()
state, program = file.strip().split("\n\n")

a, b, c = list(map(int, re.findall(r"\d+", state)))
program = list(map(int, re.findall(r"\d+", program)))
outs = []


def operand_to_val(i):
    match i:
        case 0 | 1 | 2 | 3:
            return i
        case 4:
            return a
        case 5:
            return b
        case 6:
            return c
        case _:
            raise Exception

idx = 0
while True:
    vals = program[idx:idx+2]
    if len(vals) != 2: break

    op, operand = vals
    match op:
        case 0:
            a = int(a / (2 ** (operand_to_val(operand))))
        case 1:
            b = b ^ operand
        case 2:
            b = operand_to_val(operand) % 8
        case 3:
            if a:
                idx = operand
                continue
        case 4:
            b = b^c
        case 5:
            outs.append(str(operand_to_val(operand) % 8))
        case 6:
            b = int(a / (2 ** (operand_to_val(operand))))
        case 7:
            c = int(a / (2 ** (operand_to_val(operand))))
        case _:
            raise Exception
    idx += 2
print(",".join(outs))
