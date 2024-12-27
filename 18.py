DAY = 18
TEST = False

FILE = f"{DAY}"
FILE_TEST = f"{DAY}_test"
with open(f"/Users/edgar/Downloads/aoc/{FILE_TEST if TEST else FILE}.txt", "r") as file:
    inp = file.readlines()
    inp = [x.strip() for x in inp]

X = 7 if TEST else 71
Y = X
BYTES = 12 if TEST else 1024


def parse(inp: list[str]):
    return [list(reversed([int(x) for x in y.split(",")])) for y in inp]


def valid(x: int, y: int, nogo: list[list[int]], visited: list[list[bool]]):
    return 0 <= x < X and 0 <= y < Y and [x, y] not in nogo and not visited[x][y]


def one(nogo: list[list[int]]):
    q = [[0, 0, 0]]
    visited = [[False] * Y for _ in range(X)]
    while len(q) != 0:
        x, y, cost = q.pop(0)
        if x == X - 1 and y == Y - 1:
            return cost
        if not valid(x, y, nogo, visited):
            continue
        visited[x][y] = True
        q.append([x + 1, y, cost + 1])
        q.append([x - 1, y, cost + 1])
        q.append([x, y + 1, cost + 1])
        q.append([x, y - 1, cost + 1])


def two(nogo: list[list[int]]):
    l, r = BYTES, len(nogo)
    while l != r:
        m = (l + r) // 2
        if one(nogo[:m]) is not None:
            l = m + 1
        else:
            r = m
    return nogo[l - 1]


L = parse(inp)

print(one(L[:BYTES]))
print(two(L))
