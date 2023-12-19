from math import prod
import sys
import re

workflowsStr, partsStr = open(sys.argv[1]).read().strip().split("\n\n")

workflows = dict()

for workflow in workflowsStr.split("\n"):
    name = workflow.split("{")[0]
    details = workflow[len(name) + 1 : -1]
    operations = details.split(",")

    instructions = []

    for s in operations:
        match list(filter(None, re.split(r"(\w+|\d+)", s))):
            case [varname, op, num, _colon, jumpTo] if op in ("<", ">"):
                instructions.append((varname, op, int(num), jumpTo))
            case [default]:
                instructions.append(default)
            case _:
                raise Exception

    workflows[name] = instructions


parts = [
    {s[0]: int(s[1]) for kv in p[1:-1].split(",") if (s := kv.split("="))}
    for p in partsStr.split("\n")
]


accessible_from = []
todolist = [("in", {c: (0, 4001) for c in "xmas"})]


while todolist:
    curr, running_constraints = todolist.pop()
    instrs = workflows[curr]

    for instr in instrs:
        match instr:
            case (vname, op, num, jumpTo):
                constraints_copy = running_constraints.copy()
                if op == ">":
                    constraints_copy[vname] = (
                        max(constraints_copy[vname][0], num),
                        constraints_copy[vname][1],
                    )  # add x > n
                    running_constraints[vname] = (
                        running_constraints[vname][0],
                        min(running_constraints[vname][1], num + 1),
                    )  # add x <= n, i.e. x < n + 1
                elif op == "<":
                    constraints_copy[vname] = (
                        constraints_copy[vname][0],
                        min(constraints_copy[vname][1], num),
                    )  # add x < n
                    running_constraints[vname] = (
                        max(running_constraints[vname][0], num - 1),
                        running_constraints[vname][1],
                    )  # add x >= n, i.e. x > n - 1
                if jumpTo == "A":
                    accessible_from.append(constraints_copy)
                elif jumpTo == "R":
                    pass
                else:
                    todolist.append((jumpTo, constraints_copy))
            case "A":
                accessible_from.append(running_constraints)
            case "R":
                pass
            case default:
                todolist.append((default, running_constraints))


valid_ranges = [d for d in accessible_from if all(v1 < v2 for (v1, v2) in d.values())]

print(
    sum(
        sum(pd.values())
        for pd in parts
        if any(all(e1 < pd[l] < e2 for l, (e1, e2) in c.items()) for c in valid_ranges)
    )
)

print(
    sum(
        prod([e2 - e1 - 1 for (e1, e2) in constraint.values()])
        for constraint in valid_ranges
    )
)
