import sys
import re
from functools import cache


file = open(sys.argv[1]).read()
inp_lines = file.splitlines()

numPat = re.compile(r"\d+")
hashPat = re.compile(r"#+")
data = list(map(lambda x: x.split()[0], inp_lines))
numbers = list(map(lambda x: list(map(int, numPat.findall(x.split()[1]))), inp_lines))


def gen_permutationsCountCache(data, numbers) -> int:
    @cache
    def helper(damaged: tuple[int], inp: str) -> int:
        if len(damaged) == 0:
            return int(all(s != "#" for s in inp))
        elif len(inp) == 0:
            return int(len(damaged) == 0)

        match inp[0]:
            case ".":
                return helper(damaged, inp[1:])
            case "#":
                damageCount = damaged[0]
                strHead = inp[:damageCount]

                if damageCount > len(inp):
                    return 0
                elif all(s == "#" or s == "?" for s in strHead):
                    if damageCount == len(inp):
                        # Proceed
                        return helper(damaged[1:], "")
                    elif damageCount > len(inp):
                        # More damage than input
                        return 0  # no good
                    else:
                        match inp[damageCount]:
                            case "#":
                                # More damages in input than we require
                                return 0  # no good
                            case "." | "?":
                                # Good, continue processing but consume
                                # the lookahead character
                                return helper(damaged[1:], inp[damageCount + 1 :])
                            case _:
                                raise Exception  # Impossible

                elif any(s == "." for s in strHead):
                    return 0
                else:
                    raise Exception
            case "?":
                # Try making it a '.' or '#'
                return helper(damaged, inp[1:]) + helper(damaged, "#" + inp[1:])
            case _:
                raise Exception  # Impossible

    return helper(tuple(numbers), data)


print(sum(gen_permutationsCountCache(d, n) for d, n in zip(data, numbers)))
print(
    sum(
        gen_permutationsCountCache("?".join([d] * 5), n * 5)
        for d, n in zip(data, numbers)
    )
)
