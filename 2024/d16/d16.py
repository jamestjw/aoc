import math
import sys
from collections import defaultdict
from itertools import chain
from queue import PriorityQueue
from typing import Tuple

file = open(sys.argv[1]).read()
grid = [list(line) for line in file.strip().splitlines()]

start = next(
    (i, j) for i, row in enumerate(grid) for j, val in enumerate(row) if val == "S"
)
dst = next(
    (i, j) for i, row in enumerate(grid) for j, val in enumerate(row) if val == "E"
)

CoordsDirPair = Tuple[Tuple[int, int], Tuple[int, int]]


class DirectionalGrid:
    def __init__(self, grid):
        self.grid = grid
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def flip(self, direction):
        return -direction[0], -direction[1]

    def neighbors(self, coords: CoordsDirPair) -> list[Tuple[int, int]]:
        here, d = coords
        res = []
        for direction in self.directions:
            if direction != d and direction != self.flip(direction):
                res.append((here, direction))
        new_coords = self.move(coords, d)
        if self.is_valid(new_coords):
            res.append(new_coords)
        return res

    def cost(self, src, dest):
        (c1, d1), (c2, d2) = src, dest
        if d1 == d2:
            return 1
        elif c1 == c2:
            return 1000
        raise ValueError

    def move(self, coords: CoordsDirPair, offset) -> CoordsDirPair:
        return (coords[0][0] + offset[0], coords[0][1] + offset[1]), offset

    def is_valid(self, coords: CoordsDirPair):
        x, y = coords[0]
        return (
            0 <= x < len(self.grid)
            and 0 <= y < len(self.grid[0])
            and self.grid[x][y] != "#"
        )


def djikstra(grid, dest, initial_cost=0):
    cost_dict = defaultdict(lambda: math.inf)
    journey = defaultdict(lambda: [])
    journey[dest].append([dest])

    q = PriorityQueue()
    q.put_nowait((initial_cost, dest))

    while not q.empty():
        cost, coords = q.get_nowait()
        hist = journey[coords]

        for neighbor in grid.neighbors(coords):
            new_cost = cost + grid.cost(coords, neighbor)
            if new_cost < cost_dict[neighbor]:
                cost_dict[neighbor] = new_cost
                journey[neighbor] = [j + [neighbor] for j in hist]
                q.put_nowait((new_cost, neighbor))
            elif new_cost == cost_dict[neighbor]:
                journey[neighbor] += [
                    j + [neighbor]
                    for j in hist
                    if j + [neighbor] not in journey[neighbor]
                ]

    return cost_dict, journey


res1, journeys = djikstra(DirectionalGrid(grid), (dst, (1, 0)))
# res2, journey2=(djikstra(DirectionalGrid(grid), (dst, (0,-1))))

print(res1[(start, (0, -1))])
# print(res2[(start, (0, -1))])

print(len(set(c for c, _ in list(chain.from_iterable(journeys[(start, (0, -1))])))))
