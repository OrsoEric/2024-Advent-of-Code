#------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#------------------------------------------------------------------------------------------------------------------------------

import logging
from typing import List

#------------------------------------------------------------------------------------------------------------------------------
#   RULES
#------------------------------------------------------------------------------------------------------------------------------

# PART 1: FILE SYSTEM
# - used blocks   
# - free blocks
# - sequence of incremental block IDs and empty slots
# - checksum calculation based on block positions and IDs
# Checksum:
# 6341711060162 
# Checksum part 2
# 9841222919349
# still too high
# 6386100756825
# 6377400869326
#it shsould be bigger

#part 2
#blocks id go from 0 to 9999
#start
#ID0    ID1     ID2     ID3     ID4
#7 7    2 7     4 5     9 8     1 8
#ending
#       ID9998  ID9999
#8 1    6 3     4 8
#It should be 9999 adter ID3 with no void to ID4
#it should be 9998 and 9997 after ID0 with 3 voids

#------------------------------------------------------------------------------------------------------------------------------
#   ALGORITHM
#------------------------------------------------------------------------------------------------------------------------------

# 1) Load the file system into a list of integers.
# 2) Translate the file system list into a list of block IDs.
# 3) Compute the checksum of the block ID map.

#------------------------------------------------------------------------------------------------------------------------------
#   SOLUTION
#------------------------------------------------------------------------------------------------------------------------------

