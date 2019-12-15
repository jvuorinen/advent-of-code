import logging
logging.basicConfig(format='%(levelname)s %(message)s')
from collections import defaultdict
import math

from common import *


def tuplify(s):
    a, b = s.split(' ')
    return (b, int(a))

def parse_prices(lines):
    d = {}
    for txt in lines:
        reqs_str, result_str = txt.split(" => ")
        reqs = [tuplify(x) for x in reqs_str.split(", ")]
        res_name, res_amt = tuplify(result_str)

        d[res_name] = (res_amt, dict(x for x in reqs))
    return d



def calculate_ore_requirement(fuel_amount, recipes):
    intermediate_needs = {'FUEL': fuel_amount}
    amounts_produced = defaultdict(int)
    amounts_needed = defaultdict(int)
    times_produced = defaultdict(int)
    i = 1

    # Iterate through the DAG in reverse order and calculate
    # the firsts estimates of stuff needed and produced
    while set(intermediate_needs.keys()) != {'ORE'}:
        logging.debug(f"------------- Iteration: {i} -------------")
        i += 1
        if i > 100:
            logging.error("FAILSAFE - BREAKING OUT OF LOOP")
            break

        # Go through needed items and update
        needed_next = defaultdict(int)
        for n in intermediate_needs.items():
            name, n_needed = n
            logging.debug(f"We need {n_needed} of {name}")
            if name != 'ORE':
                recipe = recipes.get(name)
                n_recipe, recipe = recipes[name]
                multiplier = math.ceil(n_needed/n_recipe)

                if name != 'FUEL':
                    amounts_produced[name] += (multiplier * n_recipe)
                    amounts_needed[name] += n_needed
                    times_produced[name] += multiplier

                for r_name, r_amt in recipe.items():
                    needed_next[r_name] += multiplier * r_amt

        needed_next['ORE'] += intermediate_needs.get('ORE', 0)
        intermediate_needs = needed_next


    amounts_needed['ORE'] = intermediate_needs['ORE']
    logging.debug(f"Amounts produced: {dict(amounts_produced)}")
    logging.debug(f"Amounts needed: {dict(amounts_needed)}")
    logging.debug(f"Times produced: {dict(times_produced)}")



    # See if anything was produced too many times
    i = 1
    logging.debug(f"Canceling useless production rounds")
    while True:
        useless_prod_rounds = defaultdict(int)
        for k, v in times_produced.items():
            surplus = amounts_produced[k] - amounts_needed[k]
            n_recipe = recipes[k][0]
            if surplus >= n_recipe:
                useless_prod_rounds[k] += int(surplus/n_recipe)

        if len(useless_prod_rounds) == 0:
            break
        else: 
            logging.debug(f"...iteration: {i}")

        # Then, "cancel" those production rounds
        for k, v in useless_prod_rounds.items():
            logging.debug(f"Canceling {v} rounds of {k} production")
            times_produced[k] -= v
            n_recipe, recipe = recipes[k]
            amounts_produced[k] -= v * n_recipe
            for r_name, r_amt in recipe.items():
                amounts_needed[r_name] -= v * r_amt     
        i+= 1
        if i > 100:
            logging.error("FAILSAFE - BREAKING OUT OF LOOP")
            break

    return amounts_needed['ORE']


def calculate_max_fuel_produced(ore_available, recipes):
    """Start from a naive guess and find the answer using 
    binary search. The question is:
    
    How much fuel can you produce with ore_available
    """
    naive_guess = ore_available
    
    guess_low = 1
    guess_high = naive_guess
    guess_mid = int((guess_high-guess_low)/2)
    guess_range = (guess_high - guess_low)

    i = 1
    while guess_range > 2:
        i += 1
        if i > 1000:
            logging.error("FAILSAFE - BREAKING OUT OF LOOP")
            break
        logging.info(f"Iteration: {i}, guess range: {guess_range}")

        ore_req_mid = calculate_ore_requirement(guess_mid, recipes)

        # Update guesses
        if ore_available < ore_req_mid:
            guess_high = guess_mid
        else:
            guess_low = guess_mid
        guess_mid = guess_low + int((guess_high-guess_low)/2)
        guess_range = (guess_high - guess_low)

    return guess_low



if __name__ == "__main__":
    logging.getLogger().setLevel("INFO")

    lines = read_input('data/day_14.txt')

    recipes = parse_prices(lines)

    # Step 1
    amount = calculate_ore_requirement(1, recipes)
    print(f"Step 1 answer: {amount}")

    # Step 2
    ore_available = 1000000000000

    n = calculate_max_fuel_produced(ore_available, recipes)
    print(f"Step 2 answer: {n}") # This gives 1 too low

    calculate_ore_requirement(1122035, recipes)
    calculate_ore_requirement(1122036, recipes)
    calculate_ore_requirement(1122037, recipes)
