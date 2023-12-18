import sys
import math
from collections import defaultdict
from queue import PriorityQueue

file = open(sys.argv[1]).read().split("\n")
grid = [[int(e) for e in row] for row in file]
max_i, max_j = len(grid), len(grid[0])
goal = max_i - 1, max_j - 1
start = 0, 0


def turn_left(coords):
    match coords:
        case (1, 0):
            return (0, 1)
        case (-1, 0):
            return (0, -1)
        case (0, 1):
            return (-1, 0)
        case (0, -1):
            return (1, 0)
        case _:
            raise Exception


def turn_right(coords):
    match coords:
        case (1, 0):
            return (0, -1)
        case (-1, 0):
            return (0, 1)
        case (0, 1):
            return (1, 0)
        case (0, -1):
            return (-1, 0)
        case _:
            raise Exception


# lo: min count before turning
# hi: max count before turning
def dijkstra(grid, src, dest, lo, hi):
    # tuple of coords, direction, and repeat count
    dist = defaultdict(lambda: math.inf)

    Q = PriorityQueue()
    
    for e in [(0, src, (0, 1), 0), (0, src, (1, 0), 0)]:
        dist[e[1:]] = 0
        Q.put(e)

    while Q:
        curr_distance, (curr_i, curr_j), direction, count = Q.get_nowait()

        if (curr_i, curr_j) == dest:
            if count >= lo:
                print(curr_distance)
                break
            else:
                continue

        next_directions = []

        if lo <= count:
            next_directions += [turn_left(direction), turn_right(direction)]
        if count < hi:
            next_directions.append(direction)

        for d in next_directions:
            next_count = count + 1 if d == direction else 1
            next_i, next_j = v = curr_i + d[0], curr_j + d[1]

            if not (0 <= next_i < len(grid) and 0 <= next_j < len(grid[0])):
                continue

            next_key = (v, d, next_count)
            alt = curr_distance + grid[next_i][next_j]

            if alt < dist[next_key]:
                dist[next_key] = alt
                Q.put_nowait((alt,) + next_key)


dijkstra(grid, start, goal, 0, 3)
dijkstra(grid, start, goal, 4, 10)
