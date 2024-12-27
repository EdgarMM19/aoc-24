from math import lcm


DAY = 13
TEST = False


FILE = f"{DAY}"
FILE_TEST = f"{DAY}_test"
with open(f"/Users/edgar/Downloads/aoc/{FILE_TEST if TEST else FILE}.txt", "r") as file:
    inp = file.readlines()
    inp = [x.strip() for x in inp]


def parse(inp: list[str]):
    inp = [x for x in inp if x]
    cases = list(zip(inp[0::3], inp[1::3], inp[2::3]))

    def parse_button(button: str):
        parsed_button = (
            button.replace("Button A: X+", "")
            .replace("Button B: X+", "")
            .replace("Y+", "")
        )
        x, y = parsed_button.split(",")
        return int(x), int(y)

    def parse_prize(prize: str, two: bool):
        parsed_prize = prize.replace("Prize: X=", "").replace("Y=", "")
        x, y = parsed_prize.split(",")
        return int(x) + (10000000000000 if two else 0), int(y) + (
            10000000000000 if two else 0
        )

    return (
        [
            (parse_button(x), parse_button(y), parse_prize(z, False))
            for x, y, z in cases
        ],
        [(parse_button(x), parse_button(y), parse_prize(z, True)) for x, y, z in cases],
    )


def solve_case(case: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]):
    A, B, obj = case
    sol = None
    for i in range(1000):
        for j in range(1000):
            if A[0] * i + B[0] * j == obj[0] and A[1] * i + B[1] * j == obj[1]:
                new_sol = i * 3 + j * 1
                sol = new_sol if not sol else min(sol, new_sol)
    return sol or 0


def solve_case_two(case: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]):
    A, B, obj = case
    a1, a2 = A
    b1, b2 = B
    o1, o2 = obj
    det = a1 * b2 - a2 * b1
    if det == 0:
        print(det)
        return 0

    a = b2 * o1 - b1 * o2
    if a % det != 0:
        return 0
    a = a // det
    b = o1 - a1 * a
    if b % b1 != 0:
        return 0
    b = b // b1
    return a * 3 + b


def one(cases: list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]):
    return sum([solve_case(x) for x in cases])


def two(cases: list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]):
    return sum([solve_case_two(x) for x in cases])


L = parse(inp)
# print(one(L[0]))
print(two(L[1]))
