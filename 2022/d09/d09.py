"""
This file contains a code attempt for advent of code day 9
"""


def is_adjacent(x1, y1, x2, y2):
    return abs(x2 - x1) <= 1 and abs(y1 - y2) <= 1


# x1,y1 for the head
def offset2adjacent(x1, y1, x2, y2):
    xoffset = (0 if x1 == x2 else 1) if (x1 - x2) >= 0 else -1
    yoffset = (0 if y1 == y2 else 1) if (y1 - y2) >= 0 else -1
    return xoffset, yoffset


if __name__ == "__main__":
    my_tests = open(0, "r", encoding="utf-8").read().splitlines()
    my_tests = [x.split() for x in my_tests]

    tail_visited = [(0, 0)]
    coords = [(0, 0) for _ in range(10)]

    for d, times in my_tests:
        offset = [(1, 0), (-1, 0), (0, 1), (0, -1)]["RLUD".index(d)]
        for _ in range(int(times)):
            coords[0] = tuple(map(lambda i, j: i + j, coords[0], offset))
            for i, tail_coords in enumerate(coords[1:]):
                if is_adjacent(*coords[i], *tail_coords): break
                tail_offset = offset2adjacent(*coords[i], *tail_coords)
                coords[i + 1] = tuple(map(lambda i, j: i + j, tail_coords, tail_offset))
                if i == len(coords) - 2:
                    tail_visited.append(coords[i + 1])

    print(f"tail visited : {len(set(tail_visited))}")
