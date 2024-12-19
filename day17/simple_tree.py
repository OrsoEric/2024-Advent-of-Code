#------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#------------------------------------------------------------------------------------------------------------------------------

import logging

from typing import Set, Dict, List, Tuple

import copy

from random import randint

from itertools import product

class Node:
    def __init__(self, i_payload):
        self.payload = i_payload
        self.n_level = -1
        #Link to the father
        self.cl_father : Node = None
        #Links to the children, if any
        self.lcl_children : List[Node] = list()
        #remember how many time this node has been visited
        self.n_cnt_visited = 0

    def add(self, i_payload, ib_debug = False):
        """Add a leaf (child node) to this tree node."""
        cl_new_node = Node(i_payload)
        cl_new_node.n_level = self.n_level +1
        cl_new_node.cl_father = self

        if ib_debug:
            logging.debug(f"New node: {cl_new_node}")
        self.lcl_children.append(cl_new_node)
        return cl_new_node

    def __repr__(self):
        """String representation of the tree structure."""
        return f"Level: {self.n_level} | Visits: {self.n_cnt_visited} | Num Children: {len(self.lcl_children)} | Payload {self.payload} "

    def __str__(self):
        return self.__repr__()

    def set_visited(self) -> bool:
        """Increase the visit counter"""
        self.n_cnt_visited += 1
        return False #OK

    def get_visits(self) -> int:
        return self.n_cnt_visited

    def get_level(self):
        return self.n_level
    
    def get_num_children(self) -> int:
        return len(self.lcl_children)
    
    def get_father(self) -> Tuple[bool, int]:
        if self.cl_father is None:
            return True, None #FAIL
        return False, self.cl_father

    def get_child(self, in_index : int ) -> Tuple[bool, int]: 
        """
        ask the tree for a child
        """
        if in_index >= len(self.lcl_children):
            logging.error(f"ERROR OOB: trying to get child {in_index} of {len(self.lcl_children)}")
            return True, None #FAIL
        return False, self.lcl_children[in_index]
    
    def show_children(self):
        for n_index, cl_child in enumerate(self.lcl_children):
            logging.debug(f"Child {n_index} | {cl_child}")

class Tree:
    def __init__(self):
        """Initialize the tree with a root node."""
        self.root = Node(None)
        self.root.n_level = 0

    def add_node(self, icl_father, i_payload):
        """Add multiple leaves to a given parent node."""
        for value in i_payload:
            icl_father.add(value)

    def __repr__(self):
        """String representation of the tree."""
        return str(self.root)

def test_tree():
    # Example usage
    tree = Tree()

    # Add leaves to the root node
    child1 = tree.root.add("Child 1")
    child2 = tree.root.add("Child 2")

    # Add more leaves to specific nodes
    tree.add_node(child1, ["Child 1.1", "Child 1.2"])
    tree.add_node(child2, ["Child 2.1", "Child 2.2"])

    # Display the tree structure
    print(tree)

#test_tree()
