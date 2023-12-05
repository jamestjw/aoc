import re
from functools import reduce

inp_lines = open("input.txt", "r", encoding="utf-8").read().split("\n\n")
pattern = re.compile(r"(\d+) (\d+) (\d+)")
seeds = list(map(int, re.findall(r"\d+", inp_lines[0])))
map_data = [
    [(int(x), int(y), int(z)) for (x, y, z) in d]
    for d in list(map(lambda x: pattern.findall(x), inp_lines[1:]))
]


def map_seed_range(
    seeds: list[tuple[int, int]], m: list[tuple[int, int, int]]
) -> list[tuple[int, int]]:
    m = sorted(m, key=lambda x: x[1])  # check lower maps first
    res = []
    for seed_start, seed_range in seeds:
        for dest, source, r in m:
            if seed_range != 0 and source <= seed_start < source + r:
                interval = min(seed_range, source + r - seed_start)

                res.append((dest + (seed_start - source), interval))
                seed_range -= interval
                seed_start += interval

        if seed_range != 0:
            res.append((seed_start, seed_range))  # identity map
    return res


seed_ranges = list(zip(*[iter(seeds)] * 2))

p1_ranges = [reduce(map_seed_range, map_data, [(seed, 1)]) for seed in seeds]
p2_ranges = [
    reduce(map_seed_range, map_data, [seed_range]) for seed_range in seed_ranges
]

print(min(r[0] for l in p1_ranges for r in l))
print(min(r[0] for l in p2_ranges for r in l))
