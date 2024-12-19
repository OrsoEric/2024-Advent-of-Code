import logging
from typing import Dict, List, Tuple

class Map_of_coordinates:
    """
    Holds coordinates as a list of touples YX
    HOLDS size of the map
    """

    def __init__(self):
        """
        """
        self.gn_height: int = 0
        self.gn_width: int = 0
        self.gltnn_coordinates : List[Tuple[int,int]] = list()
        #index for the iterator
        self.gn_cursor = -1

    def load_from_file(self, is_filename: str) -> bool:
        """
        Loads a list of coordinates from file

        Parameters:
            is_filename (str): The filename of the map to be loaded.

        Returns:
            bool: False if the map is loaded successfully, True otherwise.
        """
        try:
            with open(is_filename, 'r') as cl_file:
                ls_lines = cl_file.readlines()
                for s_line in ls_lines:
                    #process line
                    s_line_lhs, s_line_rhs = s_line.split(',')
                    #extract coordinate
                    n_x = int(s_line_lhs)
                    n_y = int(s_line_rhs)
                    tnn_coordinate = (n_y, n_x)
                    #insert coordinate
                    self.gltnn_coordinates.append( tnn_coordinate ) 
        except Exception as e:
            logging.error(f"Failed to load map: {e}")
            return True  # FAIL
        return False  # OK
    
    def detect_size_from_coordinates(self):
        """
        infer the size of the map from the content
        """
        self.gn_height = -1
        self.gn_width = -1
        for tnn_coordinate in self.gltnn_coordinates:
            n_y, n_x = tnn_coordinate
            #the +1 is because 6 is addressable, 6+1 is the boundary
            if n_x+1 > self.gn_width:
                self.gn_width = n_x+1
            if n_y+1 > self.gn_height:
                self.gn_height = n_y+1
        return False #OK
    
    def get_size(self) -> Tuple[int,int]:
        return (self.gn_height, self.gn_width)

    def show(self):
        logging.debug(f"Number of coordinates: {len(self.gltnn_coordinates)}")
        logging.debug(f"Height: {self.gn_height} | Width: {self.gn_width}")
        for n_index, tnn_coordinate in enumerate(self.gltnn_coordinates):
            logging.debug(f"Index: {n_index:4} | Y: {tnn_coordinate[0]:4} | X: {tnn_coordinate[1]:4}")

    def __repr__(self):
        return f"Number of coordinates: {len(self.gltnn_coordinates)}"
    
    def __iter__(self):
        """
        Initializes the iterator for scanning the coordinates
        """
        self.gn_cursor = 0
        return self

    def __next__(self):
        """
        Returns the next coordinate in the map during iteration.

        Raises:
            StopIteration: If the iteration reaches the end of the map.

        Returns:
            Tuple[int, int]: The current coordinate being traversed.
        """

        tnn_coordinate = self.gltnn_coordinates[self.gn_cursor]
        self.gn_cursor += 1
        if self.gn_cursor >= len(self.gltnn_coordinates):
            raise StopIteration

        return tnn_coordinate
        
