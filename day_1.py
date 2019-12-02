import pandas as pd

def get_fuel_simple(mass):
    return int(mass/3) - 2

def get_fuel_reqs(mass):
    s = 0
    while mass > 0:
        mass = get_fuel_simple(mass)
        s += mass
    return s


if __name__ == "__main__":
    data = list(pd.read_csv("data/input_1.csv", header=None)[0])
    
    print("Part 1 result: ", sum(map(get_fuel_simple, data)))
    print("Part 1 result: ", sum(map(get_fuel_reqs, data)))

