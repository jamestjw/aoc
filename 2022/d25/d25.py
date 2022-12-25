"""
This file contains a code attempt for advent of code day 25
"""
def base10_to_n(num, base):
    if num == 0:
        return [0]
    digits = []
    while num:
        digits.append(int(num % base))
        num //= base
    return digits[::-1]


def snafu2int(s):
    res = 0
    for i, l in enumerate(list(s)[::-1]):
        match l:
            case "=":
                v = -2
            case "-":
                v = -1
            case _:
                v = int(l)
        res += (5**i) * v
    return res


def int2snafu(i):
    p = 0
    while True:
        m = [2 * 5**i for i in range(p)]
        if sum(m) >= i:
            break
        p += 1
    diff_digits = [0] + base10_to_n(sum(m) - i, 5)
    digits = [2 for _ in range(p)]
    res = [x - y for x, y in zip(digits, diff_digits)]

    def snafuify(x):
        match x:
            case -1:
                return "-"
            case -2:
                return "="
            case e:
                return str(e)

    return "".join(map(snafuify, res))


if __name__ == "__main__":
    # lines = open("smol.txt").read().splitlines()
    lines = open("input.txt").read().splitlines()
    s = sum(list(map(snafu2int, lines)))

    part1 = int2snafu(s)
    part2 = 0

    print(f"Answer part1 : {part1}")
    print(f"Answer part2 : {part2}")
