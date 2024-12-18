#------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#------------------------------------------------------------------------------------------------------------------------------

import logging

from typing import Set, Dict, List, Tuple

#import copy

#from map_of_symbols import Map_of_symbols

from genetic import Individual
from genetic import Population

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

#------------------------------------------------------------------------------------------------------------------------------
#   SOLUTION
#------------------------------------------------------------------------------------------------------------------------------

def solution() -> bool:

    ln_solution = [2,4,1,2,7,5,4,7,1,3,5,5,0,3,3,0]
    ln_len_solution = len(ln_solution)
    logging.info(f"Expected Sequence {ln_solution}")
    ln_solution_reverse = reverse_sequence(ln_solution)
    logging.info(f"Reversed {ln_solution_reverse}")
    
    #cl_individual = Individual()
    #cl_individual.set( [2,4,1,2,7,5,4,7,1,3,5,5,0,3,3,0] )
    #cl_individual.set( [3,5,2,0,0,3,5,0] )
    #cl_individual.evaluate( ln_solution_reverse )
    #logging.debug(f"{cl_individual}")

    cl_population = Population()
    cl_population.ln_output_desired = ln_solution_reverse
    #cl_population.seed_initial_population(ln_len_solution-2, ln_len_solution+2)
    #manually add inputs that look promising
    #cl_population.add_input_to_population( [3, 5, 5, 7, 0, 6, 4, 0, 5, 0, 4, 0, 7, 4] )
    #cl_population.add_input_to_population( [3, 5, 5, 8, 1, 6, 4, 1, 5, 1, 6, 1, 6, 7] )
    #cl_population.add_input_to_population( [3, 5, 5, 8, 1, 5, 6, 2, 6, 3, 2, 8, 4, 7] )
    #cl_population.add_input_to_population( [3, 5, 5, 8, 0, 6, 8, 1, 6, 4, 9, 1, 2, 4] )
    #4 digit solution
    #cl_population.add_input_to_population( [3, 5, 5, 8, 0, 0, 5, 9, 0, 7, 7, 9, 0, 5] )
    #3 digit solution [0, 3, 1, 0, 5, 5, 3, 1, 7, 4, 5, 1, 2, 1, 1, 2]
    #cl_population.add_input_to_population( [3, 5, 5, 8, 0, 0, 5, 9, 8, 8, 8, 9, 7, 7] )
    #cl_population.add_input_to_population( [3, 5, 5, 8, 0, 0, 5, 9, 8, 9, 2, 1, 1, 9]  )
    #1 digit solution
    #cl_population.add_input_to_population( [3, 5, 5, 8, 0, 0, 5, 9, 8, 9, 3, 2, 3, 6] )
    #either i switch to octal or I prioritize left digits
    #7 left digits correct
    #cl_population.add_input_to_population( [3, 8, 8, 8, 6, 1, 4, 3, 7, 1, 3, 4, 5, 4] )
    #cl_population.add_input_to_population( [3, 8, 8, 8, 6, 1, 4, 6, 8, 6, 2, 2, 3, 4] )
    #8 left digits correct
    #cl_population.add_input_to_population( [3, 8, 8, 8, 6, 1, 0, 9, 8, 3, 6, 7, 2, 7] )
    #cl_population.add_input_to_population( [3, 8, 8, 8, 6, 1, 0, 9, 7, 8, 7, 6, 3, 6] )
    #10 lefft correct
    #cl_population.add_input_to_population( [3, 8, 8, 8, 6, 1, 1, 1, 1, 8, 7, 6, 3, 6] )
    #11 left correct
    #cl_population.add_input_to_population( [3, 8, 8, 8, 6, 1, 1, 0, 9, 6, 7, 6, 3, 6] )
    #13 left correct
    #cl_population.add_input_to_population( [3, 8, 8, 8, 6, 1, 1, 0, 9, 6, 9, 3, 3, 6]  )
    #14 left correct
    cl_population.add_input_to_population( [3, 8, 8, 8, 6, 1, 1, 0, 9, 6, 9, 3, 3, 0] )
    #add one digit
    #NO, I need another digit after, I just need one bit
    #cl_population.add_input_to_population( [0, 3, 8, 8, 8, 6, 1, 1, 0, 9, 6, 9, 3, 3, 0] )
    #add one bit
    #cl_population.add_input_to_population( [7, 7, 7, 7, 2, 2, 2, 1, 9, 3, 8, 6, 6, 0]  )
    
    cl_population.show()
    #cl_population.search( 1000 )
    cl_population.test_combination( 5, 9 )
    cl_population.show_as_info()

    return False #OK

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

    solution()

    #cl_genetic = Genetic()
    #ln_solution = cl_genetic.environment( 35200350 )
    #logging.info(ln_solution)
