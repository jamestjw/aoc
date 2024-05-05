"""
This file contains a code attempt for advent of code day 24
"""


import os
import sys
import numpy as np
from functools import cache


def dir2offset(e):
    return [(0, 1), (0, -1), (1, 0), (-1, 0)][list("><v^").index(e)]


def offset2dir(e):
    return "><v^"[[(0, 1), (0, -1), (1, 0), (-1, 0)].index(e)]


def input2gridelem(e):
    match e:
        case "#":
            return None
        case ".":
            return []
        case e:
            return [dir2offset(e)]


def print_grid(g):
    def elem2outstr(e):
        match e:
            case None:
                return "#"
            case []:
                return "."
            case [e]:
                return offset2dir(e)
            case [*e]:
                return str(len(e))

    tmp = [list(map(elem2outstr, e)) for e in g]

    print("\n".join(list(map(lambda x: "".join(x), tmp))))


@cache
def simulate_for_time(time):
    assert time >= 0

    if time == 0:
        return grid
    else:
        prev = simulate_for_time(time - 1)

        # Set up res
        res = np.full_like(prev, None)
        for i in range(num_rows):
            for j in range(num_cols):
                if prev[i][j] is not None:
                    res[i][j] = []

        # Move blizzard
        for i in range(num_rows):
            for j in range(num_cols):
                if prev[i][j] is not None:
                    for di, dj in prev[i][j]:
                        new_i = i + di
                        new_j = j + dj

                        if 0 <= new_i < num_rows and 0 <= new_j < num_cols:
                            # wrap around
                            if prev[new_i][new_j] is None:
                                if new_i == num_rows - 1:
                                    new_i = 1
                                elif new_i == 0:
                                    new_i = num_rows - 2
                                elif new_j == num_cols - 1:
                                    new_j = 1
                                elif new_j == 0:
                                    new_j = num_cols - 2
                                else:
                                    raise Exception

                                pass

                            res[new_i][new_j].append((di, dj))
                        else:
                            # this should never happen
                            raise Exception
        return res


def part1():
    # Queue of time and location
    Q = [(1, start)]

    seen = {(1, start)}

    while len(Q) != 0:
        data = Q.pop(0)

        time, coords = data
        i, j = coords

        g = simulate_for_time(time)

        for offset in [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]:
            di, dj = offset

            new_i = i + di
            new_j = j + dj

            if 0 <= new_i < num_rows and 0 <= new_j < num_cols:
                if g[new_i][new_j] == []:
                    if (new_i, new_j) == end:
                        print(time)
                        return

                    else:
                        if (time + 1, (new_i, new_j)) in seen:
                            continue
                        seen |= {(time + 1, (new_i, new_j))}
                        Q.append((time + 1, (new_i, new_j)))


def part2():
    # Queue of time, trip number, and location
    Q = [(1, 0, start)]

    seen = {(1, 0, start)}

    while len(Q) != 0:
        data = Q.pop(0)

        time, trip_no, coords = data
        i, j = coords

        g = simulate_for_time(time)

        for offset in [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]:
            di, dj = offset

            new_i = i + di
            new_j = j + dj

            if 0 <= new_i < num_rows and 0 <= new_j < num_cols:
                if g[new_i][new_j] == []:
                    if (new_i, new_j) == end and trip_no == 2:
                        print(time)
                        return

                    else:
                        new_trip_no = trip_no
                        if (new_i, new_j) == end and trip_no == 0:
                            new_trip_no = 1
                        if (new_i, new_j) == start and trip_no == 1:
                            new_trip_no = 2
                        new_key = (time + 1, new_trip_no, (new_i, new_j))

                        if new_key in seen:
                            continue
                        else:
                            seen |= {new_key}
                            Q.append(new_key)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    my_tests = open(sys.argv[1], "r", encoding="utf-8").read().splitlines()

    grid = np.array(list(map(list, my_tests)))
    start = tuple(np.argwhere(grid == ".")[0])
    end = tuple(np.argwhere(grid == ".")[-1])

    vf = np.vectorize(input2gridelem)
    grid = vf(grid)

    num_rows = len(grid)
    num_cols = len(grid[0])

    part1()
    part2()
