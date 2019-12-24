import logging
import numpy as np

CHARS = {n: chr(n) for n in range(256)}

def read_input(fp):
    logging.info("Reading file: " + fp)
    with open(fp) as fh:
        result = fh.read()
        
    return result.split('\n')


def getchar():
   """Returns a single character from standard input"""
   import tty, termios, sys
   fd = sys.stdin.fileno()
   old_settings = termios.tcgetattr(fd)
   try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(1)
   finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
   return ch

def str_to_array(raw_in):
    as_list = [list(l) for l in raw_in]
    tmp = [list(map(ord, l)) for l in as_list]
    return np.array(tmp)


def coords_to_array(coords):
    """Makes a np array out of coodinates"""
    # Shift coords to avoid negatives
    x_shift = abs(min(i[0] for i in coords.keys()))
    y_shift = abs(min(i[1] for i in coords.keys()))
    
    cells = {(k[0] + x_shift, k[1] + y_shift): v for k, v in coords.items()}

    # Create a numpy array from coordinate information
    # Note how x and y are represented in a np array
    x_max, y_max = map(max, zip(*cells.keys()))
    a = np.empty(shape=(y_max + 1, x_max + 1)).astype(int)
    a[:] = -1
    for (x, y), v in cells.items():
        a[y_max - y, x] = v

    return a

def print_array(a, conversion = CHARS):
    """Prints a np array to the screen"""
    # conversion = {-1: "░", 0:"▓", 1: " ", 2:"€", 3:"@", 4:"S"}
    l = a.tolist()
    for line in l:
        print("".join(conversion.get(t, " ") for t in line))


def chunked(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]