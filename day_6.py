import logging

from common import read_input


class TreeNode:
    def __init__(self, name):
        self.name = str(name)
        self.children = set()
        self.parent = None

    def __repr__(self):
        return self.name

    def get_ancestors(self):
        l = []
        p = self
        while p.parent is not None:
            l.append(p.parent)
            p = p.parent
        return l

            

class Tree:
    def __init__(self):
        self.nodes = {}
        self.n_nodes = 0
        self.n_direct_relations = 0

    def __repr__(self):
        return f"Tree object containing {self.n_nodes} nodes and {self.n_direct_relations} relations"

    def _add_relation(self, child_name, parent_name):
        if child_name not in self.nodes:
            self.nodes[child_name] = TreeNode(child_name)
            self.n_nodes += 1
            logging.debug(f"Adding node {child_name} to the system ")
        if parent_name not in self.nodes:
            self.nodes[parent_name] = TreeNode(parent_name)
            self.n_nodes += 1
            logging.debug(f"Adding node {parent_name} to the system ")
        self.nodes[child_name].parent = self.nodes[parent_name]
        self.nodes[parent_name].children.add(self.nodes[child_name])
        logging.debug(f"Adding relation {child_name} - {parent_name} to the system ")
        self.n_direct_relations += 1


def create_tree(inputs):
    tree = Tree()
    for s in inputs:
        parent, child = s.split(')')
        tree._add_relation(child, parent)
    return tree


def count_indirect_relations(tree):
    n = 0
    for node in tree.nodes.values():
        n += max(0, len(node.get_ancestors()) - 1)
    return n


def count_all_relations(tree):
    return tree.n_direct_relations + count_indirect_relations(tree)



def find_shortest_path(tree, node_1_name, node_2_name):
    a1 = tree.nodes[node_1_name].get_ancestors()
    a2 = tree.nodes[node_2_name].get_ancestors()

    common = set(a1) & set(a2)

    d1 = (i for i, n in enumerate(a1) if n in common)
    d2 = (i for i, n in enumerate(a2) if n in common)

    return next(d1) + next(d2)

if __name__ == "__main__":
    logging.getLogger().setLevel("INFO")

    inputs = read_input('data/day_6.txt')
    orbits = create_tree(inputs)

    # Part 1
    print(f"Part 1 answer: {count_all_relations(orbits)}") # should be 245089

    # Part 2:
    print(f"Part 2 answer: {find_shortest_path(orbits, 'YOU', 'SAN')}")