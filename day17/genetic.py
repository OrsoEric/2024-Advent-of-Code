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
#   ALGORITHM
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
    ln_input : List[int] = list()
    #integer representation of the input derived from the list
    n_input : int = 0
    #input is processed by the environmnet in an output
    ln_output : List[int] = list()

    def __init__(self):
        self.clear()

    @staticmethod
    def number_to_list( in_value : int ) -> List[int]:
        ln_value = [int(s_value) for s_value in str(in_value)]
        return ln_value

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
        n_a = self.n_input
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
            self.ln_output.insert(0, n_out)
        if ib_debug:
            logging.debug(f"Input: {self.n_input} | Output: {self.ln_output}")
        return False #OK

    def set( self, iln_input : List[int] ) -> bool:
        self.ln_input = iln_input
        self.cl_fitness.clear()
        return False #OK
    
    def evaluate(self, iln_output_desired : List[int], ib_debug = True) -> bool:
        self.n_input = self.list_to_number( self.ln_input )
        b_fail = self.environment()
        if b_fail:
            logging.error(f"ERROR: environment | Input{self.n_input}")
            return True #FAIL
        b_fail = self.cl_fitness.evaluate( self.ln_output, iln_output_desired )
        if b_fail:
            logging.error(f"ERROR: fitness | Output {self.ln_output}")
            return True #FAIL
        
        self.cl_fitness.evaluate_input(self.ln_input)

        if ib_debug:
            logging.debug(f"Evaluate Fitness: {self.cl_fitness}")
        return False #OK
    
    def clear(self) -> bool:
        self.ln_input = list()
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
        self.ln_input = [randint(0, 9) for _ in range(in_length)]
        
        return False #OK  

    def clone(self):
        return copy.deepcopy(self)

    def __repr__(self):
        return f"Input: {self.n_input} {self.ln_input} | Output: {self.ln_output} | Fitness: {self.cl_fitness}"

