#------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#------------------------------------------------------------------------------------------------------------------------------

import logging

from typing import Set, Dict, List, Tuple

from enum import Enum, auto

#import copy

#from map_of_symbols import Map_of_symbols

#------------------------------------------------------------------------------------------------------------------------------
#   RULES
#------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------
#   ALGORITHM
#------------------------------------------------------------------------------------------------------------------------------

class Contender_class_asi:
    def __init__(self):
        """
        Don't bother loading from file. It's short and there are no exaples
        """
        #internal registers        
        #self.gln_reg : List[int] = [729, 0, 0]
        #self.gln_mem : List[int] = [0,1,5,4,3,0]

        #PART1 PROGRAM
        #self.gln_reg : List[int] = [35200350, 0, 0]
        #self.gln_mem : List[int] = [2,4,1,2,7,5,4,7,1,3,5,5,0,3,3,0]

        #self replicating program
        #self.gln_reg : List[int] = [117440, 0, 0]
        #self.gln_mem : List[int] = [0,3,5,4,3,0]

        #TEST PART 2 ONE DIGIT SOLUTUION
        #self.gln_reg : List[int] = [35680059893236, 0, 0]
        #self.gln_mem : List[int] = [2,4,1,2,7,5,4,7,1,3,5,5,0,3,3,0]
 
        #TEST PART 14 left digit correct
        #self.gln_reg : List[int] = [38886110969334, 0, 0]
        #self.gln_mem : List[int] = [2,4,1,2,7,5,4,7,1,3,5,5,0,3,3,0]
        #add an octal 0 to the right side
        #self.gln_reg : List[int] = [311088887754672, 0, 0]
        #self.gln_mem : List[int] = [2,4,1,2,7,5,4,7,1,3,5,5,0,3,3,0]

        #from the octal scan. Match 7
        #self.gln_reg : List[int] = [37186644195828, 0, 0]
        #self.gln_mem : List[int] = [2,4,1,2,7,5,4,7,1,3,5,5,0,3,3,0]

        #14 left correct, longeer input
        self.gln_reg : List[int] = [110346850582004, 0, 0]
        self.gln_mem : List[int] = [2,4,1,2,7,5,4,7,1,3,5,5,0,3,3,0]

        logging.info(f"A List: {number_to_list(self.gln_reg[0])}")

        #program counter
        self.gn_program_counter = 0
        #argument decoding
        self.cn_arg_op_register_a = 4
        self.cn_arg_op_register_b = 5
        self.cn_arg_op_register_c = 6
        #register index
        self.cn_index_register_a = 0
        self.cn_index_register_b = 1
        self.cn_index_register_c = 2

        self.ln_out : List[int] = list()

    def __repr__(self):
        return f"PC: {self.gn_program_counter} | REG A: {self.gln_reg[self.cn_index_register_a]} | REG B: {self.gln_reg[self.cn_index_register_b]} | REG C: {self.gln_reg[self.cn_index_register_c]} | OUTPUT {self.ln_out}"

    def is_pc_invalid( self ) -> bool:
        if self.gn_program_counter < 0 or self.gn_program_counter > len(self.gln_mem) -1:
            logging.error(f"ERROR: invalid program counter {self.gn_program_counter}")
            return True
        return False #OK

    def decode_argument(self, in_arg_code : int ) -> Tuple[bool, int]:
        if in_arg_code < 0 or in_arg_code >= 7:
            logging.error(f"ERROR: invalid argument code {in_arg_code}")
            return True, -1, "N.A."

        s_arg = 'n'
        match in_arg_code:
            case self.cn_arg_op_register_a:
                return False, self.gln_reg[self.cn_index_register_a], 'R.A'
            case self.cn_arg_op_register_b:
                return False, self.gln_reg[self.cn_index_register_b], 'R.B'
            case self.cn_arg_op_register_c:
                return False, self.gln_reg[self.cn_index_register_c], 'R.C'

        #return 1, 2, 3
        return False, in_arg_code, s_arg #OK

    def execute( self ) -> bool:
        """
        execute the instruction contained inside the program counter
        """
        if self.is_pc_invalid():
            return True #FAIL
        #FETCH
        n_op_code = self.gln_mem[self.gn_program_counter]
        n_arg_code = self.gln_mem[self.gn_program_counter +1]
        #DECODE ARGUMENT
        b_fail, n_arg, s_arg = self.decode_argument( n_arg_code )
        if b_fail:
            if n_op_code != 4:
                logging.error(f"ERROR: could not decode argument. Instruction {n_op_code} | Argument Code {n_arg_code}")
                return True #FAIL
            else:
                logging.debug(f"Invalid argument but instruction {n_op_code} doesn't use arguments")

        logging.debug(f"STATE: {self}")
        logging.debug(f"Instruction {n_op_code} | Argument Code {n_arg_code} | Argument {n_arg}")
        b_fail = self.execute_op_code( n_op_code, n_arg, s_arg )
        if b_fail:
            logging.error(f"ERROR: could not execute instruction {n_op_code} argument {n_arg}")
            return True #FAIL

        return False #OK
    
    def show_registers(self):
        logging.info("-----------------------------------------------------")
        logging.info(f"A: {self.gln_reg[self.cn_index_register_a]:15} B: {self.gln_reg[self.cn_index_register_b]:15} C: {self.gln_reg[self.cn_index_register_c]:15}")
        logging.info(f"A: {oct(self.gln_reg[self.cn_index_register_a]):15} B: {oct(self.gln_reg[self.cn_index_register_b]):15} C: {oct(self.gln_reg[self.cn_index_register_c]):15}")
        logging.info("-----------------------------------------------------")
        return False
    
    def execute_op_code(self, in_op_code : int, in_arg : int, s_arg : str ) -> bool:
        if in_op_code < 0 or in_op_code > 7:
            logging.error(f"ERROR: invalid op code {in_op_code}")
            return True

        b_jump = False

        match in_op_code:
            #A-DIV
            case 0:
                n_reg_a = self.gln_reg[self.cn_index_register_a]
                n_num = n_reg_a
                n_den = 2**in_arg
                n_reg_a = int( n_num / n_den )
                logging.info(f"A-DIV | A {n_reg_a} = A {n_num} / 2**{s_arg} {n_den}")
                logging.info(f"A-DIV | A {oct(n_reg_a)} = A {oct(n_num)} / {oct(n_den)}")
                #write back
                self.gln_reg[self.cn_index_register_a] = n_reg_a
            #B-XOR
            case 1:
                n_lhs = self.gln_reg[self.cn_index_register_b]
                n_rhs = in_arg
                n_res = n_lhs ^ n_rhs
                #write back
                self.gln_reg[self.cn_index_register_b] = n_res
                logging.info(f"B-XOR | B {n_res} = B {n_lhs} ^ {n_rhs}")
                logging.info(f"B-XOR | B {oct(n_res)} = B {oct(n_lhs)} ^ {oct(n_rhs)}")
            #B-MOD
            case 2:
                n_reg_b = in_arg % 8
                #WRITE BACK
                self.gln_reg[self.cn_index_register_b] =n_reg_b
                logging.info(f"B-MOD | B {n_reg_b} = {s_arg} {in_arg} MOD 8")
                logging.info(f"B-MOD | B {oct(n_reg_b)} = {oct(in_arg)} MOD 8")
            #JUMP
            case 3:
                n_cond = self.gln_reg[self.cn_index_register_a]
                if n_cond == 0:
                    pass
                else:
                    b_jump = True
                    self.gn_program_counter = in_arg
                    logging.info(f"JUMP | {s_arg} {in_arg}")
                    self.show_registers()

            #BC-XOR
            case 4:
                n_lhs = self.gln_reg[self.cn_index_register_b]
                n_rhs = self.gln_reg[self.cn_index_register_c]
                n_res = n_lhs ^ n_rhs
                #write back
                self.gln_reg[self.cn_index_register_b] = n_res
                logging.info(f"B-XOR | B {n_res} = B {n_lhs} ^ C {n_rhs}")
                logging.info(f"B-XOR | B {oct(n_res)} = B {oct(n_lhs)} ^ C {oct(n_rhs)}")
            #PRINT
            case 5:
                n_res = in_arg % 8
                self.ln_out.append(n_res)
                logging.info(f"PRINT {n_res} | {s_arg} {in_arg} % 8")
                logging.info(f"PRINT {oct(n_res)} | {oct(in_arg)} % 8")

            #B-DIV
            case 6:
                n_num = self.gln_reg[self.cn_index_register_a]
                n_den = 2**in_arg
                n_res = int( n_num / n_den )
                logging.info(f"B-DIV | B {n_res} = A {n_num} / 2**{s_arg} {n_den}")
                logging.info(f"B-DIV | B {oct(n_res)} = A {oct(n_num)} / {oct(n_den)}")
                #write back
                self.gln_reg[self.cn_index_register_b] = n_res        
            #C-DIV
            case 7:
                n_num = self.gln_reg[self.cn_index_register_a]
                n_den = 2**in_arg
                n_res = int( n_num / n_den )
                logging.info(f"C-DIV | C {n_res} = A {n_num} / 2**{s_arg} {n_den}")
                logging.info(f"C-DIV | C {oct(n_res)} = A {oct(n_num)} / 2^ARG {oct(n_den)}")
                #write back
                self.gln_reg[self.cn_index_register_c] = n_res
            case _:
                logging.error(f"ERROR: Unhandled instruction {in_op_code}")
                return True #FAIL

        if b_jump == False:
            self.gn_program_counter += 2

        return False #OK


    def get_output(self):
        s_output = ','.join(map(str, self.ln_out))
        return s_output

    def run_program(self) -> bool:
        self.show_registers()
        b_continue = True
        while b_continue:
            b_fail = self.execute()
            if b_fail:
                logging.error("ERROR: executing instruction")
                b_continue = False

            if self.gn_program_counter == len(self.gln_mem):
                logging.debug(f"HALT")
                b_continue = False
    


