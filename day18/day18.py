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

    def generate_map( self, in_step : int ):
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
        return False #FAIL

    def show_map( self ) -> bool:
        return self.gcl_labirinth.show_map()





#------------------------------------------------------------------------------------------------------------------------------
#   SOLUTION
#------------------------------------------------------------------------------------------------------------------------------


def solution() -> bool:
    cl_memory_space = Day18()
    cl_memory_space.load_coordinates("day18/day18-example-7x7.txt")
    cl_memory_space.generate_map( 12 )
    cl_memory_space.show_map()

    return False #OK
    return True #FAIL

#------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(
        filename="day18/day18.log",
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin")

    solution()
