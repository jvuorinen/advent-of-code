from typing import List
import logging
from itertools import permutations
from dataclasses import dataclass

# from copy import deepcopy

from utils import read_input

logging.basicConfig(format="%(levelname)s %(message)s")


@dataclass
class ComputerState:
    """Class that holds all state that an intcode computer can have"""

    mem: List[int]
    pointer: int
    input_stack: List[int]
    outputs: List[int]
    relative_base: int

    def get_copy(self):
        return ComputerState(
            mem=self.mem.copy(),
            pointer=self.pointer,
            input_stack=self.input_stack.copy(),
            outputs=self.outputs.copy(),
            relative_base=self.relative_base,
        )


def bump_pointer(pointer, args):
    return pointer + len(args) + 1


def op_add(state, args):
    # logging.debug(f"Performing ADD operation, args: {args}")

    # state = state.get_copy()

    a, b = args[0], args[1]
    result = a + b

    save_address = args[-1]
    state.mem[save_address] = result

    # logging.debug(f"Calculation result: {a} + {b} = {result}, storing to address {save_address}")
    # logging.debug("mem after : " + str(res))

    state.pointer = bump_pointer(state.pointer, args)
    return state


def op_multiply(state, args):
    # logging.debug(f"Performing MULTIPLY operation, args: {args}")

    # state = state.get_copy()

    a, b = args[0], args[1]
    result = a * b

    save_address = args[-1]
    state.mem[save_address] = result

    # logging.debug(f"Calculation result: {a} * {b} = {result}, storing to address {save_address}")

    state.pointer = bump_pointer(state.pointer, args)
    return state


def op_save(state, args):
    # logging.debug(f"Performing SAVE operation, args: {args}")

    # state = state.get_copy()

    value = state.input_stack.pop()

    save_address = args[-1]
    state.mem[save_address] = value

    # logging.debug(f"Saved {value} to location {save_address}")

    state.pointer = bump_pointer(state.pointer, args)
    return state


def op_print(state, args):
    # logging.debug(f"Performing PRINT operation, args: {args}")

    # state = state.get_copy()

    stuff = args[0]
    # logging.debug(f"INTCODE COMPUTER OUTPUT: {stuff}")
    state.outputs += [stuff]

    state.pointer = bump_pointer(state.pointer, args)
    return state


def op_jump_true(state, args):
    # logging.debug(f"Performing JUMP-IF-TRUE operation, args: {args}")

    # state = state.get_copy()

    if args[0] != 0:
        state.pointer = args[1]
        # logging.debug(f"Condition fulfilled, pointer jumping to: {state.pointer}")
    else:
        state.pointer = bump_pointer(state.pointer, args)
        # logging.debug(f"Condition not fulfilled, pointer incrementing normally to: {state.pointer}")

    return state


def op_jump_false(state, args):
    # logging.debug(f"Performing JUMP-IF-FALSE operation, args: {args}")

    # state = state.get_copy()

    if args[0] == 0:
        state.pointer = args[1]
        # logging.debug(f"Condition fulfilled, pointer jumping to: {state.pointer}")
    else:
        state.pointer = bump_pointer(state.pointer, args)
        # logging.debug(f"Condition not fulfilled, pointer incrementing normally to: {state.pointer}")

    return state


def op_less_than(state, args):
    # logging.debug(f"Performing OP-LESS-THAN operation, args: {args}")

    # state = state.get_copy()

    if args[0] < args[1]:
        state.mem[args[-1]] = 1
    else:
        state.mem[args[-1]] = 0

    state.pointer = bump_pointer(state.pointer, args)
    return state


def op_equals(state, args):
    # logging.debug(f"Performing OP-EQUALS operation, args: {args}")

    # state = state.get_copy()

    if args[0] == args[1]:
        state.mem[args[-1]] = 1
    else:
        state.mem[args[-1]] = 0

    state.pointer = bump_pointer(state.pointer, args)
    return state


def op_adjust_relative_base(state, args):
    # logging.debug(f"Performing ADJUST RELATIVE BASE operation, args: {args}")

    # state = state.get_copy()

    relative_base_new = state.relative_base + args[0]
    state.relative_base = relative_base_new
    # logging.debug(f"Changed relative base from: {state.relative_base} to {relative_base_new}")

    state.pointer = bump_pointer(state.pointer, args)
    return state


