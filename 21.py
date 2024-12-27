from collections import defaultdict
import sys

sys.setrecursionlimit(10000000)

DAY = 21
TEST = False

FILE = f"{DAY}"
FILE_TEST = f"{DAY}_test"
with open(f"./{FILE_TEST if TEST else FILE}.txt", "r") as file:
    inp = file.readlines()
    inp = [x.strip() for x in inp]


def parse(inp: list[str]):
    return inp


big = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}

small = {"^": (0, 1), "A": (0, 2), "<": (1, 0), "v": (1, 1), ">": (1, 2)}


def vertical_sign_converter(a: int) -> str:
    if a > 0:
        return "v" * a
    return "^" * abs(a)


def horizontal_sign_converter(a: int) -> str:
    if a > 0:
        return ">" * a
    return "<" * abs(a)


def travel_big(a: str, b: str) -> list[str]:
    diff_x = big[b][0] - big[a][0]
    diff_y = big[b][1] - big[a][1]
    if big[a][1] == 0 and big[b][0] == 3:
        return [
            horizontal_sign_converter(diff_x) + vertical_sign_converter(diff_y) + "A"
        ]
    if big[b][1] == 0 and big[a][0] == 3:
        return [
            vertical_sign_converter(diff_x) + horizontal_sign_converter(diff_y) + "A"
        ]

    return [
        vertical_sign_converter(diff_x) + horizontal_sign_converter(diff_y) + "A",
        horizontal_sign_converter(diff_y) + vertical_sign_converter(diff_x) + "A",
    ]


def travel_small(a: str, b: str) -> list[str]:
    diff_x = small[b][0] - small[a][0]
    diff_y = small[b][1] - small[a][1]
    if small[b][0] == 0 and small[a][1] == 0:
        return [
            horizontal_sign_converter(diff_y) + vertical_sign_converter(diff_x) + "A"
        ]

    if small[a][0] == 0 and small[b][1] == 0:
        return [
            vertical_sign_converter(diff_x) + horizontal_sign_converter(diff_y) + "A"
        ]

    option1 = vertical_sign_converter(diff_x) + horizontal_sign_converter(diff_y) + "A"
    option2 = horizontal_sign_converter(diff_y) + vertical_sign_converter(diff_x) + "A"
    return [option1, option2]


def full_travel_big(a: str) -> list[str]:
    a = "A" + a
    totals = [""]
    for x, y in zip(a, a[1:]):
        options = travel_big(x, y)
        totals = [total + option for option in options for total in totals]
    return totals


def full_travel_small(a: str) -> str:
    a = "A" + a
    total = ""
    for x, y in zip(a, a[1:]):
        next = travel_small(x, y)
        total = total + next[0]
    return total


def full_travel_small_possibilities(a: str) -> list[str]:
    a = "A" + a
    totals = [""]
    for x, y in zip(a, a[1:]):
        options = travel_small(x, y)
        totals = [total + option for option in options for total in totals]
    return totals


CACHE: dict[tuple[str, int], dict[str, int]] = {}


def cache_travel_small(a: str, steps: int) -> dict[str, int]:
    if steps == 0:
        return {a: 1}
    if (a, steps) in CACHE:
        return CACHE[(a, steps)]
    SS = full_travel_small_possibilities(a)
    CACHE[(a, steps)] = None
    for s in SS:
        actual = "A"
        splits = defaultdict(int)
        for x in s[1:]:
            if x == "A":
                splits[actual + "A"] += 1
                actual = "A"
            else:
                actual += x
        part = defaultdict(int)
        for x, times in splits.items():
            for y, times_2 in cache_travel_small(x, steps - 1).items():
                part[y] += times * times_2
        if CACHE[(a, steps)] is None or value_dict(part) < value_dict(
            CACHE[(a, steps)]
        ):
            CACHE[(a, steps)] = part
    return CACHE[(a, steps)]


def to_split_travel_small(a: dict[str, int], steps) -> dict[str, int]:
    sol = defaultdict(int)
    for x, times in a.items():
        for y, times_2 in cache_travel_small(x, steps).items():
            sol[y] += times * times_2
    return sol


def value_dict(a: dict[str, int]) -> int:
    return sum([(len(x) - 1) * y for x, y in a.items()])


def prepare_small(a: str, steps=2) -> int:
    actual = "A"
    splits = defaultdict(int)
    for x in a:
        if x == "A":
            splits[actual + "A"] += 1
            actual = "A"
        else:
            actual += x
    splits = to_split_travel_small(splits, steps)
    return value_dict(splits)


def all_travel_cache(a: str, steps=2) -> int:
    travel = full_travel_big(a)
    return min(prepare_small(x, steps) for x in travel)


def all_travel(a: str, steps=2) -> int:
    travel = full_travel_big(a)
    for _ in range(steps):
        travel = [full_travel_small(x) for x in travel]
    return min(len(x) for x in travel)


def one(cases: list[str]):
    sol = 0
    sol_2 = 0
    for case in cases:
        num = int(case[:-1])
        sol += num * all_travel(case)
        sol_2 += num * all_travel_cache(case, steps=2)
    return sol, sol_2


def two(cases: list[str]):
    sol = 0
    for case in cases:
        num = int(case[:-1])
        sol += num * all_travel_cache(case, steps=25)
    return sol


L = parse(inp)

print(one(L))
print(two(L))