class Population:
    """
    I have a number
    I have a function that transforms that number into a list
    I want to find a number such that the number is transformed into a specific list
    """

    ln_output_desired : List[int] = list()
    
    def __init__(self):
        #A population is a list of individual
        self.lcl_population : List[Individual] = list()
        #List of individual that were the best of their iteration. It's here to prevent loops from forming
        self.lln_past_survivor_inputs : List[List[int]] = list()
        pass

    def seed_initial_population( self, in_length_min : int, in_length_max : int ) -> bool:

        for n_length in range(in_length_max-in_length_min):
            cl_individual = Individual()
            b_fail = cl_individual.randomize( n_length+ in_length_min)
            if b_fail:
                return True #FAIL
            b_fail = cl_individual.evaluate( self.ln_output_desired )
            if b_fail:
                return True #FAIL
            self.lcl_population.append( cl_individual )

        return False #OK

    def add_individual_to_population(self, icl_individual: Individual) -> bool:
        """
        prevent best individuals to be added twice
        """
        if icl_individual.ln_input not in self.lln_past_survivor_inputs:
            self.lcl_population.append(icl_individual)
        else:
            return True #FAIL

        return False #OK
    
    def add_input_to_population(self, iln_input : List[int] ) -> bool:

        cl_individual = Individual()
        cl_individual.clear()
        cl_individual.ln_input = iln_input
        cl_individual.evaluate(self.ln_output_desired)

        b_fail = self.add_individual_to_population(cl_individual)
        if b_fail:
            logging.error(f"could not add input {iln_input} to population")
            return True #FAIL
        
        #logging.debug(f"Adding: {cl_individual}")
        
        return False

    def mutate( self, ilcl_survivors: List[Individual] ) -> bool:
        
        logging.debug(f"survivors: {len(ilcl_survivors)}")
        for cl_survivor in ilcl_survivors:
            logging.debug(f"Survivor {cl_survivor}")

            #create one new individual by changing each digit +/-1
            #create one new individual by deleting one of each digit
            #create one new individual with a new digit at the start 0 to 9
            #create one new individual with a new digit at the end 0 to 9

            n_max_input_error = max(cl_survivor.cl_fitness.ln_error_input)

            logging.debug("CLONES with one digit changed by 1")  
            #for each digit
            for n_index, n_digit in enumerate(cl_survivor.ln_input):

                #if this digit has no input error, skip
                


                #if this digit has maximum input error
                #if cl_survivor.cl_fitness.ln_error_input[n_index] == n_max_input_error:
                #  #generate one variation for each possible digit
                #  for n_cnt in range(9+1):
                #      cl_clone = cl_survivor.clone()
                #      cl_clone.ln_input[n_index] = n_cnt
                #      cl_clone.evaluate( self.ln_output_desired )
                #      self.add_individual_to_population( cl_clone )
                #just generate variations with 1

                #if this digit is near the leftmost digit
                #if (n_index >= cl_survivor.cl_fitness.n_leftmost_correct_digit-2) and (n_index < cl_survivor.cl_fitness.n_leftmost_correct_digit+1):
                if False:
                    #generate one variation for each possible digit
                    for n_cnt in range(9+1):
                        cl_clone = cl_survivor.clone()
                        cl_clone.ln_input[n_index] = n_cnt
                        cl_clone.evaluate( self.ln_output_desired )
                        self.add_individual_to_population( cl_clone )
                elif cl_survivor.cl_fitness.ln_error_input[n_index] <= 0:
                    pass
                else:
                    #clone the survivor and increase each digit by 1
                    
                    if (n_digit < 9):
                        cl_clone = cl_survivor.clone()
                        cl_clone.ln_input[n_index] += 1
                        cl_clone.evaluate( self.ln_output_desired )
                        self.add_individual_to_population( cl_clone )
                    if (n_digit < 8):
                        cl_clone = cl_survivor.clone()
                        cl_clone.ln_input[n_index] += 2
                        cl_clone.evaluate( self.ln_output_desired )
                        self.add_individual_to_population( cl_clone )

                    #clone the survivor and decrease each digit by 1
                    
                    if (n_digit > 0):
                        cl_clone = cl_survivor.clone()
                        cl_clone.ln_input[n_index] -= 1
                        cl_clone.evaluate( self.ln_output_desired )
                        self.add_individual_to_population( cl_clone )
                        
                    if (n_digit > 1):
                        cl_clone = cl_survivor.clone()
                        cl_clone.ln_input[n_index] -= 2
                        cl_clone.evaluate( self.ln_output_desired )
                        self.add_individual_to_population( cl_clone )

            """
            logging.debug("CLONES with one additional digit as input")
            #for each possible digit
            for n_digit in range(1,9+1):
                #clone the survivor and add the number at the beginning
                cl_clone = cl_survivor.clone()
                cl_clone.ln_input.insert(0, n_digit)
                cl_clone.evaluate( self.ln_output_desired )
                self.add_individual_to_population( cl_clone )
                #clone the survivor and add the number at the end
                cl_clone = cl_survivor.clone()
                cl_clone.ln_input.append(n_digit)
                cl_clone.evaluate( self.ln_output_desired )
                self.add_individual_to_population( cl_clone )       
            
            logging.debug("CLONES with one digit removed")  
            #for each digit
            for n_index, n_digit in enumerate(cl_survivor.ln_input):
                #clone the survivor, and remove that digit
                cl_clone = cl_survivor.clone()
                del cl_clone.ln_input[n_index]
                cl_clone.evaluate( self.ln_output_desired )
                self.add_individual_to_population( cl_clone )
            """


        return False #OK
    
    def sort_population(self) -> bool:

        logging.debug(f"Target: {self.ln_output_desired}")
        # Define the sorting key
        def sort_key(icl_individual : Individual):
            #return (abs(icl_individual.cl_fitness.n_length_mismatch), icl_individual.cl_fitness.n_wrong_digits, icl_individual.cl_fitness.n_square_err)
            #prioritize getting length correct LOW
            #prioritize getting leftmost digits correct HIGH
            #prioritize digits correct LOW
            #prioritize square error LOW
            return (abs(icl_individual.cl_fitness.n_length_mismatch), -icl_individual.cl_fitness.n_leftmost_correct_digit, icl_individual.cl_fitness.n_wrong_digits, icl_individual.cl_fitness.n_square_err)

        self.lcl_population.sort( key=sort_key )
    
        return False


    def search( self, in_max_iterations ) -> bool:
        """
        Find the input that reach zero error on the output
        """
        n_iteration = 0
        logging.info("INITIAL POPULATION")
        self.show_as_info()
        self.evaluate()
        self.sort_population()
        self.show_as_info()

        while n_iteration < in_max_iterations:
            n_iteration += 1
            logging.info(f"ITERATION: {n_iteration} of {in_max_iterations}")
            if n_iteration%50==0:
                print(f"ITERATION: {n_iteration} of {in_max_iterations}")

            #get fittest solution
            cl_fittest = self.lcl_population[0]
            
            if cl_fittest.cl_fitness.n_wrong_digits == 0:
                logging.info(f"SOLUTION! {cl_fittest}")
                break
            #if this is a brand new best survivor
            elif cl_fittest.ln_input not in self.lln_past_survivor_inputs:
                self.lln_past_survivor_inputs.append( cl_fittest.ln_input )
            else:
                logging.error(f"ERROR: a best survivor was created twice! {cl_fittest.ln_input}")
                return True #FAIL
            
            
            logging.info(f"Best individual: {cl_fittest}")

            #dump the partial solutions
            self.lcl_population = list()
            #mutate a subset of the solution
            b_fail = self.mutate( [cl_fittest] )
            if b_fail:
                return True #FAIL
            #sort the population
            self.sort_population()

            self.show()

        return False #OK

    def test_combination(self, in_digits: int, in_start_index : int ):

        # Generate all combinations of three digits from 0 to 9
        ltnnn_combinations = list(product(range(10), repeat=in_digits))

        #get fittest solution
        cl_fittest = self.lcl_population[0]
        logging.info(f"Combinations from digit {in_start_index} of individual {cl_fittest}")
        #dump the partial solutions
        self.lcl_population = list()
        # Generate combinations
        for tnnn_comb in ltnnn_combinations:
            cl_clone = cl_fittest.clone()
            #all combinations
            for n_index_combo, n_combo in enumerate( tnnn_comb ):
                cl_clone.ln_input[in_start_index+n_index_combo] = n_combo

            cl_clone.evaluate( self.ln_output_desired )
            self.add_individual_to_population( cl_clone )

        self.sort_population()
        return False #OK

    def evaluate( self ) -> bool:
        for cl_individual in self.lcl_population:
            b_fail = cl_individual.evaluate( self.ln_output_desired )
            if b_fail:
                return True #FAIL
        return False #OK

    def show(self):
        logging.debug(f"Desired solution: {self.ln_output_desired}")
        for n_index, cl_individual in enumerate(self.lcl_population):
            #cl_individual.evaluate(self.ln_output_desired)
            logging.debug(f"Individual {n_index:3} | {cl_individual}")
            
        return False #OK
    
    def show_as_info(self):
        logging.info(f"Desired solution: {self.ln_output_desired}")
        for n_index, cl_individual in enumerate(self.lcl_population):
            #cl_individual.evaluate(self.ln_output_desired)
            logging.info(f"Individual {n_index:3} | {cl_individual}")
            
        return False #OK
    


    




