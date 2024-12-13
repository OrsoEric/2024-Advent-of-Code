
#------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#------------------------------------------------------------------------------------------------------------------------------

import logging

from typing import Dict, List, Tuple

#------------------------------------------------------------------------------------------------------------------------------
#   CLASS
#------------------------------------------------------------------------------------------------------------------------------

class Map_of_symbols:
    """
    A class to represent a rectangular map of symbols loaded from a file.
    """

    def __init__(self):
        """
        Initializes a new Map_of_symbols instance.
        """
        self.gn_height : int = 0
        self.gn_width : int = 0
        self.glln_map : List[List[str]] = list()
        #iterator cursor
        self.gtnn_cursor : Tuple[int, int] = (0, 0)

    #------------------------------------------------------------------------------------------------------------------------------
    #   ITERATORS
    #------------------------------------------------------------------------------------------------------------------------------

    def __iter__(self):
        """ Initializes the iterator. """
        self.gtnn_cursor = (0, 0)
        return self

    def __next__(self):
        """
        Returns the next coordinate in the map.
        """
        #next row
        if self.gtnn_cursor[1] >= self.gn_width:
            self.gtnn_cursor = (self.gtnn_cursor[0] + 1, 0)
        #scan column
        if self.gtnn_cursor[0] >= self.gn_height:
            raise StopIteration

        tnn_current = self.gtnn_cursor
        self.gtnn_cursor = (self.gtnn_cursor[0], self.gtnn_cursor[1] + 1)
        return tnn_current

    #------------------------------------------------------------------------------------------------------------------------------
    #   FILE PROCESSING
    #------------------------------------------------------------------------------------------------------------------------------

    def load_map_from_file(self, is_filename: str) -> bool:
        """
        Loads a map of symbols from a file.

        Parameters:
        is_filename (str): The filename of the map to be loaded.

        Returns:
        bool: False if the map is loaded successfully, True otherwise.
        """
        try:
            with open(is_filename, 'r') as cl_file:
                ls_lines = cl_file.readlines()
                self.gn_height = len(ls_lines)
                self.gn_width = len(ls_lines[0].strip())
                logging.debug(f"Size H Y {self.gn_height} W X {self.gn_width}")
                # allocate map
                self.glln_map = [[-1 for _ in range(self.gn_width)] for _ in range(self.gn_height)]
                # fill map
                for n_y, s_line in enumerate(ls_lines):
                    for n_x, s_char in enumerate(s_line.strip()):
                        s_plot_type = s_char
                        b_fail = self.set_coordinate((n_y, n_x), s_plot_type)
                        if b_fail:
                            logging.error(f"ERROR: failed to set symbol at C:{(n_y, n_x)} Z:{s_plot_type}")
        except Exception as e:
            logging.error(f"Failed to load map: {e}")
            return True  # fail
        return False  # OK
    
    def get_map_string(self, illtnn_symbol: List[List[Tuple[int, int]]]) -> Tuple[bool, List[str]]:
        """
        Generates a string representation of the map.

        Parameters:
        illtnn_symbol (List[List[Tuple[int, int]]]): A list of coordinates with symbols.

        Returns:
        Tuple[bool, str]: A tuple containing a boolean indicating failure, 
                          and the string representation of the map.
        """
        s_map = f"Width: {self.gn_width} | Height: {self.gn_height}\n"
        for n_y in range(self.gn_height):
            for n_x in range(self.gn_width):
                tnn_coordinate = (n_y, n_x)
                b_fail, s_symbol = self.get_coordinate(tnn_coordinate)
                if b_fail:
                    logging.error(f"ERROR: Failed to get symbol at coordinate {tnn_coordinate}")
                    return True, list()
                s_map += f"{s_symbol:2}"
            if n_y < self.gn_height -1:
                s_map += "\n"
        return False, s_map  # OK
    
    def show_map(self, illtnn_map: List[List[Tuple[int, int]]] = None, ib_debug: bool = False) -> bool:
        """
        Displays the map.

        Parameters:
        illtnn_map (List[List[Tuple[int, int]]], optional): The map to display. Defaults to None.
        ib_debug (bool, optional): Flag for debug mode. Defaults to False.

        Returns:
        bool: False if successful, True otherwise.
        """
        if illtnn_map is None:
            illtnn_map = self.glln_map

        b_fail, s_map = self.get_map_string(illtnn_map)
        if b_fail:
            return True  # FAIL
        if ib_debug:
            logging.debug(s_map)
        else:
            logging.info(s_map)
        return False  # OK
    
    #------------------------------------------------------------------------------------------------------------------------------
    #   COORDINATE AND ACCESS
    #------------------------------------------------------------------------------------------------------------------------------

    def is_coordinate_invalid(self, itnn_coordinate: Tuple[int, int]) -> bool:
        """
        Checks if a given coordinate is valid or invalid.

        Parameters:
        itnn_coordinate (Tuple[int, int]): The coordinate to check.

        Returns:
        bool: True if the coordinate is invalid, False if it is valid.
        """
        (n_y, n_x) = itnn_coordinate
        if n_x < 0 or n_y < 0 or n_x >= self.gn_width or n_y >= self.gn_height:
            return True  # invalid
        return False  # valid

    def set_coordinate(self, itnn_coordinate: Tuple[int, int], is_symbol: str) -> bool:
        """
        Sets a coordinate to a symbol.

        Parameters:
        itnn_coordinate (Tuple[int, int]): The coordinate to set.
        is_symbol (str): The symbol to set at the coordinate.

        Returns:
        bool: False if successful, True otherwise.
        """
        # if OOB
        if self.is_coordinate_invalid(itnn_coordinate):
            return True  # FAIL
        (n_y, n_x) = itnn_coordinate
        self.glln_map[n_y][n_x] = is_symbol
        return False  # ok
    
    def get_coordinate(self, itnn_coordinate: Tuple[int, int]) -> Tuple[bool, str]:
        """
        Gets the symbol at a given coordinate.

        Parameters:
        itnn_coordinate (Tuple[int, int]): The coordinate to get.

        Returns:
        Tuple[bool, str]: A tuple containing a boolean indicating failure, 
                          and the symbol at the coordinate (or a placeholder if failed).
        """
        # if OOB
        if self.is_coordinate_invalid(itnn_coordinate):
            return True, ' '  # return a placeholder symbol
        (n_y, n_x) = itnn_coordinate
        s_symbol = self.glln_map[n_y][n_x]
        return False, s_symbol  # ok, symbol
    
    def get_size(self) -> Tuple[int, int]:
        """
        Returns the size of the map.

        Returns:
        Tuple[int, int]: The width and height of the map.
        """
        return self.gn_width, self.gn_height
    
    #------------------------------------------------------------------------------------------------------------------------------
    #   TOPOLOGICAL OPERATIONS
    #------------------------------------------------------------------------------------------------------------------------------

    def find_four_connect(self, itnn_start : Tuple[int,int], is_symbol ) -> Tuple[ bool, List[Tuple[int,int]] ]:
        """
        given a coordinate
        given a symbol
        find ALL four connect coordinates that are of that symbol
        return them as list of coordinates
        """
        #get the current altitude
        b_fail, s_symbol = self.get_coordinate( itnn_start )
        if b_fail:
            logging.error(f"ERROR: invalid starting coordinate {itnn_start}")
            return True, list()
        
        #return list
        ltnn_four_connect : List[Tuple[int,int]] = list()
        
        #generate FOUR CONNECT test positions, PLUS pattern
        (n_y, n_x) = itnn_start
        ltnn_test = list()
        for n_delta_y in [-1, +1]:
            ltnn_test.append( (n_y+n_delta_y, n_x) )
        for n_delta_x in [-1, +1]:
            ltnn_test.append( (n_y, n_x+n_delta_x) )
        #scan the four connect
        for tnn_test in ltnn_test:
            b_fail, s_symbol = self.get_coordinate( tnn_test )
            #if coordinate is OOB
            if b_fail:
                pass
            elif s_symbol == is_symbol:
                ltnn_four_connect.append(tnn_test)
            else:
                pass

        logging.debug(f"Symbol {s_symbol} Coordinate {itnn_start} | {len(ltnn_four_connect)} Four Connect found | Coordinates {ltnn_four_connect}")

        return False, ltnn_four_connect