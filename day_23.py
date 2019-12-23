import logging
logging.basicConfig(format='%(levelname)s %(message)s')

from common import *
from computer import Computer


class NIC:
    def __init__(self, address, program):
        self.address = address
        self.c = Computer(program)
        self.c.add_input(address)
        self.c.run()

    def __repr__(self):
        return f"NIC-{self.address}"

    def run(self):
        if len(self.c.state.input_stack) == 0:
            self.c.add_input(-1)
            logging.debug(f"{self} input stack empty, using -1 as input")
        self.c.run()
        o = self.c.state.outputs
        self.c.state.outputs = []
        return o



def send_packet(destination, x, y):
    logging.debug(f"Sending packet({x}, {y}) to {destination}")
    destination.c.state.input_stack = [y, x] + destination.c.state.input_stack


def is_idle(network):
    statuses = [(len(n.c.state.input_stack) == 0) for n in network]
    return all(statuses)

def solve(program):
    network = [NIC(i, program) for i in range(50)]

    n = network[0]

    nat_x = -1
    nat_y = -1

    for _ in range(100):
        i = 0
        for n in network:
            packets = n.run()

            for d, x, y in chunked(packets, 3):
                if d == 255:
                    nat_x, nat_y = x, y
                else:
                    i += 1
                    send_packet(network[d], x, y)

        if is_idle(network):
            logging.info(f"Network idle, NAT sending {nat_x} to {nat_y}")
            send_packet(network[0], nat_x, nat_y)
        else:
            logging.info(f"Network processing normally, packets sent {i}")


if __name__ == "__main__":
    logging.getLogger().setLevel("INFO")

    raw_in = read_input('data/day_23.txt')
    program = [int(i) for i in raw_in[0].split(',')]

    solve(program)