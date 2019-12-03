from common import read_input

def get_fuel_simple(mass):
    return int(mass/3) - 2

def get_fuel_reqs(mass):
    s = 0
    while mass > 0:
        mass = get_fuel_simple(mass)
        s += mass
    return s


if __name__ == "__main__":
    raw_in = read_input('data/day_1.txt')
    data = [int(i) for i in raw_in]

    print("Part 1 result: ", sum(map(get_fuel_simple, data)))
    print("Part 1 result: ", sum(map(get_fuel_reqs, data)))

