from typing import List
import logging

from common import read_input

logging.basicConfig(format='%(levelname)s %(message)s')


def bump_pointer(pointer, args):
    return pointer + len(args) + 1  

def op_add(mem, args_raw, args, pointer):
    logging.debug("Performing ADD operation")
    logging.debug("Raw args: {}, arg values: {}".format(args_raw, args))   
    # logging.debug("mem before: " + str(mem))

    mem = mem.copy()
    a, b = args[0], args[1]
    result = a + b

    save_address = args_raw[-1]
    mem[save_address] = result

    logging.debug(f"Calculation result: {a} + {b} = {result}, storing to address {save_address}")
    # logging.debug("mem after : " + str(res))

    pointer_next = bump_pointer(pointer, args)
    return mem, pointer_next


def op_multiply(mem, args_raw, args, pointer):
    logging.debug("Performing MUL operation")
    logging.debug("Raw args: {}, arg values: {}".format(args_raw, args))   
    # logging.debug("mem before: " + str(mem))
    
    mem = mem.copy()
    a, b = args[0], args[1]
    result = a * b

    save_address = args_raw[-1]
    mem[save_address] = result

    logging.debug(f"Calculation result: {a} * {b} = {result}, storing to address {save_address}")
    # logging.debug("mem after : " + str(res))

    pointer_next = bump_pointer(pointer, args)  
    return mem, pointer_next


def op_save(mem, args_raw, args, pointer):
    logging.debug("Performing SAV operation")
    logging.debug("Raw args: {}, arg values: {}".format(args_raw, args))   
    # logging.debug("mem before: " + str(mem))

    mem = mem.copy()

    value = INPUT_VALUE #TODO Change to actual input
    
    save_address = args_raw[-1]
    mem[save_address] = value

    logging.debug(f"Saved {value} to location {save_address}")
    # logging.debug("mem after : " + str(res))

    pointer_next = bump_pointer(pointer, args)
    return mem, pointer_next


def op_print(mem, args_raw, args, pointer):
    logging.debug("Performing PRINT operation")
    logging.debug("Raw args: {}, arg values: {}".format(args_raw, args))   

    print("INTCODE COMPUTER OUTPUT: ", args[0])

    pointer_next = bump_pointer(pointer, args)
    return mem, pointer_next


def op_jump_true(mem, args_raw, args, pointer):
    logging.debug("Performing JUMP-IF-TRUE operation")
    logging.debug("Raw args: {}, arg values: {}".format(args_raw, args))  

    mem = mem.copy()

    if args[0] != 0:
        pointer_next = args[1]
        logging.debug(f"Condition fulfilled, pointer jumping to: {pointer_next}")
    else:
        pointer_next = bump_pointer(pointer, args)
        logging.debug(f"Condition not fulfilled, pointer incrementing normally to: {pointer_next}")

    return mem, pointer_next


def op_jump_false(mem, args_raw, args, pointer):
    logging.debug("Performing JUMP-IF-FALSE operation")
    logging.debug("Raw args: {}, arg values: {}".format(args_raw, args))  

    mem = mem.copy()

    if args[0] == 0:
        pointer_next = args[1]
        logging.debug(f"Condition fulfilled, pointer jumping to: {pointer_next}")
    else:
        pointer_next = pointer_next = bump_pointer(pointer, args)
        logging.debug(f"Condition not fulfilled, pointer incrementing normally to: {pointer_next}")

    return mem, pointer_next


def op_less_than(mem, args_raw, args, pointer):
    logging.debug("Performing OP-LESS-THAN operation")
    logging.debug(f"Raw args: {args_raw}, arg values: {args}")  

    mem = mem.copy()

    if args[0] < args[1]:
        mem[args_raw[2]] = 1
    else:
        mem[args_raw[2]] = 0

    pointer_next = bump_pointer(pointer, args)
    return mem, pointer_next


def op_equals(mem, args_raw, args, pointer):
    logging.debug("Performing OP-EQUALS operation")
    logging.debug(f"Raw args: {args_raw}, arg values: {args}")  

    mem = mem.copy()

    if args[0] == args[1]:
        mem[args_raw[2]] = 1
    else:
        mem[args_raw[2]] = 0

    pointer_next = bump_pointer(pointer, args)
    return mem, pointer_next


def get_args(mem, args_raw, arg_modes):
    l = []
    logging.debug("Getting parameter values...")
    for i in range(len(args_raw)):
        try:
            mode = int(arg_modes[i])
        except IndexError:
            mode = 0
        
        if mode == 0:
            logging.debug(f"Parameter {i+1} mode: POSITION")
            value = mem[args_raw[i]]
        elif mode == 1:
            logging.debug(f"Parameter {i+1} mode: IMMEDIATE")
            value = args_raw[i]

        l.append(value)
    return l


def parse_instruction(mem, pointer):
    logging.debug(f"Parsing instruction at address: {pointer}")
    logging.debug(f"Instruction is: {mem[pointer]}")

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

    op_int = mem[pointer]
    op_code = int(str(op_int)[-2:])

    func = op_codes[op_code]['func']
    n_args = op_codes[op_code]['n_args']

    args_raw = mem[pointer + 1: pointer + 1 + n_args]
    arg_modes = str(op_int)[:-2][::-1]
    arg_locs = get_args(mem, args_raw, arg_modes)

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
        logging.debug("--------------------------------------------------------------------")
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
    logging.getLogger().setLevel("DEBUG")

    raw_in = read_input('data/day_5.txt')
    program = [int(i) for i in raw_in[0].split(',')]

    # Part 1
    INPUT_VALUE = 1
    _ = run_program(program) # Should be 9219874

    # Part 2
    INPUT_VALUE = 5
    _ = run_program(program) # Should be 5893654