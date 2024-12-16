"""
Static methods to deal with coordinates
"""

#------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#------------------------------------------------------------------------------------------------------------------------------

import logging

from typing import Set, Dict, List, Tuple

#------------------------------------------------------------------------------------------------------------------------------
#   CLASS
#------------------------------------------------------------------------------------------------------------------------------

class Coordinates:
    @staticmethod
    def sum( itnn_a : Tuple[float, float], itnn_b : Tuple[float, float] ) -> Tuple[float, float]:
        return (itnn_a[0]+itnn_b[0], itnn_a[1]+itnn_b[1])
    
    @staticmethod
    def sub( itnn_a : Tuple[float, float], itnn_b : Tuple[float, float] ) -> Tuple[float, float]:
        return (itnn_a[0]-itnn_b[0], itnn_a[1]-itnn_b[1])

    @staticmethod
    def mul_by_constant( itnn_a : Tuple[float, float], in_mul : float ) -> Tuple[float, float]:
        return (itnn_a[0]*in_mul, itnn_a[1]*in_mul)

    @staticmethod
    def from_box_diagonal_to_four_lines( itnn_start : Tuple[int, int], itnn_end : Tuple[int, int] ) -> Tuple[ bool, List[Tuple[int, int, int, int]] ]:
        """
        
        """
        #extract coordinate names
        n_y_start, n_x_start = itnn_start
        n_y_end, n_x_end = itnn_end

        ltnnnn_lines : List[Tuple[int, int, int, int]]


        return 
