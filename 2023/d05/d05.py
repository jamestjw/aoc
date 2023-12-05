import re
from collections import defaultdict
from functools import reduce

inp_lines = open("input.txt", "r", encoding="utf-8").read().split("\n\n")
# inp_lines = open("smol.txt", "r", encoding="utf-8").read().split("\n\n")

pattern = re.compile(r"(\d+) (\d+) (\d+)")
seeds = list(map(int, re.findall(r"\d+", inp_lines[0])))
map_data = list(map(lambda x: pattern.findall(x), inp_lines[1:]))
map_data = [[(int(x), int(y), int(z)) for (x, y, z) in d] for d in map_data]


# Need this to ensure that the input map covers the entire domain
def expand_map(map_data: list[tuple[int, int, int]]):
    map_data = sorted(map_data, key=lambda x: x[1])

    end = 0
    res = []
    for d in map_data:
        res.append(d)

        if d[1] > end:
            res[-1] = (end, end, d[1] - end)
            res.append(d)

        end = d[1] + d[2]
    return res


def compose_map2(
    map_data1: list[tuple[int, int, int]], map_data2: list[tuple[int, int, int]]
):
    map_data1 = map_data1.copy()

    res = []

    for d, s, r in map_data1:
        map_data2_copy = map_data2.copy()
        # i need to find what this maps to in map_data2

        for d2, s2, r2 in map_data2:
            if r == 0 or not (s2 <= d < s2 + r2):
                continue
            if d + r < s2:
                fill_interval = min(r, s2 - d)

                res.append((d, s, fill_interval))
                r -= fill_interval
                s += fill_interval
                d += fill_interval

            if r == 0:
                break

            assert d >= s2

            offset = d - s2

            interval_size = min(r2 - offset, r)

            res.append((d2 + offset, s, interval_size))
            r -= interval_size
            s += interval_size
            d += interval_size

        if r != 0:
            res.append((d, s, r))

    # handle tail end
    max_val = max(d + r for d, s, r in map_data1)

    for d, s, r in map_data2:
        if max_val <= s:
            interval = r - (max_val - s)
            res.append((d + (max_val - s), max_val, interval))
            max_val += interval

    return expand_map(res)


def get_seed(seed, m: list[tuple[int, int, int]]) -> int:
    for d, s, r in m:
        if s <= seed < s + r:
            return d + (seed - s)
    return seed  # identity map all the way!?


def get_seed_from_range(seed: tuple[int, int], m: list[tuple[int, int, int]]) -> int:
    seed_start, seed_range = seed

    # Start iterating by lowest destination
    m = sorted(m, key=lambda x: x[0])

    for d, s, r in m:
        # seed   -------
        # map  -----------
        # Just return the map of lowest seed
        if s <= seed_start < s + r:
            return seed_start - s + d

        # seed   -------
        # map      -----------
        # Just return lowest thing that the seed could map to
        elif seed_start <= s < seed_start + seed_range:
            return d
    # If we get here, then we can map seed_start to the identity map
    return seed_start


expanded_maps = [expand_map(m) for m in map_data]
composed_map = reduce(compose_map2, expanded_maps[1:], expanded_maps[0])

seed_ranges = list(zip(*[iter(seeds)] * 2))
pt1 = min([get_seed(seed, composed_map) for seed in seeds])
pt2 = min([get_seed_from_range(seed, composed_map) for seed in seed_ranges])

# 825516882 136096660
print(pt1, pt2)
