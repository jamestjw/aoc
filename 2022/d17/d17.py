"""
This file contains a code attempt for advent of code day 17
"""

import numpy as np
import itertools

X_MIN = 0
X_MAX = 6

shapes = [
    """
  @@@@ 
""",
    """
   @   
  @@@  
   @   
""",
    """
    @  
    @  
  @@@  
""",
    """
  @    
  @    
  @    
  @    
""",
    """
  @@   
  @@   
""",
]
shapes = [list(map(list, shape.strip("\n").split("\n")))[::-1] for shape in shapes]

for shape in shapes:
    for row in shape:
        assert len(row) == X_MAX + 1

offset = {
    ">": (1, 0),
    "<": (-1, 0),
}

# Return false if should stop
def move(grid, to_move, offset):
    x_delta, y_delta = offset
    going_down = y_delta != 0
    coords = [(x + x_delta, y + y_delta) for x, y in to_move]

    if not all([0 <= x <= 6 for x, y in coords]):
        return True, to_move  # return unchanged coords if we hit a wall

    for (x, y) in coords:
        if grid[y, x] != ".":
            return not going_down, to_move

    return True, coords


if __name__ == "__main__":
    raw_text = open("smol.txt", "r", encoding="utf-8").read().strip()
    raw_text = open("input.txt", "r", encoding="utf-8").read().strip()
    wind = itertools.cycle(raw_text)
    shape_cycle = itertools.cycle(shapes)

    spawn_y_offset = 4  # spawn this many units above highest rock
    spawn_x_offset = 2  # this many units from the left wall

    highest_each_col = [0 for _ in range(X_MAX + 1)]
    highest_rock_y = 0

    SIMUL_SIZE = 4660

    grid = np.full((SIMUL_SIZE * 4, 7), ".")
    grid[0] = "#"

    for i in range(SIMUL_SIZE):
        next_shape = next(shape_cycle)

        nested_points = [
            [
                (x, y + spawn_y_offset + highest_rock_y)
                for x, c in enumerate(row)
                if c == "@"
            ]
            for y, row in enumerate(next_shape)
        ]
        points = list(itertools.chain(*nested_points))

        ok = True
        while ok:
            next_wind_offset = offset[next(wind)]
            ok, points = move(grid, points, next_wind_offset)
            ok, points = move(grid, points, (0, -1))  # go down

        for x, y in points:
            grid[y, x] = "#"
            highest_each_col[x] = max(y, highest_each_col[x])

        highest_rock_y = max(highest_each_col)

        # if highest_rock_y >= 5083:
        #     break

    print(
        "\n".join(["".join(row) for row in grid[: highest_rock_y + 1][::-1]]),
        file=open("output.txt", "w"),
    )

    part1 = highest_rock_y

    print(f"Answer part1 : {part1} Blocks used: {i+1}")
