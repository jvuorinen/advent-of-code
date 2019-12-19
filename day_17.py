import logging
logging.basicConfig(format='%(levelname)s %(message)s')
import re
from itertools import groupby
import numpy as np

from common import *
from computer import Computer

CHARS = {n: chr(n) for n in range(256)}

def to_intcode(s):
    return [ord(c) for c in s]

def output_to_array(o):
    ncols = o.index(10)
    l = [i for i in o if i != 10]
    nrows = int(len(l) / ncols)

    return np.array(l).reshape(nrows, ncols)


def substr_gen(s, min_len, max_len, randomize=False, start_from_longest=True):
    """Yields all substrings from s either longest first, or in random order"""
    MIN_LEN = min_len
    MAX_LEN = max_len

    found = set()
    illegal = {'A', 'B', 'C'} # Used to mark found subtrings

    if start_from_longest:
        lengths = range(MAX_LEN, MIN_LEN-1, -1)
    else:
        lengths = range(MIN_LEN, MAX_LEN+1)

    if randomize:
        all_ss = set()
        for len_sub in lengths:
            substrings = (s[i: i+len_sub] for i in range(0, len(s) - len_sub + 1))
            for ss in substrings:
                count = s.count(ss)
                if (count > 1) & (ss not in found) & (illegal & set(ss) == set()):
                    found |= {ss}
                    all_ss |= {ss}
        for ss in all_ss:
            yield ss            

    else:
        for len_sub in lengths:
            substrings = (s[i: i+len_sub] for i in range(0, len(s) - len_sub + 1))
            for ss in substrings:
                count = s.count(ss)
                if (count > 1) & (ss not in found) & (illegal & set(ss) == set()):
                    found |= {ss}
                    yield ss


def replace_subsstr(s, ss, c):
    return s.replace(ss, c*len(ss))

def get_indexes(s, ss):
    it = re.finditer(ss, s)
    return [m.start(0) for m in it]

def generate_main_routine(s, ss_a, ss_b, ss_c):
    ind_a = get_indexes(s, ss_a)
    ind_b = get_indexes(s, ss_b)
    ind_c = get_indexes(s, ss_c)

    inds = [('A', i) for i in ind_a] + [('B', i) for i in ind_b] + [('C', i) for i in ind_c] 
    result = ",".join(x for x, _ in sorted(inds, key=lambda x: x[1]))

    return result

def fold(s):
    tmp = [(a, str(len(list(b)))) for a, b in groupby(s)]
    return ",".join(a if a in ('R', 'L') else b for a, b in tmp)

def unfold(s):
    return "".join([x if x in ('R', 'L') else int(x)*'F' for x in s.split(',')])

def get_components(s):
    inf_a, inf_b, inf_c, inf_m = 0,0,0,0
    i_ssa, i_ssb, i_ssc = 0, 0, 0
    sg_a = substr_gen(s,randomize=True, min_len=int(len(s)*0.1), max_len=int(len(s)*0.4))
    for ss_a in sg_a:
        i_ssa += 1
        if (i_ssa % 10 == 0):
            logging.debug(f"Calculating - substrings tried: {i_ssa}, {i_ssb}, {i_ssc} - infeasibles:  M {inf_m}, FA {inf_a}, FB {inf_b}, FC {inf_c}")

        s_a = replace_subsstr(s, ss_a, 'A')
        sg_b = substr_gen(s_a, min_len=int(len(s)*0.1), max_len=int(len(s)*0.3))
        for ss_b in sg_b:            
            i_ssb += 1

            # Hack to make it search faster, also 
            # makes the search not exhaustive...
            # if i_ssb % 1000 == 0:
            #     break

            s_b = replace_subsstr(s_a, ss_b, 'B')
            sg_c = substr_gen(s_b, min_len=1, max_len=int(len(s)*0.2))
            for ss_c in sg_c:
                i_ssc += 1

                # Hack to make it search faster, also 
                # makes the search not exhaustive...
                # if i_ssc % 1_000 == 0:
                #     skips += 1
                #     break

                s_c = replace_subsstr(s_b, ss_c, 'C')
                if set(s_c) == {'A', 'B', 'C'}:
                    m = generate_main_routine(s, ss_a, ss_b, ss_c)  
                    if (len(m) > 20):
                        inf_m += 1
                        continue
                    f_a = fold(ss_a)
                    f_b = fold(ss_b)
                    f_c = fold(ss_c)
                    errors = 0
                    if (len(f_a) > 20): 
                        inf_a += 1
                        errors += 1
                    if (len(f_b) > 20): 
                        inf_b += 1
                        errors += 1
                    if (len(f_c) > 20): 
                        inf_c += 1
                        errors += 1
                    if errors == 0:
                        logging.debug(f"FEASIBLE SOLUTION FOUND on iteration {i_ssc} - tries: {i_ssa}, {i_ssb}, {i_ssc} - infeasibles:  M {inf_m}, FA {inf_a}, FB {inf_b}, FC {inf_c}")
                        return m, f_a, f_b, f_c
    logging.error("No components found!")

