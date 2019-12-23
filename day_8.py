import logging
logging.basicConfig(format='%(levelname)s %(message)s')

from common import *

import numpy as np

def get_layers(image: str, height: int, width: int):
    layer_size = height * width
    layerize = lambda x: np.array(list(x)).astype(int).reshape(height, width)
    layers = [layerize(c) for c in chunked(image, layer_size)]
    return layers


def solve_part_1(layers):
    a = min(layers, key = lambda a: (a==0).sum()) # layer with least zeros
    return (a==1).sum() * (a==2).sum()

def solve_part_2(layers):
    big_3d = np.stack(layers)
    _, n_rows, n_cols = big_3d.shape

    # Get visible pixel codes
    get_visible = lambda arr: next(x for x in arr if x != 2)
    visibles = [get_visible(big_3d[:, i, j]) for i in range(n_rows) for j in range(n_cols)]
    a = np.array(visibles).reshape(n_rows, n_cols)

    # Print the result
    conversion = {1: "▓", 0: "░"}
    l = a.tolist()
    print("\n".join(["".join(map(conversion.get, row)) for row in l]))


if __name__ == "__main__":
    raw_in = read_input('data/day_8.txt')[0]

    layers = get_layers(raw_in, 6, 25)
    print(f"Part 1 answer: {solve_part_1(layers)}")

    print("Part 2 answer:")
    solve_part_2(layers)