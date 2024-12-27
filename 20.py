from typing import Optional
import sys

sys.setrecursionlimit(10000000)

DAY = 20
TEST = False

FILE = f"{DAY}"
FILE_TEST = f"{DAY}_test"
with open(f"/Users/edgar/Downloads/aoc/{FILE_TEST if TEST else FILE}.txt", "r") as file:
    inp = file.readlines()
    inp = [x.strip() for x in inp]


def parse(inp: list[str]):
    return inp


direcs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
two_step_direcs = [(0, 2), (2, 0), (0, -2), (-2, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]

LIMIT = 50 if TEST else 100


def valid(coord, l: list):
    return 0 <= coord[0] < len(l) and 0 <= coord[1] < len(l[0])


def new_coord(coord, dir):
    return (coord[0] + dir[0], coord[1] + dir[1])


def bfs(
    maze: list[str],
    pos: tuple[int, int],
    distances: list[list[Optional[int]]],
    distance: int,
):
    distances[pos[0]][pos[1]] = distance
    for d in direcs:
        n_pos = new_coord(pos, d)
        if (
            valid(n_pos, maze)
            and distances[n_pos[0]][n_pos[1]] is None
            and maze[n_pos[0]][n_pos[1]] != "#"
        ):
            bfs(maze, n_pos, distances, distance + 1)


def bfs2(
    maze: list[str], pos: tuple[int, int], original_distances: list[list[Optional[int]]]
):
    sol = 0
    for i in range(-20, 21):
        for j in range(-20 + abs(i), 21 - abs(i)):
            n_pos = new_coord(pos, (i, j))
            if not valid(n_pos, maze) or maze[n_pos[0]][n_pos[1]] == "#":
                continue
            cheat_dist = (
                original_distances[pos[0]][pos[1]]
                - original_distances[n_pos[0]][n_pos[1]]
                - abs(i)
                - abs(j)
            )
            if cheat_dist >= LIMIT:
                sol += 1
    return sol


def cheat(distances: list[list[Optional[int]]]):
    sol = 0
    for i in range(len(distances)):
        for j in range(len(distances[0])):
            dis1 = distances[i][j]
            if dis1 is not None:
                for d in two_step_direcs:
                    n_pos = new_coord([i, j], d)
                    if not valid(n_pos, distances):
                        continue
                    dis2 = distances[n_pos[0]][n_pos[1]]
                    if dis2 is not None:
                        cheat_dist = dis1 - dis2 - 2
                        if cheat_dist >= LIMIT:
                            sol += 1
    return sol


def one(maze: list[str]):
    start = next(
        (i, j) for i, row in enumerate(maze) for j, c in enumerate(row) if c == "S"
    )
    distances: list[list[Optional[int]]] = [
        [None] * len(maze[0]) for _ in range(len(maze))
    ]
    bfs(maze, start, distances, 0)
    return cheat(distances)


def two(maze: list[str]):
    start = next(
        (i, j) for i, row in enumerate(maze) for j, c in enumerate(row) if c == "S"
    )
    distances: list[list[Optional[int]]] = [
        [None] * len(maze[0]) for _ in range(len(maze))
    ]
    bfs(maze, start, distances, 0)
    sol = 0
    for i in range(len(distances)):
        for j in range(len(distances[0])):
            dis1 = distances[i][j]
            if dis1 is not None:
                sol += bfs2(
                    maze=maze,
                    pos=(i, j),
                    original_distances=distances,
                )
    return sol


L = parse(inp)

print(one(L))
print(two(L))