class Program_search:
    ln_a = list()
    a = 35200350
    b = 0
    c = 0
    ln = [2,4,1,2,7,5,4,7,1,3,5,5,0,3,3,0]
    ln_out = list()
    
    def __init__(self):
        pass
    
    @staticmethod
    def number_to_list( in_value : int ) -> List[int]:
        ln_value = [int(s_value) for s_value in str(in_value)]
        return ln_value
    
    @staticmethod
    def list_to_number( iln_value : List[int]) -> int:
        return int

    def norm_list( iln_a : int, iln_b : int ):
        """
        absolute difference between two lists
        returns a list as short as the shortest list with digit difference
        returns a value that is the sum of the square of the difference between digits
        do not take into account long chunks
        """

        return 0

    def execute(self):
        """
        B-MOD | B 6 = 35200350 MOD 8 
        B-XOR | B 4 = B 6 ^ 2 
        C-DIV | C 2200021 = A 35200350 / 16 
        B-XOR | B 2200017 = B 4 ^ C 2200021 
        B-XOR | B 2200018 = B 2200017 ^ 3 
        PRINT 2 | 2200018 % 8 
        A-DIV | A 4400043 = A 35200350 / 8 
        JUMP | 0 
        """

        self.b = self.a % 8
        self.b = self.b ^ 2
        self.c = int(self.a / 2**self.b)
        self.b = self.b ^ self.c
        self.b = self.b ^ 3
        self.a = int(self.a / 8)
        return self.b % 8 

    def run(self, in_a : int ) -> List[int]:
        #convert a into a list of int
        self.ln_a = self.number_to_list( self.a )
        logging.debug(f"A: {self.ln_a}")

        self.ln_out = list()
        self.a = in_a
        while self.a > 0:
            #logging.info(f"a: {self.a} | b {self.b} | c {self.c}")
            n_out = self.execute()
            #self.ln_out.append(n_out)
            self.ln_out.insert(0, n_out)

