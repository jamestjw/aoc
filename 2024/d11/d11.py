import sys
from functools import lru_cache

file = open(sys.argv[1]).read()


nums = [int(e) for e in file.strip().split()]


@lru_cache(maxsize=None)
def change(num, times):
    if times == 0:
        return 1
    if num == 0:
        return change(1, times - 1)
    elif len(str(num)) % 2 == 0:
        num_str = str(num)
        left = int(num_str[: len(num_str) // 2])
        right = int(num_str[len(num_str) // 2 :])
        return change(left, times - 1) + change(right, times - 1)
    else:
        return change(num * 2024, times - 1)


print(sum(change(n, 25) for n in nums))
print(sum(change(n, 75) for n in nums))
