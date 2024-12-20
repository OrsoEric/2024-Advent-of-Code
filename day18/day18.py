#------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#------------------------------------------------------------------------------------------------------------------------------

import logging

from typing import Set, Dict, List, Tuple

#import copy

from map_of_coordinates import Map_of_coordinates

from map_of_symbols import Map_of_symbols

from labirinth import Labirinth

#------------------------------------------------------------------------------------------------------------------------------
#   RULES
#------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------
#   ALGORITHM
#------------------------------------------------------------------------------------------------------------------------------

class Day18:
    def __init__(self):
        self.gcl_map_of_coordinates : Map_of_coordinates = Map_of_coordinates()

        # self.gcl_map_of_symbols : Map_of_symbols = Map_of_symbols()

        self.gcl_labirinth : Labirinth = Labirinth()

        self.cs_void = '.'
        self.cs_wall = '#'


    def load_coordinates(self, is_filename : str ) -> bool:
        """
        
        """
        b_fail = False
        b_fail |= self.gcl_map_of_coordinates.load_from_file(is_filename)
        b_fail |= self.gcl_map_of_coordinates.detect_size_from_coordinates()
        if b_fail:
            logging.error(f"ERROR: failed to load map {is_filename}")
        self.gcl_map_of_coordinates.show()

    def generate_map( self, in_step : int ) -> bool:
        """
        I process the first coordinates into a map
        """

        #Only loads thee first symbols
        ltnn_walls = [ tnn for tnn in self.gcl_map_of_coordinates.gltnn_coordinates[:in_step] ]

        self.gcl_labirinth = Labirinth()
        tnn_size = self.gcl_map_of_coordinates.get_size()
        b_fail = self.gcl_labirinth.set_size( tnn_size )
        if b_fail:
            logging.error(f"ERROR: could not crate a labirinth of size {tnn_size}")

        b_fail = self.gcl_labirinth.load_walls_from_list( ltnn_walls )
        if b_fail:
            logging.error(f"ERROR: could not place walls inside labirinth {ltnn_walls}")
        return False #OK

    def find_shortest_path( self ) -> bool:
        """
        Find the shortest path through the labirinth
        """
        #compute coordinates
        tnn_start = (0,0)
        tnn_size = self.gcl_labirinth.gcl_map.get_size()
        tnn_end = (tnn_size[0]-1, tnn_size[1] -1)
        #find path
        b_fail, dtnn_shortest_path = self.gcl_labirinth.find_shortest_path( tnn_start, tnn_end )
        if b_fail:
            logging.error(f"ERROR: could not find shortest path")
            return True #FAIL

        return False #OK

    def find_first_wall_that_closes_the_path( self, in_starting_walls : int ) -> bool:
        """
        The walls fall one at a time
        Find the coordinate of the first wall to close off the path
        """

        #divide sequence in two.
        ltnn_initial_walls = [ tnn for tnn in self.gcl_map_of_coordinates.gltnn_coordinates[:in_starting_walls] ]
        ltnn_later_walls = [ tnn for tnn in self.gcl_map_of_coordinates.gltnn_coordinates[in_starting_walls:] ]

        logging.info(f"Wall Coordinates loaded {len(ltnn_initial_walls)}")
        self.gcl_labirinth = Labirinth()
        tnn_size = self.gcl_map_of_coordinates.get_size()
        b_fail = self.gcl_labirinth.set_size( tnn_size )
        if b_fail:
            logging.error(f"ERROR: could not crate a labirinth of size {tnn_size}")

        b_fail = self.gcl_labirinth.load_walls_from_list( ltnn_initial_walls )
        if b_fail:
            logging.error(f"ERROR: could not place walls inside labirinth {ltnn_initial_walls}")

        #compute coordinates
        tnn_start = (0,0)
        tnn_size = self.gcl_labirinth.gcl_map.get_size()
        tnn_end = (tnn_size[0]-1, tnn_size[1] -1)
        #find path
        b_fail, dtnn_shortest_path = self.gcl_labirinth.find_shortest_path( tnn_start, tnn_end )
        if b_fail:
            logging.error(f"ERROR: could not find shortest path")
            return True #FAIL
        
        #for each new wall
        for n_index, tnn_wall_new in enumerate(ltnn_later_walls):
            logging.info(f"STEP: {n_index} {in_starting_walls+n_index} | Adding wall {tnn_wall_new}")
            #add the wall to the map
            b_fail = self.gcl_labirinth.load_walls_from_list( [tnn_wall_new] )
            if b_fail:
                logging.error(f"ERROR: could not load wall {tnn_wall_new}")
                return True #FAIL
            #if wall lie on the optimal path
            if tnn_wall_new in dtnn_shortest_path:
                #recompute the path
                b_fail, dtnn_shortest_path_new = self.gcl_labirinth.find_shortest_path( tnn_start, tnn_end )
                if b_fail:
                    logging.error(f"ERROR: could not find shortest path")
                    #not an erro, it just mean I'm done
                    break
                #update new shortest path
                dtnn_shortest_path = dtnn_shortest_path_new
            #the optimal path is still valid
            else:
                pass

        #since I have the shortest path, I printo out the last valid path 
        cl_map_of_symbol = self.gcl_labirinth.get_map()
        #mark the optimal path
        for tnn_optimal in dtnn_shortest_path:
            cl_map_of_symbol.set_coordinate(tnn_optimal, "X")
        #mark the position of the last wall
        cl_map_of_symbol.set_coordinate(tnn_wall_new, "*")

        cl_map_of_symbol.show_map()
        logging.info(f"STEP {n_index} Total steps:{in_starting_walls+n_index}")

    
    def show_map( self ) -> bool:
        return self.gcl_labirinth.show_map()



#------------------------------------------------------------------------------------------------------------------------------
#   SOLUTION
#------------------------------------------------------------------------------------------------------------------------------


def solution() -> bool:
    

    cl_memory_space = Day18()

    #cl_memory_space.load_coordinates("day18/day18-example-7x7.txt")
    #cl_memory_space.generate_map( 12 )

    cl_memory_space.load_coordinates("day18/day18-data.txt")

    cl_memory_space.generate_map( 1024 )

    cl_memory_space.show_map()

    cl_memory_space.find_shortest_path()

    


    return False #OK


def solution_part_2() -> bool:

    cl_memory_space = Day18()

    cl_memory_space.load_coordinates("day18/day18-data.txt")

    cl_memory_space.find_first_wall_that_closes_the_path( 1024 )

    return False #OK

#------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(
        filename="day18/day18.log",
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin")

    #solution()

    solution_part_2()
