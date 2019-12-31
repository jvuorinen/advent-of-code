from common import *
import logging
logging.basicConfig(format='%(levelname)s %(message)s')

SIZE = 5
POINTS = np.array([2**i for i in range(SIZE**2)])


class RegularGrid:
    def __init__(self, area):
        self.area = area.copy()

    def get_neighbors(self, c):
        tmp = (c[0] + 1, c[1]), (c[0] - 1, c[1]
                                 ), (c[0], c[1] + 1), (c[0], c[1] - 1)
        return [self.area[c] for c in tmp]

    def update(self):
        a = self.area.copy()
        maxlen = SIZE + 1

        for i in range(1, maxlen):
            for j in range(1, maxlen):
                neighbors = self.get_neighbors((i, j))
                n_bugs = len([n for n in neighbors if n == ord('#')])

                if (self.area[i, j] == ord('.')) & (n_bugs in (1, 2)):
                    a[i, j] = ord('#')
                elif (self.area[i, j] == ord('#')) & (n_bugs != 1):
                    a[i, j] = ord('.')
                else:
                    a[i, j] = self.area[i, j]

        self.area = a.copy()

    def get_rating(self):
        maxlen = SIZE + 1
        bugs = self.area[1:maxlen, 1:maxlen].flatten() == ord('#')

        total = sum(bugs * POINTS)
        return total

    def draw(self):
        print_array(self.area)


def _get_same_level_neighbors(i, j):
    candidates = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
    return [(a, b) for a, b in candidates if (0 <= a <= 4) & (0 <= b <= 4) & ((a, b) != (2, 2))]


def _get_outer_level_neighbors(i, j):
    n = []
    if i == 0:
        n .append((1, 2))
    elif i == 4:
        n.append((3, 2))

    if j == 0:
        n.append((2, 1))
    elif j == 4:
        n.append((2, 3))

    return n


def _get_inner_level_neighbors(i, j):
    if (i, j) == (2, 1):
        return [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
    elif (i, j) == (2, 3):
        return [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]
    elif (i, j) == (1, 2):
        return [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
    elif (i, j) == (3, 2):
        return [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
    else:
        return []


def _create_neighbor_dict():
    neighbors = {
        (i, j): {
            -1: _get_outer_level_neighbors(i, j),
            0: _get_same_level_neighbors(i, j),
            1: _get_inner_level_neighbors(i, j)
        }
        for i in range(5) for j in range(5)}
    del(neighbors[(2, 2)])
    return neighbors


class RecursiveGrid:
    neighbors = _create_neighbor_dict()

    def __init__(self, area):
        a = area.copy()
        midpoint = int(a.shape[0]/2)
        a[midpoint, midpoint] = ord('?')
        self.levels = {0: a}

    def _create_empty_grid(self):
        a = self.levels[0].copy()
        a[:, :] = ord('.')
        midpoint = int(a.shape[0]/2)
        a[midpoint, midpoint] = ord('?')
        return a

    def _create_empty_level_dict_borders(self):
        """Creates two empty levels to both ends
        in order to avoid indexerrors"""
        lmin, lmax = min(self.levels.keys()), max(self.levels.keys())
        self.levels[lmin-2] = self._create_empty_grid()
        self.levels[lmin-1] = self._create_empty_grid()
        self.levels[lmax+1] = self._create_empty_grid()
        self.levels[lmax+2] = self._create_empty_grid()

    def _delete_empty_level_dict_borders(self):
        lmin, lmax = min(self.levels.keys()), max(self.levels.keys())

        if self.count_bugs_on_level(lmin) == 0:
            del(self.levels[lmin])
        if self.count_bugs_on_level(lmin+1) == 0:
            del(self.levels[lmin+1])
        if self.count_bugs_on_level(lmax-1) == 0:
            del(self.levels[lmax-1])
        if self.count_bugs_on_level(lmax) == 0:
            del(self.levels[lmax])

    def _count_neighboring_bugs(self, level, cell):
        n_bugs = 0
        nbrs = self.neighbors[cell]
        for level_offset, locs in nbrs.items():
            for loc in locs:
                if self.levels[level+level_offset][loc] == ord('#'):
                    n_bugs += 1
        return n_bugs

    def step(self):
        self._create_empty_level_dict_borders()
        lmin, lmax = min(self.levels.keys()), max(self.levels.keys())

        to_be_add = []
        to_be_removed = []
        for level_idx, level in self.levels.items():
            # Skip the first and last levels that cannot have bugs
            if level_idx in {lmin, lmax}:
                continue
            # Calculate the number of bugs to be add and removed
            for i in range(SIZE):
                for j in range(SIZE):
                    if i == j == 2:
                        continue
                    current_value = chr(level[i, j])
                    n_nbr_bugs = self._count_neighboring_bugs(
                        level_idx, (i, j))

                    if (current_value == '.') & (n_nbr_bugs in (1, 2)):
                        to_be_add.append((level_idx, (i, j)))
                    elif (current_value == '#') & (n_nbr_bugs != 1):
                        to_be_removed.append((level_idx, (i, j)))

        # Perform additions and deletions in one go
        for level_idx, loc in to_be_add:
            self.levels[level_idx][loc] = ord('#')

        for level_idx, loc in to_be_removed:
            self.levels[level_idx][loc] = ord('.')

        self._delete_empty_level_dict_borders()

    def count_bugs_on_level(self, level):
        return sum(sum(self.levels[level] == ord('#')))

    def count_bugs_in_total(self):
        lmin, lmax = min(self.levels.keys()), max(self.levels.keys())
        s = 0
        for i in range(lmin, lmax+1):
            s += self.count_bugs_on_level(i)
        return s

    def draw(self):
        lmin, lmax = min(self.levels.keys()), max(self.levels.keys())
        for i in range(lmin, lmax+1):
            print(f"Level {i}:")
            print_array(self.levels[i])
            print()


def solve_1(area):
    grid = RegularGrid(area)
    ratings = {grid.get_rating()}

    i = 0
    while True:
        i += 1
        if i % 100_000 == 0:
            logging.info(f"On iteration {i:,}")
        grid.update()
        s = grid.get_rating()
        if s in ratings:
            logging.info(f"Step 1 answer: {s} (iteration {i:,})")
            return
            # break
        else:
            ratings.add(s)


def solve_2(area):
    grid = RecursiveGrid(area)
    for _ in range(200):
        grid.step()
    print(f"Step 2 answer: {grid.count_bugs_in_total()}")


if __name__ == "__main__":
    logging.getLogger().setLevel("DEBUG")

    raw_in = read_input('data/day_24.txt')
    area = str_to_array(raw_in)

    # solve_1(area)

    solve_2(area)
