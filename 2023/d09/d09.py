import re


def do1(numList: list[int], reverse=False) -> int:
    resultList = [numList[::-1] if reverse else numList]
    while any(e != 0 for e in resultList[-1]):
        last = resultList[-1]
        resultList.append([e2 - e1 for e1, e2 in zip(last[:-1], last[1:])])

    resultList = resultList[::-1]

    for i, l in enumerate(resultList):
        if i == 0:
            l.append(0)
        else:
            l.append(l[-1] + resultList[i - 1][-1])
    return resultList[-1][-1]


inp_lines = open("input.txt").read().splitlines()
numPattern = re.compile(r"-?\d+")
numStrs = list(map(numPattern.findall, inp_lines))
nums = [list(map(int, l)) for l in numStrs]

# 1969958987 1068
print(sum(list(map(lambda x: do1(x, False), nums))))
print(sum(list(map(lambda x: do1(x, True), nums))))
