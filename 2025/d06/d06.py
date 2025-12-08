import math

lines = open(0).read().splitlines()
grid = [line.split() for line in lines]
transposed = list(zip(*grid))
pt1 = 0

for row in transposed:
    inp, operation = row[:-1], row[-1]
    if operation == "*":
        pt1 += math.prod([int(i) for i in inp])
    else:
        pt1 += sum([int(i) for i in inp])

operators = lines[-1]
operator_indices = [i for i, c in enumerate(operators) if c != " "]

pt2 = 0
for lo, hi in zip(operator_indices, operator_indices[1:] + [len(operators) + 1]):
    operator = operators[lo]
    grid = []
    for l in lines[:-1]:
        grid.append(list(l[lo : hi - 1]))
    nums = list(map(lambda l: int("".join(l)), zip(*grid)))
    if operator == "*":
        pt2 += math.prod([int(i) for i in nums])
    else:
        pt2 += sum([int(i) for i in nums])

print(pt1, pt2)
