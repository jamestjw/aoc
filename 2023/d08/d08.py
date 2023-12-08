from itertools import cycle
from math import lcm
import re


inp_lines = open("input.txt").read().splitlines()
directions = inp_lines[0]
strPattern = re.compile(r"\w+")
mapStrs = list(map(strPattern.findall, inp_lines[2:]))
maps = {l[0]: (l[1], l[2]) for l in mapStrs}


def timeToZ(start):
    curr = start

    steps = 0

    for direction in cycle(directions):
        if curr.endswith("Z"):
            yield (steps, curr)
        curr = maps[curr]["LR".index(direction)]
        steps += 1


print(next(timeToZ("AAA"))[0])

currs = list(filter(lambda x: x.endswith("A"), maps.keys()))
currIterators = list(map(timeToZ, currs))

res = list(map(next, currIterators))
print(lcm(*[r[0] for r in res]))
