from collections import defaultdict
from functools import cmp_to_key


FILE = "5"
# FILE = "5_test"
with open(f"/Users/edgar/Downloads/aoc/{FILE}.txt", "r") as file:
    inp = file.readlines()
    inp = [x.strip() for x in inp]
    i = inp.index("")
    rules, cases = inp[:i], inp[i + 1 :]


def one(rules: list[str], cases: list[str]):
    rules_g = defaultdict(set)
    for rule in rules:
        x, y = rule.split("|")
        rules_g[x].add(y)
    sol = 0
    other_cases = []
    for case in cases:
        numbs = case.split(",")
        prev = set()
        for n in numbs:
            if rules_g[n].intersection(prev):
                break
            prev.add(n)
        else:
            sol += int(numbs[len(numbs) // 2])
            continue
        other_cases.append(numbs)
    print(sol)
    return rules_g, other_cases


def two(rules_g: dict[str, set[str]], cases: list[list[str]]):
    def order(a: str, b: str):
        return -1 if a in rules_g[b] else 1

    sol = sum(
        int(sorted(case, key=cmp_to_key(order))[len(case) // 2]) for case in cases
    )
    print(sol)


rules_g, other_cases = one(rules, cases)
two(rules_g, other_cases)


def print_array(lines: list[str]):
    print("\n".join(lines))
    print()
