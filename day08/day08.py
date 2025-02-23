#--------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#--------------------------------------------------------------------------------------------------------------------------------

import logging

from itertools import product, combinations

import copy

from typing import Generator, Dict, Tuple, List

#--------------------------------------------------------------------------------------------------------------------------------
#   RULES
#--------------------------------------------------------------------------------------------------------------------------------

"""
There is a map
Within the map there are low case, high case and numbers
For each pair of the same symbol, two special location are generated.
    d = vector distance between pair of same symbols
    two focus # are generated at vector distance d from each of the symbols
    #...A...A...#
    #..A..A..#
    Focus must be within the map
Calculate the focus generated by the total sum of all pairs of antennas of each symbol
If multiple symbols generate a focus in the same place, that count multiple times

NO! multiple focus in the same place count as 1
"""

"""
PART 2
focus are generated at each integer multiple of distance.
antennas count as focus

"""


#--------------------------------------------------------------------------------------------------------------------------------
#   ALGORITHM
#--------------------------------------------------------------------------------------------------------------------------------

"""
PART1
I create a dictionary, where the key is the symbol (case sensitive)
the dictionary is associated with a list of coordinates XY that map all the same symbols
for each unique pair of those symbols, i generate a list of all the focus coordinates
I save that in a dictionary of focus, with one key per symbol
the solution is the total sum of all items in the focus dictionary
"""

