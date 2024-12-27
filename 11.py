from collections import defaultdict


FILE = "11"
# FILE = "11_test"
with open(f"/Users/edgar/Downloads/aoc/{FILE}.txt", "r") as file:
    inp = file.readlines()
    inp = [x.strip() for x in inp]


def parse(inp: list[str]):
    return {int(y): 1 for y in inp[0].split()}


def iter(x: int):
    if x == 0:
        return [1]
    length = len(str(x))
    if length % 2 == 0:
        return [x % (10 ** (length // 2)), x // (10 ** (length // 2))]
    return [x * 2024]


def full_iter(vals: dict[int, int]):
    sol = defaultdict(int)
    for x, y in vals.items():
        nexts = iter(x)
        for n in nexts:
            sol[n] += y
    return sol


def one(L: dict[int, int]):
    for _ in range(25):
        L = full_iter(L)
    return sum(L.values())


def two(L: dict[int, int]):
    for _ in range(75):
        L = full_iter(L)
    return sum(L.values())


L = parse(inp)
print(one(L))
print(two(L))
