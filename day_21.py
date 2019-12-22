import logging
logging.basicConfig(format='%(levelname)s %(message)s')

from common import read_input
from computer import Computer

from random import sample, randint

def to_intcode(code):
    return [ord(c) for c in code]

def to_ascii(code):
    return [chr(c) for c in code]

def solve_1(program):
    c = Computer(program)

    commands = [
        "NOT T T",
        "AND A T",
        "AND B T",
        "AND C T",
        "NOT T T",
        "AND D T",
        "OR T J",
        "WALK"]

    code = to_intcode("\n".join(commands) + '\n')

    c.state.input_stack = code[::-1]
    c.run()
    o = c.state.outputs

    try:
        print("".join(to_ascii(o)))
    except ValueError:
        print("".join(to_ascii(o[:-1])))
        print(f"Step 1 answer: {o[-1]}")


def solve_2(program):
    c = Computer(program)

    hole_ahead = [
        "OR A T",
        "AND B T",
        "AND C T",
        "NOT T T",
        ]
    
    safe_landing = [
        "AND D T",
        "OR E J",
        "OR H J",        
    ]

    ending = [
        "AND T J",
        "RUN",
    ]

    code = to_intcode("\n".join(hole_ahead + safe_landing + ending) + '\n')

    c.state.input_stack = code[::-1]
    c.run()
    o = c.state.outputs

    try:
        print("".join(to_ascii(o)))
    except ValueError:
        print("".join(to_ascii(o[:-1])))
        print(f"Step 2 answer: {o[-1]}")



if __name__ == "__main__":
    logging.getLogger().setLevel("WARNING")

    raw_in = read_input('data/day_21.txt')
    program = [int(i) for i in raw_in[0].split(',')]
        
    solve_1(program)
    solve_2(program)