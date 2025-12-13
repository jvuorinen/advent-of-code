from time import time
from dataclasses import dataclass, field
from re import findall
from tqdm import tqdm
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
    update = False
    while _state := _do_forced_moves(buttons, jolts, cnt):
        buttons, jolts, cnt, update = _state
    return buttons, jolts, cnt, update

def _do_forced_moves(buttons, jolts, cnt):
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
            return buttons, jolts, cnt, True

def is_infeasible(buttons, jolts, cnt, tally):
    if (cnt > tally.best) or (len(buttons) == 0) or any([x < 0 for x in jolts]):
        return True
    if tally.is_overtime():
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


@dataclass
class Tally:
    best = 300
    start_ts: float = field(default_factory=time)
    def is_overtime(self):
        return time() - self.start_ts > 10


def dfs(buttons, jolts, cnt=0, tally=None):
    tally = tally or Tally()

    if all([x==0 for x in jolts]):
        tally.best = min(tally.best, cnt)
        return cnt

    buttons, jolts, cnt, update = do_forced_moves(buttons, jolts, cnt)
    if update:
        return dfs(buttons, jolts, cnt, tally)

    buttons = [b for b in buttons if is_possible(b, jolts)]

    if is_infeasible(buttons, jolts, cnt, tally):
        return 999

    _pressed = list(jolts)
    for b in buttons[0]:
        _pressed[b] -= 1

    return min(
        dfs(buttons, _pressed, cnt + 1, tally),
        dfs(buttons[1:], jolts, cnt, tally),
    )


machine = machines[18]
_, buttons, jolts = machine
%time dfs(buttons, list(jolts))

def solve_all(machines):
    problems = 0
    for machine in tqdm(machines):
        _, buttons, jolts = machine
        # ilp = solve_ilp(machine)

        a = dfs(buttons, list(jolts))
        if a == 999:
            problems += 1
        # print(a, i, len(buttons))
    print(f"Unsolved: {problems}")

solve_all(machines)

import numpy as np

A = np.zeros((len(buttons), len(jolts)), int)
for i, b in enumerate(buttons):
    for x in b:
        A[i, x] = 1
A

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
