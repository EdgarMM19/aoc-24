from typing import Optional
import sys

sys.setrecursionlimit(1000000)

DAY = 16
TEST = False

FILE = f"{DAY}"
FILE_TEST = f"{DAY}_test"
with open(f"/Users/edgar/Downloads/aoc/{FILE_TEST if TEST else FILE}.txt", "r") as file:
    inp = file.readlines()
    inp = [x.strip() for x in inp]


def parse(inp: list[str]):
    return [[x for x in y] for y in inp]


directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
symbol_to_dir = {"<": 0, "v": 1, ">": 2, "^": 3}
dir_to_symbol = {0: "<", 1: "v", 2: ">", 3: "^"}


def insert(
    x: int,
    y: int,
    direction: int,
    cost: int,
    q: list,
    memo: list[list[list[Optional[int]]]],
):
    if memo[x][y][direction] is None or memo[x][y][direction] > cost:
        memo[x][y][direction] = cost
        q.append([cost, x, y, direction])


def dp(
    mp: list[list[str]],
    x,
    y,
    direction: int,
    memo: list[list[list[Optional[int]]]],
    cost,
    q,
):
    if mp[x][y] == "E":
        return
    if memo[x][y][direction] != cost:
        return
    if mp[x][y] == "#":
        return
    memo[x][y][direction] = cost
    insert(
        x + directions[direction][0],
        y + directions[direction][1],
        direction,
        cost + 1,
        q,
        memo,
    )
    insert(x, y, (direction + 1) % 4, cost + 1000, q, memo)
    insert(x, y, (direction + 3) % 4, cost + 1000, q, memo)
    return


def one(mp: list[list[str]]):
    x, y = next(
        (x, y) for x, row in enumerate(mp) for y, cell in enumerate(row) if cell == "S"
    )
    memo: list[list[list[Optional[int]]]] = [[[None] * 4 for _ in row] for row in mp]
    memo[x][y][2] = 0
    q = [[0, x, y, 2]]
    while len(q) != 0:
        cost, x, y, dir = q.pop(0)
        sol = dp(mp, x, y, dir, memo, cost, q)
        if sol:
            return sol, memo
        q = sorted(q)

    x, y = next(
        (x, y) for x, row in enumerate(mp) for y, cell in enumerate(row) if cell == "E"
    )
    return min([z or 1e18 for z in memo[x][y]]), memo


def bfs(x, y, dir, memo, cost, sol, mp):
    if memo[x][y][dir] != cost or sol[x][y][dir] or mp[x][y] == "#":
        return
    sol[x][y][dir] = True
    bfs(x, y, (dir + 1) % 4, memo, cost - 1000, sol, mp)
    bfs(x, y, (dir + 3) % 4, memo, cost - 1000, sol, mp)
    bfs(x - directions[dir][0], y - directions[dir][1], dir, memo, cost - 1, sol, mp)


def two(sol, memo, mp):
    print(sol)
    x, y = next(
        (x, y) for x, row in enumerate(mp) for y, cell in enumerate(row) if cell == "E"
    )
    sols = [[[False] * 4 for _ in row] for row in memo]
    for dir in [dir for dir in range(4) if memo[x][y][dir] == sol]:
        bfs(x, y, dir, memo, sol, sols, mp)
    print("\n".join(["".join([" " if sum(z) == 0 else "X" for z in x]) for x in sols]))
    return sum([sum(sum(z) != 0 for z in x) for x in sols])


L = parse(inp)
print(two(*one(L), L))
