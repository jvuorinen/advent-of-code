import numpy as np
from utils import read, print_answers

raw = read(2025, 7).split("\n")

chars = np.array(list(map(list, raw)))
beams = (chars[0]=='S').astype(int)

a1 = 0
for line in chars[1:]:
    spl = beams * (line=='^')
    a1 += sum(spl > 0)
    beams += np.roll(spl, 1)
    beams += np.roll(spl, -1)
    beams[spl > 0] = 0

a2 = sum(beams)

print_answers(a1, a2, day=7)

