#------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#------------------------------------------------------------------------------------------------------------------------------

import logging

from typing import Set, Dict, List, Tuple

import copy

from random import randint

from itertools import product

from individual import Individual

#------------------------------------------------------------------------------------------------------------------------------
#   RULES
#------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------
#   fitness
#------------------------------------------------------------------------------------------------------------------------------
#   Evaluate the fitnness of a solution

    
#------------------------------------------------------------------------------------------------------------------------------
#   left to right brute force
#------------------------------------------------------------------------------------------------------------------------------
#   there should be algorithmic separation
#   I compute the leftmost digit that are correct
#   I roll a number of octal digit in all combinations
#   I sort by error

class Solver_left_to_right():
    def __init__(self):
        self.cn_octal_base = 8
        self.gln_octal_reverse_initial : List[int] = list()
        self.gn_input_decimal = -1
        self.gln_output_desired : List[int] = list()
    
        self.glcl_population : List[Individual] = list()

        #solutions to be excluded for survivor choice
        self.gdln_exclude : List[List[Individual]] = list()

    def load_initial_solution( self,  iln_octal_reverse_initial : List[int], iln_desired_output : List[int] ) -> bool:
        self.gln_octal_reverse_initial = iln_octal_reverse_initial
        self.gln_output_desired = iln_desired_output
        logging.info(f"Input Octal Reverse: {self.gln_octal_reverse_initial}")
        logging.info(f"Output Desired: {self.gln_output_desired}")
        return False #OK

    def generate_solutions(self, icl_individual : Individual, in_index_start : int, in_num_octal_digits : int ) -> bool:
        """
        Starting from an individual
        Roll a number of octal digits. e.g. 3 -> 000 to 777
        clone the individual that number of times changing the octal reverse input
        at a given index with the rolled combos
        """

        #commit genocide of the current population
        self.glcl_population = list()
        #roll the range
        ltnnn_combinations_octal = list(product(range(self.cn_octal_base), repeat=in_num_octal_digits))
        # Generate combinations
        for tnnn_comb in ltnnn_combinations_octal:
            cl_clone = icl_individual.clone()

            #all octal digits in the combination
            for n_index_combo, n_combo in enumerate( tnnn_comb ):
                cl_clone.ln_input_octal_reverse[in_index_start+n_index_combo] = n_combo

            b_fail = cl_clone.evaluate( self.gln_output_desired )
            if b_fail:
                return True #OK        

            #this check against a forbidden list
            self.add_individual_to_population( cl_clone )

        logging.info(f"Generated {len(self.glcl_population)} individual")

        return False #OK

    def generate_solutions_interleaved(self, icl_individual : Individual, in_index_start : int, in_num_octal_digits : int, in_num_blanks : int ) -> bool:
        """
        Starting from an individual
        Roll a number of octal digits. e.g. 3 -> 000 to 777
        clone the individual that number of times changing the octal reverse input
        at a given index with the rolled combos

        INERLEAVING
        |..|.||
        two blanks
        one blank
        zero blanks

        """
        n_blank_index = in_num_blanks

        n_total_blanks = 0
        for n_cnt in range(in_num_blanks):
            n_total_blanks += n_cnt+1
        logging.info(f"Scanning from {in_index_start} to {in_index_start+in_num_octal_digits+n_total_blanks}")
        #commit genocide of the current population
        self.glcl_population = list()
        #roll the range
        ltnnn_combinations_octal = list(product(range(self.cn_octal_base), repeat=in_num_octal_digits))
        #generate indees
        ln_index = list()
        for n_index in range(in_num_octal_digits):
            ln_index.append(in_index_start +n_index+n_blank_index)
            if n_blank_index <= in_num_blanks:
                n_blank_index += 1

        # Generate combinations
        for tnnn_comb in ltnnn_combinations_octal:
            cl_clone = icl_individual.clone()
            ln_index_scanned = list()
            #all octal digits in the combination
            for n_index_combo, n_combo in enumerate( tnnn_comb ):
                n_index = ln_index[n_index_combo]
                #logging.info(f"Combo Index: {n_index_combo} Index: {n_index}")
                ln_index_scanned.append(n_index)
                if n_index >= len(cl_clone.ln_input_octal_reverse):
                    logging.error(f"OOB: {n_index} of {len(cl_clone.ln_input_octal_reverse)}")
                    return True #FAIL
                cl_clone.ln_input_octal_reverse[n_index] = n_combo

            b_fail = cl_clone.evaluate( self.gln_output_desired )
            if b_fail:
                return True #OK        

            self.add_individual_to_population( cl_clone )

        logging.info(f"Generated {len(self.glcl_population)} individual. Scanned {ln_index_scanned} digits")

        return False #OK


    def sort_population(self) -> bool:

        logging.debug(f"Target: {self.gln_output_desired}")
        # Define the sorting key
        def sort_key(icl_individual : Individual):
            #return (abs(icl_individual.cl_fitness.n_length_mismatch), icl_individual.cl_fitness.n_wrong_digits, icl_individual.cl_fitness.n_square_err)
            #prioritize getting length correct LOW
            #prioritize getting leftmost digits correct HIGH
            #prioritize digits correct LOW
            #prioritize square error LOW
            return (abs(icl_individual.cl_fitness.n_length_mismatch), -icl_individual.cl_fitness.n_leftmost_correct_digit, icl_individual.cl_fitness.n_wrong_digits, icl_individual.cl_fitness.n_square_err)

        self.glcl_population.sort( key=sort_key )
    
        return False

    def add_forbidden(self, icl_individual: Individual) -> bool:
        self.gdln_exclude.append(icl_individual.ln_input_octal_reverse)
        logging.info(f"Tot: {len(self.gdln_exclude)} Forbidden: {icl_individual.ln_input_octal_reverse}")
        return False #OK

    def add_individual_to_population(self, icl_individual: Individual) -> bool:
        """
        prevent best individuals to be added twice
        """
        if icl_individual.ln_input_octal_reverse not in self.gdln_exclude:
            self.glcl_population.append(icl_individual)
        else:
            #logging.error(f"excluded: {icl_individual.ln_input_octal_reverse}")
            return True #FAIL

        return False #OK

    def solve_left_to_right_brute_force( self ) -> bool:

        cl_individual = Individual()
        cl_individual.ln_input_octal_reverse = self.gln_octal_reverse_initial
        b_fail = cl_individual.evaluate( self.gln_output_desired )
        if b_fail:
            return True #FAIL

        self.gn_input_decimal = cl_individual.n_input
        n_len_input = len(cl_individual.ln_input_octal_reverse)
        logging.info(f"Input Decimal: {self.gn_input_decimal} | Num digits: {n_len_input}")

        logging.debug(f"{cl_individual}")

        self.add_forbidden( cl_individual )

        b_continue = True
        n_index_start = 7
        n_num_octal_digits = 7
        n_num_blanks = 0


        while b_continue:
            logging.info(f"Scanning index {n_index_start} to {n_index_start +n_num_octal_digits}")
            logging.info(f"SURVIVOR: {cl_individual} | Leftmost: {cl_individual.cl_fitness.n_leftmost_correct_digit}")

            #exclude current individual from being selected again
            self.add_forbidden(cl_individual)

            #
            #b_fail = self.generate_solutions( cl_individual, n_index_start, n_num_octal_digits )
            b_fail = self.generate_solutions_interleaved( cl_individual, n_index_start, n_num_octal_digits, n_num_blanks )
            if b_fail:
                return True #OK   

            b_fail = self.sort_population()
            if b_fail:
                return True #OK   

            #pick the survivor before the genocide
            cl_individual = self.glcl_population[0]
            logging.info(f"Leftmost: {cl_individual.cl_fitness.n_leftmost_correct_digit}")
            
            #move the search right
            n_index_start += 1
            if n_index_start > n_len_input-n_num_octal_digits:
                b_continue = False

            #self.show_as_info()

        return False #OK
    

    def show_as_info(self):
        logging.info(f"Desired solution: {self.gln_output_desired}")
        for n_index, cl_individual in enumerate(self.glcl_population):
            #cl_individual.evaluate(self.ln_output_desired)
            logging.info(f"Individual {n_index:3} | {cl_individual}")
            
        return False #OK
        