import logging

def add_operation(data, in_a_loc, in_b_loc, res_loc):
    logging.debug("Performing ADD operation {} {} => {}".format(in_a_loc, in_b_loc, res_loc))

    res = data.copy()
    a, b, r = res[in_a_loc], res[in_b_loc], res[res_loc]
    res[r] = res[a] + res[b]

    logging.debug("Data before: " + str(data))
    logging.debug("Data after : " + str(res))
    return res

def mul_operation(data, in_a_loc, in_b_loc, res_loc):
    logging.debug("Performing MUL operation {} {} => {}".format(in_a_loc, in_b_loc, res_loc))

    res = data.copy()
    a, b, r = res[in_a_loc], res[in_b_loc], res[res_loc]
    res[r] = res[a] * res[b]

    logging.debug("Data before: " + str(data))
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
    iterations = 0
    while data[cursor] != 99:
        logging.debug("Parsing data at cursor location " + str(cursor))
        op, arg_locs, next_cursor = parse_command(data, cursor)
        data = op(data, *arg_locs)
        cursor = next_cursor
        iterations += 1
        if iterations == 1000:
            raise RuntimeError("Possible infinite loop detected, aborting")
    return data

if __name__ == "__main__":
    logging.getLogger().setLevel("DEBUG")

    
    data = [2,3,0,3,99]

    print("Result:",  str(compute(data)))

