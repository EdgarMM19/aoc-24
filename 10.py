from typing import Optional


FILE = "10"
FILE = "10_test"
with open(f"/Users/edgar/Downloads/aoc/{FILE}.txt", "r") as file:
    inp = file.readlines()
    inp = [x.strip() for x in inp]


def parse(inp: list[str]):
    return [[int(x) for x in y] for y in inp]


def dp(i: int, j: int, val: int, memo: list[list[int]], L: list[list[int]]) -> int:
    if i < 0 or j < 0 or i >= len(L) or j >= len(L[i]):
        return 0
    if L[i][j] != val:
        return 0
    if memo[i][j] != -1:
        return memo[i][j]

    if L[i][j] == 9:
        memo[i][j] = 1
        return 1
    memo[i][j] = (
        dp(i + 1, j, val + 1, memo, L)
        + dp(i, j + 1, val + 1, memo, L)
        + dp(i - 1, j, val + 1, memo, L)
        + dp(i, j - 1, val + 1, memo, L)
    )
    return memo[i][j]


def dp2(
    i: int, j: int, val: int, memo: list[list[Optional[set]]], L: list[list[int]]
) -> set[tuple[int, int]]:
    if i < 0 or j < 0 or i >= len(L) or j >= len(L[i]):
        return set()
    if L[i][j] != val:
        return set()
    if memo[i][j] is not None:
        return memo[i][j]
    if L[i][j] == 9:
        memo[i][j] = set()
        memo[i][j].add((i, j))
        return memo[i][j]
    memo[i][j] = set()
    memo[i][j] |= dp2(i + 1, j, val + 1, memo, L)
    memo[i][j] |= dp2(i - 1, j, val + 1, memo, L)
    memo[i][j] |= dp2(i, j + 1, val + 1, memo, L)
    memo[i][j] |= dp2(i, j - 1, val + 1, memo, L)
    return memo[i][j]


def one(L: list[list[int]]):
    memo = [[None for _ in y] for y in L]
    return sum(
        [
            len(dp2(i, j, 0, memo, L)) if L[i][j] == 0 else 0
            for i in range(len(L))
            for j in range(len(L[i]))
        ]
    )


def two(L: list[list[int]]):
    memo = [[-1 for _ in y] for y in L]
    return sum(
        [
            dp(i, j, 0, memo, L) if L[i][j] == 0 else 0
            for i in range(len(L))
            for j in range(len(L[i]))
        ]
    )


L = parse(inp)
print(one(L))
print(two(L))
