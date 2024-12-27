DAY = 19
TEST = True

FILE = f"{DAY}"
FILE_TEST = f"{DAY}_test"
with open(f"/Users/edgar/Downloads/aoc/{FILE_TEST if TEST else FILE}.txt", "r") as file:
    inp = file.readlines()
    inp = [x.strip() for x in inp]


def parse(inp: list[str]):
    return inp[0].split(", "), inp[2:]


def dp(s: str, memo: dict[str, int], pieces: list[str]):
    if s in memo:
        return memo[s]
    sol = 0
    for piece in pieces:
        l = len(piece)
        if len(s) >= l and s[-l:] == piece:
            sol += dp(s[:-l], memo, pieces)
    memo[s] = sol
    return memo[s]


def one(pieces: list[str], cases: list[str]):
    memo = {"": 1}
    return sum([dp(case, memo, pieces) != 0 for case in cases])


def two(pieces: list[str], cases: list[str]):
    memo = {"": 1}
    return sum([dp(case, memo, pieces) for case in cases])


L = parse(inp)

print(one(L[0], L[1]))
print(two(L[0], L[1]))
