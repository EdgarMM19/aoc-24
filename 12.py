from collections import defaultdict

DAY = 12
TEST = False


FILE = f"{DAY}"
FILE_TEST = f"{DAY}_test"
with open(f"/Users/edgar/Downloads/aoc/{FILE_TEST if TEST else FILE}.txt", "r") as file:
    inp = file.readlines()
    inp = [x.strip() for x in inp]


def parse(inp: list[str]):
    return inp


directions = [[0, 1], [1, 0], [-1, 0], [0, -1]]


def bfs(
    i: int,
    j: int,
    tauler: list[str],
    visited: list[list[bool]],
    sides: set[tuple[int, int, int]],
    prev_direction: int,
    c: str,
):
    if i < 0 or j < 0 or i >= len(tauler) or j >= len(tauler[0]) or tauler[i][j] != c:
        sides.add((i, j, prev_direction))
        return 0, 1
    if visited[i][j]:
        return 0, 0
    visited[i][j] = True
    area, perimeter = 1, 0
    for l, direc in enumerate(directions):
        n_area, n_perim = bfs(i + direc[0], j + direc[1], tauler, visited, sides, l, c)
        area += n_area
        perimeter += n_perim
    return area, perimeter


def one(tauler: list[str]):
    sol = 0
    visited = [[False for _ in x] for x in tauler]
    two_inp = []
    for i in range(len(tauler)):
        for j in range(len(tauler[0])):
            if not visited[i][j]:
                sides = set()
                area, perimeter = bfs(i, j, tauler, visited, sides, -1, tauler[i][j])
                two_inp.append([area, sides])
                sol += area * perimeter
    return sol, two_inp


def process_side(side: list[tuple[int, int]]):
    by_y_coordinate = defaultdict(list)
    for x, y in side:
        by_y_coordinate[y].append(x)
    sol = 0
    for _, coords in by_y_coordinate.items():
        sorted_coords = sorted(coords)
        prev = -1000
        for x in sorted_coords:
            if prev + 1 != x:
                sol += 1
            prev = x
    return sol


def process_sides(sides: set[tuple[int, int, int]]):
    north = [x[0:2] for x in sides if x[2] == 0]
    south = [x[0:2] for x in sides if x[2] == 3]
    east = [(x[1], x[0]) for x in sides if x[2] == 1]
    west = [(x[1], x[0]) for x in sides if x[2] == 2]
    return (
        process_side(north)
        + process_side(south)
        + process_side(east)
        + process_side(west)
    )


def two(L: list[str]):
    sol, all_sides = one(L)
    print(sol)
    sol2 = sum([area * process_sides(sides) for area, sides in all_sides])
    print(sol2)


L = parse(inp)
two(L)
