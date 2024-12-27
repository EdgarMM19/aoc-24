with open("/Users/edgar/Downloads/aoc/2.txt", "r") as file:
    inp = file.readlines()


def first(line: list[int]):
    if line[0] > line[-1]:
        line.reverse()
    return all(x < y < x + 4 for x, y in zip(line, line[1:]))


sol = 0
sol2 = 0
for line in inp:
    line = [int(x) for x in line.split()]
    sol += first(line)
    sol2 += any(
        [first(line)] + [first(line[:i] + line[i + 1 :]) for i in range(len(line))]
    )

print(sol, sol2)
