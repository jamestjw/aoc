import sys
from collections import defaultdict
from queue import PriorityQueue
import math


file = open(sys.argv[1]).read()
grid = [list(map(int, line)) for line in file.splitlines()]

start = (0, 0)
dest = (len(grid) - 1, len(grid[0]) - 1)


class Grid:
    def get(self, coords):
        raise NotImplementedError()

    def is_valid(self, coords):
        raise NotImplementedError()

    def get_offset(self, coords, offset):
        return self.get((coords[0] + offset[0], coords[1] + offset[1]))

    def move(self, coords, offset):
        return coords[0] + offset[0], coords[1] + offset[1]


class BaseGrid(Grid):
    def __init__(self, grid):
        self.grid = grid

    def get(self, coords):
        return self.grid[coords[0]][coords[1]]

    def is_valid(self, coords):
        return 0 <= coords[0] < len(self.grid) and 0 <= coords[1] < len(self.grid[0])

    def move(self, coords, offset):
        return coords[0] + offset[0], coords[1] + offset[1]


class BigGrid(BaseGrid):
    def get(self, coords):
        x, y = coords
        scale_x, scale_y = x // len(self.grid), y // len(self.grid[0])
        value = self.grid[x % len(self.grid)][y % len(self.grid[0])] + scale_x + scale_y
        while value > 9:
            value -= 9
        return value

    def is_valid(self, coords):
        return (
            0 <= coords[0] < len(self.grid) * 5
            and 0 <= coords[1] < len(self.grid[0]) * 5
        )


def djikstra(grid: Grid, dest):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # No diagonal movement

    cost_dict = defaultdict(lambda: math.inf)

    q = PriorityQueue()
    q.put_nowait((grid.get(dest), dest))

    while not q.empty():
        cost, coords = q.get_nowait()
        i, j = coords

        for direction in directions:
            new_coords = grid.move(coords, direction)
            if grid.is_valid(new_coords):
                new_cost = cost + grid.get(new_coords)
                if new_cost < cost_dict[new_coords]:
                    cost_dict[new_coords] = new_cost
                    q.put_nowait((new_cost, new_coords))

    return cost_dict

def manhattan(src,dest):
    return abs(src[0]-dest[0]) + abs(src[1]-dest[1])

def astar(grid: Grid, dest):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # No diagonal movement

    cost_dict = defaultdict(lambda: math.inf)

    q = PriorityQueue()
    q.put_nowait((grid.get(dest), dest))

    while not q.empty():
        cost, coords = q.get_nowait()
        i, j = coords

        for direction in directions:
            new_coords = grid.move(coords, direction)
            if grid.is_valid(new_coords):
                new_cost = cost + grid.get(new_coords) + manhattan(new_coords,dest) - manhattan(coords,dest)
                if new_cost < cost_dict[new_coords]:
                    cost_dict[new_coords] = new_cost
                    q.put_nowait((new_cost, new_coords))

    return cost_dict

# Part 1

cost_dict = djikstra(BaseGrid(grid), dest)
print(cost_dict[start] - grid[start[0]][start[1]])

# cost_dict = astar(BaseGrid(grid), dest)
# print(cost_dict[start] - grid[start[0]][start[1]] - manhattan(start,dest))

# Part 2

new_dest = dest[0] + 4 * len(grid), dest[1] + 4 * len(grid[0])
cost_dict = djikstra(BigGrid(grid), new_dest)
print(cost_dict[start] - grid[start[0]][start[1]])

# cost_dict = astar(BigGrid(grid), new_dest)
# print(cost_dict[start] - grid[start[0]][start[1]] - manhattan(start, new_dest))
