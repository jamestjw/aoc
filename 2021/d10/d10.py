import sys
from functools import reduce

programs = open(sys.argv[1]).read().splitlines()

opening = ("[", "(", "{", "<")
closing = ("]", ")", "}", ">")
illegal_points = {")": 3, "]": 57, "}": 1197, ">": 25137}
completion_points = {")": 1, "]": 2, "}": 3, ">": 4}


# Returns first invalid
def check(program: str):
    stack = []
    for c in program:
        if c in opening:
            stack.append(c)
        elif c in closing:
            expected = opening[closing.index(c)]
            if stack[-1] == expected:
                stack.pop(-1)
            else:
                return c
        else:
            raise Exception  # impossible

    return None


def complete(program: str):
    stack = []
    for c in program:
        if c in opening:
            stack.append(c)
        elif c in closing:
            expected = opening[closing.index(c)]
            if stack[-1] == expected:
                stack.pop(-1)
            else:
                raise Exception
        else:
            raise Exception  # impossible

    return [closing[opening.index(c)] for c in stack[::-1]]


res = list(map(check, programs))

print(sum([illegal_points[r] for r in res if r]))

incompletes = [p for p in programs if not check(p)]

completion_scores = [
    reduce(lambda acc, e: acc * 5 + completion_points[e], completion, 0)
    for completion in map(complete, incompletes)
]

print(sorted(completion_scores)[len(completion_scores) // 2])
