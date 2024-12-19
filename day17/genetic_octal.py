#------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#------------------------------------------------------------------------------------------------------------------------------

import logging

from typing import Set, Dict, List, Tuple

import copy

from random import randint

from itertools import product

#------------------------------------------------------------------------------------------------------------------------------
#   RULES
#------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------
#   fitness
#------------------------------------------------------------------------------------------------------------------------------
#   Evaluate the fitnness of a solution

class Individual:
    """
    An individual carries genes
    """
    #input 
    ln_input_octal_reverse : List[int] = list()
    #integer representation of the input derived from the list
    n_input : int = 0
    #input is processed by the environmnet in an output
    ln_output : List[int] = list()

    def __init__(self):
        self.clear()

    def translate_octal_reverse_to_decimal( self, iln_octal_reverse : List[int] ) -> Tuple[bool, int]:
        """
        For reasons, the algorithm should manipulate a reversed octal list of numbers instead of a decimal list of numbers

        4 5 6 7                         |   octal Reverse
        7 6 5 4                         |   octal
        7*8^3 +6*8^2 +5*8^1 4*8^0       |   octal->decimal
        4012                            |   decimal

        """
        n_decimal = 0
        for n_index, n_octal_digit in enumerate(iln_octal_reverse):
            if (n_octal_digit < 0) or (n_octal_digit > 7):
                return True, -1 #FAIL
            n_decimal += n_octal_digit * (8**n_index)

        return False, n_decimal

    @staticmethod
    def list_to_number( iln_value : int ) -> int:
        ln_value = int(''.join(map(str, iln_value)))
        return ln_value

    #Fitness metrics
    class Fitness:
        #mismatch in the length of the solution vs expected solution
        n_length_mismatch : int = 0
        ln_error : List[int] = list()
        n_square_err = -1
        n_wrong_digits = -1
        ln_error_input : List[int] = list()
        n_leftmost_correct_digit : int = -1

        def __init__(self):
            self.clear()

        def evaluate(self, iln_output : List[int], iln_output_desired : List[int], ib_debug = True) -> bool:

            n_length_desired = len(iln_output_desired)
            n_length = len(iln_output)

            self.n_length_mismatch = n_length -n_length_desired

            n_length_min = min(n_length_desired,n_length ) 

            self.ln_error = [abs(iln_output_desired[n_index] - iln_output[n_index]) for n_index in range(n_length_min)]

            b_zero_chain = True
            self.n_leftmost_correct_digit = -1
            self.n_square_err = 0
            for n_index, n_digit in enumerate(self.ln_error):
                self.n_square_err += n_digit *n_digit

                if n_digit == 0 and b_zero_chain == True:
                    pass
                elif n_digit != 0 and b_zero_chain == True:
                    b_zero_chain = False
                    self.n_leftmost_correct_digit = n_index -1

            self.n_wrong_digits = 0
            for n_index in range(n_length_min):
                if iln_output[n_index] != iln_output_desired[n_index]:
                    self.n_wrong_digits +=1

            if ib_debug:
                logging.debug(f"Fitness.evaluate: {self}")

            return False #OK

        def evaluate_input( self, iln_input ):
            #allocate input sized error vector
            n_len_input = len(iln_input)
            n_len_output = len(self.ln_error)
            self.ln_error_input = [0 for _ in range(n_len_input)]

            #for each output
            for n_index_output, n_error in enumerate(self.ln_error):
                n_index_input = round(n_index_output *n_len_input /n_len_output)
                #accumulate error there
                self.ln_error_input[n_index_input] += n_error
                #accumulate the error on neighbour
                if n_index_input > 0:
                    self.ln_error_input[n_index_input-1] += n_error
                if n_index_input < n_len_input -1:
                    self.ln_error_input[n_index_input+1] += n_error

            return False #OK

        def clear(self):
            self.n_length_mismatch
            self.ln_error = list()
            self.ln_error_input = list()
            self.n_square_err = -1
            self.n_wrong_digits = -1
            self.n_leftmost_correct_digit = -1

        def __repr__(self):
            return f"FITNESS | Length Error: {self.n_length_mismatch} | Square Error {self.n_square_err} | Wrong digits: {self.n_wrong_digits} | Left Correct: {self.n_leftmost_correct_digit} | Digit Error {self.ln_error} | input Error {self.ln_error_input}"

    cl_fitness = Fitness()

    #------------------------------------------------------------------------------------------------------------------------------
    #   environment
    #------------------------------------------------------------------------------------------------------------------------------
    #   The environent processes an input and returns the output
    #   It's the function that the input must survive to
    #   I insert in the head so that the digits are correlated directly
    #   this function has digits affecting the digit in the near position

    def environment( self, ib_debug = False ) -> bool:
        #translate the value of register A to decimal
        b_fail, n_a = self.translate_octal_reverse_to_decimal( self.ln_input_octal_reverse )
        n_b = 0
        n_c = 0
        self.ln_output = list()
        while n_a > 0:
            n_b = n_a % 8
            n_b = n_b ^ 2
            n_c = int(n_a / 2**n_b)
            n_b = n_b ^ n_c
            n_b = n_b ^ 3
            n_a = int(n_a / 8)
            n_out = n_b % 8
            #self.ln_output.insert(0, n_out)
            #I no longer want the ouput reversed, I'm reversing the input
            self.ln_output.append(n_out)

        if ib_debug:
            logging.debug(f"Input: {self.n_input} | Output: {self.ln_output}")

        return False #OK

    def set( self, iln_input : List[int] ) -> bool:
        self.ln_input_octal_reverse = iln_input
        self.cl_fitness.clear()
        return False #OK
    
    def evaluate(self, iln_output_desired : List[int], ib_debug = True) -> bool:

        b_fail, self.n_input = self.translate_octal_reverse_to_decimal( self.ln_input_octal_reverse )
        if b_fail:
            return True #FAIL
        
        b_fail = self.environment()
        if b_fail:
            logging.error(f"ERROR: environment | Input{self.n_input}")
            return True #FAIL
        
        b_fail = self.cl_fitness.evaluate( self.ln_output, iln_output_desired )
        if b_fail:
            logging.error(f"ERROR: fitness | Output {self.ln_output}")
            return True #FAIL
        
        self.cl_fitness.evaluate_input(self.ln_input_octal_reverse)

        if ib_debug:
            logging.debug(f"Evaluate Fitness: {self.cl_fitness}")
        return False #OK
    
    def clear(self) -> bool:
        self.ln_input_octal_reverse = list()
        self.n_input = 0
        self.ln_output = list()
        self.cl_fitness = self.Fitness()
        return False #Ok

    def randomize( self, in_length : int ) -> bool:
        """
        Randomize this individual to length
        """
        #without this, the fitness gets reused ??? what?
        self.clear()
        self.ln_input_octal_reverse = [randint(0, 9) for _ in range(in_length)]
        
        return False #OK  

    def clone(self):
        return copy.deepcopy(self)

    def __repr__(self):
        return f"Input: {self.n_input} {self.ln_input_octal_reverse} | Output: {self.ln_output} | Fitness: {self.cl_fitness}"
    
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
        self.gdln_exclude : Set[List[Individual]] = set()

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

            self.glcl_population.append( cl_clone )
            #this check against a forbidden list
            #self.add_individual_to_population( cl_clone )

        logging.info(f"Generated {len(self.glcl_population)} individual")

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

    def add_individual_to_population(self, icl_individual: Individual) -> bool:
        """
        prevent best individuals to be added twice
        """
        if icl_individual.ln_input not in self.gdln_exclude:
            self.glcl_population.append(icl_individual)
        else:
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

        b_continue = True
        n_index_start = 0
        n_num_octal_digits = 4

        while b_continue:
            logging.info(f"Scanning index {n_index_start} to {n_index_start +n_num_octal_digits}")
            logging.info(f"SURVIVOR: {cl_individual} | Leftmost: {cl_individual.cl_fitness.n_leftmost_correct_digit}")

            #exclude current individual from being selected again
            self.gdln_exclude.add(cl_individual.ln_input_octal_reverse)

            #
            b_fail = self.generate_solutions( cl_individual, n_index_start, n_num_octal_digits )
            if b_fail:
                return True #OK   

            b_fail = self.sort_population()
            if b_fail:
                return True #OK   

            #pick the survivor before the genocide
            cl_individual = self.glcl_population[0]

            #move the search right
            n_index_start += 1
            if n_index_start >= n_len_input-n_num_octal_digits:
                b_continue = False



            #self.show()



        return False #OK
    

    def show_as_info(self):
        logging.info(f"Desired solution: {self.gln_output_desired}")
        for n_index, cl_individual in enumerate(self.glcl_population):
            #cl_individual.evaluate(self.ln_output_desired)
            logging.info(f"Individual {n_index:3} | {cl_individual}")
            
        return False #OK
        