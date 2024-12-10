#--------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#--------------------------------------------------------------------------------------------------------------------------------

import logging

#from itertools import product, combinations

#import copy

from typing import Generator, Dict, Tuple, List

#--------------------------------------------------------------------------------------------------------------------------------
#   RULES
#--------------------------------------------------------------------------------------------------------------------------------

#       PART1
#   FILE SYSTEM
#   used blocks   
#   free blocks
#   2333133121414131402
#   BLOCK ID
#   sequence of incremental block ID and empty slots
#   each block has an ID. It's single digit in THIS example but is an int
#   00...111...2...333.44.5555.6666.777.888899
#   COMPACT BLOCK IDs
#   fill the latest block ID to the earliest empty slot
#   0099811188827773336446555566..............
#       note it's an irreversible operation.
#       if I reverse translate block id map to file system, I will lose the block IDs
#       fecause the file system doesn't have a block ID map
#   CHECKSUM
#   integral product of block position by block id
#   0         1         2         3
#   012345678901234567890123456789012345678901
#   0099811188827773336446555566..............
#   0*0 + 1*0 + 2*9 + 3*9 + 4*8 + ....
#   the problem is to return the checksum
#   

#--------------------------------------------------------------------------------------------------------------------------------
#   ALGORITHM
#--------------------------------------------------------------------------------------------------------------------------------

# 1) load file system into a list of int
# 2) transate list of int (file system) into list of int (block id)
# 3) compute checksum of a block id map

#--------------------------------------------------------------------------------------------------------------------------------
#   SOLUTION
#--------------------------------------------------------------------------------------------------------------------------------

class Defrag:
    def __init__(self):
        self.ln_file_system : List[int] = list()
        self.ln_block_id : List[int] = list()
        self.cn_void_id = -1

    def load_filesystem_from_file(self, is_filename: str) -> bool:
        """
        From a file, load a file system.
        """
        try:
            with open(is_filename, 'r') as cl_file:
                ls_lines = cl_file.readlines()
                #I expect exactly one long line
                if (len(ls_lines)>1):
                    logging.error(f"ERROR: file system has more than 1 line: {len(ls_lines)}")
                n_len_file_system = len(ls_lines[0])
                self.ln_file_system = list()
                for s_char in ls_lines[0]:
                    self.ln_file_system.append(int(s_char))

        except Exception as e:
            logging.error(f"ERROR: Loading file{e}")
            return False
        
        logging.info(f"File system size: {len(self.ln_file_system)}")
        logging.info(f"File system: {self.ln_file_system}")
        
    def translate_file_system_to_block_id( self ) -> bool:
        """
        even numbers are block size
        odd numbers are void size
        create a list of length total block size
        Fill it with -1 for voids
        block id increasing sequentially
        """
        #reset block id
        self.ln_block_id = list()
        #init scanner
        b_true_block_false_void = True
        n_block_id = 0
        #scan file system block sizes
        for n_file_system in self.ln_file_system:
            #scanning a block
            if b_true_block_false_void == True:
                for n_cnt in range(n_file_system):
                    self.ln_block_id.append(n_block_id)
                n_block_id += 1
                b_true_block_false_void = False
            else:
                for n_cnt in range(n_file_system):
                    self.ln_block_id.append(self.cn_void_id)
                b_true_block_false_void = True
        logging.info(f"Block ID size: {len(self.ln_block_id)}")
        logging.info(f"File system: {self.ln_block_id}")

        return False #OK

    def defrag(self) -> bool:
        """
        Defrag a block id
        take the latest non void block
        swap it with the earliest void block
        """

        n_block_index = len(self.ln_block_id) -1
        n_void_index = 0
        b_continue = True
        while b_continue:
            #scan the next void
            while ((n_void_index < len(self.ln_block_id)) and (self.ln_block_id[n_void_index] != self.cn_void_id)):
                n_void_index += 1
            #scan the next block id
            while ((n_block_index >= 0) and (self.ln_block_id[n_block_index] == self.cn_void_id)):
                n_block_index -= 1
            #check done
            if n_block_index < 0:
                b_continue = False
            elif n_void_index >= len(self.ln_block_id): 
                b_continue = False
            elif n_block_index < n_void_index:
                b_continue = False
            else:
                #swap blocks
                self.ln_block_id[n_void_index], self.ln_block_id[n_block_index] = self.ln_block_id[n_block_index], self.ln_block_id[n_void_index]
                logging.debug(f"swap block {n_block_index} with void {n_void_index}")
        logging.info(f"Block ID size: {len(self.ln_block_id)}")
        logging.info(f"File system: {self.ln_block_id}")
        return False #OK

    def compute_checksum(self) -> int:
        """
        from a block id, compute the checksum
        """
        n_checksum = 0
        for n_index, n_block_id in enumerate(self.ln_block_id):
            if (n_block_id != self.cn_void_id):
                n_checksum += n_index * n_block_id
        logging.debug(f"Checksum: {n_checksum}")
        return n_checksum

#--------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#--------------------------------------------------------------------------------------------------------------------------------

#   if interpreter has the intent of executing this file
if __name__ == "__main__":
    logging.basicConfig(
        filename="day09\day_9.log",
        # Specify the log file name
        level=logging.DEBUG,
        # Set the level of debug to show
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin") 

    cl_defrag = Defrag()
    #cl_defrag.load_filesystem_from_file("day09\day_9_example.txt")
    cl_defrag.load_filesystem_from_file("day09\day_9_data.txt")
    cl_defrag.translate_file_system_to_block_id()
    cl_defrag.defrag()
    cl_defrag.compute_checksum()