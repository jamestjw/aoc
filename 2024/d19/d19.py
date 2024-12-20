import sys
from functools import cache

file = open(sys.argv[1]).read()
patterns, targets = file.strip().split("\n\n")
patterns, targets = patterns.split(", "), targets.splitlines()


@cache
def solve(target: str) -> int:
    if target == "":
        return 1
    return sum([solve(target[len(p) :]) for p in patterns if target.startswith(p)])


print(len(list(filter(solve, targets))))
print(sum(solve(t) for t in targets))
