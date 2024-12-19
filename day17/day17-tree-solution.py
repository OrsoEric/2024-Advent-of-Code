#------------------------------------------------------------------------------------------------------------------------------
#   
#------------------------------------------------------------------------------------------------------------------------------
#   I observe that I should match from the end and match one digit at a time
#   I can build a tree were each octal digit spawn a leaf
#
#   I got the tree working, I want to always increase the rightmost matching
#   as I know  no solution has a decreasing matching number (???)
#
#   Exploration policies:
#   1)
#       if matching doesn't increase
#       mark the exploration count of the node +1
#       go up
#       I need to select the node that has been explored the least, with the highest fitness
#
#   There is still an heavy bias toward visiting instead of spawning new nodes
#   I also need to look at the visit counters
#   



#------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#------------------------------------------------------------------------------------------------------------------------------

import logging

from typing import Set, Dict, List, Tuple

from copy import deepcopy

#from map_of_symbols import Map_of_symbols

from individual import Individual


from simple_tree import Tree, Node

from random import randint

#------------------------------------------------------------------------------------------------------------------------------
#   RULES
#------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------
#   ALGORITHM
#------------------------------------------------------------------------------------------------------------------------------

class Payload:
    ln_input_octal_reverse : List[int] = list()
    ln_output : List[int] = list()
    n_rightmost_valid : int = -1
    n_valid : int = -1

    def __init__(self):
        self.clear()

    def clear(self):
        self.ln_input_octal_reverse = list()
        self.ln_output = list()
        self.n_rightmost_valid = -1
        self.n_valid = -1

    def __repr__(self):
        return f"Fitness: {self.n_rightmost_valid} {self.n_valid} | Input: {self.ln_input_octal_reverse} | Output {self.ln_output}"
    
