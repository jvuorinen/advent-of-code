from time import time
from re import findall
from ortools.sat.python import cp_model
from utils import read, print_answers

raw = read(2025, 10).split("\n")


machines = []
for line in raw:
    a, b, c = findall(r"\[(.*)\] (.*)\{(.*)}", line)[0]
    target = tuple([x == "#" for x in a])
    buttons = [tuple(map(int, x.split(","))) for x in findall(r"\(([,\d]*)\)", b)]
    buttons = sorted(buttons, key=lambda x: (len(x), x))[::-1]
    jolts = tuple(map(int, c.split(",")))
    machines.append((target, buttons, jolts))


def do_forced_moves(buttons, jolts, cnt):
    for i, n in enumerate(jolts):
        if (n > 0) and len(bs := [b for b in buttons if i in b]) == 1:
            # print(f"forced! {buttons} {jolts} {cnt} =>")
            _jolts = list(jolts)
            for j in bs[0]:
                _jolts[j] -= n
            jolts = tuple(_jolts)
            cnt = cnt + n
            # print(f"{buttons} {jolts} {cnt}")
            # print()
            return buttons, jolts, cnt

def is_infeasible(buttons, jolts, cnt, best):
    if (cnt > best[0]) or (len(buttons) == 0) or any([x < 0 for x in jolts]):
        return True
    needed = set([i for i, x in enumerate(jolts) if x > 0]) 
    available = set.union(*[set(x) for x in buttons])
    if not ((needed & available) == needed):
        return True
    return False


def is_possible(button, jolts):
    bs = button
    if any([i in bs for i in button if jolts[i] == 0]):
        return False
    return True


def dfs(buttons, jolts, cnt=0, best=None):
    if best == None:
        best = [300]
    if all([x==0 for x in jolts]):
        best[0] = min(best[0], cnt)
        return cnt
    if (_state := do_forced_moves(buttons, jolts, cnt)):
        return dfs(*_state)

    buttons = [b for b in buttons if is_possible(b, jolts)]

    if is_infeasible(buttons, jolts, cnt, best):
        return 999

    _pressed = list(jolts)
    for b in buttons[0]:
        _pressed[b] -= 1

    return min(
        dfs(buttons, _pressed, cnt + 1, best),
        dfs(buttons[1:], jolts, cnt, best),
    )



machine = machines[44]
_, buttons, jolts = machine
%time dfs(buttons, list(jolts))

def solve_all(machines):
    a2 = 0
    for i, machine in enumerate(machines):
        if i in [18, 21, 33, 36]:
            continue
        _, buttons, jolts = machine
        ilp = solve_ilp(machine)

        a = dfs(buttons, list(jolts))
        print(i, a, a == ilp)
    return a2

a2 = solve_all(machines)

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


a2 = sum(map(solve_ilp, machines))

print_answers(a1, a2, day=10)

import numpy as np

d = len(buttons)
len(jolts)
A = np.zeros((len(buttons), len(jolts)), int)

for i, b in enumerate(buttons):
    for x in b:
        A[i, x] = 1

A