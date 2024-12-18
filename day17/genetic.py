#------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#------------------------------------------------------------------------------------------------------------------------------

import logging

from typing import Set, Dict, List, Tuple

import copy

#------------------------------------------------------------------------------------------------------------------------------
#   RULES
#------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------
#   ALGORITHM
#------------------------------------------------------------------------------------------------------------------------------

class Gene:
    #input
    ln_input : List[int] = list()
    #integer representation of the input derived from the list
    n_input : int = 0
    #input is processed by the environmnet in an output
    ln_output : List[int] = list()
    #Fitness metrics
    class Fitness:
        #mismatch in the length of the solution vs expected solution
        n_length_mismatch : int = 0
        pass


    #------------------------------------------------------------------------------------------------------------------------------
    #   fitness
    #------------------------------------------------------------------------------------------------------------------------------
    #   Evaluate the fitnness of a solution

    def fitness( self ) -> Tuple[bool, float]:
        return True, 0 #FAIL
    
    #
    st_fitness : Fitness = Fitness()

    #------------------------------------------------------------------------------------------------------------------------------
    #   environment
    #------------------------------------------------------------------------------------------------------------------------------
    #   The environent processes an input and returns the output
    #   It's the function that the input must survive to
    #   I insert in the head so that the digits are correlated directly
    #   this function has digits affecting the digit in the near position

    def environment( self, in_input ) -> Tuple[bool, List[int]]:
        n_a = in_input
        n_b = 0
        n_c = 0
        ln_out = list()
        while n_a > 0:
            n_b = n_a % 8
            n_b = n_b ^ 2
            n_c = int(n_a / 2**n_b)
            n_b = n_b ^ n_c
            n_b = n_b ^ 3
            n_a = int(n_a / 8)
            n_out = n_b % 8
            ln_out.insert(0, n_out)

        logging.debug(f"Input: {in_input} | Output: {ln_out}")
        return ln_out
    
    def 


class Genetic:
    """
    I have a number
    I have a function that transforms that number into a list
    I want to find a number such that the number is transformed into a specific list
    """

    def __init__(self):
        self.gn_out = [2,4,1,2,7,5,4,7,1,3,5,5,0,3,3,0]


    




