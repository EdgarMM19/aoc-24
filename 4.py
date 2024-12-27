import re

FILE = "4"
# FILE = "4_test"
with open(f"/Users/edgar/Downloads/aoc/{FILE}.txt", "r") as file:
    inp = file.readlines()
    inp = [x.strip() for x in inp]


def one(inp):
    REGEX1 = r"XMAS"

    def first(line: str):
        return len(re.findall(REGEX1, line))

    def both_directions(lines: list[str]):
        return first("-".join(lines)) + first("".join(reversed("-".join(lines))))

    def convert_to_vertical(lines: list[str]):
        return ["".join(x) for x in zip(*lines)]

    def convert_to_diagonal(lines: list[str]):
        return convert_to_vertical(
            ["*" * i + x + "*" * (len(lines) - i) for i, x in enumerate(lines)]
        )

    vertical = convert_to_vertical(inp)
    diagonal1 = convert_to_diagonal(inp)
    diagonal2 = convert_to_diagonal(list(reversed(inp)))
    sol = (
        both_directions(inp)
        + both_directions(vertical)
        + both_directions(diagonal1)
        + both_directions(diagonal2)
    )
    print(sol)


def two(inp):
    def correct_diags(a, b):
        return {a, b} == {"M", "S"}

    sol = 0
    for i in range(1, len(inp) - 1):
        for j in range(1, len(inp[0]) - 1):
            if (
                inp[i][j] == "A"
                and correct_diags(inp[i + 1][j + 1], inp[i - 1][j - 1])
                and correct_diags(inp[i - 1][j + 1], inp[i + 1][j - 1])
            ):
                sol += 1
    print(sol)


one(inp)
two(inp)


def print_array(lines: list[str]):
    print("\n".join(lines))
    print()
