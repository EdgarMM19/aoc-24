DAY = 25
TEST = False

FILE = f"{DAY}"
FILE_TEST = f"{DAY}_test"
with open(f"./{FILE_TEST if TEST else FILE}.txt", "r") as file:
    inp = file.readlines()
    inp = [x.strip() for x in inp]


def get_code(form: list[str]):
    simple = [sum([form[x][i] == "#" for x in range(7)]) for i in range(5)]
    return form[0] == "#####", simple


def parse(inp: list[str]):
    up = []
    down = []
    for form in zip(*[inp[i::8] for i in range(7)]):
        goes_up, simple = get_code(form)
        if goes_up:
            up.append(simple)
        else:
            down.append(simple)
    return up, down


def compare(up: list[int], down: list[int]):
    return all([up[i] + down[i] < 8 for i in range(5)])


def one(up: list[list[int]], down: list[list[int]]):
    return sum([compare(x, y) for x in (up) for y in (down)])


L = parse(inp)
print(one(*L))
