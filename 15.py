from copy import deepcopy
from typing import Optional


DAY = 15
TEST = False


FILE = f"{DAY}"
FILE_TEST = f"{DAY}_test"
with open(f"/Users/edgar/Downloads/aoc/{FILE_TEST if TEST else FILE}.txt", "r") as file:
    inp = file.readlines()
    inp = [x.strip() for x in inp]


def parse(inp: list[str]):
    sep = inp.index("")
    mp = [[y for y in x] for x in inp[:sep]]
    moves = "".join(inp[sep + 1 :])
    return mp, moves


direc = [(0, -1), (1, 0), (0, 1), (-1, 0)]
simbol_to_dir = {"<": 0, "v": 1, ">": 2, "^": 3}


def find_next_available(mp: list[list[str]], x: int, y: int, d: int):
    while True:
        x += direc[d][0]
        y += direc[d][1]
        if mp[x][y] == ".":
            return x, y
        if mp[x][y] == "#":
            return None


def vertical_directions(
    mp: list[list[str]],
    x: int,
    y: int,
    d: int,
    visited: list[list[Optional[bool]]],
    lateral: bool = False,
):
    if visited[x][y] is not None:
        return visited[x][y]
    if mp[x][y] == "#":
        visited[x][y] = False
        return visited[x][y]
    if mp[x][y] == ".":
        visited[x][y] = True
        return visited[x][y]
    if mp[x][y] == "@":
        visited[x][y] = vertical_directions(mp, x + direc[d][0], y, d, visited)
        return visited[x][y]
    if mp[x][y] == "[":
        visited[x][y] = vertical_directions(mp, x + direc[d][0], y, d, visited) and (
            lateral or vertical_directions(mp, x, y + 1, d, visited, True)
        )
        return visited[x][y]

    visited[x][y] = vertical_directions(mp, x + direc[d][0], y, d, visited) and (
        lateral or vertical_directions(mp, x, y - 1, d, visited, True)
    )
    return visited[x][y]


def find_at(mp):
    x, y = next(
        (y, x) for y, row in enumerate(mp) for x, cell in enumerate(row) if cell == "@"
    )
    return x, y


def move(mp: list[list[str]], x: int, y: int, d: int):
    if d in [0, 2]:
        to_move = find_next_available(mp, x, y, d)
        if not to_move:
            return mp
        n_x, n_y = to_move
        prev = "."
        while True:
            mp[x][y], prev = prev, mp[x][y]
            if x == n_x and y == n_y:
                return mp
            x, y = x + direc[d][0], y + direc[d][1]
    if d == 1:
        mp = list(reversed(mp))
    x, y = find_at(mp)
    visited: list[list[Optional[bool]]] = [[None for _ in row] for row in mp]
    possible = vertical_directions(mp, x, y, 3, visited)
    if possible:
        for i in range(len(mp)):
            for j in range(len(mp[0])):
                if visited[i][j]:
                    mp[i][j] = "." if not visited[i + 1][j] else mp[i + 1][j]
    if d == 1:
        mp = list(reversed(mp))
    return mp


def count(mp: list[list[str]]):
    return sum(
        i * 100 + j
        for i, row in enumerate(mp)
        for j, cell in enumerate(row)
        if cell == "O" or cell == "["
    )


def duplicate(mp: list[list[str]]):
    nw = []
    for row in mp:
        new_row = []
        for cell in row:
            if cell == "@":
                new_row.extend(["@", "."])
            elif cell == "O":
                new_row.extend(["[", "]"])
            else:
                new_row.extend([cell, cell])
        nw.append(new_row)
    return nw


def one(mp: list[list[str]], moves: str):
    x, y = next(
        (y, x) for y, row in enumerate(mp) for x, cell in enumerate(row) if cell == "@"
    )
    for move in moves:
        dir = simbol_to_dir[move]
        pos_to_move = find_next_available(mp, x, y, dir)
        if not pos_to_move:
            continue
        next_pos = x + direc[dir][0], y + direc[dir][1]
        mp[pos_to_move[0]][pos_to_move[1]] = mp[next_pos[0]][next_pos[1]]
        mp[next_pos[0]][next_pos[1]] = "@"
        mp[x][y] = "."
        x, y = next_pos
    return count(mp)


def two(mp: list[list[str]], moves: str):
    mp = duplicate(mp)
    x, y = find_at(mp)
    for step in moves:
        x, y = find_at(mp)
        dir = simbol_to_dir[step]
        mp = move(mp, x, y, dir)
    return count(mp)


L = parse(inp)
print(one(deepcopy(L[0]), L[1]))
print(two(L[0], L[1]))
