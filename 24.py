import random
from typing import Optional

DAY = 24
TEST = False

FILE = f"{DAY}"
FILE_TEST = f"{DAY}_test"
with open(f"./{FILE_TEST if TEST else FILE}.txt", "r") as file:
    inp = file.readlines()
    inp = [x.strip() for x in inp]


def convert_to_easy_format(s: str):
    if s[0] not in ["x", "y", "z"]:
        return s
    return f"{s[0]}{int(s[1:])}"


def parse(inp: list[str]):
    gates: dict[str, Gate] = {}
    separator = next(i for i, x in enumerate(inp) if x == "")
    set_values = inp[:separator]
    unset_values = inp[separator + 1 :]
    for line in set_values:
        gate, value = line.split(": ")
        gates[convert_to_easy_format(gate)] = Gate(
            int(value) == 1, None, None, None, convert_to_easy_format(gate)
        )
    for line in unset_values:
        operation, objective = line.split(" -> ")
        child1, operator, child2 = operation.split(" ")
        gates[convert_to_easy_format(objective)] = Gate(
            None,
            convert_to_easy_format(child1),
            convert_to_easy_format(child2),
            operator,
            convert_to_easy_format(objective),
        )
    for gate in gates.values():
        gate.set_real_name(gates)
    return gates


class Gate:
    def __init__(
        self,
        value: Optional[bool],
        child_1: Optional[str],
        child_2: Optional[str],
        operator: Optional[str],
        original_name: str,
    ):
        self.value = value
        self.child_1 = child_1
        self.child_2 = child_2
        self.operator = operator
        self.original_name = original_name
        self.correct_name = None

    def get_value(self, values: dict[str, "Gate"]):
        if self.value is None:
            assert self.child_1 is not None
            assert self.child_2 is not None
            return self.calculate_gate(
                values[self.child_1].get_value(values),
                values[self.child_2].get_value(values),
                self.operator,
            )
        return self.value

    def set_real_name(self, gates: dict[str, "Gate"]):
        if self.correct_name:
            return self.correct_name
        if self.original_name[0] in ["x", "y"]:
            self.correct_name = self.original_name
        else:
            self.correct_name = f"({gates[self.child_1].set_real_name(gates)} {self.operator} {gates[self.child_2].set_real_name(gates)})"
        return self.correct_name

    @classmethod
    def get_parent_name(cls, name: str, gates: dict[str, "Gate"], timeout=4):
        if timeout == 0:
            return
        for gate in gates.values():
            if gate.child_1 == name or gate.child_2 == name:
                print(f"[{gate.original_name}] := {gate.correct_name}")
                cls.get_parent_name(gate.original_name, gates, timeout - 1)

    @staticmethod
    def calculate_gate(value1, value2, operator):
        if operator == "AND":
            return value1 & value2
        if operator == "OR":
            return value1 | value2
        if operator == "XOR":
            return value1 ^ value2
        raise ValueError(f"Invalid operator: {operator}")

    def bfs(self, gates: dict[str, "Gate"], bad_gates: dict[str, int]):
        if self.child_1:
            gates[self.child_1].bfs(gates, bad_gates)
        if self.child_2:
            gates[self.child_2].bfs(gates, bad_gates)
        bad_gates[self.original_name] += 1

    def inspect(self, gates: dict[str, "Gate"]):
        if self.child_1:
            gates[self.child_1].inspect(
                gates,
            )
        if self.child_2:
            gates[self.child_2].inspect(
                gates,
            )

        print(f"{self.original_name} : {self.child_1} {self.operator} {self.child_2}")


def one(gates: dict[str, Gate]):
    return sum(
        [
            2 ** int(name[1:])
            for name, gate in gates.items()
            if gate.get_value(gates) and name[0] == "z"
        ]
    )


def test_one(
    gates: dict[str, Gate], bad_gates: dict[str, int], pos_count: dict[int, int]
):
    A = random.randint(0, 2**45 - 1)
    B = random.randint(0, 2**45 - 1)
    for i in range(45):
        gates[f"x{i}"].value = (A >> i) & 1
        gates[f"y{i}"].value = (B >> i) & 1
    result = A + B
    for i in range(46):
        if gates[f"z{i}"].get_value(gates) != (result >> i) & 1:
            pos_count[i] += 1
            gates[f"z{i}"].bfs(gates, bad_gates)


def two(gates: dict[str, Gate]):
    names = [name for name, _ in gates.items()]
    for name in names:
        print(name)
        for name2 in names:
            try:
                if (
                    name[0] in ["x", "y"]
                    or name2[0] in ["x", "y"]
                    or int(gates[name].child_1[1:]) < 34
                    or int(gates[name].child_2[1:]) < 34
                ):
                    continue
            except:
                pass
            try:
                copy_gates = {name: gate for name, gate in gates.items()}
                copy_gates[name], copy_gates[name2] = gates[name2], gates[name]
                bad_gates = {name: 0 for name in gates}
                pos_count = {i: 0 for i in range(46)}
                for _ in range(5):
                    test_one(copy_gates, bad_gates, pos_count)
                if sum(bad_gates.values()) == 0:
                    print(f"Swapped {name} and {name2}")
                    print(pos_count)
                    return
            except:
                pass


L = parse(inp)
print(",".join(sorted(["dkr", "z05", "z15", "htp", "z20", "hhh", "rhv", "ggk"])))
print(one(L))
