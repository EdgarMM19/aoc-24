from collections import defaultdict


DAY = 22
TEST = False

FILE = f"{DAY}"
FILE_TEST = f"{DAY}_test"
with open(f"./{FILE_TEST if TEST else FILE}.txt", "r") as file:
    inp = file.readlines()
    inp = [x.strip() for x in inp]


def parse(inp: list[str]):
    return [int(x) for x in inp]


def mix(x: int, y: int):
    return x ^ y


def prune(x: int):
    return x % 16777216


def next(x: int):
    x = prune(mix(x, x * 64))
    x = prune(mix(x, x // 32))
    x = prune(mix(x, x * 2048))
    return x


def hash(l: list[int]):
    sum = 0
    for x in l:
        sum = 30 * sum + x + 10
    return sum


def changes(x: list[int]):
    return [x - y for x, y in zip(x[1:], x)]


def single(
    x: int,
    prices: defaultdict[int, int] = defaultdict(int),
):
    seen = set()
    last_five = []
    for i in range(2000):
        x = next(x)
        last_five.append(x % 10)
        if len(last_five) > 5:
            last_five.pop(0)
        elif len(last_five) < 5:
            continue
        hashed = hash(changes(last_five))
        if hashed not in seen:
            prices[hashed] += last_five[-1]
            seen.add(hashed)
    return x


def one(cases: list[int]):
    return sum([single(x) for x in cases])


def two(cases: list[int]):
    prices = defaultdict(int)
    for x in cases:
        single(x, prices)
    return max(prices.values())


L = parse(inp)

print(one(L))
print(two(L))
