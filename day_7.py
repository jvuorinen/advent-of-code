from typing import List
import logging
from itertools import permutations

from common import read_input

logging.basicConfig(format='%(levelname)s %(message)s')


def bump_pointer(pointer, args):
    return pointer + len(args) + 1  

def op_add(mem, args_raw, args, pointer, inputs, outputs):
    logging.debug("Performing ADD operation")
    logging.debug("Raw args: {}, args: {}".format(args_raw, args))   
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


def op_multiply(mem, args_raw, args, pointer, inputs, outputs):
    logging.debug("Performing MUL operation")
    logging.debug("Raw args: {}, args: {}".format(args_raw, args))   
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


def op_save(mem, args_raw, args, pointer, inputs, outputs):
    logging.debug("Performing SAV operation")
    logging.debug("Raw args: {}, args: {}".format(args_raw, args))   
    # logging.debug("mem before: " + str(mem))

    mem = mem.copy()

    value = inputs.pop()
    
    save_address = args_raw[-1]
    mem[save_address] = value

    logging.debug(f"Saved {value} to location {save_address}")
    # logging.debug("mem after : " + str(res))

    pointer_next = bump_pointer(pointer, args)
    return mem, pointer_next


def op_print(mem, args_raw, args, pointer, inputs, outputs):
    logging.debug("Performing PRINT operation")
    logging.debug("Raw args: {}, args: {}".format(args_raw, args))   

    logging.info(f"INTCODE COMPUTER OUTPUT: {args[0]}")
    outputs.append(args[0])

    pointer_next = bump_pointer(pointer, args)
    return mem, pointer_next


def op_jump_true(mem, args_raw, args, pointer, inputs, outputs):
    logging.debug("Performing JUMP-IF-TRUE operation")
    logging.debug("Raw args: {}, args: {}".format(args_raw, args))  

    mem = mem.copy()

    if args[0] != 0:
        pointer_next = args[1]
        logging.debug(f"Condition fulfilled, pointer jumping to: {pointer_next}")
    else:
        pointer_next = bump_pointer(pointer, args)
        logging.debug(f"Condition not fulfilled, pointer incrementing normally to: {pointer_next}")

    return mem, pointer_next


def op_jump_false(mem, args_raw, args, pointer, inputs, outputs):
    logging.debug("Performing JUMP-IF-FALSE operation")
    logging.debug("Raw args: {}, args: {}".format(args_raw, args))  

    mem = mem.copy()

    if args[0] == 0:
        pointer_next = args[1]
        logging.debug(f"Condition fulfilled, pointer jumping to: {pointer_next}")
    else:
        pointer_next = pointer_next = bump_pointer(pointer, args)
        logging.debug(f"Condition not fulfilled, pointer incrementing normally to: {pointer_next}")

    return mem, pointer_next


def op_less_than(mem, args_raw, args, pointer, inputs, outputs):
    logging.debug("Performing OP-LESS-THAN operation")
    logging.debug(f"Raw args: {args_raw}, args: {args}")  

    mem = mem.copy()

    if args[0] < args[1]:
        mem[args_raw[2]] = 1
    else:
        mem[args_raw[2]] = 0

    pointer_next = bump_pointer(pointer, args)
    return mem, pointer_next


def op_equals(mem, args_raw, args, pointer, inputs, outputs):
    logging.debug("Performing OP-EQUALS operation")
    logging.debug(f"Raw args: {args_raw}, args: {args}")  

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



class Amp:
    def __init__(self, phase, program):
        self.phase = phase
        self.state = "IDLE"
        self._program = program.copy()
        self.mem = self._program.copy()
        self.outputs = []
        self.pointer = 0

        self.run(self.phase)

    def __repr__(self):
        return f"Amplifier. Phase: {self.phase}, state: {self.state}, pointer at: {self.pointer}"

    def run(self, in_signal):
        inputs = [in_signal]

        while True:
            if self.mem[self.pointer] == 99:
                self.state = "FINISHED"
                # logging.info("Amplifier finished")
                break
            
            try:
                func, args_raw, arg_locs = parse_instruction(self.mem, self.pointer)
            except:
                raise RuntimeError(f"Failed to parse instruction at {self.pointer}")

            try:
                self.mem, self.pointer = func(self.mem, args_raw, arg_locs, self.pointer, inputs, self.outputs)
            except:
                raise RuntimeError(f"Failed to execute instruction at {self.pointer}")         

            if self.mem[self.pointer] == 3:
                self.state = "WAITING INPUT"
                break




def solve(phase_possibilities):
    phase_combos = permutations(phase_possibilities)

    all_outputs = []
    for phase_order in phase_combos:
        # logging.info(f"Testing phase order {phase_order}")

        amps = [Amp(p, program) for p in phase_order]
        signal = 0
        iteration = 0
        while True:
            iteration += 1
            # print(f"Loop: {iteration}, signal value {signal}")
            # print("Amp states:")
            # print(amps)
            for i in range(5):
                # print(f"Amp {i} running on signal {signal}")
                amps[i].run(signal)
                signal = amps[i].outputs[-1]
            
            if amps[4].state == "FINISHED":
                all_outputs.append(signal)
                break

    return max(all_outputs)

# def find_best_signal(program):
#     phase_combos = permutations([0,1,2,3,4])

#     all_outputs = []
#     for phase_order in phase_combos:
#         logging.info(f"Running phase combo {phase_order}")
#         inputs = [0]
#         for phase in phase_order:
#             inputs.append(phase)
#             output, _ = run_program(program, inputs)
#             inputs.insert(0, output[0])
#             all_outputs += output

#     return max(all_outputs)


if __name__ == "__main__":
    logging.getLogger().setLevel("WARNING")

    raw_in = read_input('data/day_7.txt')
    program = [int(i) for i in raw_in[0].split(',')]

    print("Step 1 answer: ", solve([0,1,2,3,4]))
    print("Step 2 answer: ", solve([5,6,7,8,9]))
