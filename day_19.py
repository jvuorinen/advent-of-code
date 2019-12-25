import logging
logging.basicConfig(format='%(levelname)s %(message)s')
from functools import partial

from common import *
from computer import Computer

HEURISTIC_MAX = 5_000
OBJECT_SIZE = 100

class Scanner:
    def __init__(self, program):
        self.c = Computer(program)
    
    def scan(self, x, y):
        self.c.add_input(y)
        self.c.add_input(x)
        self.c.run()
        result = self.c.state.outputs[-1]    
        self.c.reset()    
        return result


def solve_1(scanner, high=50):
    coords = {}
    for x in range(high+1):
        for y in range(high+1):
            coords[(x, y)] = scanner.scan(x, y)
    a = coords_to_array(coords)
    print_array(a, {0: "░", 1: "▓"})
    print(f"Step 1 answer: {sum(sum(a==1))}")


def scan_row(computer, row_i):
    result = []
    for col_i in range(HEURISTIC_MAX):
        computer.reset()
        computer.add_input(row_i)
        computer.add_input(col_i)
        computer.run()
        result.append(computer.state.outputs[-1])
    computer.reset()
    return np.array(result)
    

def find_one_spot(func):
    range_len = len(range(0, HEURISTIC_MAX))

    tried = set()
    for i in range(2, range_len):
        sample_points = range(0, HEURISTIC_MAX+1, int(HEURISTIC_MAX/i))
        for s in sample_points:
            if s not in tried:
                res = func(s)
                if res == 1:
                    return s
                else:
                    tried.add(s)


def find_func_change_point(func, low, high, return_first):
    """Returns the first point where f_low is different than f_high"""
    while high-low > 1:
        mid = int((high-low)/2) + low

        f_low = func(low)
        f_mid = func(mid)
        # f_high = func(high)

        if f_mid == f_low: low = mid
        else: high = mid

    if return_first:
        return low
    else:
        return high


def get_func_one_area(func):
    """Returns the low and high points where func is 1"""
    # First find a place where func is one
    one_spot = find_one_spot(func)

    # Then find the low and high points of 
    # these areas with logarithmic seach
    low = find_func_change_point(func, low=0, high=one_spot, return_first=False)
    high = find_func_change_point(func, low=one_spot, high=HEURISTIC_MAX, return_first=True)
    
    return low, high


def find_tractor_area(scanner, ref_x, ref_y):
    # Find out the 1-areas on the row and col intersecting at ref point
    row_func = lambda p: scanner.scan(x=p, y=ref_y)
    col_func = lambda p: scanner.scan(x=ref_x, y=p)

    row_area = get_func_one_area(row_func)
    col_area = get_func_one_area(col_func)

    return (row_area, col_area)


def get_info(scanner, x, y):
    row_area, col_area = find_tractor_area(scanner, x, y)
    
    row_first = row_area[1] - OBJECT_SIZE + 1
    col_first = col_area[1] - OBJECT_SIZE + 1

    row_offset = row_first - x
    col_offset = col_first - y

    # print(f"At {x, y}, beam area on row: {row_area}, beam area on col: {col_area}")
    if x < row_area[0]:
        print("Above cone")
    if x > row_area[1]:
        print("Above cone") 

    return row_offset, col_offset, row_area, col_area

def solve_2(scanner):
    # Initial guess
    x, y = 800, 500
    row_offset, col_offset, _, _ = get_info(scanner, x, y)         

    STEP = 20
    while (row_offset != 0) | (col_offset != 0):
        print(f"Detailed search in progress, at {x, y}, offsets now: {row_offset, col_offset}")

        row_offset, col_offset, _, _ = get_info(scanner, x, y)         
        if (row_offset > 0):
            x -= STEP
        elif (row_offset < 0):
            x += STEP

        row_offset, col_offset, _, _ = get_info(scanner, x, y)            
        if (col_offset > 0):
            y += STEP
        elif (col_offset < 0):
            y -= STEP

        if ((abs(row_offset) + abs(col_offset)) < (4*STEP) ) & (STEP > 1):
            new_step = int(STEP/2)
            print(f"Decreasing step from {STEP} to {new_step}")
            STEP = new_step     

    print(f"Step 2 answer: {x*10_000+y}")


if __name__ == "__main__":
    logging.getLogger().setLevel("WARNING")

    raw_in = read_input('data/day_19.txt')
    program = [int(i) for i in raw_in[0].split(',')]
    scanner = Scanner(program)

    solve_1(scanner, 50)
    solve_2(scanner)
