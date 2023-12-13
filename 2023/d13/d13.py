import sys
import numpy as np

file = open(sys.argv[1]).read()
patterns = file.split("\n\n")


def do_pattern(pattern_str: str, acceptance_fn) -> int:
    grid = np.array([[c for c in line] for line in pattern_str.split("\n")])
    num_rows, num_cols = grid.shape

    score = 0

    for j in range(1, num_cols):
        left = grid[:, :j]
        right = grid[:, j:]

        if left.shape > right.shape:
            left = left[:, -(right.shape[1]) :]
        elif right.shape > left.shape:
            right = right[:, : left.shape[1]]

        if acceptance_fn(left, right[:, ::-1]):
            score += j
            break

    for i in range(1, num_rows):
        top = grid[:i, :]
        bottom = grid[i:, :]

        if top.shape > bottom.shape:
            top = top[-(bottom.shape[0]) :, :]
        elif bottom.shape > top.shape:
            bottom = bottom[: top.shape[0], :]

        if acceptance_fn(top, bottom[::-1, :]):
            score += i * 100
            break

    return score


print(sum(list(map(lambda x: do_pattern(x, lambda x, y: (x == y).all()), patterns))))
print(
    sum(list(map(lambda x: do_pattern(x, lambda x, y: np.sum(x != y) == 1), patterns)))
)
