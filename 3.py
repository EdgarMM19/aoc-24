import re


with open("/Users/edgar/Downloads/aoc/3.txt", "r") as file:
    inp = file.readlines()
    line = "".join(inp)

REGEX1 = r"mul\(\d+,\d+\)"

REGEX2 = r"(mul\(\d+,\d+\))|(don\'t)|(do)"


def first(line: str):
    matches = [match[4:-1].split(",") for match in re.findall(REGEX1, line)]
    return sum(int(match[0]) * int(match[1]) for match in matches)


def second(line: str):
    matches = re.findall(REGEX2, line)
    enabled = True
    sol = 0
    for match in matches:
        if match[0] and enabled:
            x = match[0][4:-1].split(",")
            sol += int(x[0]) * int(x[1])
        if match[1]:
            enabled = False
        if match[2]:
            enabled = True
    return sol


print(first(line), second(line))
