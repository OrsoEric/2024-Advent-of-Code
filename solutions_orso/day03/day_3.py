"""
--- Day 3: Mull It Over ---
"Our computers are having issues, so I have no idea if we have any Chief Historians in stock!
You're welcome to check the warehouse, though,"
says the mildly flustered shopkeeper at the North Pole Toboggan Rental Shop.
The Historians head out to take a look.

The shopkeeper turns to you
"Any chance you can see why our computers are having issues again?"

The computer appears to be trying to run a program, but its memory (your puzzle input) is corrupted.
All of the instructions have been jumbled up!

It seems like the goal of the program is just to multiply some numbers.
It does that with instructions like mul(X,Y), where X and Y are each 1-3 digit numbers.
For instance, mul(44,46) multiplies 44 by 46 to get a result of 2024.
Similarly, mul(123,4) would multiply 123 by 4.

However, because the program's memory has been corrupted, there are also many invalid characters that should be ignored
even if they look like part of a mul instruction.
Sequences like mul(4*, mul(6,9!, ?(12,34), or mul ( 2 , 4 ) do nothing.

For example, consider the following section of corrupted memory:

xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))

Only the four highlighted sections are real mul instructions.
Adding up the result of each instruction produces 161 (2*4 + 5*5 + 11*8 + 8*5).

Scan the corrupted memory for uncorrupted mul instructions. What do you get if you add up all of the results of the multiplications?
"""
"""
ALGORITHM
do a finite state machine that matches
1) match "mul("
2) search an int
3) search ","
4) search an int
5) search )
6) return two operands X, Y
"""

from typing import Tuple, List

def load_string(is_filename: str) -> str:
    """
    From file, load the full string

    :param filename: The name of the file containing the location IDs.
    :return: string of the problem
    """
    s_sequence = str()

    with open(is_filename, 'r') as c_file:
        for s_line in c_file:
            s_sequence += s_line

    return s_sequence

def parse_sequence( s_sequence : str ) -> List[Tuple[int, int]]:
    """
    From a sequence, extract mul(X,Y)->[(X,Y)]
    :param s_sequence: sequence of characters
    """

    ltn_result = list()

    ls_state = ["m", "u", "l", "(", "X", ",", "Y", ")"]

    #start from searching m
    s_state = ls_state[0]
    s_number = ""
    n_arg_x = int(0)
    n_arg_y = int(0)
    n_index = 0
    n_max_index = len(s_sequence)
    while n_index < n_max_index:
        #fetch character
        s_char = s_sequence[n_index]
        #next character
        n_index += 1
        print(f"{s_char}")
        if (s_state == ls_state[0]):
            if (s_char == s_state):
                #match
                s_state = ls_state[1]
                print(f"match {s_char}")
            else:
                #reset
                s_state = ls_state[0]
                print(f"Char: {s_char} | state: {s_state} | FSM error, reset.")
        elif (s_state == ls_state[1]):
            if (s_char == s_state):
                #match
                s_state = ls_state[2]
                print(f"match {s_char}")
            else:
                #reset
                s_state = ls_state[0]
                print(f"Char: {s_char} | state: {s_state} | FSM error, reset.")
        elif (s_state == ls_state[2]):
            if (s_char == s_state):
                #match
                s_state = ls_state[3]
                print(f"match {s_char}")
            else:
                #reset
                s_state = ls_state[0]
                print(f"Char: {s_char} | state: {s_state} | FSM error, reset.")
        elif (s_state == ls_state[3]):
            if (s_char == s_state):
                #detect number
                s_state = ls_state[4]
                s_number = ""
                print(f"match {s_char}")
            else:
                #reset
                s_state = ls_state[0]
                print(f"Char: {s_char} | state: {s_state} | FSM error, reset.")
        #match number, I eat all numbers and parse them into int when I get a non number
        elif (s_state == ls_state[4]):
            #number
            if (s_char >= "0") and (s_char <= "9"):
                s_number += s_char
                print(f"detecting number {s_char} ->{s_number}")
            #no numbers were eaten
            elif len(s_number) <= 0:
                #reset
                s_state = ls_state[0]
                print(f"Char: {s_char} | state: {s_state} | FSM error, no number detected.")
            #parse number to int
            else:
                n_arg_x = int(s_number)
                print(f"Detected X {n_arg_x}")
                #I need to reprocess this character
                n_index -= 1
                #next state
                s_state = ls_state[5]
        elif (s_state == ls_state[5]):
            if (s_char == s_state):
                #detect number
                s_state = ls_state[6]
                s_number = ""
                print(f"match {s_char}")
            else:
                #reset
                print(f"Char: {s_char} | state: {s_state} | FSM error, reset.")
                s_state = ls_state[0]
        #match number, I eat all numbers and parse them into int when I get a non number
        elif (s_state == ls_state[6]):
            #number
            if (s_char >= "0") and (s_char <= "9"):
                s_number += s_char
                print(f"detecting number {s_char} ->{s_number}")
            #no numbers were eaten
            elif len(s_number) <= 0:
                #reset
                s_state = ls_state[0]
                print(f"Char: {s_char} | state: {s_state} | FSM error, no number detected.")
            #parse number to int
            else:
                n_arg_y = int(s_number)
                print(f"Detected Y {n_arg_y}")
                #I need to reprocess this character
                n_index -= 1
                #next state
                s_state = ls_state[7]
        elif (s_state == ls_state[7]):
            if (s_char == s_state):
                #detect number
                print(f"FINAL MATCH, VALID X: {n_arg_x} Y: {n_arg_y}")
                tn_mul = (n_arg_x,n_arg_y)
                ltn_result.append(tn_mul)
                #reset
                s_state = ls_state[0]
            else:
                #reset
                print(f"Char: {s_char} | state: {s_state} | FSM error, reset.")
                s_state = ls_state[0]
        else:
            s_state = ls_state[0]
            print("ERR:ALGORITHM: ask the dev to finish his job")
        
    return ltn_result

def process_mul( iltn_args : List[Tuple[int,int]] ) -> int:
    n_result = 0
    for tn_arg in iltn_args:
        n_result += tn_arg[0] * tn_arg[1]
    return n_result

def day_3(is_filename: str) -> bool:
    #from file load the sequence
    s_sequence = load_string( is_filename )
    print(s_sequence)
    ltn_args = parse_sequence( s_sequence )
    print(ltn_args)
    n_result = process_mul( ltn_args )
    print(f"Result of valid mul(X,Y) = {n_result}")

#--------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#--------------------------------------------------------------------------------------------------------------------------------

# Example usage
gs_filename_example = 'advent_of_code\day_3_example.txt'
gs_filename = 'advent_of_code\day_3.txt'
#   if interpreter has the intent of executing this file
if __name__ == "__main__":
    day_3( gs_filename_example )
    day_3( gs_filename )