import logging
logging.getLogger().setLevel("INFO")

def add_operation(data, in_a_loc, in_b_loc, res_loc):
    logging.debug("Doing ADD operation {} {} => {}".format(in_a_loc, in_b_loc, res_loc))

    res = data.copy()
    res[res_loc] = res[in_a_loc] + res[in_b_loc]
    return res

def mul_operation(data, in_a_loc, in_b_loc, res_loc):
    logging.debug("Doing MUL operation {} {} => {}".format(in_a_loc, in_b_loc, res_loc))

    res = data.copy()
    res[res_loc] = res[in_a_loc] * res[in_b_loc]
    return res

def parse_command(data, cursor):



    return operation, args, next_cursor

def compute(data, op_codes):
    cursor = 0
    for _ in range(3):

if __name__ == "__main__":
    op_codes = {
        1: add_operation
        2: mul_operation
    }

    data = [1,9,10,3,2,3,11,0,99,30,40,50]
