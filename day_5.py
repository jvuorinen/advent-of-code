from typing import List
import logging

from common import read_input

logging.getLogger().setLevel('DEBUG')


def op_add(data, args_raw, arg_values, pointer):
    logging.debug("Performing ADD operation")
    logging.debug("Raw args: {}, arg values: {}".format(args_raw, arg_values))   
    # logging.debug("Data before: " + str(data))

    data = data.copy()
    a, b = arg_values[0], arg_values[1]
    result = a + b

    result_address = args_raw[-1]
    data[result_address] = result

    logging.debug(f"Calculation result: {a} + {b} = {result}, storing to address {result_address}")
    # logging.debug("Data after : " + str(res))
    return data, pointer + len(args_raw) + 1


def op_multiply(data, args_raw, arg_values, pointer):
    logging.debug("Performing MUL operation")
    logging.debug("Raw args: {}, arg values: {}".format(args_raw, arg_values))   
    # logging.debug("Data before: " + str(data))
    
    data = data.copy()
    a, b = arg_values[0], arg_values[1]
    result = a * b

    result_address = args_raw[-1]
    data[result_address] = result

    logging.debug(f"Calculation result: {a} * {b} = {result}, storing to address {result_address}")
    # logging.debug("Data after : " + str(res))
    return data, pointer + len(args_raw) + 1


def op_save(data, args_raw, arg_values, pointer):
    logging.debug("Performing SAV operation")
    logging.debug("Raw args: {}, arg values: {}".format(args_raw, arg_values))   
    # logging.debug("Data before: " + str(data))

    data = data.copy()

    value = INPUT_VALUE #TODO Change to actual input
    
    result_address = args_raw[-1]
    data[result_address] = value

    logging.debug(f"Saved {value} to location {result_address}")
    # logging.debug("Data after : " + str(res))
    return data, pointer + len(args_raw) + 1


def op_print(data, args_raw, arg_values, pointer):
    logging.debug("Performing PRINT operation")
    logging.debug("Raw args: {}, arg values: {}".format(args_raw, arg_values))   

    print("INTCODE COMPUTER OUTPUT: ", arg_values[0])
    return data, pointer + len(args_raw) + 1


def op_jump_true(data, args_raw, arg_values, pointer):
    logging.debug("Performing JUMP-IF-TRUE operation")
    logging.debug("Raw args: {}, arg values: {}".format(args_raw, arg_values))  

    data = data.copy()

    if arg_values[0] != 0:
        pointer_next = arg_values[1]
        logging.debug("Condition fulfilled, pointer jumping to: {pointer_next}")
    else:
        pointer_next = pointer + len(args_raw) + 1
        logging.debug("Condition not fulfilled, pointer incrementing normally to: {pointer_next}")

    return data, pointer_next


def op_jump_false(data, args_raw, arg_values, pointer):
    logging.debug("Performing JUMP-IF-FALSE operation")
    logging.debug("Raw args: {}, arg values: {}".format(args_raw, arg_values))  

    data = data.copy()

    if arg_values[0] == 0:
        pointer_next = arg_values[1]
        logging.debug("Condition fulfilled, pointer jumping to: {pointer_next}")
    else:
        pointer_next = pointer + len(args_raw) + 1
        logging.debug("Condition not fulfilled, pointer incrementing normally to: {pointer_next}")

    return data, pointer_next


def op_less_than(data, args_raw, arg_values, pointer):
    logging.debug("Performing OP-LESS-THAN operation")
    logging.debug("Raw args: {}, arg values: {}".format(args_raw, arg_values))  

    data = data.copy()

    if arg_values[0] < arg_values[1]:
        data[args_raw[2]] = 1
    else:
        data[args_raw[2]] = 0

    return data, pointer + len(args_raw) + 1


def op_equals(data, args_raw, arg_values, pointer):
    logging.debug("Performing OP-EQUALS operation")
    logging.debug("Raw args: {}, arg values: {}".format(args_raw, arg_values))  

    data = data.copy()

    if arg_values[0] == arg_values[1]:
        data[args_raw[2]] = 1
    else:
        data[args_raw[2]] = 0

    return data, pointer + len(args_raw) + 1


def get_arg_values(data, args_raw, arg_modes):
    l = []
    logging.debug("Getting parameter values...")
    for i in range(len(args_raw)):
        try:
            mode = int(arg_modes[i])
        except IndexError:
            mode = 0
        
        if mode == 0:
            logging.debug(f"Parameter {i+1} mode: POSITION")
            value = data[args_raw[i]]
        elif mode == 1:
            logging.debug(f"Parameter {i+1} mode: IMMEDIATE")
            value = args_raw[i]

        l.append(value)
    return l


def parse_instruction(data, pointer):
    logging.debug(f"Parsing instruction at address: {pointer}")
    logging.debug(f"Data at this section looks like: {data[pointer:pointer+4]}")
    logging.debug(f"Instruction is: {data[pointer]}")

    op_codes = {
        1: {'func': op_add, 'n_args': 3},
        2: {'func': op_multiply, 'n_args': 3},
        3: {'func': op_save, 'n_args': 1},
        4: {'func': op_print, 'n_args': 1},
        5: {'func': op_jump_true, 'n_args': 2},
        6: {'func': op_jump_false, 'n_args': 2},
        7: {'func': op_less_than, 'n_args': 3},
        8: {'func': op_equals, 'n_args': 3},
    }

    try:
        op_int = data[pointer]
        op_code = int(str(op_int)[-2:])

        func = op_codes[op_code]['func']
        n_args = op_codes[op_code]['n_args']

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
        except:
            raise RuntimeError(f"Failed to parse instruction at {pointer}")

        try:
            mem, pointer = func(mem, args_raw, arg_locs, pointer)
        except:
            raise RuntimeError(f"Failed to execute instruction at {pointer}")         

        i += 1
        if i > failsafe:
            raise RuntimeError(f"Number of iterations exceeded failsafe ({failsafe})")
    
    return mem[0], mem


if __name__ == "__main__":
    logging.getLogger().setLevel("INFO")

    raw_in = read_input('data/day_5.txt')
    program = [int(i) for i in raw_in[0].split(',')]

    # Part 1
    INPUT_VALUE = 1
    _ = run_program(program) # Should be 9219874

    # Part 2
    INPUT_VALUE = 5
    _ = run_program(program) # Should be 5893654