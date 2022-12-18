"""
This file contains a code attempt for advent of code day 20
"""


import os
import numpy as np

if __name__ == "__main__":
    # input = list(map(int, open(f"smol.txt").read().splitlines()))
    input = list(map(int, open(f"input.txt").read().splitlines()))
    id2int = {i: v for i, v in enumerate(input)}
    data = [i for i in range(len(input))]

    for i in range(len(input)):
        curr_pos = data.index(i)
        data.pop(curr_pos)

        offset = id2int[i]
        new_pos = (curr_pos + offset) % (len(input) - 1)

        data.insert(new_pos, i)

        assert len(data) == len(set(data))

    restored_data = [id2int[e] for e in data]

    zero = restored_data.index(0)
    part1 = sum(restored_data[(zero + i) % len(data)] for i in (1000, 2000, 3000))

    k = 811589153
    id2int2 = {i: v * k for i, v in enumerate(input)}
    data2 = [i for i in range(len(input))]

    for _ in range(10):
        for i in range(len(input)):
            curr_pos = data2.index(i)
            data2.pop(curr_pos)

            offset = id2int2[i]
            new_pos = (curr_pos + offset) % (len(input) - 1)

            data2.insert(new_pos, i)
        print([id2int2[e] for e in data2])

    restored_data2 = [id2int2[e] for e in data2]

    zero2 = restored_data2.index(0)
    part2 = sum(restored_data2[(zero2 + i) % len(data)] for i in (1000, 2000, 3000))
    print([restored_data2[(zero2 + i) % len(data)] for i in (1000, 2000, 3000)])

    print(f"Answer part1 : {part1}")
    print(f"Answer part2 : {part2}")
