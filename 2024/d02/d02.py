import sys

file = open(sys.argv[1]).read()

inp_lines = [list(map(int, l.split())) for l in file.splitlines()]


def is_ok(done: list[int], already_failed: bool, remaining: list[int]):
    if not remaining:
        return True
    else:
        num, nums = remaining[0], remaining[1:]
        match done:
            case [prev, *rest] if not (0 < abs(num - prev) <= 3):
                return not already_failed and (
                    is_ok(rest, True, remaining) or is_ok(done, True, nums)
                )
            case [prev, prevprev, *rest]:
                if (prev - prevprev > 0) != (num - prev > 0):
                    return not already_failed and (
                        is_ok([prevprev, *rest], True, remaining)
                        or is_ok(done, True, nums)
                        or is_ok([prev, *rest], True, remaining)
                    )

        return is_ok([num] + (done), already_failed, nums)


def part1(nums):
    return is_ok([], True, nums)


def part2(nums):
    return is_ok([], False, nums)


print(len(list(filter(part1, inp_lines))))
print(len(list(filter(part2, inp_lines))))
