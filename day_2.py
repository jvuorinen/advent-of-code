from typing import List
import logging

import data.programs 

logging.getLogger().setLevel('DEBUG')

def add_operation(data, in_a_addr, in_b_addr, res_addr):
    logging.debug("Performing ADD operation with args ({} {} {})".format(in_a_addr, in_b_addr, res_addr))
    logging.debug("Data before: " + str(data))

    res = data.copy()
    a, b, r = res[res[in_a_addr]], res[res[in_b_addr]], res[res_addr]
    result = a + b
    res[r] = result

    logging.debug(f"Calculation result: {a} + {b} = {result}, storing to address {r}")
    logging.debug("Data after : " + str(res))
    return res

def mul_operation(data, in_a_addr, in_b_addr, res_addr):
    logging.debug("Performing MUL operation with args ({} {} {})".format(in_a_addr, in_b_addr, res_addr))
    logging.debug("Data before: " + str(data))
    
    res = data.copy()
    a, b, r = res[res[in_a_addr]], res[res[in_b_addr]], res[res_addr]
    result = a * b
    res[r] = result

    logging.debug(f"Calculation result: {a} * {b} = {result}, storing to address {r}")
    logging.debug("Data after : " + str(res))
    return res

def parse_instruction(data, pointer):
    op_codes = {
        1: {'op': add_operation, 'n_args': 3},
        2: {'op': mul_operation, 'n_args': 3}
    }

    try:
        op = op_codes.get(data[pointer])['op']
    except TypeError:
        raise RuntimeError(f"Failed to convert number {data[pointer]} at pointer {pointer} to opcode")

    n_args = op_codes.get(data[pointer])['n_args']
    arg_addrs = list(range(pointer + 1, pointer + n_args + 1)) 
    next_pointer = pointer + n_args + 1

    return op, arg_addrs, next_pointer


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
        logging.debug("Parsing instruction at address: " + str(pointer))
        try:
            op, args, next_pointer = parse_instruction(mem, pointer)
            mem = op(mem, *args)
        except:
            logging.error("Program failed with params {} {}".format(verb, noun))
            return None

        pointer = next_pointer
        i += 1

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

    # Part 1
    prog = data.programs.program_day_2
    res_1, _  = run_program(prog, 12, 2)
    print("Part 1 result:",  str(res_1))

    # Part 2
    n, v = find_arguments(prog, 19690720)
    print("Part 2 result:",  str(100 * n + v))

