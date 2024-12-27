DAY = 14
TEST = False


FILE = f"{DAY}"
FILE_TEST = f"{DAY}_test"
with open(f"/Users/edgar/Downloads/aoc/{FILE_TEST if TEST else FILE}.txt", "r") as file:
    inp = file.readlines()
    inp = [x.strip() for x in inp]

X = 11 if TEST else 101
Y = 7 if TEST else 103


def parse(inp: list[str]):
    def parse_case(case: str):
        return [[int(y) for y in x.split(",")] for x in case[2:].split(" v=")]

    return [parse_case(x) for x in inp]


def quadrant(x: int, y: int):
    if x == X // 2 or y == Y // 2:
        return 4
    x_half = x < X // 2
    y_half = y < Y // 2
    return x_half * 2 + y_half


def calculate_pos(robot: list[list[int]], time=100):
    pos1, pos2 = robot[0]
    v1, v2 = robot[1]
    end1 = ((pos1 + v1 * time) % X + X) % X
    end2 = ((pos2 + v2 * time) % Y + Y) % Y
    return [end1, end2]


def one(cases: list[list[list[int]]]):
    quadrants = [0] * 5
    for case in cases:
        quadrants[quadrant(*calculate_pos(case))] += 1
    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]


def two(cases: list[list[list[int]]]):
    for i in range(13, 101 * 103, 101):
        mp = [[" "] * X for _ in range(Y)]
        for case in cases:
            x, y = calculate_pos(case, i)
            mp[y][x] = "#"
        print(f"Time: {i}")
        print("\n".join(["".join(x) for x in mp]))
        print("-" * X)


L = parse(inp)
print(one(L))
two(L)
