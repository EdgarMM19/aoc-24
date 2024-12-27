from collections import defaultdict


DAY = 23
TEST = False

FILE = f"{DAY}"
FILE_TEST = f"{DAY}_test"
with open(f"./{FILE_TEST if TEST else FILE}.txt", "r") as file:
    inp = file.readlines()
    inp = [x.strip() for x in inp]


def parse(inp: list[str]):
    nodes = set()
    edges = defaultdict(set)
    for line in inp:
        x, y = line.split("-")
        nodes.add(x)
        nodes.add(y)
        edges[x].add(y)
        edges[y].add(x)
    return list(nodes), edges


def triples(node: str, edges: dict[str, set[str]]):
    found = set()
    for x in edges[node]:
        for y in edges[node]:
            if y in edges[x]:
                found.add(",".join(sorted([x, y, node])))
    return found


def str_to_list(s: str):
    return s.split(",")


def difference_is_one(p: list[str], q: list[str]):
    return len(set(p).symmetric_difference(set(q))) == 2


def difference_is_total(p: list[str], q: list[str]):
    return len(set(p).symmetric_difference(set(q))) == len(p) + len(q)


def brute_force_check(p: list[str], edges: dict[str, set[str]]):
    for i, y in enumerate(p):
        for x in p[i + 1 :]:
            if y not in edges[x]:
                return False
    return True


def combine(p: list[str], q: list[str]):
    sol = []
    i, j = 0, 0
    while i < len(p) and j < len(q):
        if p[i] == q[j]:
            return None
        elif p[i] < q[j]:
            sol.append(p[i])
            i += 1
        else:
            sol.append(q[j])
            j += 1
    return sol + p[i:] + q[j:]


def extend_by_triangles(
    previous: set[str], triangles: set[str], edges: dict[str, set[str]]
):
    previous_lists = [str_to_list(x) for x in previous]
    previous_triangles = [str_to_list(x) for x in triangles]
    new = set()
    for i, p in enumerate(previous_lists):
        if i % 1000 == 0:
            print(i, len(new))
        for q in previous_triangles:
            to_try = combine(p, q)
            if to_try and brute_force_check(list(to_try), edges):
                new.add(",".join(sorted(to_try)))
    return new


def extend_double(previous: set[str], edges: dict[str, set[str]]):
    previous_lists = [str_to_list(x) for x in previous]
    new = set()
    for i, p in enumerate(previous_lists):
        if i % 1000 == 0:
            print(i)
        for q in previous_lists[i + 1 :]:
            to_try = combine(p, q)
            if to_try and brute_force_check(list(to_try), edges):
                new.add(",".join(sorted(to_try)))
    return new


def extend(previous: set[str], edges: dict[str, set[str]]):
    previous_lists = [str_to_list(x) for x in previous]
    new = set()
    for i, p in enumerate(previous_lists):
        for q in previous_lists[i + 1 :]:
            if difference_is_one(p, q):
                y = set(p).difference(set(q)).pop()
                if all([y in edges[x] for x in q]):
                    new.add(",".join(sorted([y] + q)))
    return new


def one(nodes: list[str], edges: dict[str, set[str]]):
    found_triples = set()
    for node in nodes:
        found_triples = found_triples.union(triples(node, edges))
    return found_triples


def two(nodes: list[str], edges: dict[str, set[str]]):
    found_lan = one(nodes, edges)
    triangles = found_lan.copy()
    new_lan = extend_by_triangles(found_lan, triangles, edges)
    while new_lan:
        print(len(new_lan), (len(list(new_lan)[0]) + 1) // 3)
        new_lan, found_lan = extend_by_triangles(new_lan, triangles, edges), new_lan
    print("XXX", len(found_lan), (len(list(found_lan)[0]) + 1) // 3)
    new_lan = extend(found_lan, edges)
    while new_lan:
        print(len(new_lan), (len(list(new_lan)[0]) + 1) // 3)
        new_lan, found_lan = extend(new_lan, edges), new_lan
    print(found_lan)
    return found_lan.pop()


L = parse(inp)

print(len(one(*L)))
print(two(*L))