class Tree_search:

    def __init__(self):
        self.cn_octal_base = 8
        self.gln_output_desired : List[int] = list()
        self.gln_input_octal_reverse_start : List[int] = list()
        #create a tree
        self.gcl_tree = Tree()

        #COUNTERS
        self.n_cnt_down = 0
        self.n_cnt_up = 0
        self.n_cnt_new = 0
        self.cnt_father_fitness_roll = 0
        self.cnt_father_visit_roll = 0

    def choose_next_node(self, icl_node : Node ) -> Tuple[bool, Node ]:
        """
        How to choose what node to explore
        IF I have a better node, always go down
        IF the level is lower than the match, I have an higher and higher chance of going up
        """

        #sort the nodes by fitness
        self.sort_payloads(icl_node.lcl_children)
        icl_node.show_children()

        #the next node to explore is the one with the highest fitness
        b_fail, cl_node_cursor_fittest = icl_node.get_child(0)
        if b_fail:
            logging.error(f"I tried to get the best child, but failed to get it")
            return True #FAIL

        #difference between fitness of target -current
        #a positive number  means down is better
        n_delta = cl_node_cursor_fittest.payload.n_rightmost_valid -icl_node.payload.n_rightmost_valid 
        logging.debug(f"Current fitness {cl_node_cursor_fittest.payload.n_rightmost_valid } Best child fitness: {icl_node.payload.n_rightmost_valid} | Delta: {n_delta}")
        cl_node_next : Node = None

        #If I have a fitter child
        if n_delta > 0:
            #always go down
            return False, cl_node_cursor_fittest
        else:
            #look at the current level
            #the new delta is how much deeper I am thean the rightmost match
            n_delta = icl_node.n_level -icl_node.payload.n_rightmost_valid
            #roll a number
            n_roll = randint( -2, 5 )
            b_go_up = False
            #The deeper I am compared to the match, the higher the chance I have to go up to fix something earlier and pick another path
            #E.g. level 12. match 8. delta 4
            #I need to roll better than 4 to keep going down, low chance
            #E.g. level 8. match 8. delta 0
            #I need to roll better than 0 to keep going down, high chance
            if n_roll > n_delta:
                logging.debug(f"FITNESS ROLL {n_delta} of {n_roll} -> GO DOWN")
                b_go_up = False
            else:
                logging.debug(f"FITNESS ROLL {n_delta} of {n_roll} -> GO UP")
                self.cnt_father_fitness_roll += 1
                b_go_up = True

        
        b_fail, cl_node_cursor_father = icl_node.get_father()
        if b_fail:
            logging.error(f"Want to go up, but could not get father ling")
            return True, None #FAI

        #VISITS cannot force a Up from previous rule
        #Compute the difference between child visits and father visits.
        #if the visit of child is high and the number is positive
        #child needs to roll high to keep going down and keep visiting
        #this adds a bias to explore
        n_delta_visit = cl_node_cursor_fittest.n_cnt_visited -4*cl_node_cursor_father.n_cnt_visited
        n_roll_visit = randint( 0, 2*8 )
        #if the child wins the roll
        if n_roll_visit > n_delta_visit:
            logging.debug(f"VISIT ROLL {n_roll_visit} of {n_delta_visit} -> GO DOWN")
            b_go_up |= False
        else:
            logging.debug(f"VISIT ROLL {n_roll_visit} of {n_delta_visit} -> GO UP")
            self.cnt_father_visit_roll += 1
            b_go_up |= True

        #if cl_node_cursor.payload.n_rightmost_valid < cl
        if b_go_up and icl_node.n_level > 0:
            self.n_cnt_up += 1
            cl_node_next = cl_node_cursor_father
        else:
            cl_node_next = cl_node_cursor_fittest
            self.n_cnt_down += 1

        return False, cl_node_next #OK

    def search(self) -> bool:
        #initialize root payload
        st_payload = Payload()
        st_payload.clear()
        st_payload.ln_input_octal_reverse = self.gln_input_octal_reverse_start

        #at the root
        cl_node_cursor : Node = self.gcl_tree.root
        cl_node_cursor.payload = st_payload

        n_len_input = len(self.gln_input_octal_reverse_start)

        n_cnt_iteration = 0

        b_continue = True
        while b_continue:
            n_cnt_iteration += 1
            if n_cnt_iteration % 500 == 0:
                logging.info(f"Iteration {n_cnt_iteration} Processing {cl_node_cursor} | DOWN {self.n_cnt_down} | UP {self.n_cnt_up} | NEW {self.n_cnt_new} | ROLL {self.cnt_father_fitness_roll}  {self.cnt_father_visit_roll}")
                print(f"Iteration {n_cnt_iteration} Processing {cl_node_cursor}")

            if n_cnt_iteration > 1000000:
                logging.info("ITERATION LIMIT")
                b_continue = False

            #fetch this node's input
            ln_current_input = cl_node_cursor.payload.ln_input_octal_reverse
            logging.debug(f"PROCESS: {cl_node_cursor}")

            if cl_node_cursor.payload.n_rightmost_valid == n_len_input:
                logging.info(f"SOLUTION: {cl_node_cursor}")
                cl_individual : Individual = Individual()
                cl_individual.clear()
                cl_individual.ln_input_octal_reverse = cl_node_cursor.payload.ln_input_octal_reverse
                cl_individual.environment()
                logging.info(f"Decimal: {cl_individual.n_input} octal: {oct(cl_individual.n_input)}")

            #if it's the last node
            if cl_node_cursor.get_level() == n_len_input:
                #Remember the visit
                cl_node_cursor.set_visited()

                #go up a level
                b_fail, cl_node_cursor_next = cl_node_cursor.get_father()
                if b_fail:
                    logging.error(f"Could not go up from {cl_node_cursor} to {cl_node_cursor_next}")
                    return True #FAIL
                cl_node_cursor = cl_node_cursor_next
                logging.debug(f"UP {cl_node_cursor}")

            #if the node doesn't have children
            elif cl_node_cursor.get_num_children() <= 0:
                self.n_cnt_new += 1
                #Remember the visit
                cl_node_cursor.set_visited()
                #add one octal digit
                for n_cnt in range(self.cn_octal_base):
                    
                    #make a copy of the payload
                    ln_new_input = deepcopy( ln_current_input )
                    #change the digit according to the node level
                    n_index = len(ln_current_input) -1 -cl_node_cursor.get_level()
                    ln_new_input[n_index] = n_cnt

                    #compute the output
                    cl_individual = Individual()
                    cl_individual.clear()
                    cl_individual.ln_input_octal_reverse = ln_new_input
                    cl_individual.environment()

                    #compute the fitness metric
                    b_fail,n_rightmost_valid = cl_individual.compute_rightmost_correct_digits( self.gln_output_desired )
                    b_fail,n_valid = cl_individual.compute_valid_digits( self.gln_output_desired )

                    #create a new payload
                    st_payload = Payload()
                    st_payload.clear()
                    st_payload.ln_input_octal_reverse = ln_new_input
                    st_payload.ln_output = cl_individual.ln_output
                    st_payload.n_rightmost_valid = n_rightmost_valid
                    st_payload.n_valid = n_valid

                    #Add the input and the fitness to the node
                    cl_node_cursor.add( st_payload )

                b_fail, cl_node_cursor = self.choose_next_node( cl_node_cursor )
                if b_fail:
                    logging.error("ERROR: failed to select next")
                    return True
                
                logging.debug(f"SELECT: {cl_node_cursor}")
                
            #if the node already has children
            else:
                #I have visited the node
                cl_node_cursor.set_visited()
                
                b_fail, cl_node_cursor = self.choose_next_node( cl_node_cursor )
                if b_fail:
                    logging.error("ERROR: failed to select next")
                    return True


        logging.debug(f"{self.gcl_tree}")

        return False #OK

    def sort_payloads(self, ilcl_children : List[Node] ) -> bool:
        """
        Given a list of children, sort them by payload 
        1 - lowest visits (positive)
        2 - rightmost digits correct HIGH (negative)
        3 - then getting most overall digits correct (negative)


        """

        # Define the sorting key
        def sort_key(icl_node : Node):
            #return ( icl_node.n_cnt_visited, -icl_node.payload.n_rightmost_valid, -icl_node.payload.n_valid )
            return ( 10*(-icl_node.payload.n_rightmost_valid) +1*(-icl_node.payload.n_valid) +1*(icl_node.n_cnt_visited) )
        #sort by key
        ilcl_children.sort( key=sort_key )

        return False #OK



#

#------------------------------------------------------------------------------------------------------------------------------
#   SOLUTION
#------------------------------------------------------------------------------------------------------------------------------

def solution() -> bool:
    #I want the output to be this
    ln_output_desired       = [2, 4, 1, 2, 7, 5, 4, 7, 1, 3, 5, 5, 0, 3, 3, 0]
    #this is the starting input reversed octal input
    ln_input_octal_reverse  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #ln_input_octal_reverse  = [4, 6, 7, 6, 3, 1, 5, 6, 0, 4, 0, 6, 4, 0, 5, 1, 0]
    #ln_input_octal_reverse  = [3, 2, 2, 3, 5, 7, 5, 7, 2, 3, 0, 6, 5, 6, 0, 1, 0]

    cl_tree_search = Tree_search()
    cl_tree_search.gln_output_desired = ln_output_desired
    cl_tree_search.gln_input_octal_reverse_start = ln_input_octal_reverse
    b_fail = cl_tree_search.search()
    if b_fail:
        logging.error(f"ERROR: Search failed")




    return False #OK

#------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(
        filename="day17/day17.log",
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin")

    solution()
