import logging

from common import read_input

logging.getLogger().setLevel('DEBUG')


def has_double(i):
    s = str(i)
    return any((c1 == c2) for c1, c2 in zip(s[:-1], s[1:]))

def has_strict_double(i):
    s = str(i)

    quads = [t for t in zip(s[:-3], s[1:-2], s[2:-1], s[3:])]   

    check_start = (s[0] == s[1] != s[2])
    check_end = (s[-3] != s[-2] == s[-1])
    check_middle = any((a!=b==c!=d) for (a,b,c,d) in quads)

    return check_start | check_end | check_middle

def is_ascending(i):
    s = str(i)
    return all((c1 <= c2) for c1, c2 in zip(s[:-1], s[1:]))

# For part 1
def is_valid(i):
    s = str(i)
    return has_double(s) & is_ascending(s)

def find_valids(low, high):
    return [i for i in range(low, high +1) if is_valid(i)]

# For part 2
def is_valid_2(i):
    s = str(i)
    return has_strict_double(s) & is_ascending(s)

def find_valids_2(low, high):
    return [i for i in range(low, high +1) if is_valid_2(i)]


if __name__ == "__main__":
    print("Part 1 answer: ", len(find_valids(231832, 767346)))
    print("Part 2 answer: ", len(find_valids_2(231832, 767346)))