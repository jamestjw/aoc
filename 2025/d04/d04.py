inp = open(0).read().splitlines()
grid = {complex(i, j): c for i, row in enumerate(inp) for j, c in enumerate(row)}
adjacent = [1, -1, 1j, -1j, 1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j]


def find_removable(grid):
    return [
        coords
        for coords, v in grid.items()
        if v == "@" and sum([grid.get(coords + d) == "@" for d in adjacent]) < 4
    ]


def remove_all(grid):
    removed = []
    while to_remove := find_removable(grid):
        removed += to_remove
        for r in to_remove:
            grid.pop(r)
    return removed


print(len(find_removable(grid)))
print(len(remove_all(grid)))