class Defrag:
    def __init__(self):
        self.b_check_block_conservation = False
        self.ln_file_system: List[int] = list()  # List to store the file system blocks
        self.ln_block_id: List[int] = list()     # List to store the block IDs
        #this is a companion list to file system, that lists the block id. makes it easier to do part 2 defrag
        self.ln_file_system_block_id : List[int] = list() 
        self.cn_void_id = -1                     # Constant for void blocks

    def load_filesystem_from_file(self, is_filename: str) -> bool:
        """
        Load a file system from a file.
        :param is_filename: Name of the file containing the file system.
        :return: True if the file system is loaded successfully, False otherwise.
        """
        try:
            with open(is_filename, 'r') as cl_file:
                ls_lines = cl_file.readlines()
                # Expect exactly one long line
                if len(ls_lines) > 1:
                    logging.error(f"ERROR: file system has more than 1 line: {len(ls_lines)}")
                for s_char in ls_lines[0].strip():
                    self.ln_file_system.append(int(s_char))
            logging.info(f"File system size: {len(self.ln_file_system)}")
            logging.info(f"File system: {self.ln_file_system}")
            #if it's odd, it means it ends with a block
            if (len(self.ln_file_system)%2 != 0):
                #for reasons that will be clear later, the last entry should be a void of size 0
                self.ln_file_system.append(0)
            return True
        except Exception as e:
            logging.error(f"ERROR: Loading file: {e}")
            return False
        
    def translate_file_system_to_block_id(self) -> bool:
        """
        Translate the file system to block IDs.
        Even numbers represent block sizes; odd numbers represent void sizes.
        :return: True if the translation is successful, False otherwise.
        """
        # Reset block ID
        self.ln_block_id = list()
        # Initialize scanner
        b_true_block_false_void = True
        n_block_id = 0
        #prefill the block id companion to file system
        self.ln_file_system_block_id = [self.cn_void_id] * len(self.ln_file_system)

        # Scan file system block sizes
        for n_index, n_file_system in enumerate(self.ln_file_system):
            if b_true_block_false_void:
                for _ in range(n_file_system):
                    self.ln_block_id.append(n_block_id)
                #since I'm at it I fill the companion list
                self.ln_file_system_block_id[n_index] = n_block_id
                n_block_id += 1
                b_true_block_false_void = False
            else:
                for _ in range(n_file_system):
                    self.ln_block_id.append(self.cn_void_id)
                b_true_block_false_void = True

        logging.info(f"Filesystem Block ID size: {len(self.ln_file_system_block_id)}")
        logging.info(f"Filesystem  Block IDs: {self.ln_file_system_block_id}")
        logging.info(f"File system size: {len(self.ln_file_system)}")
        logging.info(f"File system: {self.ln_file_system}")
        logging.info(f"Block ID size: {len(self.ln_block_id)}")
        logging.info(f"Block ID : {self.ln_block_id}")
        return False #ok
    
    def smart_translate_file_system_to_block_id(self):
        """
        I use the block id vector
        """

        # Reset block ID
        self.ln_block_id = list()
        # Scan file system block sizes
        for n_index, n_block_size in enumerate(self.ln_file_system):
            print(f"build {n_index} of {len(self.ln_file_system)}")
            n_block_id = self.ln_file_system_block_id[n_index]
            for _ in range(n_block_size):
                self.ln_block_id.append(n_block_id)

        logging.info(f"Block ID size: {len(self.ln_block_id)}")
        logging.info(f"Block ID: {self.ln_block_id}")
        print("DONE")
        return False #OK

    def show_file_system(self):
        s_line =f"size:{len(self.ln_file_system)}\n"
        for n_num in range(len(self.ln_file_system)):
            s_line+=f"{n_num:3},"
        s_line+="\n"
        for n_num in self.ln_file_system:
            s_line+=f"{n_num:3},"
        s_line+="\n"
        for n_num in self.ln_file_system_block_id:
            s_line+=f"{n_num:3},"
        logging.debug(s_line)

    def defrag(self) -> bool:
        """
        Defrag the block IDs by swapping the latest non-void block with the earliest void block.
        :return: True if the defragmentation is successful, False otherwise.
        """
        n_block_index = len(self.ln_block_id) - 1
        n_void_index = 0
        b_continue = True
        while b_continue:
            # Scan the next void
            while n_void_index < len(self.ln_block_id) and self.ln_block_id[n_void_index] != self.cn_void_id:
                n_void_index += 1
            # Scan the next block ID
            while n_block_index >= 0 and self.ln_block_id[n_block_index] == self.cn_void_id:
                n_block_index -= 1
            # Check if done
            if n_block_index < 0 or n_void_index >= len(self.ln_block_id) or n_block_index < n_void_index:
                b_continue = False
            else:
                # Swap blocks
                self.ln_block_id[n_void_index], self.ln_block_id[n_block_index] = self.ln_block_id[n_block_index], self.ln_block_id[n_void_index]
                logging.debug(f"Swap block {n_block_index} with void {n_void_index}")
        logging.info(f"Defragged block ID size: {len(self.ln_block_id)}")
        logging.info(f"Defragged block IDs: {self.ln_block_id}")
        return True

    def insert_block(self, in_block_index, in_void_index) -> bool:
        """
        insert a block inside a void
        """
        logging.debug(f"INSERT block position {in_block_index} inside void position {in_void_index}")

        if (in_void_index >= in_block_index):
            logging.error("ERROR: defrag should never move blocks forward, creating void, because it'ss a stupid algorithm")
            return True #FAIL
        
        self.show_file_system()

        n_block_size = self.ln_file_system[in_block_index]
        n_block_id = self.ln_file_system_block_id[in_block_index]
        n_void_size = self.ln_file_system[in_void_index]
        if (n_block_size > n_void_size):
            logging.error(f"ERROR: trying to move block size {n_block_size} into void size {n_void_size}")
            return True #FAIL

        logging.info(f"MOVE Block size {n_block_size} ID {n_block_id} - Void size {n_void_size} after block ID {self.ln_file_system_block_id[in_void_index-1]}")
        
        #reduce the size of the void to zero, as block become contiguous
        self.ln_file_system[in_void_index] = 0
        
        #backup void after block
        n_void_after_block_size = self.ln_file_system[in_block_index+1]

        #I need to make space after the void to insert block
        #the block that comes after the void
        #needs to be copied two slots after
        logging.debug(f"translate {in_void_index+1,in_block_index-1} ->{in_void_index+3,in_block_index+1}")
        self.ln_file_system[in_void_index+3:in_block_index+1+1] = self.ln_file_system[in_void_index+1:in_block_index-1+1]
        self.ln_file_system_block_id[in_void_index+3:in_block_index+1+1] = self.ln_file_system_block_id[in_void_index+1:in_block_index-1+1]

        #the block after the void becomes the block I inserted
        self.ln_file_system[in_void_index+1] = n_block_size
        self.ln_file_system_block_id[in_void_index+1] = n_block_id
        
        #the void after the block I inserted is the size of the void minus size of the block
        self.ln_file_system[in_void_index+2] = n_void_size -n_block_size 

        logging.debug(f"index: {in_block_index+1} already there {self.ln_file_system[in_block_index+1]} block size {n_block_size} backup {n_void_after_block_size}")
        #the void after the original block has increased in size by the block size
        self.ln_file_system[in_block_index+1] += n_block_size
        #the void must retain the size it had before it was backed up
        self.ln_file_system[in_block_index+1] += n_void_after_block_size

        self.show_file_system()

        #self.ln_file_system = self.ln_file_system[:n_index_b] +

        #self.ln_file_system = self.ln_file_system[:n_index_b] + [n_block_size_a,0] +self.ln_file_system[n_index_b:]
        #self.ln_file_system_block_id = self.ln_file_system_block_id[:n_index_b] + [n_block_id_a,0] +self.ln_file_system_block_id[n_index_b:]
        return False #OK

    def defrag_stupid( self ) -> bool:
        """
        try to move the highest full block id
        to the earliest void big enough to fit it
        a stupid way to defrag a disk...
        I already have a map of blocks and voids
        It's easier to list the block ids, by the side of the file system vector
        file system
            [ 1, 1, 1, 1, 1, 1, 1]
            [ 0,-1, 1,-1, 2,-1, 3]
            0.1.2.3
        ID3->void after ID0
            [ 1, 0, 1, 0, 1, 1, 1, 1]
            [ 0,-1, 3,-1, 1,-1, 2, -1]
            031.2..
        I see that I moved all blocks forward to leave space
        I needed to add one void at the end if it wasn't already there
        almost there, i miss two spaces, likely a bug in the void update
        got
        [0, 0, 9, 9, 2, 1, 1, 1, 7, 7, 7, -1, 4, 4, -1, 3, 3, 3, -1, -1, 5, 5, 5, 5, -1, 6, 6, 6, 6, -1, -1, -1, -1, -1, 8, 8, 8, 8, -1, -1] 
        desired
        [0, 0, 9, 9, 2, 1, 1, 1, 7, 7, 7, -1, 4, 4, -1, 3, 3, 3, -1, -1, -1, -1, 5, 5, 5, 5, -1, 6, 6, 6, 6, -1, -1, -1, 8, 8, 8, 8, -1, -1] 
        [2024-12-10 15:12:31,346] DEBUG day_9:124 > size:20
        0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
        2,  0,  2,  1,  3,  0,  3,  0,  1,  3,  3,  1,  2,  1,  4,  1,  4,  3,  4,  2,
        0, -1,  9, -1,  1, -1,  7, -1,  2, -1,  3, -1,  4, -1,  5, -1,  6, -1,  8, -1, 
        [2024-12-10 15:12:31,346] DEBUG day_9:171 > MOVE Block size 2 ID 4 - Void size 3 
        [2024-12-10 15:12:31,346] DEBUG day_9:179 > translate (10, 11) ->(12, 13) 
        [2024-12-10 15:12:31,346] DEBUG day_9:124 > size:20
        0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
        2,  0,  2,  1,  3,  0,  3,  0,  1,  0,  2,  1,  3,  2,  4,  1,  4,  3,  4,  2,
        0, -1,  9, -1,  1, -1,  7, -1,  2, -1,  4, -1,  3, -1,  5, -1,  6, -1,  8, -1, 
        should be: it's the address 13 that is wrong
        0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
        2,  0,  2,  1,  3,  0,  3,  0,  1,  0,  2,  1,  3,  4,  4,  1,  4,  3,  4,  2,
        0, -1,  9, -1,  1, -1,  7, -1,  2, -1,  4, -1,  3, -1,  5, -1,  6, -1,  8, -1,        
        when I overwrite 13, i need to backup the void, and add it

        the last number is huge overflows
        added conservation of blocks
        there is a fail in conservation.
        the void 19 should be the 18 moved (2) 
        the void already in 19 (2)
        the void before in 17 that merges (1)
        [2024-12-10 17:00:32,911] DEBUG day_9:146 > size:20
        0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
        2,  0,  2,  1,  3,  3,  1,  3,  3,  1,  2,  1,  4,  1,  4,  1,  3,  1,  2,  2,
        0, -1,  9, -1,  1, -1,  2, -1,  3, -1,  4, -1,  5, -1,  6, -1,  7, -1,  8, -1, 
        [2024-12-10 17:00:32,911] INFO day_9:193 > MOVE Block size 2 ID 8 - Void size 3 after block ID 1 
        [2024-12-10 17:00:32,911] DEBUG day_9:204 > translate (6, 17) ->(8, 19) 
        [2024-12-10 17:00:32,911] DEBUG day_9:146 > size:20
        0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
        2,  0,  2,  1,  3,  0,  2,  1,  1,  3,  3,  1,  2,  1,  4,  1,  4,  1,  3,  6,
        0, -1,  9, -1,  1, -1,  8, -1,  2, -1,  3, -1,  4, -1,  5, -1,  6, -1,  7, -1, 
        [2024-12-10 17:00:32,911] ERROR day_9:306 > block conservation broken! 40 is 41 

        """
        #the number of blocks should be conserved
        n_sum_block = sum(self.ln_file_system)

        #start scanning blocks from the end, skip the last void
        n_index_a = len(self.ln_file_system) - 1 -1
        # Scan the blocks in reverse
        while n_index_a > 0:
            print(f"scanning {self.ln_file_system_block_id[n_index_a]} - {n_index_a}")
            logging.info(f"scanning {self.ln_file_system_block_id[n_index_a]}")
            n_block_size_a = self.ln_file_system[n_index_a]
            n_block_id_a = self.ln_file_system_block_id[n_index_a]
            logging.debug(f"scan {n_index_a} block size {n_block_size_a} block id {n_block_id_a}")
            #if it's a block
            if (n_block_id_a != self.cn_void_id):
                #start from the first void
                n_index_b = 1
                #scan the voids forward
                b_continue_scan_void = True
                while ((b_continue_scan_void == True) and (n_index_b < len(self.ln_file_system) - 1) and (n_index_a > n_index_b)):
                    n_void_size_b = self.ln_file_system[n_index_b]
                    n_void_id_b = self.ln_file_system_block_id[n_index_b]
                    if (n_void_id_b != self.cn_void_id):
                        logging.error(f"ERROR: NOT A VOID position {n_index_b} id: {n_void_id_b}")
                        return True #FAIL
                    #if the void is too small
                    elif (n_void_size_b < n_block_size_a):
                        logging.debug(f"void {n_index_b} is too small to fit block id {n_block_id_a}. size {n_void_size_b} needed {n_block_size_a}")
                        #reverse to previous block
                    #if it's a void that EXACTLY fits the block
                    elif (n_void_size_b >= n_block_size_a):
                        logging.debug(f"void {n_index_b} fits block id {n_block_id_a}. size {n_void_size_b} needed {n_block_size_a}")
                        #the void becomes size zero
                        #I insert the block in the list
                        #followed by a void of size zero
                        #the block and void needs to be ereased
                        
                        self.insert_block( n_index_a, n_index_b)

                        if (self.b_check_block_conservation):
                            n_sum_block_new = sum(self.ln_file_system)
                            if (n_sum_block != n_sum_block_new):
                                logging.error(f"block conservation broken! {n_sum_block} is {n_sum_block_new}")
                                logging.info(self.ln_file_system)
                                return True #fail

                        b_continue_scan_void = False
                        #I need not to advance because I have overwritten
                        #n_index_a -= 2
                    else:
                        logging.error("ERROR: algorithm is wrong")
                    #advance to the next void
                    n_index_b += 2
                    #if I reached the end of the void scan
                if (b_continue_scan_void == True):
                    #I can scan the next block
                    n_index_a -= 2
                    logging.debug("cannot move this block")
                #stop the search early when debugging the algorithm
                if (n_block_id_a < 0):
                    break
            else:
                logging.error(f"ERROR: block is addressing a void! position: {n_index_a}")

        logging.info("DONE")
        return False # OK
            
    def compute_checksum(self) -> int:
        """
        Compute the checksum of the block IDs.
        :return: The checksum value.
        """
        n_checksum = 0
        for n_index, n_block_id in enumerate(self.ln_block_id):
            if n_block_id != self.cn_void_id:
                if (n_block_id!=self.cn_void_id):
                    n_checksum += n_index * n_block_id
        logging.info(f"Checksum: {n_checksum}")
        return n_checksum
    
    def smart_checksum(self) -> int:
        """
        compute checksum without building build ID list
        """
        # Reset block ID
        n_accumulator = 0
        n_final_index = 0
        # Scan file system block sizes
        for n_index, n_block_size in enumerate(self.ln_file_system):
            n_block_id = self.ln_file_system_block_id[n_index]
            print(f"scan {n_index} of {len(self.ln_file_system)} - ID {n_block_id} - Size: {n_block_size}")
            if (n_block_id!=self.cn_void_id):
                for _ in range(n_block_size):
                    n_accumulator += n_block_id*n_final_index
                    n_final_index += 1
            else:
                n_final_index += n_block_size
    
        s_line = f"checksum: {n_accumulator} final index: {n_final_index}"
        logging.info("FILE SYSTEM - BLOCK SIZE")
        logging.info(self.ln_file_system)
        logging.info("FILE SYSTEM - BLOCK ID")
        logging.info(self.ln_file_system_block_id)
        logging.info(s_line)
        print(s_line)
        
        return n_accumulator



#------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(
        filename="day09/day_9.log",
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin")

    cl_defrag = Defrag()
    #s_filename_file_system = "day09/day_9_critical_case_example.txt"
    #s_filename_file_system = "day09/day_9_example.txt"
    s_filename_file_system = "day09/day_9_data.txt"
    """
    if cl_defrag.load_filesystem_from_file(s_filename_file_system):
        if cl_defrag.translate_file_system_to_block_id():
            cl_defrag.defrag()
            checksum = cl_defrag.compute_checksum()
            logging.info(f"Checksum: {checksum}")
        else:
            logging.error("Translation failed.")
    else:
        logging.error("Failed to load file system.")
    """
    cl_defrag.load_filesystem_from_file(s_filename_file_system)
    cl_defrag.translate_file_system_to_block_id()
    n_checksum_original = cl_defrag.compute_checksum()
    cl_defrag.defrag_stupid()
    #cl_defrag.smart_translate_file_system_to_block_id()
    #n_checksum = cl_defrag.compute_checksum()
    n_checksum = cl_defrag.smart_checksum()

    print(f"second algorithm checksum: {n_checksum}")
    #example give:
    # second algorithm checksum: 2858
    #TOO HIGH
    #second algorithm checksum: 9841222919349