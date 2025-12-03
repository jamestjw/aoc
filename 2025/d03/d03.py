inp = open(0).read().splitlines()


def find_max(digits: str, n=2) -> int:
    def inner(digits, n, acc):
        if n == 0:
            return int("".join(map(str, acc)))
        else:
            i = max(list(range(len(digits) - n + 1)), key=digits.__getitem__)
            return inner(digits[i + 1 :], n - 1, acc + [digits[i]])

    return inner(list(map(int, digits)), n, [])


print(sum(find_max(ds, n=2) for ds in inp))
print(sum(find_max(ds, n=12) for ds in inp))