class Focus:
    def __init__(self):
        """
        Initialize the Focus class
        """
        self.gn_width = -1
        self.gn_height = -1
        # store symbol as key, and item is a list of coordinates where that symbol appears
        self.gd_symbol = dict()
        #store coordinates, with the symbol associated with that coordinate
        self.gd_coordinate_symbol = dict()
        #for each symbol as key, store the focus as list of coordinates
        self.gd_focus = dict()
        #store coordinates, and the number of unique focus in that coordinate
        self.gd_coordinate_focus = dict()

    def load_map_from_file(self, is_filename: str) -> bool:
        """
        From a file, load a map.
        For each symbol in a coordinate, add that coordinate to the dictionary as a list of coordinates with the symbol as key
        """
        try:
            with open(is_filename, 'r') as file:
                lines = file.readlines()
                self.gn_height = len(lines)
                self.gn_width = max(len(line.strip()) for line in lines)

                for n_y, line in enumerate(lines):
                    for n_x, s_symbol in enumerate(line.strip()):
                        if s_symbol != '.':
                            tnn_coordinate = (n_x, n_y)
                            #fill symbol dictionary
                            if s_symbol not in self.gd_symbol:
                                self.gd_symbol[s_symbol] = []
                            self.gd_symbol[s_symbol].append( tnn_coordinate )
                            #fill coordinate dictionary
                            self.gd_coordinate_symbol[tnn_coordinate] = s_symbol

        except Exception as e:
            print(f"Error loading map: {e}")
            return False
        logging.info(f"Map Size: Width: {self.gn_width} | Height: {self.gn_height}")
        logging.info(f"Number of frequencies (symbols): {len(self.gd_symbol)}")
        logging.info(f"Number of antennas: {len(self.gd_coordinate_symbol)}")
        logging.info(f"Symbols: {self.gd_symbol}")
        logging.info(f"Antennas: {self.gd_coordinate_symbol }")
        
    def show(self):
        logging.info(f"Map Size: Width: {self.gn_width} | Height: {self.gn_height}")
        s_line = "\n"
        for n_y in range(self.gn_height):
            for n_x in range(self.gn_width):
                tnn_coordinate = (n_x, n_y)
                if tnn_coordinate in self.gd_coordinate_symbol:
                    s_line += f"{self.gd_coordinate_symbol[tnn_coordinate]}"
                else:
                    s_line += "."
            s_line += '\n'
        logging.debug(s_line)

    def sum_vector( self, tnn_origin : Tuple[int, int], tnn_vector : Tuple[int, int] ) -> Tuple[int, int]:
        """
        sum two XY coordinates,
        """
        return (tnn_origin[0]+tnn_vector[0], tnn_origin[1]+tnn_vector[1])

    def sub_vector( self, tnn_origin : Tuple[int, int], tnn_vector : Tuple[int, int] ) -> Tuple[int, int]:
        """
        fsub two XY coordinates
        """
        return (tnn_origin[0]-tnn_vector[0], tnn_origin[1]-tnn_vector[1])

    def is_oob( self, tnn_origin : Tuple[int, int] ) -> bool:
        """
        if the coordinate is out of bound, return True
        """
        if (tnn_origin[0] < 0):
            return True #OOB
        if (tnn_origin[1] < 0):
            return True #OOB
        if (tnn_origin[0] >= self.gn_width):
            return True #OOB
        if (tnn_origin[1] >= self.gn_height):
            return True #OOB
        return False

    def process_focus( self, tnn_origin : Tuple[int, int], tnn_vector : Tuple[int, int] ) -> List[Tuple[int, int]]:
        """
        given an origin and a distance, compute all the integer multiples of vector that are not OOB
        focus will occour at each integer multiple including 1, until the focus is OOB
        """
        #coordinate of a focus
        tnn_focus = tnn_origin
        #list of focuses
        ltnn_focus = list()
        #while the focus is within bounds
        while self.is_oob(tnn_focus) == False:
            #add focus to the list of focus
            ltnn_focus.append(tnn_focus)
            #move the focus
            tnn_focus = self.sum_vector( tnn_focus, tnn_vector )
        #return the focuses that are within bounds
        return ltnn_focus

    def compute_focus(self):
        """
        for each pair of symbols
        create two focus in line with the symbols
        at the distance between the symbols
        works for T example UNIQUE FOCUS: 9
        works for example UNIQUE FOCUS: 34
        """
        #for each symbol
        for s_symbol in self.gd_symbol:
            #create an empty list in the focus dictionary associated with the symbol
            self.gd_focus[s_symbol] = list()
            #get the list of coordinates where that symbol appear
            ltnn_coordinates = self.gd_symbol[s_symbol]
            #allocate list of focus
            ltnn_focus = list()
            #for each pair of coordinates
            
            for tst_pair_of_coordinates in combinations( ltnn_coordinates, 2 ):
                logging.debug(f"Pair: {tst_pair_of_coordinates}")
                #compute distance between pair
                tnn_vector_distance_ab = self.sub_vector( tst_pair_of_coordinates[1], tst_pair_of_coordinates[0])
                #focuses that originate from this pair
                ltnn_focus_from_pair = self.process_focus( tst_pair_of_coordinates[1], tnn_vector_distance_ab )
                #add them to the total list of focusesd
                ltnn_focus += ltnn_focus_from_pair
                #do the same on the other end
                tnn_vector_distance_ab = self.sub_vector( tst_pair_of_coordinates[0], tst_pair_of_coordinates[1])
                ltnn_focus_from_pair = self.process_focus( tst_pair_of_coordinates[0], tnn_vector_distance_ab )
                ltnn_focus += ltnn_focus_from_pair

                logging.info(f"Number of focus for symbol {s_symbol}: {len(ltnn_focus)}")

            for tnn_focus in ltnn_focus:
                self.gd_focus[s_symbol].append(tnn_focus)
                #add focus to the coordinate of the focus
                if tnn_focus not in self.gd_coordinate_focus:
                    self.gd_coordinate_focus[tnn_focus] = 1
                else:
                    self.gd_coordinate_focus[tnn_focus] += 1
            logging.info(f"Focus Coordinates: {self.gd_coordinate_focus}")
        print(f"UNIQUE FOCUS: {len(self.gd_coordinate_focus)}")

#--------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#--------------------------------------------------------------------------------------------------------------------------------

#   if interpreter has the intent of executing this file
if __name__ == "__main__":
    logging.basicConfig(
        filename='day08\day_8.log',
        # Specify the log file name
        level=logging.DEBUG,
        # Set the level of debug to show
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin") 

    cl_focus = Focus()
    #cl_focus.load_map_from_file('day08\day_8_example_simple.txt')
    #cl_focus.load_map_from_file('day08\day_8_example.txt')
    cl_focus.load_map_from_file('day08\day_8_map.txt')
    cl_focus.show()
    cl_focus.compute_focus()