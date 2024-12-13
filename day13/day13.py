#------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#------------------------------------------------------------------------------------------------------------------------------

import numpy

import logging

from typing import Set, Dict, List, Tuple

#import copy


#------------------------------------------------------------------------------------------------------------------------------
#   RULES
#------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------
#   ALGORITHM
#------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------
#   SOLUTION
#------------------------------------------------------------------------------------------------------------------------------

class Problem:
    def __init__(self):
        self.gm_a = numpy.zeros((2,2))
        self.gm_in = numpy.zeros((2))
        self.gm_out = numpy.zeros((2))
        #maximum number before the matrix is considered singular
        self.cn_condition_number_limit = 100
        #error before considering the solution invalid
        self.cn_error_limit = 0.5

    def load_parameters( self, iln_button_a : List[int], iln_button_b : List[int], iln_out : List[int] ) -> bool:
        self.gm_a[0][0] = iln_button_a[0]
        self.gm_a[0][1] = iln_button_a[1]
        self.gm_a[1][0] = iln_button_b[0]
        self.gm_a[1][1] = iln_button_b[1]
        self.gm_out[0] = iln_out[0]
        self.gm_out[1] = iln_out[1]

        logging.debug(f"PROBLEM\nMatrix A:\n{self.gm_a}\nOUT:\n{self.gm_out}")
        logging.debug(f"shape IN: {self.gm_in.shape} A: {self.gm_a.shape} OUT: {self.gm_out.shape}")

        return False #OK

    def get_in(self):
        ln_in = [self.gm_in[0],self.gm_in[1]]
        return ln_in

    def solve(self, b_debug=False) -> Tuple[bool,bool]:
        """
        True FAILED to find an integer solution
        False OK
        """
        if b_debug:
            formatted_solution = [f"{x:.0f}" for x in self.gm_out]
            logging.debug(f"PROBLEM\nMatrix A:\n{self.gm_a}\nOUT:\n{formatted_solution}")
        n_determinant = numpy.linalg.det(self.gm_a)
        n_condition_number = numpy.linalg.cond(self.gm_a)
        if b_debug:
            logging.debug(f"determinant: {n_determinant} Condition number: {n_condition_number}")
        #if I have exactly one solution
        if abs(n_condition_number) < self.cn_condition_number_limit:
            #compute the inverse
            m_a_inverse = numpy.linalg.inv(self.gm_a)
            #compute the button presses
            self.gm_in = numpy.matmul(self.gm_out,m_a_inverse)
            #make the numbers integer
            if b_debug:
                formatted_solution = [f"{x:.0f}" for x in self.gm_in]
                logging.debug(f"Solution f: {formatted_solution}")
            self.gm_in[0] = round(self.gm_in[0])
            self.gm_in[1] = round(self.gm_in[1])
            if b_debug:
                formatted_solution = [f"{x:.0f}" for x in self.gm_in]
                logging.debug(f"Solution i: {formatted_solution}")
            test_solution = numpy.matmul(self.gm_in,self.gm_a)
            n_error = numpy.linalg.norm(test_solution-self.gm_out)
            if b_debug:
                formatted_solution = [f"{x:.0f}" for x in test_solution]
                formatted_error = f"{n_error:.6f}"
                logging.debug(f"Test Solution: {formatted_solution} Error {formatted_error}")
            if n_error > self.cn_error_limit:
                return False, True #FAIL
        else:
            if b_debug:
                logging.debug("SINGULAR!!!")
            return True, False #FAIL

        return False,False #OK

class Claw_machine:
    def __init__(self):
        self.cn_big_offset = 10000000000000 
        self.glcl_problems : List[Problem] = list()
        self.glcl_unsolved_problems : List[Problem] = list()

    def load_problems_from_file(self, is_filename, b_add_offset=False ) -> bool:
        with open(is_filename, 'r') as file:
            ls_lines = file.readlines()
            #initialize the problem parameters
            ln_button_a = [0,0]
            ln_button_b = [0,0]
            ln_out = [0,0]
            for line in ls_lines:
                parts = line.strip().split(',')
                if parts[0].startswith('Button A'):
                    ln_button_a[0] = int(parts[0].split('+')[1])
                    ln_button_a[1] = int(parts[1].split('+')[1])
                elif parts[0].startswith('Button B'):
                    ln_button_b[0] = int(parts[0].split('+')[1])
                    ln_button_b[1] = int(parts[1].split('+')[1])
                elif parts[0].startswith('Prize'):
                    ln_out[0] = int(parts[0].split('=')[1])
                    ln_out[1] = int(parts[1].split('=')[1])
                    if b_add_offset:
                        ln_out[0] += self.cn_big_offset 
                        ln_out[1] += self.cn_big_offset 
                    cl_problem = Problem()
                    cl_problem.load_parameters( ln_button_a, ln_button_b, ln_out )
                    #append the problem to the list of problems
                    self.glcl_problems.append(cl_problem)
                else:
                    pass

        logging.info(f"Loaded {len(self.glcl_problems)} Problems")
        return False #OK

    def find_solutions(self):
        """
        each claw machine has spawned a problem
        """
        b_button_limit_disabled = True
        n_token = 0
        n_total_token = 0
        n_cnt_too_many_buttons = 0
        n_cnt_singular = 0
        n_cnt_integer = 0
        n_cnt_valid = 0
        for cl_problem in self.glcl_problems:
            b_fail_singular, b_fail_integer = cl_problem.solve(b_debug=True)

            if b_fail_singular:
                n_cnt_singular += 1
            if b_fail_integer:
                n_cnt_integer += 1
            else:
                ln_button = cl_problem.get_in()
                #if don't press too many buttons
                if b_button_limit_disabled or (ln_button[0] < 100) and (ln_button[1] < 100):
                    n_cnt_valid += 1
                    #valid solution
                    n_token = ln_button[0]*3 +ln_button[1]
                    n_total_token += n_token
                    logging.debug(f"SOLUTION: {ln_button} | Cost {n_token} Total {n_total_token}")
                else:
                    n_cnt_too_many_buttons += 1

        logging.debug(f"VALID: {n_cnt_valid}")
        logging.debug(f"ERR: Singular: {n_cnt_singular}")
        logging.debug(f"ERR: Integer: {n_cnt_integer}")
        logging.debug(f"ERR: Buttons: {n_cnt_too_many_buttons}")
        logging.debug(f"Total Cost: {n_total_token}")


#------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(
        filename="day13/day13.log",
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin")

    cl_claw_machine = Claw_machine()
    #cl_claw_machine.load_problems_from_file("day13/day13-example.txt",b_add_offset=True)
    #cl_claw_machine.load_problems_from_file("day13/day13-example-big.txt")
    #cl_claw_machine.load_problems_from_file("day13/day13-data.txt")
    cl_claw_machine.load_problems_from_file("day13/day13-data.txt",b_add_offset=True)
    cl_claw_machine.find_solutions()


