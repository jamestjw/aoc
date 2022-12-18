"""
This file contains a code attempt for advent of code day 18
"""

import numpy as np

directions = [
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
]

if __name__ == "__main__":
    my_tests = open(f"input.txt", "r", encoding="utf-8").read().splitlines()
    # my_tests = open(f"smol.txt", "r", encoding="utf-8").read().splitlines()
    points = set([tuple(map(int, x.split(","))) for x in my_tests])

    min_x = min(x for x, _, _ in points)
    max_x = max(x for x, _, _ in points)
    min_y = min(y for _, y, _ in points)
    max_y = max(y for _, y, _ in points)
    min_z = min(x for _, _, x in points)
    max_z = max(x for _, _, x in points)

    grid = np.full((max_x + 1, max_y + 1, max_z + 1), False)

    for coord in points:
        grid[coord] = True

    def valid(x, y, z):
        return max_x >= x >= 0 and max_y >= y >= 0 and 0 <= z <= max_z

    bubbles_candidates = set()
    all_grid_coords = set()
    # find air bubbles
    for x in range(max_x + 1):
        for y in range(max_y + 1):
            for z in range(max_z + 1):
                all_grid_coords.add((x, y, z))
                if (x, y, z) in points:
                    continue
                out = False

                for offset in directions:
                    if out:
                        break
                    curr = (x, y, z)
                    while True:
                        curr = tuple(map(sum, zip(curr, offset)))
                        if curr in points:  # if we hit another point
                            break  # not good
                        elif not valid(*curr):
                            # we hit a border, thats good!
                            out = True
                            break

                if not out:
                    bubbles_candidates.add((x, y, z))

    non_bubbles_candidates = all_grid_coords - points - bubbles_candidates
    actual_bubbles = set()

    # a true bubble will not be adjacent to a non bubble
    for coord in bubbles_candidates:
        ok = True
        for offset in directions:
            new = tuple(map(sum, zip(coord, offset)))
            if new in non_bubbles_candidates:
                ok = False
                break
        if ok:
            actual_bubbles.add(coord)

    score1 = 0
    score2 = 0

    for coord in points:
        for offset in directions:
            new = tuple(map(sum, zip(coord, offset)))
            if new not in points:
                score1 += 1
                if new not in actual_bubbles:
                    score2 += 1

    print(f"Answer part1 : {score1}")
    print(f"Answer part2 : {score2}")
