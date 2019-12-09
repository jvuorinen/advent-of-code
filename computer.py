from typing import List
import logging
from itertools import permutations

from common import read_input

logging.basicConfig(format='%(levelname)s %(message)s')


def bump_pointer(pointer, args):
    return pointer + len(args) + 1  

def op_add(mem, args_raw, args, pointer, inputs, outputs, relative_base):
    logging.debug("Performing ADD operation")
    logging.debug("Raw args: {}, args: {}".format(args_raw, args))   
    # logging.debug("mem before: " + str(mem))

    mem = mem.copy()
    a, b = args[0], args[1]
    result = a + b

    save_address = args_raw[-1] #TODO fix this
    mem[save_address] = result

    logging.debug(f"Calculation result: {a} + {b} = {result}, storing to address {save_address}")
    # logging.debug("mem after : " + str(res))

    pointer_next = bump_pointer(pointer, args)
    return mem, pointer_next, relative_base


def op_multiply(mem, args_raw, args, pointer, inputs, outputs, relative_base):
    logging.debug("Performing MUL operation")
    logging.debug("Raw args: {}, args: {}".format(args_raw, args))   
    # logging.debug("mem before: " + str(mem))
    
    mem = mem.copy()
    a, b = args[0], args[1]
    result = a * b

    save_address = args_raw[-1] #TODO fix this
    mem[save_address] = result

    logging.debug(f"Calculation result: {a} * {b} = {result}, storing to address {save_address}")
    # logging.debug("mem after : " + str(res))

    pointer_next = bump_pointer(pointer, args)  
    return mem, pointer_next, relative_base


def op_save(mem, args_raw, args, pointer, inputs, outputs, relative_base):
    logging.debug("Performing SAV operation")
    logging.debug("Raw args: {}, args: {}".format(args_raw, args))   
    # logging.debug("mem before: " + str(mem))

    mem = mem.copy()

    value = inputs.pop()
    
    save_address = args_raw[-1] #TODO fix this
    mem[save_address] = value

    logging.debug(f"Saved {value} to location {save_address}")
    # logging.debug("mem after : " + str(res))

    pointer_next = bump_pointer(pointer, args)
    return mem, pointer_next, relative_base


def op_print(mem, args_raw, args, pointer, inputs, outputs, relative_base):
    logging.debug("Performing PRINT operation")
    logging.debug("Raw args: {}, args: {}".format(args_raw, args))   

    logging.info(f"INTCODE COMPUTER OUTPUT: {args[0]}")
    outputs.append(args[0])

    pointer_next = bump_pointer(pointer, args)
    return mem, pointer_next, relative_base


def op_jump_true(mem, args_raw, args, pointer, inputs, outputs, relative_base):
    logging.debug("Performing JUMP-IF-TRUE operation")
    logging.debug("Raw args: {}, args: {}".format(args_raw, args))  

    mem = mem.copy()

    if args[0] != 0:
        pointer_next = args[1]
        logging.debug(f"Condition fulfilled, pointer jumping to: {pointer_next}")
    else:
        pointer_next = bump_pointer(pointer, args)
        logging.debug(f"Condition not fulfilled, pointer incrementing normally to: {pointer_next}")

    return mem, pointer_next, relative_base


def op_jump_false(mem, args_raw, args, pointer, inputs, outputs, relative_base):
    logging.debug("Performing JUMP-IF-FALSE operation")
    logging.debug("Raw args: {}, args: {}".format(args_raw, args))  

    mem = mem.copy()

    if args[0] == 0:
        pointer_next = args[1]
        logging.debug(f"Condition fulfilled, pointer jumping to: {pointer_next}")
    else:
        pointer_next = pointer_next = bump_pointer(pointer, args)
        logging.debug(f"Condition not fulfilled, pointer incrementing normally to: {pointer_next}")

    return mem, pointer_next, relative_base


def op_less_than(mem, args_raw, args, pointer, inputs, outputs, relative_base):
    logging.debug("Performing OP-LESS-THAN operation")
    logging.debug(f"Raw args: {args_raw}, args: {args}")  

    mem = mem.copy()

    if args[0] < args[1]:
        mem[args_raw[2]] = 1 #TODO fix this
    else:
        mem[args_raw[2]] = 0 #TODO fix this

    pointer_next = bump_pointer(pointer, args)
    return mem, pointer_next, relative_base


def op_equals(mem, args_raw, args, pointer, inputs, outputs, relative_base):
    logging.debug("Performing OP-EQUALS operation")
    logging.debug(f"Raw args: {args_raw}, args: {args}")  

    mem = mem.copy()

    if args[0] == args[1]:
        mem[args_raw[2]] = 1 #TODO fix this
    else:
        mem[args_raw[2]] = 0 #TODO fix this

    pointer_next = bump_pointer(pointer, args)
    return mem, pointer_next, relative_base


def op_adjust_relative_base(mem, args_raw, args, pointer, inputs, outputs, relative_base):
    logging.debug("Performing ADJUST RELATIVE BASE operation")
    logging.debug(f"Raw args: {args_raw}, args: {args}")  

    mem = mem.copy()

    relative_base_new = relative_base + args[0]
    logging.debug(f"Changed relative base from: {relative_base} to {relative_base_new}")  

    pointer_next = bump_pointer(pointer, args)
    return mem, pointer_next, relative_base_new

def get_args(mem, args_raw, arg_modes, pointer, relative_base):
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
        elif mode == 2:
            logging.debug(f"Parameter {i+1} mode: RELATIVE")
            value = mem[relative_base + args_raw[i]]

        l.append(value)
    return l


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
    arg_modes = str(op_int)[:-2][::-1]
    args = get_args(mem, args_raw, arg_modes, pointer, relative_base)

    return func, args_raw, args



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
            func, args_raw, arg_locs = parse_instruction(self.mem, self.pointer, self.relative_base)
        except:
            raise RuntimeError(f"Failed to parse instruction at {self.pointer}")

        try:
            self.mem, self.pointer, self.relative_base = func(self.mem, args_raw, arg_locs, self.pointer, self.input_stack, self.outputs, self.relative_base)
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
