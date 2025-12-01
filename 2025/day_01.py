from utils import read, print_answers

a1 = a2 = 0
r = 50
for x in read(2025, 1).split("\n"):
    n = int(x[1:]) * (-1, 1)[x[0] == "R"]
    d, m = divmod(r + n, 100)
    a1 += (m == 0)
    if n > 0:
        a2 += d
    else:
        a2 += abs(d) + (m == 0)
        if r == 0:
            a2 -= 1
    r = m

print_answers(a1, a2, day=1)
