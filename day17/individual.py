
import logging

from typing import List, Tuple

import copy

from random import randint

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

        def evaluate(self, iln_output : List[int], iln_output_desired : List[int], ib_debug = False) -> bool:

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
        self.n_input = n_a
        n_b = 0
        n_c = 0
        self.ln_output = list()
        b_continue = True
        while b_continue:
            n_b = n_a % 8
            n_b = n_b ^ 2
            n_c = int(n_a / 2**n_b)
            n_b = n_b ^ n_c
            n_b = n_b ^ 3
            n_a = int(n_a / 8)
            n_out = n_b % 8

            if n_a <= 0:
                b_continue = False
            #self.ln_output.insert(0, n_out)
            #I no longer want the ouput reversed, I'm reversing the input
            self.ln_output.append(n_out)
            if ib_debug:
                logging.debug(f"OUT: {n_out} | A: {n_a} | B: {n_b} | C: {n_c} |")

        if ib_debug:
            logging.debug(f"Environment | Input: {self.n_input} | Output: {self.ln_output}")

        return False #OK

    def set( self, iln_input : List[int] ) -> bool:
        self.ln_input_octal_reverse = iln_input
        self.cl_fitness.clear()
        return False #OK
    
    def evaluate(self, iln_output_desired : List[int], ib_debug = False) -> bool:

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
    
    def compute_rightmost_correct_digits(self, iln_output_desired : List[int] ) -> Tuple[bool, int]:
        n_len = len(iln_output_desired)
        if (n_len != len(self.ln_output)):
            return True, -1 #Length mismatch
        for n_index in range(n_len):
            n_index_reverse = n_len -1 -n_index
            if self.ln_output[n_index_reverse] != iln_output_desired[n_index_reverse]:
                return False, n_index #rightmost valid digits
        return False, n_len #all valid digits

    def compute_valid_digits(self, iln_output_desired : List[int] ) -> Tuple[bool, int]:
        n_len = len(iln_output_desired)
        if (n_len != len(self.ln_output)):
            return True, -1 #Length mismatch
        n_valid_digits = 0
        for n_value_lhs, n_value_rhs in zip(self.ln_output, iln_output_desired):
            if n_value_lhs == n_value_rhs:
                n_valid_digits += 1
        return False, n_valid_digits

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