# path = unfold('R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2')
# m, f_a, f_b, f_c = get_components(path)

def solve_1(program):
    c = Computer(program)
    c.run()

    o = c.state.outputs
    a = output_to_array(o)  
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


def get_path(a):
    """The horror..."""
    loc_r, loc_c = map(lambda x: x[0], np.where(a == ord("^")))
    hdng = 'N'

    commands = []

    while True:
        logging.debug(f"Now at {loc_r, loc_c}")
        # Determine next hdng
        if hdng == 'N':
            if loc_c > 0:
                left = chr(a[loc_r, loc_c-1])
            else:
                left = '.'
            try:
                right = chr(a[loc_r, loc_c+1])
            except:
                right = '.'

            if left =='#': 
                hdng = 'W'
                commands.append('L')
                logging.debug(f"Turning LEFT toward {hdng}")
            elif right == '#': 
                hdng = 'E'
                commands.append('R')
                logging.debug(f"Turning RIGHT toward {hdng}")
            else:
                logging.debug(f"Journey ended")
                return "".join(commands)
        elif hdng == 'S':
            try:
                left = chr(a[loc_r, loc_c+1])
            except:
                left = '.'
            if loc_c > 0:
                right = chr(a[loc_r, loc_c-1])
            else:
                right = '.'

            if left =='#': 
                hdng = 'E'
                commands.append('L')
                logging.debug(f"Turning LEFT toward {hdng}")
            elif right == '#': 
                hdng = 'W'
                commands.append('R')
                logging.debug(f"Turning RIGHT toward {hdng}")
            else:
                logging.debug(f"Journey ended")
                return "".join(commands)
        elif hdng == 'W':
            try:
                left = chr(a[loc_r+1, loc_c])
            except:
                left = '.'
            if loc_r > 0:
                right = chr(a[loc_r-1, loc_c])
            else:
                right = '.'
            
            if left =='#': 
                hdng = 'S'
                commands.append('L')
                logging.debug(f"Turning LEFT toward {hdng}")
            elif right == '#': 
                hdng = 'N'
                commands.append('R')
                logging.debug(f"Turning RIGHT toward {hdng}")
            else:
                logging.debug(f"Journey ended")
                return "".join(commands)
        elif hdng == 'E':
            if loc_r > 0:
                left = chr(a[loc_r-1, loc_c])
            else:
                left = '.'
            try:
                right = chr(a[loc_r+1, loc_c])
            except:
                right = '.'
            
            if left =='#': 
                hdng = 'N'
                commands.append('L')
                logging.debug(f"Turning LEFT toward {hdng}")
            elif right == '#': 
                hdng = 'S'
                commands.append('R')
                logging.debug(f"Turning RIGHT toward {hdng}")
            else:
                logging.debug(f"Journey ended")
                return "".join(commands)


        # Then walk
        logging.debug("Walking forward")
        if hdng == 'N':
            peek = chr(a[loc_r-1, loc_c])
            while peek == '#':
                commands.append('F')
                loc_r -= 1
                if loc_r > 0:
                    peek = chr(a[loc_r-1, loc_c])
                else:
                    peek = '.'

        if hdng == 'S':
            peek = chr(a[loc_r+1, loc_c])
            while peek == '#':
                commands.append('F')
                loc_r += 1
                try:
                    peek = chr(a[loc_r+1, loc_c])
                except:
                    peek = '.'
              
        if hdng == 'W': 
            peek = chr(a[loc_r, loc_c-1])
            while peek == '#':
                commands.append('F')
                loc_c -= 1
                if loc_c > 0:
                    peek = chr(a[loc_r, loc_c-1])
                else:
                    peek = '.'

        if hdng == 'E':
            peek = chr(a[loc_r, loc_c+1])
            while peek == '#':
                commands.append('F')
                loc_c += 1
                try:
                    peek = chr(a[loc_r, loc_c+1])
                except:
                    peek = '.'


def solve_2(program):
    # First find the path to goal
    c = Computer(program)
    c.run()
    o = c.state.outputs
    a = output_to_array(o)  
    path = get_path(a)

    # Break it to components and build the solution program
    m, f_a, f_b, f_c = get_components(path) # Takes many hours...
    solution_text = "\n".join([m, f_a, f_b, f_c, 'n']) + "\n"

    # Run the solution program
    solution_code = list(reversed(to_intcode(solution_text))) # Inputs are popped from the end
    c = Computer(program)
    c.state.mem[0] = 2
    c.state.input_stack = solution_code
    c.run()

    s = c.state.outputs[-1]
    print(f"Part 2 answer: {s}")

    
if __name__ == "__main__":
    logging.getLogger().setLevel("INFO")

    raw_in = read_input('data/day_17.txt')
    program = [int(i) for i in raw_in[0].split(',')]


    solve_1(program)
    solve_2(program)