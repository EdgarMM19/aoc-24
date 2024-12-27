from copy import deepcopy
import sys

sys.setrecursionlimit(100000)

FILE = "7"
# FILE = "7_test"
with open(f"/Users/edgar/Downloads/aoc/{FILE}.txt", "r") as file:
    inp = file.readlines()


def parse(line: str):
    obj, numbs = line.split(": ")
    return int(obj), [int(x) for x in numbs.split(" ")]


cases = [parse(x) for x in inp]


def calculate(objective: int, numbers: list[int], cheat: bool = False):
    if len(numbers) == 1:
        return numbers[0] == objective

    last = numbers[-1]
    if objective % last == 0 and calculate(objective // last, numbers[:-1], cheat):
        return True
    if cheat:
        digs = len(str(last))
        if objective % 10**digs == last and calculate(
            objective // 10**digs, numbers[:-1], cheat
        ):
            return True
    return calculate(objective - last, numbers[:-1], cheat)


def one(cases: list[tuple[int, list[int]]]):
    return sum([obj if calculate(obj, numbers) else 0 for obj, numbers in cases])


def two(cases: list[tuple[int, list[int]]]):
    return sum([obj if calculate(obj, numbers, True) else 0 for obj, numbers in cases])


print(one(cases))
print(two(cases))
