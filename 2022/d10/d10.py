if __name__ == "__main__":
    my_tests = open(0).read().splitlines()

    X = 1
    sum = 0

    instructions = [x.split() for x in my_tests][::-1]
    curr_instruction = instructions.pop()

    i = 0
    crt = ["." for _ in range(240)]
    while len(instructions) > 0 or curr_instruction is not None:
        it = i + 1
        if it == 20 or (it - 20) % 40 == 0:
            sum += it * X

        if i % 40 in [X - 1, X, X + 1]:
            crt[i] = "#"

        match curr_instruction or instructions.pop():
            case ["noop"]:
                curr_instruction = None
            case ["addx", v]:
                curr_instruction = ["add-now", v]
            case ["add-now", v]:
                curr_instruction = None
                X += int(v)
        i += 1
    print(sum)
    group_of_40 = list_of_groups = zip(*(iter(crt),) * 40)
    print("\n".join(map(lambda x: "".join(x), group_of_40)))
