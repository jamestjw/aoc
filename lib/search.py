from collections import defaultdict
from queue import PriorityQueue
import math


class Grid:
    def get(self, coords):
        raise NotImplementedError()

    def is_valid(self, coords):
        raise NotImplementedError()

    def get_offset(self, coords, offset):
        return self.get((coords[0] + offset[0], coords[1] + offset[1]))

    def neighbors(self, coords):
        raise NotImplementedError()

    def move(self, coords, offset):
        return coords[0] + offset[0], coords[1] + offset[1]


class BaseGrid(Grid):
    # Whether or not diagonal movement is allowed
    def __init__(self, grid, diagonal=False):
        self.grid = grid
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        if diagonal:
            self.directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    def get(self, coords):
        return self.grid[coords[0]][coords[1]]

    def is_valid(self, coords):
        return 0 <= coords[0] < len(self.grid) and 0 <= coords[1] < len(self.grid[0])

    def move(self, coords, offset):
        return coords[0] + offset[0], coords[1] + offset[1]

    def neighbors(self, coords):
        res = []
        for direction in self.directions:
            new_coords = self.move(coords, direction)
            if self.is_valid(new_coords):
                res.append(new_coords)
        return res


def djikstra(grid: Grid, dest):
    cost_dict = defaultdict(lambda: math.inf)

    q = PriorityQueue()
    q.put_nowait((grid.get(dest), dest))

    while not q.empty():
        cost, coords = q.get_nowait()

        for neighbor in grid.neighbors(coords):
            new_cost = cost + grid.get(neighbor)
            if new_cost < cost_dict[neighbor]:
                cost_dict[neighbor] = new_cost
                q.put_nowait((new_cost, neighbor))

    return cost_dict


def manhattan(src, dest):
    return abs(src[0] - dest[0]) + abs(src[1] - dest[1])


def astar(grid: Grid, dest, heuristic=manhattan):
    cost_dict = defaultdict(lambda: math.inf)

    q = PriorityQueue()
    q.put_nowait((grid.get(dest), dest))

    while not q.empty():
        cost, coords = q.get_nowait()

        for neighbor in grid.neighbors(coords):
            new_cost = (
                cost
                + grid.get(neighbor)
                + heuristic(neighbor, dest)
                - heuristic(coords, dest)
            )
            if new_cost < cost_dict[neighbor]:
                cost_dict[neighbor] = new_cost
                q.put_nowait((new_cost, neighbor))

    return cost_dict
