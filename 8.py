from collections import defaultdict


FILE = "8"
FILE = "8_test"
with open(f"/Users/edgar/Downloads/aoc/{FILE}.txt", "r") as file:
    inp = file.readlines()
    inp = [x.strip() for x in inp]


def parse(inp: list[str]):
    dic = defaultdict(list)
    for i, line in enumerate(inp):
        for j, char in enumerate(line):
            if char.isalnum():
                dic[char].append((i, j))
    p_inp = [[x for x in y] for y in inp]
    return len(inp), len(inp[0]), dic, p_inp


rows, cols, dic, p_inp = parse(inp)


def check_single(i: int, j: int, l: tuple[int, int], l2: tuple[int, int]):
    v1 = [l[0] - i, l[1] - j]
    v2 = [l2[0] - i, l2[1] - j]
    return (v1[0] * 2 == v2[0] and v1[1] * 2 == v2[1]) or (
        v1[0] == v2[0] * 2 and v1[1] == v2[1] * 2
    )


def check_single_easy(i: int, j: int, l: tuple[int, int], l2: tuple[int, int]):
    v1 = [l[0] - i, l[1] - j]
    v2 = [l2[0] - i, l2[1] - j]
    return v1[0] * v2[1] == v1[1] * v2[0]


def check_position_character(i: int, j: int, l: list[tuple[int, int]]):
    for l1 in l:
        for l2 in l:
            if l1 != l2 and check_single(i, j, l1, l2):
                p_inp[i][j] = "*"
                return True
    return False


def check_position_character_easy(i: int, j: int, l: list[tuple[int, int]]):
    for l1 in l:
        for l2 in l:
            if l1 != l2 and check_single_easy(i, j, l1, l2):
                p_inp[i][j] = "*"
                return True
    return False


def one(rows: int, cols: int, dic: dict[str, list[tuple[int, int]]]):
    sol = 0
    for i in range(rows):
        for j in range(cols):
            for key, value in dic.items():
                if check_position_character(i, j, value):
                    sol += 1
                    break
    return sol


def two(rows: int, cols: int, dic: dict[str, list[tuple[int, int]]]):
    sol = 0
    for i in range(rows):
        for j in range(cols):
            for key, value in dic.items():
                if check_position_character_easy(i, j, value):
                    sol += 1
                    break
    return sol


print(one(rows, cols, dic))
print(two(rows, cols, dic))
