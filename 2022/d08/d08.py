"""
This file contains a code attempt for advent of code day 8
"""
# Indices of stuff that are in sorted order
def visible_indices(l):
    m = "0"
    return [i for i, e in enumerate(l) if e > m and (m := max(m, e))]

def scenic_score(grid, i, j, max_i, max_j):
    me = grid[i][j]
    score = 1

    for (x_offset, y_offset) in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        x, y = i, j
        s = 0
        while True:
            x += x_offset
            y += y_offset
            if not (x >= 0 and x < max_i) or not (y >= 0 and y < max_j):
                break
            s += 1
            if grid[x][y] >= me:
                break
        score *= s
    return score

if __name__ == "__main__":
    data = open(0).read().splitlines()
    transposed = [list(x) for x in zip(*data)]

    num_rows = len(data)
    num_cols = len(data[0])

    from_left = [(i, j) for i, row in enumerate(data) for j in visible_indices(row)]
    from_right = [(i, num_cols - j - 1) for i, row in enumerate(data) for j in visible_indices(row[::-1])]
    from_top = [(i, j) for j, col in enumerate(transposed) for i in visible_indices(col)]
    from_btm = [(num_rows - i - 1, j) for j, col in enumerate(transposed) for i in visible_indices(col[::-1])]

    outer = [(i, j) for i in range(num_cols) for j in range(num_cols) if i * j == 0]

    visible = set(from_left + from_right + from_top + from_btm + outer)

    part1 = len(visible)
    part2 = max(scenic_score(data, i, j, num_rows, num_cols) for i, j in visible)

    print(f"Answer part1 : {part1}")
    print(f"Answer part2 : {part2}")
