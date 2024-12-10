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
        self.ln_file_system: List[int] = list()  # List to store the file system blocks
        self.ln_block_id: List[int] = list()     # List to store the block IDs
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
        # Scan file system block sizes
        for n_file_system in self.ln_file_system:
            if b_true_block_false_void:
                for _ in range(n_file_system):
                    self.ln_block_id.append(n_block_id)
                n_block_id += 1
                b_true_block_false_void = False
            else:
                for _ in range(n_file_system):
                    self.ln_block_id.append(self.cn_void_id)
                b_true_block_false_void = True
        logging.info(f"Block ID size: {len(self.ln_block_id)}")
        logging.info(f"Block IDs: {self.ln_block_id}")
        return True

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

    def compute_checksum(self) -> int:
        """
        Compute the checksum of the block IDs.
        :return: The checksum value.
        """
        n_checksum = 0
        for n_index, n_block_id in enumerate(self.ln_block_id):
            if n_block_id != self.cn_void_id:
                n_checksum += n_index * n_block_id
        logging.debug(f"Checksum: {n_checksum}")
        return n_checksum

#------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(
        filename="day09/day_9.log",
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin")

    cl_defrag = Defrag()
    #s_filename_file_system = "day09/day_9_example.txt"
    s_filename_file_system = "day09/day_9_data.txt"
    if cl_defrag.load_filesystem_from_file(s_filename_file_system):
        if cl_defrag.translate_file_system_to_block_id():
            cl_defrag.defrag()
            checksum = cl_defrag.compute_checksum()
            logging.info(f"Checksum: {checksum}")
        else:
            logging.error("Translation failed.")
    else:
        logging.error("Failed to load file system.")
