import sys
import math
import copy
from functools import reduce
from itertools import permutations

numbers = list(map(eval, open(sys.argv[1]).read().splitlines()))


# Return index of possible explosion
def may_explode(number):
    def helper(n: int | list, prev_index):
        match n:
            case [int(e1), int(e2)]:
                return prev_index
            case list():
                return next(
                    iter(
                        res
                        for i, e in enumerate(n)
                        if (res := helper(e, prev_index + [i])) and len(res) == 4
                    ),
                    prev_index,
                )
            case _:
                return []

    return helper(number, [])


def may_split(number):
    def helper(n: int | list, prev_index):
        match n:
            case int(e) if e >= 10:
                return prev_index
            case list():
                return next(
                    iter(
                        res
                        for i, e in enumerate(n)
                        if (res := helper(e, prev_index + [i])) and len(res) != 0
                    ),
                    [],
                )
            case _:
                return []

    return helper(number, [])


def snailfish_reduce(number):
    if (explode_indices := may_explode(number)) and len(explode_indices) == 4:
        number = copy.deepcopy(number)
        i, j, k, l = explode_indices
        sublist = number[i][j][k]
        left, right = sublist[l]

        sublist[l] = 0  # replace with zero

        def add_to_left(num, indices, to_add):
            if len(indices) == 0:
                return False
            l = indices[-1]
            sublist = reduce(lambda acc, e: acc[e], indices[:-1], num)

            for l2 in range(l - 1, -1, -1):
                if 0 <= l2 < len(sublist):
                    if isinstance(sublist[l2], int):
                        sublist[l2] += to_add
                        return True
                    else:
                        if add_to_left(sublist[l2], [len(sublist[l2])], to_add):
                            return True
            return add_to_left(num, indices[:-1], to_add)

        def add_to_right(num, indices, to_add):
            if len(indices) == 0:
                return False
            l = indices[-1]
            sublist = reduce(lambda acc, e: acc[e], indices[:-1], num)

            for l2 in range(l + 1, len(sublist)):
                if 0 <= l2 < len(sublist):
                    if isinstance(sublist[l2], int):
                        sublist[l2] += to_add
                        return True
                    else:
                        if add_to_right(sublist[l2], [-1], to_add):
                            return True
            return add_to_right(num, indices[:-1], to_add)

        add_to_left(number, explode_indices, left)
        add_to_right(number, explode_indices, right)

        return snailfish_reduce(number)
    elif (split_indices := may_split(number)) and len(split_indices) != 0:
        number = copy.deepcopy(number)
        parent = reduce(lambda acc, e: acc[e], split_indices[:-1], number)
        split_candidate = parent[split_indices[-1]]
        parent[split_indices[-1]] = [
            math.floor(split_candidate / 2),
            math.ceil(split_candidate / 2),
        ]

        return snailfish_reduce(number)
    else:
        return number


def snailfish_addition(l1, l2):
    return snailfish_reduce([l1, l2])


def magnitude(n):
    match n:
        case int(n):
            return n
        case [e1, e2]:
            return 3 * magnitude(e1) + 2 * magnitude(e2)
        case _:
            raise Exception


res = reduce(snailfish_addition, numbers)

# Part 1
print(magnitude(res))


# Part 2
print(max(magnitude(snailfish_addition(n1, n2)) for n1, n2 in permutations(numbers, 2)))
