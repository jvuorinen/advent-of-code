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


def build_lookups(buttons):
    everybody = set.union(*[set(b) for b in buttons])
    nb = len(buttons)

    cant_avoid = []
    for i in range(nb):
        d = {}
        for e in everybody:
            relevant = [x for x in buttons[i:] if e in x]
            omnipresent = {ee for ee in everybody if all([ee in x for x in relevant])} - {e}
            if omnipresent:
                d[e] = omnipresent
        cant_avoid.append(d)

    available = []
    for i in range(nb):
        available.append(set.union(*[set(x) for x in buttons[i:]]))

    return cant_avoid, available


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
            return jolts, cnt
    return jolts, cnt


def dfs(buttons, jolts, ix=0, cnt=0, cant_avoid=None, available=None, tally=None):
    if tally is None:
        tally = {
            "best": 500,
            "start_time": time(),
        }
    if cnt > 300:
        return

    if cant_avoid is None:
        cant_avoid, available = build_lookups(buttons)
    # print(jolts, ix, cnt, br)
    if len(buttons) == 0:
        if sum(jolts) == 0:
            return cnt
        return 

    jolts, cnt = do_forced_moves(buttons, jolts, cnt)

    # Infeasibilty checks
    needed = set([i for i, x in enumerate(jolts) if x > 0])
    if any([x < 0 for x in jolts]):
        return

    if not ((needed & available[ix]) == needed):
        return

    dontpush = set([i for i, x in enumerate(jolts) if x == 0])
    for x in needed:
        if dontpush & cant_avoid[ix].get(x, set()):
            return

    _pressed = list(jolts)
    for b in buttons[0]:
        _pressed[b] -= 1

    best = (
        dfs(buttons[:], _pressed, ix, cnt + 1, cant_avoid, available, tally)
        or dfs(buttons[1:], _pressed, ix + 1, cnt + 1, cant_avoid, available, tally)
        or dfs(buttons[1:], jolts, ix + 1, cnt, cant_avoid, available, tally)
    )

    return best


machine = machines[18]
_, buttons, jolts = machine
dfs(buttons, list(jolts))

def solve_all(machines):
    a2 = 0
    for i, machine in enumerate(machines):
        _, buttons, jolts = machine
        # solve_ilp(machine)

        a2 += dfs(buttons, list(jolts))
        print(i, a2)
    return a2

%time a2 = solve_all(machines)

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
