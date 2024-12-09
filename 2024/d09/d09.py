import sys

file = open(sys.argv[1]).read()

occupied = []
free_space = []
next_free_idx = 0
for i, d in enumerate(map(int, file.strip())):
    if i % 2 == 0:
        # file
        file_id = i // 2
        occupied.append((next_free_idx, next_free_idx + d, file_id))
    else:
        # free space
        free_space.append((next_free_idx, next_free_idx + d))
    next_free_idx += d


def show(occupied):
    i = 0
    for a, b, c in sorted(occupied):
        for _ in range(i, a):
            print(".", end="")
        print(str(c) * (b - a), end="")
        i = b
    print("")


def part1(occupied, free_space):
    new_occupied = []
    while True:
        file_start, file_end, filename = occupied[-1]
        file_sz = file_end - file_start
        free_start, free_end = free_space.pop(0)
        space = free_end - free_start

        if free_start >= file_end:
            break

        if space < file_sz:
            new_occupied.append((free_start, free_end, filename))
            occupied[-1] = (file_start, file_end - space, filename)
        else:
            free_space.insert(0, (free_start + file_sz, free_end))
            new_occupied.append((free_start, free_start + file_sz, filename))
            occupied.pop()

    print(sum(arith_sum(a, b) * c for a, b, c in occupied + new_occupied))


def arith_sum(a, b):
    return (b - a) * (a + (b - 1)) // 2


def part2(occupied, free_space):
    new_occupied = []
    for i, (file_start, file_end, file_name) in reversed(list(enumerate(occupied))):
        file_sz = file_end - file_start
        free_idx = next(
            (i for i, (start, end) in enumerate(free_space) if end - start >= file_sz),
            None,
        )
        if free_idx is None:
            continue
        free_start, free_end = free_space[free_idx]

        if free_start >= file_end:
            continue

        free_space[free_idx] = (free_start + file_sz, free_end)
        new_occupied.append((free_start, free_start + file_sz, file_name))
        occupied.pop(i)

    print(sum(arith_sum(a, b) * c for a, b, c in occupied + new_occupied))


part1(occupied.copy(), free_space.copy())
part2(occupied.copy(), free_space.copy())
