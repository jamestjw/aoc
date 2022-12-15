"""
This file contains a code attempt for advent of code day 15
"""

from collections import defaultdict
import re
import sys
import itertools

if __name__ == "__main__":
    # targ = 10
    # upperbound = 20
    # rows = open(f"smol.txt", "r", encoding="utf-8").read().splitlines()

    targ = 2000000
    upperbound = 4000000
    rows = open(f"input.txt", "r", encoding="utf-8").read().splitlines()
    
    data = [list(map(int, re.findall("-?\d+", x))) for x in rows]

    occupied = defaultdict(list)
    obstacles = []
    for x1, y1, x2, y2 in data:
        obstacles += [(x2, y2), (x1, y1)]
        dist = abs(x2 - x1) + abs(y2 - y1)
        for y in range(-dist, dist + 1):
            remaining = dist - abs(y)
            occupied[y + y1].append((x1 - remaining, x1 + remaining))

    print(len(set(filter(lambda x: (x, targ) not in obstacles, itertools.chain(*[range(s,e+1) for s,e in occupied[targ]])))))

    for y in range(upperbound + 1):
        intervals = sorted(occupied[y])
        s1, e1 = intervals[0]
        for s2, e2 in intervals[1:]:
            if s2 > e1 + 1:
                print(f"{e1 + 1, y} => {(e1 + 1) * 4000000 + y}")
                sys.exit(0)
            else:
                e1 = max(e1, e2)
