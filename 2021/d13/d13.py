import sys
from functools import reduce


file = open(sys.argv[1]).read()
file_dots, file_folds = file.split("\n\n")
dots = [tuple(map(int, pair.split(","))) for pair in file_dots.splitlines()]
folds = [i.split()[2].split("=") for i in file_folds.splitlines()]


def vertical_fold(dots, fold_along):
    upper = [coords for coords in dots if coords[1] < fold_along]
    below = [coords for coords in dots if coords[1] > fold_along]

    for x, y in below:
        upper.append((x, 2 * fold_along - y))

    return list(set(upper))


def transpose(dots: list):
    return [(j, i) for i, j in dots]


def horizontal_fold(dots, fold_along):
    return transpose(vertical_fold(transpose(dots), fold_along))


def do_fold(dots, fold):
    axis, fold_along = fold
    match axis:
        case "x":
            return horizontal_fold(dots, int(fold_along))
        case "y":
            return vertical_fold(dots, int(fold_along))
        case _:
            raise Exception


## Part1

print(len(do_fold(dots, folds[0])))

## Part2

final_dots = reduce(lambda dots, fold: do_fold(dots, fold), folds, dots)

max_x = max([x for x, y in final_dots])
max_y = max([y for x, y in final_dots])


for y in range(max_y + 1):
    for x in range(max_x + 1):
        if (x, y) in final_dots:
            print("#", end="")
        else:
            print(".", end="")
    print("")
