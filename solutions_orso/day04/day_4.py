"""
--- Day 4: Ceres Search ---
"Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:

..X...
.SAMX.
.A..A.
XMAS.S
.X....
The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX
Take a look at the little Elf's word search. How many times does XMAS appear?exit
"""

"""
ALGORITHM:
1) from file create a matrix (numpy?)
-generic scan function, takes a start coordinate

SEARCH ALGORITHM
-find all X and their coordinates
-find all M and their coordinates
-from those two lists, find all X with distance 1 from an M
-From there, try to match the rest of the string
"""

#--------------------------------------------------------------------------------------------------------------------------------
#   IMPORTS
#--------------------------------------------------------------------------------------------------------------------------------

import logging

import itertools

from typing import Dict, Tuple, List

#--------------------------------------------------------------------------------------------------------------------------------
#   
#--------------------------------------------------------------------------------------------------------------------------------

class Matrix:
    """
    A class to represent a matrix loaded from a text file.

    Attributes:
    -----------
    lls_matrix : List[List[str]]
        A 2D list to store the matrix elements.
    n_num_rows : int
        Number of rows in the matrix.
    n_num_cols : int
        Number of columns in the matrix.
    """

    def __init__(self):
        """
        Initializes the Matrix with empty attributes.
        """
        self.lls_matrix: List[List[str]] = list()
        self.dtn_matrix = dict()
        self.n_num_rows: int = 0
        self.n_num_cols: int = 0

    def load_matrix(self, s_filename: str) -> bool:
        """
        Loads the matrix from a text file. Ensures all rows have the same length.

        Parameters:
        -----------
        s_filename : str
            The name of the file to load the matrix from.

        Returns:
        --------
        bool
            False if the matrix is loaded successfully, True if there is an error.
        """
        with open(s_filename, 'r') as cl_file:
            for s_line in cl_file:
                s_row: List[str] = list(s_line.strip())
                if self.lls_matrix and len(s_row) != len(self.lls_matrix[0]):
                    logging.error("All rows in the matrix must be the same length.")
                    return True # fail
                self.lls_matrix.append(s_row)

        if not self.lls_matrix:
            logging.error("The matrix is empty.")
            return True # fail

        self.n_num_rows = len(self.lls_matrix)
        self.n_num_cols = len(self.lls_matrix[0])

        logging.info(f"Matrix loaded successfully with size {self.n_num_rows} rows x {self.n_num_cols} columns.")

        self.create_dict()

        return False # OK

    def create_dict(self) -> Dict[Tuple[int, int], str]:
        """
        Creates a dictionary from the matrix where the key is a tuple of coordinates
        and the value is the letter at that position.

        Returns:
        bool
            False if the matrix is loaded successfully, True if there is an error.
        --------
        Dict[Tuple[int, int], str]
            A dictionary with coordinates as keys and letters as values.
        """
        self.dtn_matrix = dict()
        for row_index, row in enumerate(self.lls_matrix):
            for col_index, elem in enumerate(row):
                self.dtn_matrix[(row_index, col_index)] = elem
        logging.info(f"Dict: {self.dtn_matrix}")
        return False

    def print_matrix(self) -> None:
        """
        Prints the matrix size, its elements, and coordinates with a spacing of three characters per element.
        """
        logging.info(f"Matrix size: {self.n_num_rows} rows x {self.n_num_cols} columns")
        
        # Print column indices
        header = "  " + " ".join(f"{i:3}" for i in range(self.n_num_cols))
        logging.info(header)
        print(header)
        
        # Print rows with row indices
        for i, row in enumerate(self.lls_matrix):
            row_string = f"{i:3} " + " ".join(f"{elem:3}" for elem in row)
            logging.info(row_string)
            print(row_string)

    def seek_letter_from_matrix(self, s_char: str) -> List[Tuple[int, int]]:
        """
        Search for all occurrences of a character within the matrix.

        Parameters:
        -----------
        s_char : str
            The character to search for in the matrix.

        Returns:
        --------
        List[Tuple[int, int]]
            A list of tuples where each tuple contains the row and column indices of an occurrence of the character.
        """
        ltn_result = list()
        if len(s_char) != 1:
            return ltn_result

        for row_index, row in enumerate(self.lls_matrix):
            for col_index, elem in enumerate(row):
                if elem == s_char:
                    ltn_result.append((row_index, col_index))
        logging.debug(f"Seek {s_char} {len(ltn_result)} | {ltn_result}")
        return ltn_result
    
    
    def seek_letter(self, s_char: str) -> List[Tuple[int, int]]:
        """
        Search for all occurrences of a character within the matrix using the dictionary.

        Parameters:
        -----------
        s_char : str
            The character to search for in the matrix.

        Returns:
        --------
        List[Tuple[int, int]]
            A list of tuples where each tuple contains the row and column indices of an occurrence of the character.
        """
        ltn_result = [tn_coordinate for tn_coordinate, s_letter in self.dtn_matrix.items() if s_letter == s_char]
        logging.debug(f"Seek {s_char} {len(ltn_result)} | {ltn_result}")
        return ltn_result

    def find_neighbour( self, iltn_first : List[Tuple[int, int]], iltn_second : List[Tuple[int, int]] ) -> List[Tuple[int, int, int, int]]:
        """
        given two lists of coordinates, find all the instances where one coordinate from the first list is 1 distance from one coordinate in the second 
        generate a list of touple with the X,Y coordinate of the first letter
        followed by the X increment and Y increment where the second letter is located
        this way following the increment you can match the rest of the word
        """
        ltn_result = list()
        for tn_first, tn_second in itertools.product(iltn_first, iltn_second):
            # Check if the distance between the two is 1 in any direction
            if abs(tn_first[0] - tn_second[0]) <= 1 and abs(tn_first[1] - tn_second[1]) <= 1:
                x_increment = tn_second[0] - tn_first[0]
                y_increment = tn_second[1] - tn_first[1]
                ltn_result.append((tn_first[0], tn_first[1], x_increment, y_increment))
        logging.debug(f"Neighbour: {len(ltn_result)} | {ltn_result}")
        return ltn_result

    def match_sequence( self, itn_origin_direction : Tuple[int,int,int,int], s_sequence : str ) -> bool:
        """
        From an origin and a direction, try to match a whole sequence. First two characters already match.
        """

        if (len(s_sequence) == 2):
            return True #already a match
        elif (len(s_sequence) < 1):
            raise False #algorithm error
        
        n_x = itn_origin_direction[0]
        n_y = itn_origin_direction[1]
        n_delta_x = itn_origin_direction[2]
        n_delta_y = itn_origin_direction[3]
        
        for n_cnt in range( 2, len(s_sequence) ):
            if (0 <= (n_x +n_delta_x*n_cnt) < self.n_num_cols) and (0 <= (n_y +n_delta_y*n_cnt) < self.n_num_rows):
                if (self.lls_matrix[n_x +n_delta_x*n_cnt][n_y+n_delta_y*n_cnt] != s_sequence[n_cnt]):
                    return False #do not match because letters are different
            else:
                return False #do not match because it overflows

        #logging.debug(f"match: {itn_origin_direction}")

        return True #match

    def seek_sequence( self, s_sequence : str ) -> List[Tuple[int,int,int,int]]:
        """
        Search for all the occurrences of a sequence within the matrix in eight directions
        """
        
        #find where the first letter appears
        ltn_first_char = self.seek_letter( s_sequence[0] )
        #find where the second letter appears
        ltn_second_char = self.seek_letter( s_sequence[1] )
        #now, find all pairs of first and second letter that are within 1 distance from each other
        ltn_neighbour = self.find_neighbour( ltn_first_char, ltn_second_char )
        #now I have a starting coordinate where at least two letters match, and a scan direction. I now match the whole sequence

        ltn_result = list()
        n_match = 0

        for tn_neighbour in ltn_neighbour:
            if self.match_sequence( tn_neighbour, s_sequence):
                n_match += 1
                ltn_result.append( tn_neighbour )

        logging.debug(f"Neighbour: {len(ltn_result)} | {ltn_result}")

        return ltn_result

def day_4_part_1( s_filename: str ):
    cl_matrix = Matrix()
    cl_matrix.load_matrix(s_filename)
    cl_matrix.print_matrix()
    ltn_result = cl_matrix.seek_sequence("XMAS")
    print(f"Matches: {len(ltn_result)}")
    import logging

#--------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#--------------------------------------------------------------------------------------------------------------------------------

# Example usage
gs_filename_example = 'day04\day_4_example.txt'
gs_filename = 'day04\day_4.txt'
#   if interpreter has the intent of executing this file
if __name__ == "__main__":
    logging.basicConfig(
        filename='day04\day_4.log',
        # Specify the log file name
        level=logging.DEBUG,
        # Set the level of debug to show
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin") 

    day_4_part_1( gs_filename_example )
    day_4_part_1( gs_filename )



