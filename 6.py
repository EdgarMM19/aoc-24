from copy import deepcopy
import sys

sys.setrecursionlimit(100000)

FILE = "6"
# FILE = "6_test"
with open(f"/Users/edgar/Downloads/aoc/{FILE}.txt", "r") as file:
    inp = file.readlines()
    tauler = [x.strip() for x in inp]


directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def valid(pos, tauler):
    return 0 <= pos[0] < len(tauler) and 0 <= pos[1] < len(tauler[0])


def one(pre_tauler: list[str]):
    pos = None

    for i, line in enumerate(pre_tauler):
        j = line.find("^")
        if j != -1:
            pos = [i, j]
            break
    tauler = [[c for c in line] for line in pre_tauler]
    assert pos is not None
    direction = 0
    while valid(pos, tauler):
        if tauler[pos[0]][pos[1]] == "#":
            pos[0] -= directions[direction][0]
            pos[1] -= directions[direction][1]
            direction = (direction + 1) % 4
        tauler[pos[0]][pos[1]] = "X"
        pos[0] += directions[direction][0]
        pos[1] += directions[direction][1]
    return sum([line.count("X") for line in tauler])


def trail(pos, visited, tauler, direction):
    if not valid(pos, tauler):
        return False
    if tauler[pos[0]][pos[1]] in ["#", "0"]:
        return trail(
            [pos[0] - directions[direction][0], pos[1] - directions[direction][1]],
            visited,
            tauler,
            (direction + 1) % 4,
        )
    if visited[pos[0]][pos[1]][direction] == 2:
        return True
    visited[pos[0]][pos[1]][direction] += 1
    sol = trail(
        [pos[0] + directions[direction][0], pos[1] + directions[direction][1]],
        visited,
        tauler,
        direction,
    )
    visited[pos[0]][pos[1]][direction] -= 1
    return sol


def two(pre_tauler: list[str]):
    pos = None

    for i, line in enumerate(pre_tauler):
        j = line.find("^")
        if j != -1:
            pos = [i, j]
            break
    tauler = [[c for c in line] for line in pre_tauler]
    visited = [[[0] * 4 for _ in line] for line in tauler]

    assert pos is not None
    direction = 0
    sol = 0
    while valid(pos, tauler):
        if tauler[pos[0]][pos[1]] == "#":
            pos[0] -= directions[direction][0]
            pos[1] -= directions[direction][1]
            direction = (direction + 1) % 4
            continue
        tauler[pos[0]][pos[1]] = "0"
        if sum(visited[pos[0]][pos[1]]) == 0 and trail(
            deepcopy(pos), visited, tauler, direction
        ):
            sol += 1
        tauler[pos[0]][pos[1]] = "X"
        visited[pos[0]][pos[1]][direction] += 1
        pos[0] += directions[direction][0]
        pos[1] += directions[direction][1]
    return sol


print(one(tauler))
print(two(tauler))


def print_array(lines: list[str]):
    print("\n".join(lines))
    print()
