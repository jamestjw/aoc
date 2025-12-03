import re
from functools import partial


def generate_integers_of_length(n):
    start = 10 ** (n - 1)
    end = (10**n) - 1

    return list(range(start, end + 1))


def is_invalid(limits, candidate):
    return any(lo <= candidate <= hi for lo, hi in limits)


inp = open(0).read().strip()
numbers = list(map(int, re.findall(r"\d+", inp)))
pairs = list(zip(numbers[::2], numbers[1::2]))
limit = max(numbers)
gen_size = len(str(limit)) // 2

pt1_candidates = []
pt2_candidates = set()
for i in range(1, gen_size + 1):
    for c in generate_integers_of_length(i):
        candidate = f"{c}{c}"
        pt1_candidates.append(int(candidate))
        pt2_candidate = candidate

        while len(pt2_candidate) <= len(str(limit)):
            pt2_candidates.add(int(pt2_candidate))
            pt2_candidate += str(c)


print(sum(filter(partial(is_invalid, pairs), pt1_candidates)))
print(sum(filter(partial(is_invalid, pairs), pt2_candidates)))
