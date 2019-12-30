from common import *
from itertools import count
from string import ascii_letters
import logging
logging.basicConfig(format='%(levelname)s %(message)s')


CHARS = {n: chr(n) for n in range(256)}
FILL_SYMBOL = " "


def find_symbol(symbol, a):
    tmp = np.where(a == ord(symbol))
    if sum(sum(tmp)) > 0:
        if len(tmp[0]) > 1:
            return list(zip(*tmp))
        else:
            return [(tmp[0][0], tmp[1][0])]


def create_teleport_dict(area):
    pairs = {}
    for c in ascii_letters:
        locs = find_symbol(c, area)
        try:
            if len(locs) >= 2:
                pairs[c] = locs
        except:
            pass
    return pairs


def get_unfilled_neighbors(c, a):
    tmp = (c[0] + 1, c[1]), (c[0] - 1, c[1]
                             ), (c[0], c[1] + 1), (c[0], c[1] - 1)
    return set([c for c in tmp if a[c] not in (ord('#'), ord(' '))])


def get_teleport_pair(symbol, loc, teleport_dict):
    logging.debug(f"Trying to get {symbol} from {loc}")
    both = teleport_dict.get(symbol)
    for i in both:
        if i != loc:
            return i


class Maze:
    def __init__(self, area, start=None, level=None):
        self.area = area.copy()
        self.frontier = set()

        if start:
            self.area[start] = ord(FILL_SYMBOL)
            self.frontier |= get_unfilled_neighbors(start, self.area)

        if level == 'first':
            td = create_teleport_dict(self.area)
            for _, cells in td.items():
                for c in cells:
                    if self._is_outer_tele(c):
                        self.area[c] = ord('#')

        if level == 'inner':
            start = find_symbol('A', self.area)[0]
            end = find_symbol('Z', self.area)[0]

            self.area[start] = ord('#')
            self.area[end] = ord('#')

    def _is_outer_tele(self, loc):
        last_row = self.area.shape[0] - 2
        last_col = self.area.shape[1] - 2

        if (loc[0] in (1, last_row)) | (loc[1] in (1, last_col)):
            return True
        else:
            return False

    def draw(self):
        print_array(self.area, CHARS)

    def step(self):
        nodes_reached = set()
        next_round = self.frontier.copy()
        for c in self.frontier:
            next_round -= {c}
            code = self.area[c]

            if code == ord('.'):
                next_round |= get_unfilled_neighbors(
                    c, self.area)  # Get next round neighbors
            else:
                nodes_reached.add((chr(code), c))

            self.area[c] = ord(FILL_SYMBOL)  # Fill
        self.frontier = next_round
        return nodes_reached

    def teleport_to(self, destination):
        self.area[destination] = ord(FILL_SYMBOL)
        neighbors = get_unfilled_neighbors(destination, self.area)
        for n in neighbors:
            self.area[n] = ord(FILL_SYMBOL)
            self.frontier |= get_unfilled_neighbors(
                n, self.area)  # Get next round neighbors


def solve_1(area):
    start = find_symbol('A', area)[0]
    td = create_teleport_dict(area)

    maze = Maze(area, start)

    for i in range(10_000):
        nodes_reached = maze.step()
        if nodes_reached:
            for symbol, loc in nodes_reached:
                if symbol == 'Z':
                    print(f"Step 1 answer: reached end on step {i-1}")
                    return maze
                else:
                    destination = get_teleport_pair(symbol, loc, td)
                    maze.teleport_to(destination)
    maze.draw()


def solve_2(area):
    start = find_symbol('A', area)[0]
    td = create_teleport_dict(area)

    mazes = {0: Maze(area, start, level='first')}

    for i in range(20_000):
        # Take a step in all mazes and collect teleports reached
        teles_this_round = []
        for m_idx, maze in mazes.items():
            nodes_reached = maze.step()
            if nodes_reached:
                for symbol, loc in nodes_reached:
                    if symbol == 'Z':
                        print(f"Step 2 answer: reached end on step {i-1}")
                        return mazes
                    else:
                        if maze._is_outer_tele(loc):
                            dst_maze_idx = m_idx-1
                        else:
                            dst_maze_idx = m_idx+1
                        dst_loc = get_teleport_pair(symbol, loc, td)
                        teles_this_round.append((dst_maze_idx, dst_loc))

        # Perform the teleportations for this round
        for dst_maze_idx, dst_loc in teles_this_round:
            if dst_maze_idx not in mazes:
                mazes[dst_maze_idx] = Maze(area, level='inner')
            mazes[dst_maze_idx].teleport_to(dst_loc)
    print("Goal not reached")


if __name__ == "__main__":
    logging.getLogger().setLevel("INFO")

    raw_in = read_input('data/day_20.txt')
    area = str_to_array(raw_in)

    maze = solve_1(area)
    mazes = solve_2(area)
