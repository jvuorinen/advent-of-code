from typing import List
import logging
from itertools import permutations

from common import read_input

logging.basicConfig(format='%(levelname)s %(message)s')


def bump_pointer(pointer, args):
    return pointer + len(args) + 1  

def op_add(mem, args, pointer, inputs, outputs, relative_base):
    logging.debug(f"Performing ADD operation, args: {args}")   

    mem = mem.copy()
    a, b = args[0], args[1]
    result = a + b

    save_address = args[-1]
    mem[save_address] = result

    logging.debug(f"Calculation result: {a} + {b} = {result}, storing to address {save_address}")
    # logging.debug("mem after : " + str(res))

    pointer_next = bump_pointer(pointer, args)
    return mem, pointer_next, relative_base


def op_multiply(mem, args, pointer, inputs, outputs, relative_base):
    logging.debug(f"Performing MULTIPLY operation, args: {args}")   

    mem = mem.copy()

    a, b = args[0], args[1]
    result = a * b

    save_address = args[-1] 
    mem[save_address] = result

    logging.debug(f"Calculation result: {a} * {b} = {result}, storing to address {save_address}")

    pointer_next = bump_pointer(pointer, args)  
    return mem, pointer_next, relative_base


def op_save(mem, args, pointer, inputs, outputs, relative_base):
    logging.debug(f"Performing SAVE operation, args: {args}")   

    mem = mem.copy()

    value = inputs.pop()
    
    save_address = args[-1]
    mem[save_address] = value

    logging.debug(f"Saved {value} to location {save_address}")

    pointer_next = bump_pointer(pointer, args)
    return mem, pointer_next, relative_base


def op_print(mem, args, pointer, inputs, outputs, relative_base):
    logging.debug(f"Performing PRINT operation, args: {args}")  

    stuff = args[0]
    logging.info(f"INTCODE COMPUTER OUTPUT: {stuff}")
    outputs.append(stuff)

    pointer_next = bump_pointer(pointer, args)
    return mem, pointer_next, relative_base


def op_jump_true(mem, args, pointer, inputs, outputs, relative_base):
    logging.debug(f"Performing JUMP-IF-TRUE operation, args: {args}")  

    mem = mem.copy()

    if args[0] != 0:
        pointer_next = args[1]
        logging.debug(f"Condition fulfilled, pointer jumping to: {pointer_next}")
    else:
        pointer_next = bump_pointer(pointer, args)
        logging.debug(f"Condition not fulfilled, pointer incrementing normally to: {pointer_next}")

    return mem, pointer_next, relative_base


def op_jump_false(mem, args, pointer, inputs, outputs, relative_base):
    logging.debug(f"Performing JUMP-IF-FALSE operation, args: {args}")  

    mem = mem.copy()

    if args[0] == 0:
        pointer_next = args[1]
        logging.debug(f"Condition fulfilled, pointer jumping to: {pointer_next}")
    else:
        pointer_next = pointer_next = bump_pointer(pointer, args)
        logging.debug(f"Condition not fulfilled, pointer incrementing normally to: {pointer_next}")

    return mem, pointer_next, relative_base


def op_less_than(mem, args, pointer, inputs, outputs, relative_base):
    logging.debug(f"Performing OP-LESS-THAN operation, args: {args}")  

    mem = mem.copy()

    if args[0] < args[1]:
        mem[args[-1]] = 1 
    else:
        mem[args[-1]] = 0 

    pointer_next = bump_pointer(pointer, args)
    return mem, pointer_next, relative_base


def op_equals(mem, args, pointer, inputs, outputs, relative_base):
    logging.debug(f"Performing OP-EQUALS operation, args: {args}")

    mem = mem.copy()

    if args[0] == args[1]:
        mem[args[-1]] = 1 
    else:
        mem[args[-1]] = 0 

    pointer_next = bump_pointer(pointer, args)
    return mem, pointer_next, relative_base


def op_adjust_relative_base(mem, args, pointer, inputs, outputs, relative_base):
    logging.debug(f"Performing ADJUST RELATIVE BASE operation, args: {args}")  

    mem = mem.copy()

    relative_base_new = relative_base + args[0]
    logging.debug(f"Changed relative base from: {relative_base} to {relative_base_new}")  

    pointer_next = bump_pointer(pointer, args)
    return mem, pointer_next, relative_base_new


