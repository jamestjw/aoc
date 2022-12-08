text = list(map(int, open(0).read().splitlines()))


def num_increases(l):
    return len([() for i, j in zip(l[:-1], l[1:]) if j > i])


print(num_increases(text))
print(num_increases([i + j + k for i, j, k in zip(text[:-1], text[1:], text[2:])]))