def get_args(mem, args_raw, arg_modes, pointer, relative_base, op_code):
    l = []
    # logging.debug("Getting parameter values...")

    for i, mode in enumerate(arg_modes):
        if mode == 0:
            # logging.debug(f"Parameter {i+1} mode: POSITION")

            # This is ugly stuff... have to do this fix to make writing work properly
            if (op_code in (1, 2, 3, 7, 8)) and (i == (len(arg_modes) - 1)):
                value = args_raw[-1]
            else:
                value = mem[args_raw[i]]

        elif mode == 1:
            # logging.debug(f"Parameter {i+1} mode: IMMEDIATE")
            value = args_raw[i]
        elif mode == 2:
            # logging.debug(f"Parameter {i+1} mode: RELATIVE (using {relative_base} as relative base)")

            # This is ugly stuff... have to do this fix to make writing work properly
            if (op_code in (1, 2, 3, 7, 8)) and (i == (len(arg_modes) - 1)):
                value = relative_base + args_raw[-1]
            else:
                value = mem[relative_base + args_raw[i]]

        else:
            raise ValueError(f"Invalid parameter mode: {mode}")
        l.append(value)

    # logging.debug(f"Arguments parsed - raw args: {args_raw}, final_args: {l}")
    return l


def parse_arg_modes(op_int, n_args):
    parsed = [] + [int(x) for x in list(str(op_int)[:-2][::-1])]
    implied = (n_args - len(parsed)) * [0]
    return parsed + implied


def parse_instruction(mem, pointer, relative_base):
    # logging.debug(f"Parsing instruction at address: {pointer}")
    # logging.debug(f"Instruction is: {mem[pointer]}")

    op_codes = {
        1: {"func": op_add, "n_args": 3},
        2: {"func": op_multiply, "n_args": 3},
        3: {"func": op_save, "n_args": 1},
        4: {"func": op_print, "n_args": 1},
        5: {"func": op_jump_true, "n_args": 2},
        6: {"func": op_jump_false, "n_args": 2},
        7: {"func": op_less_than, "n_args": 3},
        8: {"func": op_equals, "n_args": 3},
        9: {"func": op_adjust_relative_base, "n_args": 1},
    }

    op_int = mem[pointer]
    op_code = int(str(op_int)[-2:])

    func = op_codes[op_code]["func"]
    n_args = op_codes[op_code]["n_args"]

    args_raw = mem[pointer + 1 : pointer + 1 + n_args]
    arg_modes = parse_arg_modes(op_int, n_args)

    args = get_args(mem, args_raw, arg_modes, pointer, relative_base, op_code)

    return func, args


class Computer:
    def __init__(self, program=None, failsafe=1000000, mem_size=5_000):
        self.status = "IDLE, NO PROGRAM LOADED"
        self.failsafe = failsafe
        self.mem_size = mem_size
        self.state = ComputerState(
            mem=None, pointer=None, input_stack=None, outputs=None, relative_base=None
        )
        if program:
            self.load(program)

    def __repr__(self):
        return f"Intcode Computer\nstatus: {self.status}\npointer at: {self.state.pointer}\nrelative base: {self.state.relative_base}\ninput stack: {self.state.input_stack}\noutputs: {self.state.outputs}"

    def load(self, program, noun=None, verb=None):
        self.status = "IDLE, NOT STARTED"
        self._program = program.copy()

        if noun:
            # logging.debug(f"Setting noun to {noun}")
            self._program[1] = noun
        if verb:
            # logging.debug(f"Setting verb to {verb}")
            self._program[2] = verb

        logging.debug("Program loaded")
        self.reset()

    def reset(self):
        self.status = "IDLE, NOT STARTED"
        buffer = self.mem_size - len(self._program)
        self.state.mem = self._program.copy() + [0] * buffer
        self.state.input_stack = []
        self.state.outputs = []
        self.state.pointer = 0
        self.state.relative_base = 0
        logging.debug("State has been reset")

    def _step(self):
        try:
            func, args = parse_instruction(
                self.state.mem, self.state.pointer, self.state.relative_base
            )
        except:
            raise RuntimeError(f"Failed to parse instruction at {self.state.pointer}")

        try:
            self.state = func(self.state, args)
        except:
            raise RuntimeError(f"Failed to execute instruction at {self.state.pointer}")

    def add_input(self, to_be_added):
        self.state.input_stack += [to_be_added]

    def run(self):
        self.status = "PROGRAM STARTED"
        i = 0
        while True:
            if (str(self.state.mem[self.state.pointer])[-1] == "3") & (
                len(self.state.input_stack) == 0
            ):
                self.status = "WAITING INPUT"
                logging.debug(
                    "Program needs input and cannot continue running because input stack is empty"
                )
                break

            if self.state.mem[self.state.pointer] == 99:
                self.status = "FINISHED"
                logging.debug("Program has reached exit code and finished running")
                break

            # logging.debug("--------------------------------------------------------------------")
            # logging.debug("Running program, iteration: " + str(i))
            # logging.debug("Pointer at: " + str(self.state.pointer))

            self._step()

            i += 1
            if i > self.failsafe:
                raise RuntimeError(f"Number of iterations exceeded failsafe ({self.failsafe})")


if __name__ == "__main__":
    logging.getLogger().setLevel("INFO")

    raw_in = read_input("inputs/day_9.txt")
    program = [int(i) for i in raw_in[0].split(",")]

    # program = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]

    c = Computer()
    c.load(program)
    c.add_input(1)
    # c.run()
