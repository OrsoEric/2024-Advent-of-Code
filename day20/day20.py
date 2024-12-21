#------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#------------------------------------------------------------------------------------------------------------------------------

import logging

from typing import Set, Dict, List, Tuple

from itertools import combinations

#import copy

#from map_of_symbols import Map_of_symbols

from labirinth import Labirinth

#used to count the paths
from collections import Counter

#------------------------------------------------------------------------------------------------------------------------------
#   RULES
#------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------
#   ALGORITHM
#------------------------------------------------------------------------------------------------------------------------------


class Day20:
    def __init__(self):
        self.gcl_labirinth = Labirinth()
        self.cs_solution = 'x'
        #dictionary that counts all the possible cheats and their score
        self.gd_count : Counter = Counter()
        #dictionary that count the savings compared to original labirinth
        self.gd_count_savings : Counter = Counter()
        
    def load(self, is_filename : str ) -> bool:
        self.gcl_labirinth.load_from_file( is_filename )

        return False #OK
    
    def solve(self) -> Tuple[bool, Set[Tuple[int,int]] ]:
        """
        Solve the labirinth
        Returns the set of all coordinates that lie on the optimal path
        """
        b_fail, dtnn_tiles_on_optimal_path = self.gcl_labirinth.find_shortest_path()
        #if labirinth is not solvable
        if b_fail:
            return True #FAIL
        self.gcl_labirinth.get_map_cost().show_map()
        return False, dtnn_tiles_on_optimal_path #OK
    
    @staticmethod
    def from_line_to_list_of_points(itnn_start : Tuple[int,int], itnn_end : Tuple[int,int], ib_debug = False) -> Tuple[ bool,List[Tuple[int,int]] ]:
        """
        Give a start and end point
        part of a horizontal or vertical line
        Return a list of all the points that make up that line
        """

        #points that make up the line
        ltnn_line : List[Tuple[int,int]] = list()

        tnn_a = itnn_start
        tnn_b = itnn_end
        #Vertical lines have the same X
        if (tnn_a[1] == tnn_b[1]):
            n_x = tnn_a[1]
            #make sure that the pairs are in the correct order
            if (tnn_a[0] > tnn_b[0]):
                tnn_b, tnn_a = tnn_a, tnn_b
            #scan from A.Y to B.Y
            for n_y in range(tnn_a[0], tnn_b[0]+1):
                tnn_coordinate = (n_y, n_x)
                #add this point to the line
                ltnn_line.append( tnn_coordinate )
        #Horizontal lines have the same Y
        elif (tnn_a[0] == tnn_b[0]):
            n_y = tnn_a[0]
            #make sure that the pairs are in the correct order
            if (tnn_a[1] > tnn_b[1]):
                tnn_b, tnn_a = tnn_a, tnn_b
            #scan from A.X to B.X
            for n_x in range(tnn_a[1], tnn_b[1]+1):
                tnn_coordinate = (n_y, n_x)
                #add this point to the line
                ltnn_line.append( tnn_coordinate )
        #Points are not H or V line
        else:
            return True, list() #NOT a H-V line
        if ib_debug:
            logging.debug(f"Found line of length {len(ltnn_line)} | Points: {ltnn_line}")
        #Return H or V Line 
        return False, ltnn_line #OK

    def find_possible_cheats( self, idtnn_tiles_on_optimal_path : Set[Tuple[int,int]], ib_debug = False ) -> Tuple[ bool,List[List[Tuple[int,int]]] ]:
        """
        Given a set of tiles that are on the optimal path
        find a list of all possible cheat positions
        A cheat is either one or two coordinates of a wall '#' "##"
        That is sandwitched between two optimal tiles 'O'

        There could be an exception for O.#O
        a void not on optimal because of a wall
        looking at the map it's not the case here because it's a single line corridor
        """

        cl_map = self.gcl_labirinth.get_map()
        #list of all possible cheats
        lltnn_cheats : List[List[Tuple[int,int]]] = list()

        #scan all unique combinations of pairs
        for tst_pairs in combinations(idtnn_tiles_on_optimal_path,2):
            #logging.debug(f"Pair: {tst_pairs}")
            #extract the coordinates
            tnn_a = tst_pairs[0]
            tnn_b = tst_pairs[1]
            #From the coordinates, get the list of points if it's a line
            b_fail, ltnn_line_points = self.from_line_to_list_of_points( tnn_a, tnn_b )
            #if not a H or V line
            if b_fail:
               #skip
               pass
            #I only want lines of lenght 3 and 4 that have 1 or 2 possible walls
            elif len(ltnn_line_points) >= 3 and len(ltnn_line_points) <= 4:
                ltnn_cheat_walls : List[Tuple[int,int]] = list()
                #counter for what's in the line
                n_cnt_walls = 0
                n_cnt_void = 0
                #scan the line
                for tnn_line_point in ltnn_line_points:
                    #get the tile symbol
                    b_fail, s_value = cl_map.get_coordinate( tnn_line_point )
                    if b_fail:
                        logging.error("Invalid coordinate {tnn_line_point}")
                        return True, list() #FAIL
                    elif s_value == self.gcl_labirinth.cs_void:
                        n_cnt_void += 1
                    elif s_value == self.gcl_labirinth.cs_wall:
                        n_cnt_walls += 1
                        ltnn_cheat_walls.append(tnn_line_point)
                    else:
                        logging.error(f"Invalid labirinth symbol: {s_value}")
                        return True, list() #FAIL
                logging.debug(f"Found line of length {len(ltnn_line_points)} | Voids: {n_cnt_void} | Walls: {n_cnt_walls} | Points: {ltnn_line_points}")
                #A valid line should only have 2 voids and walls
                if n_cnt_void == 2:
                    #I found a cheat. Save all the cheat wallsin the solution
                    lltnn_cheats.append(ltnn_cheat_walls)

        logging.info(f"Found {len(lltnn_cheats)} cheats | {lltnn_cheats}")
        return False, lltnn_cheats

    def find_cheats(self) -> bool: 
        b_fail, dtnn_tiles_on_optimal_path = self.gcl_labirinth.find_shortest_path()
        if b_fail:
            logging.error("ERROR: no solution...")
            return True #FAIL
        #get the score
        n_score = self.gcl_labirinth.get_score()
        #count the score
        self.gd_count[n_score] +=1
        self.gd_count_savings[0] += 1


        b_fail, lltnn_cheat_wall = self.find_possible_cheats( dtnn_tiles_on_optimal_path )
        if b_fail:
            logging.error("ERROR: couldn't find any cheat...")
            return True #FAIL

        #dictionary to count all the cheats
        
        #get the map
        cl_map = self.gcl_labirinth.get_map()
        cs_void = self.gcl_labirinth.cs_void
        cs_wall = self.gcl_labirinth.cs_wall
        #for each cheat
        for n_index, ltnn_cheat in enumerate(lltnn_cheat_wall):
            if n_index % 10 == 0:
                print(f"Processing cheat {n_index} of {len(lltnn_cheat_wall)}")

            logging.info(f"CHEAT: {ltnn_cheat}")

            #for each wall in the cheat
            for tnn_cheat_wall in ltnn_cheat:
                #get symbol
                b_fail, s_symbol = cl_map.get_coordinate( tnn_cheat_wall )
                if b_fail:
                    logging.error(f"ERROR: Failed to get symbol at {tnn_cheat_wall}")
                    return True
                elif s_symbol != cs_wall:
                    logging.error(f"ERROR: there should be a wall {cs_wall} at {tnn_cheat_wall} but there is a  {s_symbol}")
                    return True

                #in the map turn that wall into a void
                b_fail = cl_map.set_coordinate( tnn_cheat_wall, cs_void )
                if b_fail:
                    logging.error(f"ERROR: Could not set {tnn_cheat_wall} to {cs_void}")
                    return True
                
            #solve the labirinth
            b_fail, dtnn_cheat_solution = self.gcl_labirinth.find_shortest_path()
            if b_fail:
                logging.error(f"ERROR: Could not find solution to cheat labirinth...")
                return True

            n_cheat_score = self.gcl_labirinth.get_score()
            logging.info(f"Cheat {ltnn_cheat} has cost: {n_cheat_score}")
            self.gd_count[n_cheat_score] += 1
            self.gd_count_savings[n_score -n_cheat_score] += 1

            #for each wall in the cheat
            for tnn_cheat_wall in ltnn_cheat:
                #get symbol
                b_fail, s_symbol = cl_map.get_coordinate( tnn_cheat_wall )
                if b_fail:
                    logging.error(f"ERROR: Failed to get symbol at {tnn_cheat_wall}")
                    return True
                elif s_symbol != cs_void:
                    logging.error(f"ERROR: there should be a void {cs_void} at {tnn_cheat_wall} but there is a  {s_symbol}")
                    return True
                #in the map turn that void into a wall
                b_fail = cl_map.set_coordinate( tnn_cheat_wall, cs_wall )
                if b_fail:
                    logging.error(f"ERROR: Could not set {tnn_cheat_wall} to {cs_wall}")
                    return True

        logging.info("Score of all possible cheats:")
        logging.info(f"{sorted(self.gd_count.items(), key=lambda i: -i[0])}")

        logging.info("Savings of all possible cheats:")
        logging.info(f"{sorted(self.gd_count_savings.items(), key=lambda i: -i[0])}")

        

        return False
    


#------------------------------------------------------------------------------------------------------------------------------
#   SOLUTION
#------------------------------------------------------------------------------------------------------------------------------

def solution() -> bool:

    #cl_labirinth = Labirinth()
    #cl_labirinth.load_from_file( "day20/day20-example.txt" )
    
    cl_day20 = Day20()
    #cl_day20.load( "day20/day20-example-15x15.txt" )
    cl_day20.load( "day20/day20-labirinth-141x141.txt" )

    #cl_day20.solve()

    cl_day20.find_cheats()

    return False #OK

#------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(
        filename="day20/day20.log",
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin")

    solution()
