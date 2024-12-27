import sys

sys.setrecursionlimit(1000000)

DAY = 17
TEST = False

FILE = f"{DAY}"
FILE_TEST = f"{DAY}_test"
with open(f"/Users/edgar/Downloads/aoc/{FILE_TEST if TEST else FILE}.txt", "r") as file:
    inp = file.readlines()
    inp = [x.strip() for x in inp]


def parse(inp: list[str]):
    A = int(inp[0][11:])
    B = int(inp[1][11:])
    C = int(inp[2][11:])
    ins = [int(x) for x in inp[4][8:].split(",")]
    return [A, B, C], ins


def combo(val: int, regs: list[int]):
    if val < 4:
        return val
    if val == 7:
        raise Exception("!!!!!")
    return regs[val - 4]


ins_names = [
    "A := A // 8",
    "B := B ^ ",
    "B := A mod 8",
    "if A != 0 jump",
    "B:= B^C",
    "print B",
    "B := A // 2**comb",
    "C := A // 2**B",
]


def execute(regs: list[int], instruction: int, operand: int):
    match instruction:
        case 0:
            regs[0] = regs[0] // 8
        case 1:
            regs[1] = regs[1] ^ operand
        case 2:
            regs[1] = regs[0] % 8
        case 3:
            if regs[0] != 0:
                return 0, "jump"
        case 4:
            regs[1] = regs[1] ^ regs[2]
        case 5:
            return regs[1] % 8, "out"
        case 6:
            regs[1] = regs[0] // pow(2, combo(operand, regs))
        case 7:
            regs[2] = regs[0] // pow(2, regs[1])


def one(regs, instructions: list[int], first=True):
    sol: list[int] = []
    ins = 0
    while ins < len(instructions) - 1:
        x, y = instructions[ins], instructions[ins + 1]
        print(ins_names[x], y)
        out = execute(regs, x, y)
        if out is not None:
            if out[1] == "jump":
                ins = out[0]
                continue
            else:
                sol.append(out[0])
                if (
                    sol[-1] != instructions[min(len(instructions), len(sol)) - 1]
                ) and not first:
                    return sol
        ins += 2
    return sol


OBJECTIVE = [2, 4, 1, 5, 7, 5, 1, 6, 4, 2, 5, 5, 0, 3, 3, 0]


def single_value(A):
    return ((A % 8) ^ 3 ^ (A // (2 ** ((A % 8) ^ 5)))) % 8


def simple(A):
    sol = []
    while A != 0:
        sol.append(single_value(A))
        A = A // 8
    return sol


def iter_simple(obj: int):
    possible = []
    for i in range(8):
        b = i ^ 5
        A = i + (2**b) * ((obj ^ i ^ 3) % 8)
        if obj == single_value(A):
            # print([i, b, obj ^ i ^ 3, obj])
            possible.append([i, b, obj ^ i ^ 3])
    return possible


def construct(target):
    bricks = [iter_simple(x) for x in target]
    combs = [0]
    for j in range(len(bricks)):
        print("Combs:", combs)
        x = bricks[-j - 1]
        next_combs = []
        print("Obj:", target[-1 : -j - 2 : -1])
        for i, pw, big in x:
            for z in combs:
                zz = 8 * z
                zz = zz - ((zz // (2**pw)) % 8) * (2**pw) + (2**pw * big) + i
                print(z, zz, simple(zz))
                if simple(zz)[j::-1] == target[-1 : -j - 2 : -1]:
                    next_combs.append(zz)
        combs = next_combs
    sol = None
    for comb in combs:
        if simple(comb) == target:
            print(comb, simple(comb))
            if sol is None or sol > comb:
                sol = comb
    print(sol)


def two():
    construct(OBJECTIVE)


two()
