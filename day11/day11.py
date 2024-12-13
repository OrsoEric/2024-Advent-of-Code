#------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#------------------------------------------------------------------------------------------------------------------------------

import logging

from typing import Dict, List, Tuple

import copy

#------------------------------------------------------------------------------------------------------------------------------
#   RULES
#------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------
#   ALGORITHM
#------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------
#   SOLUTION
#------------------------------------------------------------------------------------------------------------------------------

class Moai:
    def __init__(self):
        #list of stones with their number
        self.gln_stone_number : List[int] = list()
        #dictionary of stones numbers with their current quantity and next quantity
        self.gdn_stone_number : Dict[int] = dict()

    def load_from_file(self, is_filename: str) -> bool:
        """
        """
        try:
            with open(is_filename, 'r') as cl_file:
                ls_lines = cl_file.readlines()
                # Expect exactly one long line
                if len(ls_lines) > 1:
                    logging.error(f"ERROR: file has more than 1 line: {len(ls_lines)}")
                for s_char in ls_lines[0].split():
                    self.gln_stone_number.append(int(s_char))
            logging.info(f"Number of Moai Stones: {len(self.gln_stone_number)}")
            logging.info(f"Moai: \n{self.gln_stone_number}")
            
        except Exception as e:
            logging.error(f"ERROR: Loading file: {e}")
            return True #FAIL
        
        b_fail = self.compute_dict()
        if b_fail:
            logging.error("ERROR: failed to turn list of numbers into dictionary")
            return True #FAIL
        return False #OK
        
    def show(self)-> bool:
        sorted(self.gdn_stone_number.items())
        logging.info(f"Number of Moai Stones: {len(self.gln_stone_number)}")
        for n_key, ln_quantity in self.gdn_stone_number.items():
            logging.info(f"Engraved Number {n_key:10} | Current Quantity: {ln_quantity[0]:5} | Quantity increment {ln_quantity[1]:5}")

    def compute_dict(self):
        """
        it looks like position doesn't matter, I use a dictionary to store a stone number with the number of occurrences
        I store a list of two numbers, current, and next, because all stones are processed concurrently
        """

        #allocate stones numbered zero and 1
        self.gdn_stone_number[0] = [0, 0]
        self.gdn_stone_number[1] = [0, 0]

        for n_stone_number in self.gln_stone_number:
            if n_stone_number not in self.gdn_stone_number:
                #the stone appears 1 in current number, and the next iteration has 0 additional stones with that number
                self.gdn_stone_number[n_stone_number] = [1, 0]
            else:
                tnn_quantity = self.gdn_stone_number[n_stone_number]
                #I currently have 1 additional stone
                tnn_quantity[0] +=1
                #this list should still link to the dictionary, no need to write back

        logging.info(f"Unique numbers {len(self.gdn_stone_number)}")
        logging.info(f"Stone Numbers and Quantity\n{self.gdn_stone_number}")

        return False #OK

    def apply_quantity_increment( self ) -> Tuple[bool, int]:
        """
        """

        #store total stone quantity
        n_accumulator = 0

        #list of keys to be deleted from the dictionary
        ln_delete : List[int] = list()
        #for all stones
        for n_key, ln_quantity in self.gdn_stone_number.items():
            #incorporate NEXT into CURRENT, NEXT becomes 0
            ln_quantity[0] += ln_quantity[1]
            ln_quantity[1] = 0
            #if the key is not a common 0/1 key and has 0 quantity
            if n_key != 0 and n_key != 1 and ln_quantity[0] == 0:
                #add the key to the list of keys to be deleted
                ln_delete.append(n_key)
            #update quantity accumulator
            n_accumulator += ln_quantity[0]

        #delete all the zero quantity keys from the dictionary
        for n_key_to_be_deleted in ln_delete:
            del self.gdn_stone_number[n_key_to_be_deleted]

        logging.debug("STEP0: APPLY INCREMENT")
        #self.show()

        logging.info(f"Total Stone Quantity: {n_accumulator}")

        return False, n_accumulator #OK


    def apply_rule(self):
        """
        apply rules to all stones simultaneously
        """

        #dictionary to store new keys to be added
        d_new_numbers = dict()

        #for all stones
        for n_key, ln_quantity in self.gdn_stone_number.items():
            #convert key to string, needed for rule 2
            s_key = str(n_key)
            #RULE 1 0 -> 1
            if n_key == 0:
                logging.debug(f"{n_key} apply RULE 1")
                n_backup = ln_quantity[0]
                #STONE0: add negative quantity as they get replaced
                ln_quantity[1] += -n_backup
                #STONE1: add positive quantity of stones
                ln_quantity_one = self.gdn_stone_number[1] 
                ln_quantity_one[1] += n_backup
            #if the number is of even length, split it in two numbers
            elif len(s_key) %2 == 0:
                logging.debug(f"{n_key} apply RULE 2")
                #compute the split
                n_pivot = len(s_key) // 2
                n_new_left = int(s_key[:n_pivot])
                n_new_right = int(s_key[n_pivot:])
                #backup stone quantity
                n_quantity_backup = ln_quantity[0]
                #decrease the stone quantity as the stone is split
                ln_quantity[0] += -n_quantity_backup
                #create a stone with the left part of the number
                if n_new_left not in self.gdn_stone_number:
                    if n_new_left not in d_new_numbers:
                        d_new_numbers[n_new_left] = [0,n_quantity_backup]
                    else:
                        ln_new_quantity = d_new_numbers[n_new_left]
                        ln_new_quantity[1] += n_quantity_backup
                else:
                    ln_new_quantity = self.gdn_stone_number[n_new_left]
                    ln_new_quantity[1] += n_quantity_backup
                #create a stone with the right part of the number
                if n_new_right not in self.gdn_stone_number:
                    if n_new_right not in d_new_numbers:
                        d_new_numbers[n_new_right] = [0,n_quantity_backup]
                    else:
                        ln_new_quantity = d_new_numbers[n_new_right]
                        ln_new_quantity[1] += n_quantity_backup
                else:
                    ln_new_quantity = self.gdn_stone_number[n_new_right]
                    ln_new_quantity[1] += n_quantity_backup

            #number * 2024
            else:
                logging.debug(f"{n_key} apply RULE 3")
                n_quantity_backup = ln_quantity[0]
                #STONE0: add negative quantity as they get replaced
                ln_quantity[1] += -n_quantity_backup
                #multiply the key number
                n_new_key = n_key * 2024
                #increase quantity of the appropriate stone
                if n_new_key not in self.gdn_stone_number:
                    if n_new_key not in d_new_numbers:
                        d_new_numbers[n_new_key] = [0,n_quantity_backup]
                    else:
                        ln_new_quantity = d_new_numbers[n_new_key]
                        ln_new_quantity[1] += n_quantity_backup
                else:
                    ln_new_quantity = self.gdn_stone_number[n_new_key]
                    ln_new_quantity[1] += n_quantity_backup

        #self.show()
        self.gdn_stone_number.update(d_new_numbers)
        del d_new_numbers

        logging.debug("STEP1: APPLY RULE")
        #self.show()

        return False #OK

    def simulate(self, in_steps ) -> bool:
        """
        simulate a number of steps (blinks)
        """

        self.show()

        for n_cnt in range(in_steps):
            logging.info(f"SIMULATE STEP: {n_cnt+1}")
            self.apply_quantity_increment()
            self.show()
            self.apply_rule()
            self.show()
            
        
        self.apply_quantity_increment()

        self.show()

        return False #OK

#------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(
        filename="day11/day11.log",
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin")

    cl_moai = Moai()
    #b_fail = cl_moai.load_from_file("day11/day11-example.txt")
    #b_fail = cl_moai.load_from_file("day11/day11-example-b.txt")
    b_fail = cl_moai.load_from_file("day11/day11-data.txt")
    if b_fail:
        logging.error("ERROR: failed to load")
        pass
    
    cl_moai.simulate(75)



