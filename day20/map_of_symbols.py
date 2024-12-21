import logging
from typing import Dict, List, Tuple

class Map_of_symbols:
    """
    A class to represent a rectangular map of symbols loaded from a file or list of strings.

    Attributes:
        gn_height (int): Height of the map (number of rows).
        gn_width (int): Width of the map (number of columns).
        glln_map (List[List[str]]): 2D list representing the map of symbols.
        gtnn_cursor (Tuple[int, int]): Iterator cursor for traversing the map.
    """

    def __init__(self):
        """
        Initializes a new Map_of_symbols instance with default values.
        """
        self.gn_height: int = 0
        self.gn_width: int = 0
        self.glln_map: List[List[str]] = list()
        self.gtnn_cursor: Tuple[int, int] = (0, 0)  # Iterator cursor
        self.gn_show_spacing : int = 2

    def __iter__(self):
        """
        Initializes the iterator for traversing the map.

        Returns:
            Map_of_symbols: The iterator instance.
        """
        self.gtnn_cursor = (0, 0)
        return self

    def __next__(self):
        """
        Returns the next coordinate in the map during iteration.

        Raises:
            StopIteration: If the iteration reaches the end of the map.

        Returns:
            Tuple[int, int]: The current coordinate being traversed.
        """
        if self.gtnn_cursor[1] >= self.gn_width:  # Move to next row
            self.gtnn_cursor = (self.gtnn_cursor[0] + 1, 0)
        if self.gtnn_cursor[0] >= self.gn_height:  # End of map
            raise StopIteration

        tnn_current = self.gtnn_cursor
        self.gtnn_cursor = (self.gtnn_cursor[0], self.gtnn_cursor[1] + 1)
        return tnn_current

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
                b_fail = self.load_map_from_list(ls_lines)
                if b_fail:
                    logging.error("ERROR: failed to load map from list")
                    return True  # ERROR
        except Exception as e:
            logging.error(f"Failed to load map: {e}")
            return True  # FAIL
        return False  # OK

    def load_map_from_list(self, ils_lines: List[str]) -> bool:
        """
        Loads a map from a list of lines containing symbols.

        Parameters:
            ils_lines (List[str]): List of strings representing the map.

        Returns:
            bool: False if the map is loaded successfully, True otherwise.
        """
        self.gn_height = len(ils_lines)
        self.gn_width = len(ils_lines[0].strip()) if ils_lines else 0
        logging.debug(f"Size H: {self.gn_height} W: {self.gn_width}")

        self.glln_map = [[-1 for _ in range(self.gn_width)] for _ in range(self.gn_height)]

        for n_y, s_line in enumerate(ils_lines):
            for n_x, s_char in enumerate(s_line.strip()):
                b_fail = self.set_coordinate((n_y, n_x), s_char)
                if b_fail:
                    logging.error(f"ERROR: failed to set symbol at C:{(n_y, n_x)} Z:{s_char}")
                    return True  # FAIL
        logging.info(f"Loaded map size H: {self.gn_height} W: {self.gn_width}")
        return False  # OK

    def set_show_spacing( self, in_spacing : int ) -> bool:
        self.gn_show_spacing = in_spacing
        return False #OK

    def get_map_string(self, illtnn_symbol: List[List[Tuple[int, int]]]) -> Tuple[bool, List[str]]:
        """
        Generates a string representation of the map.

        Parameters:
            illtnn_symbol (List[List[Tuple[int, int]]], optional): A list of coordinates with symbols.

        Returns:
            Tuple[bool, List[str]]: A tuple containing a boolean indicating failure, 
                                    and a list of strings representing the map.
        """
        s_map = [f"Width: {self.gn_width} | Height: {self.gn_height}"]
        #format specifier
        s_spacing = f"{self.gn_show_spacing }"
        format_spec = f"{{:>{s_spacing}}}"

        #add COL indexes
        s_line = ""
        s_line += format_spec.format(' ')
        for n_x in range(self.gn_width):
            s_line += format_spec.format(n_x)
        s_map.append(s_line)
        #scan rows
        for n_y in range(self.gn_height):
            s_line = ""
            #add ROW index
            s_line += format_spec.format(n_y)
            #scan cols
            for n_x in range(self.gn_width):
                tnn_coordinate = (n_y, n_x)
                b_fail, s_symbol = self.get_coordinate(tnn_coordinate)
                if b_fail:
                    logging.error(f"ERROR: Failed to get symbol at coordinate {tnn_coordinate}")
                    return True, []
                s_line += format_spec.format(s_symbol)

            s_map.append(s_line)
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
            logging.debug("\n" + "\n".join(s_map))
        else:
            logging.info("\n" + "\n".join(s_map))
        return False  # OK

    def is_coordinate_invalid(self, itnn_coordinate: Tuple[int, int]) -> bool:
        """
        Checks if a given coordinate is invalid.

        Parameters:
            itnn_coordinate (Tuple[int, int]): The coordinate to check.

        Returns:
            bool: True if the coordinate is invalid, False otherwise.
        """
        if type(itnn_coordinate) != type(tuple()) and (len(itnn_coordinate)!=2):
            logging.error(f"ERROR: bad type {type(itnn_coordinate)} | {itnn_coordinate}")
        (n_y, n_x) = itnn_coordinate
        return n_x < 0 or n_y < 0 or n_x >= self.gn_width or n_y >= self.gn_height

    def set_coordinate(self, itnn_coordinate: Tuple[int, int], is_symbol: str) -> bool:
        """
        Sets a symbol at a specific coordinate.

        Parameters:
            itnn_coordinate (Tuple[int, int]): The coordinate to set.
            is_symbol (str): The symbol to place at the coordinate.

        Returns:
            bool: False if successful, True otherwise.
        """
        if self.is_coordinate_invalid(itnn_coordinate):
            return True  # FAIL
        (n_y, n_x) = itnn_coordinate
        self.glln_map[n_y][n_x] = is_symbol
        return False  # OK

    def get_coordinate(self, itnn_coordinate: Tuple[int, int]) -> Tuple[bool, str]:
        """
        Gets the symbol at a specific coordinate.

        Parameters:
            itnn_coordinate (Tuple[int, int]): The coordinate to retrieve.

        Returns:
            Tuple[bool, str]: A tuple containing a boolean indicating failure,
                              and the symbol at the coordinate (or a placeholder if failed).
        """
        if self.is_coordinate_invalid(itnn_coordinate):
            return True, ' '  # Placeholder symbol
        (n_y, n_x) = itnn_coordinate
        return False, self.glln_map[n_y][n_x]  # OK

    def get_size(self) -> Tuple[int, int]:
        """
        Returns the dimensions of the map.

        Returns:
            Tuple[int, int]: Height (Y) and Width (X) of the map.
        """
        return self.gn_height, self.gn_width

    def get_four_connect(self, itnn_start: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Given a position
        Returns all four connect position that are within boundaries
        It's ordered in N, E, S, W clockwise fron North
        """

        if self.is_coordinate_invalid( itnn_start ):
            return list()

        ltnn_four_connect: List[Tuple[int, int]] = list()
        (n_y, n_x) = itnn_start
        
        ltnn_delta = [(-1,0), (0,1), (1,0), (0,-1)]

        for tnn_delta in ltnn_delta:
            tnn_test = (n_x+tnn_delta[0], n_y+tnn_delta[1])
            if self.is_coordinate_invalid(tnn_test):
                pass
            else:
                ltnn_four_connect.append(tnn_test)
        return ltnn_four_connect
    
    def get_four_connect_direction(self, itnn_start: Tuple[int, int]) -> List[Tuple[int, int, int]]:
        """
        Given a position
        Returns all four connect position that are within boundaries
        It's ordered in N=0, E=1, S=2, W=3 clockwise fron North
        RETURNS
        X,Y,D
        """

        if self.is_coordinate_invalid( itnn_start ):
            return list()

        ltnn_four_connect: List[Tuple[int, int]] = list()
        (n_y, n_x) = itnn_start
        
        ltnn_delta = [(-1,0), (0,1), (1,0), (0,-1)]

        for n_dir, tnn_delta in enumerate(ltnn_delta):
            tnn_test = (n_y+tnn_delta[0], n_x+tnn_delta[1])
            if self.is_coordinate_invalid(tnn_test):
                pass
            else:
                ltnn_four_connect.append((tnn_test[0], tnn_test[1], n_dir))
        return ltnn_four_connect

    def find_four_connect(self, itnn_start: Tuple[int, int], is_symbol: str, ib_debug=False) -> Tuple[bool, List[Tuple[int, int]]]:
        """
        Finds all four-connected coordinates with the same symbol.

        Parameters:
            itnn_start (Tuple[int, int]): The starting coordinate.
            is_symbol (str): The symbol to match.

        Returns:
            Tuple[bool, List[Tuple[int, int]]]: A tuple containing a boolean indicating failure, 
                                               and a list of four-connected coordinates with the same symbol.
        """
        b_fail, s_symbol_at_start = self.get_coordinate(itnn_start)
        if b_fail:
            logging.error(f"ERROR: Invalid starting coordinate {itnn_start}")
            return True, []

        ltnn_four_connect: List[Tuple[int, int]] = list()
        (n_y, n_x) = itnn_start
        ltnn_test = [(n_y + dy, n_x) for dy in [-1, 1]] + [(n_y, n_x + dx) for dx in [-1, 1]]

        for tnn_test in ltnn_test:
            b_fail, s_symbol = self.get_coordinate(tnn_test)
            if not b_fail and s_symbol == is_symbol:
                ltnn_four_connect.append(tnn_test)
        if ib_debug:
            logging.debug(f"Symbol {s_symbol} Coordinate {itnn_start} | {len(ltnn_four_connect)} Four Connect found | Coordinates {ltnn_four_connect}")
        return False, ltnn_four_connect
    

    def find_symbol(self, is_symbol: str) -> Tuple[bool, List[Tuple[int, int]]]:
        """
        Finds ALL occurrences of a given symbol in the map.

        Parameters:
            is_symbol (str): The symbol to search for.

        Returns:
            Tuple[bool, List[Tuple[int, int]]]: A tuple containing a boolean indicating failure,
                                               and a list of coordinates where the symbol is found.
                                               (True, []) if not found or on failure.
        """
        ltnn_coordinates = list()

        for tnn_coordinate in self:
            b_fail, s_symbol_at_coord = self.get_coordinate(tnn_coordinate)
            if b_fail:
                logging.error(f"ERROR: Failed to get symbol at coordinate {tnn_coordinate}")
                return True, list()  # FAIL
            if s_symbol_at_coord == is_symbol:
                ltnn_coordinates.append(tnn_coordinate)
        return False, ltnn_coordinates  # Success, return list of coordinates
    
    def set_size( self, tnn_size : Tuple[int, int], is_default_value : str ):
        self.gn_height = tnn_size[0]
        self.gn_width = tnn_size[1]
        logging.debug(f"Size H: {self.gn_height} W: {self.gn_width}")
        self.glln_map = [[-1 for _ in range(self.gn_width)] for _ in range(self.gn_height)]

        self.clear_map(is_default_value)
        return False #OK

    def clear_map(self, is_default_value):
        for tnn_coordinate in self:
            b_fail = self.set_coordinate( tnn_coordinate, is_default_value )
            if b_fail:
                logging.error(f"ERROR: failed to set coordinate {tnn_coordinate} to {is_default_value}")
                return True #FAIL
        return False #OK

