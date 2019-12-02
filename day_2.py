import logging

logging.getLogger().setLevel('DEBUG')

def add_operation(data, in_a_loc, in_b_loc, res_loc):
    logging.debug("Performing ADD operation with args ({} {} {})".format(in_a_loc, in_b_loc, res_loc))

    logging.debug("Data before: " + str(data))

    res = data.copy()
    a, b, r = res[res[in_a_loc]], res[res[in_b_loc]], res[res_loc]
    result = a + b
    res[r] = result

    logging.debug(f"Calculation result: {a} + {b} = {result}, storing to location {r}")

    logging.debug("Data after : " + str(res))
    return res

def mul_operation(data, in_a_loc, in_b_loc, res_loc):
    logging.debug("Performing MUL operation with args ({} {} {})".format(in_a_loc, in_b_loc, res_loc))

    logging.debug("Data before: " + str(data))
    
    res = data.copy()
    a, b, r = res[res[in_a_loc]], res[res[in_b_loc]], res[res_loc]
    result = a * b
    res[r] = result

    logging.debug(f"Calculation result: {a} * {b} = {result}, storing to location {r}")

    logging.debug("Data after : " + str(res))
    return res

def parse_command(data, cursor):
    op_codes = {
        1: {'op': add_operation, 'n_args': 3},
        2: {'op': mul_operation, 'n_args': 3}
    }

    op = op_codes.get(data[cursor])['op']
    n_args = op_codes.get(data[cursor])['n_args']
    arg_locs = list(range(cursor + 1, cursor + n_args + 1)) 
    next_cursor = cursor + n_args + 1

    return op, arg_locs, next_cursor

def compute(data):
    data = data.copy()
    cursor = 0
    iteration = 0
    while data[cursor] != 99:        
        logging.debug("Iteration: " + str(iteration))
        logging.debug("Parsing data at cursor location " + str(cursor))
        op, arg_locs, next_cursor = parse_command(data, cursor)
        data = op(data, *arg_locs)
        cursor = next_cursor
        iteration += 1
        if iteration == 1000:
            raise RuntimeError("Possible infinite loop detected, aborting")
    return data

def get_result(data):
    # Fix 1202 bug
    data = data.copy()
    data[1] = 12
    data[2] = 2

    result = compute(data)[0]
    return result

if __name__ == "__main__":
    logging.getLogger().setLevel("INFO")

    data = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,13,19,1,9,19,23,2,13,23,27,2,27,13,31,2,31,10,35,1,6,35,39,1,5,39,43,1,10,43,47,1,5,47,51,1,13,51,55,2,55,9,59,1,6,59,63,1,13,63,67,1,6,67,71,1,71,10,75,2,13,75,79,1,5,79,83,2,83,6,87,1,6,87,91,1,91,13,95,1,95,13,99,2,99,13,103,1,103,5,107,2,107,10,111,1,5,111,115,1,2,115,119,1,119,6,0,99,2,0,14,0]

    print("Part 1 result:",  str(get_result(data)))

