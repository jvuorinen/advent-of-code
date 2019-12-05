from typing import List
import logging

from common import read_input

logging.getLogger().setLevel('DEBUG')

# TODO Should be dynamic
INPUT_VALUE = 1



def add_operation(data, args_raw, arg_values, pointer):
    logging.debug("Performing ADD operation")
    logging.debug("Raw args: {}, arg values: {}".format(args_raw, arg_values))   
    # logging.debug("Data before: " + str(data))

    res = data.copy()
    a, b = arg_values[0], arg_values[1]
    result = a + b
    res_address = args_raw[-1]
    res[res_address] = result

    logging.debug(f"Calculation result: {a} + {b} = {result}, storing to address {res_address}")
    # logging.debug("Data after : " + str(res))
    return res, pointer + len(args_raw) + 1

def mul_operation(data, args_raw, arg_values, pointer):
    logging.debug("Performing MUL operation")
    logging.debug("Raw args: {}, arg values: {}".format(args_raw, arg_values))   
    # logging.debug("Data before: " + str(data))
    
    res = data.copy()
    a, b = arg_values[0], arg_values[1]
    result = a * b
    res_address = args_raw[-1]
    res[res_address] = result

    logging.debug(f"Calculation result: {a} * {b} = {result}, storing to address {res_address}")
    # logging.debug("Data after : " + str(res))
    return res, pointer + len(args_raw) + 1

def save_operation(data, args_raw, arg_values, pointer):
    logging.debug("Performing SAV operation")
    logging.debug("Raw args: {}, arg values: {}".format(args_raw, arg_values))   
    # logging.debug("Data before: " + str(data))
    
    value = INPUT_VALUE #TODO Change to actual input

    res = data.copy()
    res_address = args_raw[-1]
    res[res_address] = value

    # logging.debug("Data after : " + str(res))
    return res, pointer + len(args_raw) + 1


def print_operation(data, args_raw, arg_values, pointer):
    logging.debug("Performing PRINT operation")
    logging.debug("Raw args: {}, arg values: {}".format(args_raw, arg_values))   

    res_address = args_raw[-1]
    print("INTCODE COMPUTER OUTPUT: ", data[res_address])
    return data, pointer + len(args_raw) + 1

def get_arg_values(data, args_raw, arg_modes):
    l = []
    for i in range(len(args_raw)):
        try:
            mode = int(arg_modes[i])
        except IndexError:
            mode = 0
        
        if mode == 0:
            logging.debug(f"Parameter {i} mode: POSITION")
            value = data[args_raw[i]]
        elif mode == 1:
            logging.debug(f"Parameter {i} mode: IMMEDIATE")
            value = args_raw[i]

        l.append(value)
    return l



def parse_instruction(data, pointer):
    logging.debug("Parsing instruction at address: " + str(pointer))

    op_codes = {
        1: {'func': add_operation, 'n_args': 3},
        2: {'func': mul_operation, 'n_args': 3},
        3: {'func': save_operation, 'n_args': 1},
        4: {'func': print_operation, 'n_args': 1}
    }

    try:
        op_int = data[pointer]
        op_code = int(str(op_int)[-2:])

        func = op_codes.get(op_code)['func']
        n_args = op_codes.get(op_code)['n_args']

        args_raw = data[pointer + 1: pointer + 1 + n_args]
        arg_modes = str(op_int)[:-2][::-1]
        arg_locs = get_arg_values(data, args_raw, arg_modes)

    except TypeError:
        raise RuntimeError(f"Failed to parse instruction at address {pointer}")

    return func, args_raw, arg_locs


def run_program(program, noun=None, verb=None, failsafe=1000):
    """Returns a tuple (result, mem_state)"""
    pointer = 0
    mem = program.copy()

    if noun:
        mem[1] = noun
    if verb:
        mem[2] = verb

    i = 0
    while mem[pointer] != 99:
        logging.debug("Running program, iteration: " + str(i))
        logging.debug("Pointer at: " + str(pointer))

        try:
            func, args_raw, arg_locs = parse_instruction(mem, pointer)
            mem, pointer = func(mem, args_raw, arg_locs, pointer)
        except:
            logging.error("Program failed with params {} {}".format(verb, noun))
            return None

        if i > failsafe:
            raise RuntimeError(f"Number of iterations exceeded failsafe ({failsafe})")
    
    return mem[0], mem


def find_arguments(program, desired_value):
    logging.info(f"Finding correct parameter values to get {desired_value}")
    logging.getLogger().setLevel("INFO")
    LOW, HIGH = 0, 99
    FAILSAFE = 100

    results = {
        run_program(program, n, v, FAILSAFE)[0]: (n, v)
        for n in range(LOW, HIGH+1) 
        for v in range(LOW, HIGH+1)}

    return results.get(desired_value, "Desired result not found")


if __name__ == "__main__":
    logging.getLogger().setLevel("INFO")

    raw_in = read_input('data/day_5.txt')
    program = [int(i) for i in raw_in[0].split(',')]

    # Part 1
    run_program(program)

    assert run_program([1,0,0,0,99])[1] == [2,0,0,0,99]
    assert run_program([2,3,0,3,99])[1] == [2,3,0,6,99]
    assert run_program([2,4,4,5,99,0])[1] == [2,4,4,5,99,9801]
    assert run_program([1,1,1,4,99,5,6,0,99])[1] == [30,1,1,4,2,5,6,0,99]
    assert run_program([1,9,10,3,2,3,11,0,99,30,40,50])[1] == [3500,9,10,70,2,3,11,0,99,30,40,50]


    run_program([3,0,99])