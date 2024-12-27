from copy import deepcopy
import sys

sys.setrecursionlimit(10000000)
FILE = "9"
# FILE = "9_test"
with open(f"/Users/edgar/Downloads/aoc/{FILE}.txt", "r") as file:
    inp = file.readlines()
    inp = [x.strip() for x in inp]


def parse(inp: list[str]):
    return [(int(x), int(i) // 2 if i % 2 == 0 else -1) for i, x in enumerate(inp[0])]


def check_sum(l: list[tuple[int, int]]):
    sum = 0
    pos = 0
    for i, val in l:
        if val == -1:
            pos += i
            continue
        sum += val * (2 * pos + i + 1 - 2) * (i) // 2
        pos += i
    return sum


def move(i: int, j: int, l: list[tuple[int, int]]):
    if i + j >= len(l):
        return l
    if l[i][1] != -1 or l[i][0] == 0:
        return move(i + 1, j, l)
    if l[-j][1] == -1 or l[-j][0] == 0:
        return move(i, j + 1, l)
    to_move = min(l[i][0], l[-j][0])
    l[-j] = (l[-j][0] - to_move, l[-j][1])
    l[i] = (l[i][0] - to_move, l[i][1])
    l.insert(i, (to_move, l[-j][1]))
    return move(i, j, l)


def move2(j: int, l: list[tuple[int, int]]):
    if j == len(l):
        return l
    size = l[-j][0]
    value = l[-j][1]
    if value == -1:
        return move2(j + 1, l)
    for i in range(len(l) - j):
        if l[i][1] == -1 and l[i][0] >= size:
            l[-j] = (size, -1)
            l[i] = (l[i][0] - size, -1)
            l.insert(i, (size, value))
            return move2(j + 1, l)
    return move2(j + 1, l)


def one(l: list[tuple[int, int]]):
    l = move(0, 1, l)
    return check_sum(l)


def two(l: list[tuple[int, int]]):
    l = move2(1, l)
    print("".join(str("." if y == -1 else y) * x for x, y in l))
    return check_sum(l)


L = parse(inp)
print(one(deepcopy(L)))
print(two(L))
