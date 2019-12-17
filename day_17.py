import logging
logging.basicConfig(format='%(levelname)s %(message)s')

from common import *
from computer import Computer

CHARS = {n: chr(n) for n in range(256)}

def make_array(o):
    ncols = o.index(10)
    l = [i for i in o if i != 10]
    nrows = int(len(l) / ncols)

    return np.array(l).reshape(nrows, ncols)


def solve_1(program):
    c = Computer(program)
    c.run()

    o = c.state.outputs
    a = make_array(o)  
    # print_array(a, CHARS)

    SCF_CHAR = 35
    params = []
    rows, cols = a.shape
    for r in range(1, rows-1):
        for c in range(1, cols-1):
            up = a[r+1, c]
            down = a[r-1, c]
            left = a[r, c-1]
            right = a[r, c+1]
            if a[r, c] == up == down == left == right == SCF_CHAR:
                params.append(c*r) 
    print(f"Part 1 answer: {sum(params)}")

    
if __name__ == "__main__":
    logging.getLogger().setLevel("DEBUG")

    raw_in = read_input('data/day_17.txt')
    program = [int(i) for i in raw_in[0].split(',')]


    solve_1(program)