#------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#------------------------------------------------------------------------------------------------------------------------------

import logging

from typing import Set, Dict, List, Tuple

#import copy

#from map_of_symbols import Map_of_symbols

from genetic_octal import Individual

#------------------------------------------------------------------------------------------------------------------------------
#   RULES
#------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------
#   ALGORITHM
#------------------------------------------------------------------------------------------------------------------------------


def reverse_sequence( in_sequence : List[int] ) -> List[int]:
    ln_tmp = [n_value for n_value in in_sequence]
    ln_tmp.reverse()
    return ln_tmp

def number_to_list( in_value : int ) -> List[int]:
    ln_value = [int(s_value) for s_value in str(in_value)]
    return ln_value



#------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(
        filename="day17/day17.log",
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin")

    n = number_to_list(1065674065136766)
    nr = n[::-1]
    logging.info(f"Convert number to list {n} | reverse {nr}")

    #desired sequence
    ln_desired = [0, 3, 3, 0, 5, 5, 3, 1, 7, 4, 5, 7, 2, 1, 4, 2] 


    #decimal
    #38886110969334
    #octal
    #0o1065674065136766
    #octal list
    #[1, 0, 6, 5, 6, 7, 4, 0, 6, 5, 1, 3, 6, 7, 6, 6] 
    #octal reverse list
    #[6, 6, 7, 6, 3, 1, 5, 6, 0, 4, 7, 6, 5, 6, 0, 1] 

    cl_individual = Individual()
    cl_individual.ln_input_octal_reverse = [6, 6, 7, 6, 3, 1, 5, 6, 0, 4, 7, 6, 5, 6, 0, 1] 
    cl_individual.evaluate( ln_desired )
    logging.info(f"{cl_individual}")