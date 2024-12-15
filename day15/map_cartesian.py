import logging
from typing import Dict, List, Tuple

from map_of_symbols import Map_of_symbols


class Map_cartesian(Map_of_symbols):
    """
    A class to represent a map with cartesian coordinate capabilities,
    extending the functionality of Map_of_symbols.

    Attributes:
        origin (Tuple[int, int]): The origin point in cartesian coordinates.
    """

    cs_cartesian = "NESW"

    def __init__(self):
        """
        Initializes the Map_cartesian object.

        Args:
            glln_map (List[List[str]]): 2D list representing the map of symbols.
            origin (Tuple[int, int], optional): The origin point for cartesian coordinates. Defaults to (0, 0).
        """

        super().__init__()

    #get a coordinate in a given direction from the given position
    def get_coordinate_cartesian(self, itnn_origin : Tuple[int, int], is_cardinal : str, in_distance : int = 1 ) -> Tuple[bool,Tuple[int, int]]:

        if self.is_coordinate_invalid(itnn_origin):
            logging.error(f"starting position is OOB: {itnn_origin}")
            return True, (-1,-1) #FAIL
        #compute the coordinate moving one from the 
        (n_y, n_x) = itnn_origin
        if is_cardinal == self.cs_cartesian[0]:
            tnn_cartesian = (n_y-in_distance, n_x) 
        elif is_cardinal == self.cs_cartesian[2]:
            tnn_cartesian = (n_y+in_distance, n_x)
        elif is_cardinal == self.cs_cartesian[1]:
            tnn_cartesian = (n_y, n_x+in_distance)
        elif is_cardinal == self.cs_cartesian[3]:
            tnn_cartesian = (n_y, n_x-in_distance)
        else:
            logging.error(f"invalid cardinal direction: {is_cardinal}")
            return True, (-1,-1) #FAIL
        
        if self.is_coordinate_invalid(tnn_cartesian):
            logging.error(f"Moving toward cardinal direction {is_cardinal} by {in_distance} is OOB: {tnn_cartesian}")
            return True, (-1,-1) #FAIL

        return False, tnn_cartesian #OK
    
