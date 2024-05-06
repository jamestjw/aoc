import sys
from functools import reduce

file = open(sys.argv[1]).read().splitlines()
patterns = [l.split(" | ")[0].split() for l in file]
problems = [l.split(" | ")[1].split() for l in file]

count = 0
for problem in problems:
    for p in problem:
        if len(p) in (2, 4, 3, 7):
            count += 1

print("Part 1: ",count)

def decode_pattern(pattern):
    #  aaaa 
    # b    c
    # b    c
    #  dddd 
    # e    f
    # e    f
    #  gggg 

    #  0000
    # 1    2
    # 1    2
    #  3333
    # 4    5
    # 4    5
    #  6666
    pattern = [set(e) for e in pattern]

    mapping = dict()

    # Find one
    one = pattern.pop(next(i for i, p in enumerate(pattern) if len(p) == 2))
    seven = pattern.pop(next(i for i, p in enumerate(pattern) if len(p) == 3))
    four = pattern.pop(next(i for i, p in enumerate(pattern) if len(p) == 4))
    eight = pattern.pop(next(i for i, p in enumerate(pattern) if len(p) == 7))

    lenfives = [e for e in pattern if len(e) == 5]

    mapping[0] = list(seven - one)[0]

    leftside_candidates = []

    for c in reduce(lambda x, y: x | y, lenfives):
        if sum(c in s for s in lenfives) == 1:
            leftside_candidates.append(c)
    
    mapping[1] = leftside_candidates.pop(next(i for i,c in enumerate(leftside_candidates) if c in four))
    mapping[4] = leftside_candidates.pop(0)
    for c in four:
        if c not in one and c != mapping[1]:
            mapping[3] = c
    
    fg_candidates = []

    for candidate in lenfives:
        tmp = candidate - {mapping[0], mapping[1], mapping[3]}
        if len(tmp) == 2:
            fg_candidates.extend(tmp)

    mapping[5] = fg_candidates.pop(next(i for i,c in enumerate(fg_candidates) if c in one))
    mapping[6] = fg_candidates.pop(0)
    mapping[2] = next(e for e in one if e not in mapping.values())

    def ids2set(ids):
        return {mapping[i] for i in ids}

    two = ids2set([0,2,3,4,6])
    three = ids2set([0,2,3,5,6])
    five = ids2set([0,1,3,5,6])
    six = ids2set([0,1,3,4,5,6])
    zero = eight - {mapping[3]}
    nine = eight - {mapping[4]}

    res = [zero, one, two, three, four, five, six, seven, eight, nine]

    return res

total = 0

for pattern, problem in zip(patterns, problems):
    mapping = decode_pattern(pattern)
    digits = []

    for p in problem:
        digits.append(str(next(i for i, e in enumerate(mapping) if set(p) == e)))

    total += int("".join(digits))

print("Part 2: ",total)
