import sys
from collections import defaultdict


file = open(sys.argv[1]).read()
start, mappings_data = file.split("\n\n")
mappings = {
    p[0]: p[1] for pair in mappings_data.splitlines() if (p := pair.split(" -> "))
}


def do(iters):
    pair_counter = defaultdict(lambda: 0)

    for i in range(len(start) - 1):
        pair_counter[start[i : i + 2]] += 1

    for i in range(iters):
        tmp_dict = defaultdict(lambda: 0)
        for key, count in pair_counter.items():
            mapping = mappings[key]
            tmp_dict[key[0] + mapping] += count
            tmp_dict[mapping + key[1]] += count
        pair_counter = tmp_dict

    final_counter = defaultdict(lambda: 0)

    for k, count in pair_counter.items():
        final_counter[k[0]] += count
        final_counter[k[1]] += count

    # First and last characters are not double counted,
    # so we compensate for it
    final_counter[start[0]] += 1
    final_counter[start[-1]] += 1

    # Divide by 2 as the characters are double counted
    print((max(final_counter.values()) - min(final_counter.values())) // 2)


do(10)
do(40)
