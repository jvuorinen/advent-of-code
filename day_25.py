import logging
logging.basicConfig(format='%(levelname)s %(message)s')
from itertools import combinations
import re

from common import *
from computer import Computer

def to_intcode(code):
    return [ord(c) for c in code]

def to_ascii(code):
    return [chr(c) for c in code]


def run_command(computer, command):
    as_code = to_intcode(command + '\n')
    computer.state.input_stack = as_code[::-1]
    computer.run()
    o = "".join(chr(c) for c in computer.state.outputs)
    computer.state.outputs = []
    return o

def try_combo(combo):
    return [f"take {i}" for i in combo] + ['north']

def drop_combo(combo):
    return [f"drop {i}" for i in combo]

def solve_1(program):
    c = Computer(program, mem_size = 10_000)
    c.run()

    # First collect all items and go to the right place
    first_commands = iter([
        "west",
        "take fixed point",
        "north",
        "take sand",
        "south",
        "east",
        "east",
        "north",
        "north",
        "north",
        "north",
        "take easter egg",
        "south",
        "take coin",
        "south",
        "take hypercube",
        "south",
        "west",
        "north",
        "take spool of cat6",
        "north",
        "take shell",
        "west",
        "drop easter egg",
        "drop sand",
        "drop fixed point",
        "drop coin",
        "drop spool of cat6",
        "drop shell",
        "drop hypercube",
        "east",
        "west"
    ])

    for cmd in first_commands:
        last = run_command(c, cmd)

    # Then try out all item combinations
    all_items = [
        "easter egg",
        "sand",
        "fixed point",
        "coin",
        "spool of cat6",
        "shell",
        "hypercube",
    ]

    i = 1
    combo_found = False
    while not combo_found:
        combos = combinations(all_items, i)

        for combo in combos:
            commands = try_combo(combo)
            for cmd in commands:
                last = run_command(c, cmd)

            status = re.findall("heavier|lighter", last)
            if status:
                print(f"Status: should be {status[0]}    {combo}")
            else: 
                print(f"Found good combo: {combo}")
                combo_found = True
                break

            commands = drop_combo(combo)
            for cmd in commands:
                last = run_command(c, cmd)
        i += 1
        
    print()
    print(last)


if __name__ == "__main__":
    logging.getLogger().setLevel("INFO")

    raw_in = read_input('data/day_25.txt')
    program = [int(i) for i in raw_in[0].split(',')]

    solve_1(program)