import sys

file = open(sys.argv[1]).read()
inp_lines = file.splitlines()
grid = {(i + 1j * j): e for i, row in enumerate(inp_lines) for j, e in enumerate(row)}
max_i, max_j = len(inp_lines), len(inp_lines[1])
start_coords = [k for k, v in grid.items() if v == "S"][0]


## Area of polygon
def triangle(l):
    return (
        abs(
            sum(
                (p1.real * p2.imag) - (p1.imag * p2.real)
                for p1, p2 in zip(l, l[1:] + [l[0]])
            )
        )
        / 2
    )


pipe_compatibility = {
    "|": {-1: ["|", "F", "7"], 1: ["|", "L", "J"]},
    "-": {-1j: ["-", "L", "F"], 1j: ["-", "7", "J"]},
    "L": {-1: ["|", "F", "7"], 1j: ["-", "7", "J"]},
    "J": {-1: ["|", "7", "F"], -1j: ["-", "L", "F"]},
    "7": {1: ["|", "L", "J"], -1j: ["-", "L", "F"]},
    "F": {1: ["|", "L", "J"], 1j: ["-", "7", "J"]},
    "S": {
        -1: ["|", "F", "7"],
        1: ["|", "L", "J"],
        -1j: ["-", "L", "F"],
        1j: ["-", "7", "J"],
    },
}


for _, v in pipe_compatibility.items():
    list(map(lambda x: x.append("S"), v.values()))


def find_valid_next_pipes(curr_loc: complex) -> list[complex]:
    # i, j = curr_loc
    start_pipe = grid[curr_loc]
    res = []
    for delta in (1, -1, 1j, -1j):
        new_loc = curr_loc + delta
        if not (0 <= new_loc.real < max_i and 0 <= new_loc.imag < max_j):
            continue

        pipe = grid[new_loc]
        if pipe in pipe_compatibility[start_pipe].get(delta, []):
            res.append(new_loc)

    return res


def get_main_loop(grid, s_loc):
    path = [s_loc]

    while path[-1] != s_loc or len(path) == 1:
        last_pipe = path[-1]
        next_pipes = find_valid_next_pipes(path[-1])

        match next_pipes:
            case [p1, p2] if last_pipe == s_loc or ((p1 in path) ^ (p2 in path)):
                next_pipe = p1 if p2 in path else p2
                path.append(next_pipe)

            # We are done
            case [p1, p2] if (p1 in path) and (p2 in path):
                break
            case _:
                raise Exception
    return path


def printMainLoop(grid, path):
    for i, row in enumerate(grid):
        for j, e in enumerate(row):
            toPrint = e if (i, j) in path else e
            print(toPrint, end="")
        print("")


# Use polygon area + Pick's theorem to find the number of interior points
path = get_main_loop(grid, start_coords)
perimeter = len(path)

print(int(triangle(path) - perimeter / 2 + 1))
