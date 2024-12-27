with open("/Users/edgar/Downloads/a.txt", "r") as file:
    inp = file.readlines()

a, b = [], []
for line in inp:
    aa, bb = line.split()
    a.append(int(aa))
    b.append(int(bb))
a.sort()
b.sort()
sol = 0
i = 0
prev = None
prev_count = 0
for x in a:
    if x == prev:
        sol += prev_count
        continue
    prev_count = 0
    while i < len(b) and x > b[i]:
        i += 1
    while i < len(b) and x == b[i]:
        prev_count += x
        i += 1
    sol += prev_count
    prev = x

print(sol)
