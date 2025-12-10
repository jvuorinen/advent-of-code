from re import findall
from ortools.sat.python import cp_model
from utils import read, print_answers

raw = read(2025, 10).split("\n")

machines = []
for line in raw:
    a, b, c = findall(r"\[(.*)\] (.*)\{(.*)}", line)[0]
    target = tuple([x == "#" for x in a])
    buttons = [tuple(map(int, x.split(","))) for x in findall(r"\(([,\d]*)\)", b)]
    jolts = tuple(map(int, c.split(",")))
    machines.append((target, buttons, jolts))


def bfs(machine):
    target, buttons, _ = machine

    start = tuple([False] * len(target))
    batch = [start]
    for i in range(1000):
        _batch = []
        for state in batch:
            if state == target:
                return i
            for b in buttons:
                _state = list(state)
                for ix in b:
                    _state[ix] = not _state[ix]
                _batch.append(tuple(_state))
        batch = _batch


def solve_ilp(machine):
    _, buttons, jolts = machine

    model = cp_model.CpModel()
    x = [model.NewIntVar(0, 1000, f"x{i}") for i in range(len(buttons))]

    coeffs = [[0 for _ in range(len(buttons))] for _ in range(len(jolts))]
    for i, b in enumerate(buttons):
        for j in b:
            coeffs[j][i] = 1

    for cf, jolt in zip(coeffs, jolts):
        ixs = [i for i, val in enumerate(cf) if val]
        model.Add(sum(x[i] for i in ixs) == jolt)

    model.Minimize(sum(x))

    solver = cp_model.CpSolver()
    solver.Solve(model)
    return sum(solver.Value(v) for v in x)


a1 = sum(map(bfs, machines))
a2 = sum(map(solve_ilp, machines))

print_answers(a1, a2, day=10)