def get_args(mem, args_raw, arg_modes, pointer, relative_base):
    l = []
    logging.debug("Getting parameter values...")
 
    for i, mode in enumerate(arg_modes):
        if mode == 0:
            logging.debug(f"Parameter {i+1} mode: POSITION")
            value = mem[args_raw[i]]
        elif mode == 1:
            logging.debug(f"Parameter {i+1} mode: IMMEDIATE")
            value = args_raw[i]
        elif mode == 2:
            logging.debug(f"Parameter {i+1} mode: RELATIVE (using {relative_base} as relative base)")
            value = mem[relative_base + args_raw[i]]
        else:
            raise ValueError(f"Invalid parameter mode: {mode}")
        l.append(value)
    
    logging.debug(f"Arguments parsed - raw args: {args_raw}, final_args: {l}")   
    return l


def parse_arg_modes(op_int, n_args):
    parsed = [] + [int(x) for x in list(str(op_int)[:-2][::-1])]
    implied = (n_args - len(parsed))*[0]
    return parsed + implied


def parse_instruction(mem, pointer, relative_base):
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
        9: {'func': op_adjust_relative_base, 'n_args': 1}
    }

    op_int = mem[pointer]
    op_code = int(str(op_int)[-2:])

    func = op_codes[op_code]['func']
    n_args = op_codes[op_code]['n_args']

    args_raw = mem[pointer + 1: pointer + 1 + n_args]
    arg_modes = parse_arg_modes(op_int, n_args)

    args = get_args(mem, args_raw, arg_modes, pointer, relative_base)

    # This is ugly stuff... Basically have to do this fix 
    # to make writing work properly
    if (op_code in (1, 2, 3, 7, 8)) and (arg_modes[-1] == 0):
        args[-1] = args_raw[-1]

    if (op_code in (1, 2, 3, 7, 8)) and (arg_modes[-1] == 2):
        args[-1] = relative_base + args_raw[-1]


    return func, args



class Computer:
    def __init__(self, program=None, failsafe = 1000, mem_size = 2000):
        self.state = "IDLE, NO PROGRAM LOADED"
        self.failsafe = failsafe
        self.pointer = None
        self.input_stack = None
        self.outputs = None
        self.relative_base = 0
        self.mem_size = 2000

        if program:
            self.load(program)

    def __repr__(self):
        return f"Intcode Computer\nstate: {self.state}\npointer at: {self.pointer}\nrelative base: {self.relative_base}\ninput stack: {self.input_stack}\noutputs: {self.outputs}"

    def load(self, program, noun=None, verb=None):
        self.state = "IDLE, NOT STARTED"
        self._program = program.copy()

        if noun:
            logging.debug(f"Setting noun to {noun}")
            self._program[1] = noun
        if verb:
            logging.debug(f"Setting verb to {verb}")
            self._program[2] = verb

        logging.info("Program loaded")
        self.reset()

    def reset(self):
        buffer = self.mem_size - len(self._program)
        self.mem = self._program.copy() + [0]*buffer
        self.input_stack = []
        self.outputs = []
        self.pointer = 0
        self.relative_base = 0
        logging.info("State has been reset")

    def _step(self):
        try:
            func, args = parse_instruction(self.mem, self.pointer, self.relative_base)
        except:
            raise RuntimeError(f"Failed to parse instruction at {self.pointer}")

        try:
            self.mem, self.pointer, self.relative_base = func(self.mem, args, self.pointer, self.input_stack, self.outputs, self.relative_base)
        except:
            raise RuntimeError(f"Failed to execute instruction at {self.pointer}")

    def add_input(self, to_be_added):
        self.input_stack += [to_be_added]

    def run(self):
        i = 0
        while True:
            if (self.mem[self.pointer] == 3) & (len(self.input_stack) == 0):
                self.state = "WAITING INPUT"
                logging.info("Program needs input and cannot continue running because input stack is empty")
                break

            if self.mem[self.pointer] == 99:
                self.state = "FINISHED"
                logging.info("Program has reached exit code and finished running")                
                break

            logging.debug("--------------------------------------------------------------------")
            logging.debug("Running program, iteration: " + str(i))
            logging.debug("Pointer at: " + str(self.pointer))

            self._step()

            i += 1
            if i > self.failsafe:
                raise RuntimeError(f"Number of iterations exceeded failsafe ({self.failsafe})")
        


if __name__ == "__main__":
    logging.getLogger().setLevel('INFO')

    raw_in = read_input('data/day_9.txt')
    program = [int(i) for i in raw_in[0].split(',')]

    # program = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]

    c = Computer()
    c.load(program)
    c.add_input(1)
    c.run()