#------------------------------------------------------------------------------------------------------------------------------
#   SOLUTION
#------------------------------------------------------------------------------------------------------------------------------

def number_to_list( in_value : int ) -> List[int]:
    ln_value = [int(s_value) for s_value in str(in_value)]
    return ln_value

def solution() -> bool:
    cl_mendicant_bias = Contender_class_asi()
    cl_mendicant_bias.run_program()
    s_output = cl_mendicant_bias.get_output()
    logging.info(f"OUTPUT: {s_output}")

    return False #OK

def solution2():
    
    cl_search = Program_search()
    #cl_search.run(35580059893236)
    #cl_search.run(38886110969330)
    #cl_search.run(77772221938660)


    
    
    
    logging.info(f"OUT  {cl_search.ln_out} | {number_to_list(cl_search.a)}")
    """
    for n_cnt in range (1000):
        n_a = 35200350+n_cnt
        cl_search.run(n_a)
        logging.info(f"A {n_a} | OUT  {cl_search.ln_out}")
    """


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

    #solution2()

    


    #logging.info(f"Convert to list: {number_to_list(77772221938660)}")
    #n_decimal = 35580059893236
    #n_octal = oct(n_decimal)
    #logging.info(f"{n_octal}")
    #ln = number_to_list(1005604065136764)
    #ln=[3, 5, 5, 8, 0, 0, 5, 9, 8, 9, 3, 2, 3, 6]
    #logging.info(f"eversse List: {ln[::-1]}")
    
