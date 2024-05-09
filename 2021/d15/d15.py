import sys

# To import lib
sys.path.insert(0, "../..")
from lib.search import *


file = open(sys.argv[1]).read()
grid = [list(map(int, line)) for line in file.splitlines()]

start = (0, 0)
dest = (len(grid) - 1, len(grid[0]) - 1)


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


# Part 1

cost_dict = djikstra(BaseGrid(grid), dest)
print(cost_dict[start] - grid[start[0]][start[1]])

# Part 2

new_dest = dest[0] + 4 * len(grid), dest[1] + 4 * len(grid[0])
cost_dict = djikstra(BigGrid(grid), new_dest)
print(cost_dict[start] - grid[start[0]][start[1]])
