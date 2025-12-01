from utils import read, print_answers

a1 = a2 = 0
r = 50
for x in read(2025, 1).split("\n"):
    a = -1 if x[0] == "L" else 1
    b = int(x[1:])
    n = (a * b)

    d, m = divmod(r + n, 100)
    a1 += (m == 0)

    if n > 0:
        a2 += d
    elif r > 0:
        a2 += abs(d) + (m == 0)
    else:
        a2 += abs(d) - 1 + (m == 0)

    r = m


print_answers(a1, a2, day=1)
