"""
This file contains a code attempt for advent of code day 7
"""


import re


class Node:
    def size(self):
        raise Exception


class Dir(Node):
    def __init__(self):
        self.contents = {}

    def add(self, name, n: Node):
        self.contents[name] = n

    def size(self):
        res = sum(n.size() for n in self.contents.values())
        print(res)
        return res

    def get(self, n):
        return self.contents[n]


class File(Node):
    def __init__(self, sz):
        self.sz = sz

    def size(self):
        return self.sz


if __name__ == "__main__":
    my_tests = open(0).read()
    blocks = re.findall(r"\$[^\$]+", my_tests)
    blocks = [x.rstrip("\n").split("\n") for x in blocks]
    blocks = [(x[0][2:].split(), [tuple(x_.split()) for x_ in x[1:]]) for x in blocks]

    root = Dir()

    history = []
    curr = root

    for cmdargs, output in blocks:
        cmd = cmdargs[0]
        if cmd == "cd":
            arg = cmdargs[1]
            if arg == "..":
                curr = history.pop()
            elif arg == "/":
                curr = root
                history = []
            else:
                history.append(curr)
                curr = curr.get(arg)
        elif cmd == "ls":
            for attr, filename in output:
                if attr == "dir":
                    curr.add(filename, Dir())
                else:
                    curr.add(filename, File(int(attr)))

    root.size()
