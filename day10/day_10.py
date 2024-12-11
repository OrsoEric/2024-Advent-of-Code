#------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#------------------------------------------------------------------------------------------------------------------------------

import logging

from typing import List, Tuple

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

class Map_altitude:
    #lowest and highest altitudes in the map
    cn_altitude_low = 0
    cn_altitude_high = 9
    def __init__(self):
        """
        Initialize the Patrol_route class
        """
        self.gn_width = -1
        self.gn_height = -1
        self.glln_map_altitude : List[List[Tuple[int,int]]] = list()

    def load_map_from_file(self, is_filename: str) -> bool:
        """
        From file, load a map of altitudes

        Parameters:
        is_filename (str): The filename of the map to be loaded

        Returns:
        bool: True if fail
        """
        try:
            with open(is_filename, 'r') as cl_file:
                ls_lines = cl_file.readlines()
                self.gn_height = len(ls_lines)
                self.gn_width = len(ls_lines[0].strip())
                logging.debug(f"Size H Y {self.gn_height} W X {self.gn_width}")
                #allocate map
                self.glln_map_altitude = [[-1 for _ in range(self.gn_width)] for _ in range(self.gn_height)]
                #fill map
                for n_y, s_line in enumerate(ls_lines):
                    for n_x, s_char in enumerate(s_line.strip()):
                        n_altitude = int(s_char)
                        b_fail = self.set_altitude( (n_y, n_x), n_altitude )
                        if b_fail:
                            logging.error(f"ERROR: failed to set altitude C:{(n_y, n_x)} Z:{n_altitude}")
        except Exception as e:
            logging.error(f"Failed to load map: {e}")
            return True #fail
        #self.show_map(gs_filename_output)
        return False #OK

    def is_invalid( self, itnn_coordinate : Tuple[int, int] )-> bool:
        """
        given a coordinate, find if it's valid or invalid
        """
        (n_y, n_x) = (itnn_coordinate[0], itnn_coordinate[1])
        if n_x < 0:
            return True #invalid
        if n_y < 0:
            return True #invalid
        if n_x >= self.gn_width:
            return True #invalid
        if n_y >= self.gn_height:
            return True #invalid
        return False #valid

    def set_altitude( self, itnn_coordinate : Tuple[int, int], in_z : int ) -> bool :
        """
        set a coordinate to an height
        """
        #if OOB
        if self.is_invalid(itnn_coordinate):
            return True #FAIL
        (n_y, n_x) = (itnn_coordinate[0], itnn_coordinate[1])
        self.glln_map_altitude[n_y][n_x] = in_z
        return False #ok
    
    def get_altitude( self, itnn_coordinate : Tuple[int, int] ) -> Tuple[bool, int]:
        """
        set a coordinate to an height
        """
        #if OOB
        if self.is_invalid(itnn_coordinate):
            return True, self.cn_altitude_low-1
        (n_y, n_x) = (itnn_coordinate[0], itnn_coordinate[1])
        n_z = self.glln_map_altitude[n_y][n_x]
        return False, n_z #ok, altitude
    
    def get_size(self):
        """
        return size of the map
        """
        return (self.gn_width, self.gn_height)

    def get_map_string( self, illtnn_altitude : List[List[Tuple[int,int]]] ) -> Tuple[int, List[str]]:
        """
        generate a string detailing a map
        """
        s_map = f"Width: {self.gn_width} | Height: {self.gn_height}\n"
        for n_y in range (self.gn_height):
            for n_x in range (self.gn_width):
                s_map += f"{illtnn_altitude[n_y][n_x]:3}"
            s_map += "\n"
        return False, s_map #OK

    def find_origin(self) -> List[Tuple[int,int]]:
        """
        Given a map, find all the 0 and return them as list of coordinates
        """

        ltnn_origin : List[Tuple[int,int]] = list()

        for n_y in range(self.gn_height):
            for n_x in range(self.gn_width):
                b_fail, tnn_altitude = self.get_altitude( (n_y, n_x) )
                if b_fail:
                    logging.error(f"ERROR: OOB {(n_y, n_x)}")
                    return True, list()
                if (tnn_altitude == self.cn_altitude_low):
                    ltnn_origin.append((n_y, n_x))

        logging.debug(f"Num Origins: {len(ltnn_origin)}")
        logging.debug(f"Origins: {ltnn_origin}")
        return False, ltnn_origin

    def find_four_connect(self, itnn_start : Tuple[int,int] ) -> List[Tuple[int,int]]:
        """
        given a coordinate, find an altitude that is higher by one in the four connect squares around it and return those coordinates
        """
        #get the current altitude
        b_fail, n_altitude = self.get_altitude( itnn_start )
        if b_fail:
            logging.error(f"ERROR: start is OOB {itnn_start}")
            return True, list(), -1
        #if altitude is invalid
        if ((n_altitude < self.cn_altitude_low) or (n_altitude > self.cn_altitude_high)):
            logging.error(f"ERROR: altitude is invalid {n_altitude}")
            return True, list(), -1
        
        ltnn_four_connect : List[Tuple[int,int]] = list()
        
        #generate FOUR CONNECT test positions, PLUS pattern
        (n_y, n_x) = (itnn_start[0], itnn_start[1])
        ltnn_test = list()
        for n_delta_y in [-1, +1]:
            ltnn_test.append( (n_y+n_delta_y, n_x) )
        for n_delta_x in [-1, +1]:
            ltnn_test.append( (n_y, n_x+n_delta_x) )

        #scan the four connect
        for tnn_test in ltnn_test:
            b_fail, n_test_altitude = self.get_altitude( tnn_test )
            logging.debug(f"Test position {tnn_test} Z {n_test_altitude}")
            #if coordinate is OOB
            if b_fail:
                pass
            elif n_test_altitude != n_altitude +1:
                pass
            else:
                logging.debug(f"C {itnn_start} Z {n_altitude} found C {tnn_test} Z {n_test_altitude}")
                ltnn_four_connect.append(tnn_test)

        return False, ltnn_four_connect, n_altitude +1

    def find_trail( self, itnn_start : Tuple[int, int] ) -> List[List[Tuple[int,int]]]:
        """
        given an origin, find a list of all trails that lead from LOW to HIGH altitude
        -build a temp solution vector with origin
        -for ALL temp solutions
            -read the altitude of the last coordinate
            -increase altitude
            -look at four connect of that altitude
            -create one new partial solution with partial solution followed by the coordinate of the new altitude
            -if HIGH, create a complete solution instead
            -delete the partial solution
        """
        logging.info(f"Find all trails starting from C{itnn_start}")
        #list of solutions
        lltnn_solution : List[List[Tuple[int,int]]] = list()
        #list of partial solutions
        lltnn_partial_solution : List[List[Tuple[int,int]]] = list()
        #create first partial solution with START
        ltnn_partial_solution = [itnn_start]
        #add the START to the list of partial solution
        lltnn_partial_solution.append( ltnn_partial_solution )
        
        #while I have partial solutions
        while len(lltnn_partial_solution) > 0:
            logging.debug(f"There are {len(lltnn_partial_solution)} partial solutions")
            #create a list of new partial solutions        
            lltnn_partial_solution_new : List[List[Tuple[int,int]]] = list()
            #scan all the partial solutions
            for ltnn_partial_solution in lltnn_partial_solution:
                logging.debug(f"processing Partial Solution {ltnn_partial_solution}")
                #get the last coordinate of the partial solution
                tnn_end = ltnn_partial_solution[-1]
                #find all four connect points that increase in height by 1
                b_fail, ltnn_four_connect, n_altitude_new = self.find_four_connect( tnn_end )
                if b_fail:
                    logging.error("ERROR: FOUR CONNECT FAIL")
                    return True, list() #FAIL
                logging.debug(f"There are {len(ltnn_four_connect)} NEW partial solutions of Z {n_altitude_new}")
                #for each continuation of the solution, create a new partial solution
                for tnn_new in ltnn_four_connect:
                    logging.debug(f"add coordinate {tnn_new} Z {n_altitude_new}")
                    #create a new partial solution
                    ltnn_partial_solution_new = copy.deepcopy( ltnn_partial_solution )
                    ltnn_partial_solution_new.append( tnn_new )
                    logging.debug(f"new partial solution: {ltnn_partial_solution_new}")
                    #if the new solution ends on maximum altitude
                    if n_altitude_new == self.cn_altitude_high:
                        #I actually have a SOLUTION
                        lltnn_solution.append(ltnn_partial_solution_new)
                    else:
                        #I have a new partial solution
                        lltnn_partial_solution_new.append(ltnn_partial_solution_new)
                #get rid of the current partial solutions, they outlived their usefullness
                del lltnn_partial_solution
                #promote the new partial solutions to current partial solutions
                lltnn_partial_solution = lltnn_partial_solution_new 
                    
        logging.debug(f"Found {len(lltnn_solution)} solutions")
        return False, lltnn_solution #OK
    

    def find_trails(self) -> Tuple[bool, List[List[Tuple[int, int]]]]:
        """
        Given a map, it will find all the four connect path from every zero to every nine
        """

        #ask the map for all the origin points
        b_fail, ltnn_origin = self.find_origin()
        if b_fail:
            logging.error("Could not find ANY origins")
            return True, list() #FAIL
        
        #allocate solutions
        lltnn_solutions : List[List[Tuple[int, int]]] = list()
        #scan all the origins
        for tnn_origin in ltnn_origin:
            #get the altitude
            b_fail, n_altitude = self.get_altitude( tnn_origin )
            if ((b_fail == True) or (n_altitude != 0)):
                logging.error(f"ERROR: altitude of origin is NOT zero! {n_altitude} ")
                return True, list() #fail
            #as long as the 
            #while (n_altitude < self.gcl_map.cn_altitude_high):
            #self.gcl_map.find_four_connect((0,0))
            b_fail, lltnn_solutions_new = self.find_trail(tnn_origin)
            if b_fail:
                logging.error("ERROR: find trail failed...")
                return True, list() #fail
            #append the new solutions
            for ltnn_solution_new in lltnn_solutions_new:
                lltnn_solutions.append(ltnn_solution_new)

        return False, lltnn_solutions #OK

    def show_map_generic(self,illtnn_altitude : List[List[Tuple[int,int]]], ib_debug : bool = False) -> bool:
        b_fail, s_map = self.get_map_string(illtnn_altitude)
        if b_fail:
            return True #FAIL
        if ib_debug:
            logging.debug(s_map)
        else:    
            logging.info(s_map)
        return False #OK

    def show_map(self, ib_debug = False):
        return self.show_map_generic(self.glln_map_altitude, True)

    def save_map(self, output_filename: str) -> None:
        """
        Print the map to logging.debug and an output file.

        Parameters:
        output_filename (str): The filename of the output file to save the map.
        """
        logging.info(f"Width: {self.gn_width} | Height: {self.gn_height} | obstacles: {len(self.gd_obstacle)}")
        logging.info(f"Obstacles: {self.gd_obstacle}")
        self.gst_guard_position.show_position()
        try:
            with open(output_filename, 'w') as file:
                for y in range(self.gn_height):
                    line = ""
                    for x in range(self.gn_width):
                        if (x, y) in self.gd_obstacle:
                            line += '#'
                        elif (x, y) == (self.gst_guard_position.n_x, self.gst_guard_position.n_y):
                            line += '^'
                        else:
                            line += '.'
                    logging.debug(line)
                    file.write(line + '\n')
        except Exception as e:
            logging.error(f"Failed to show map: {e}")

class Trail:
    def __init__(self):
        """
        Initialize the Patrol_route class
        """
        #Map class that load and compute trails
        self.gcl_map = Map_altitude()
        #list of all trails from all LOW to all HIGH
        self.glltnn_trails : List[List[Tuple[int,int]]] = list()

    def load_map_from_file(self, is_filename: str) -> bool:
        """

        Parameters:
        is_filename (str): The filename of the map to be loaded

        Returns:
        bool: True if fail
        """
        b_fail = self.gcl_map.load_map_from_file( is_filename )
        if b_fail:
            logging.error(f"ERROR: failed to load map {is_filename}")
            return True #fail
        b_fail = self.gcl_map.show_map()
        if b_fail:
            logging.error(f"ERROR: failed to show map {is_filename}")
            return True #fail
        return False #OK
    
    def compute_trailhead_score(self):
        """

        Given a LOW
            the trailhead score
            measure how many unique different HIGH you reach from that LOW
            
        Measure the total trailhead score of all LOWs

        create a dictionary with two coordinates, start and stop
        Works on small example
        [2024-12-11 17:35:14,659] INFO day_10:364 > Num of Trailheads: 1 
        [2024-12-11 17:35:14,659] INFO day_10:365 > Trailheads: {((0, 0), (3, 0)): 15} 
        Works on medium example
        [2024-12-11 17:36:03,288] INFO day_10:368 > Num of Trailheads: 36 
        [2024-12-11 17:36:03,288] INFO day_10:369 > Trailheads: {((0, 2), (3, 4)): 3, ((0, 2), (5, 4)): 3, ((0, 2), (4, 5)): 3, ((0, 2), (0, 1)): 3, ((0, 2), (3, 0)): 3, ((0, 4), (3, 4)): 4, ((0, 4), (5, 4)): 3, ((0, 4), (4, 5)): 4, ((0, 4), (0, 1)): 3, ((0, 4), (3, 0)): 3, ((0, 4), (2, 5)): 1, ((2, 4), (3, 4)): 1, ((2, 4), (5, 4)): 1, ((2, 4), (4, 5)): 1, ((2, 4), (0, 1)): 1, ((2, 4), (3, 0)): 1, ((4, 6), (2, 5)): 1, ((4, 6), (4, 5)): 0, ((4, 6), (3, 4)): 0, ((5, 2), (6, 4)): 0, ((5, 5), (2, 5)): 1, ((5, 5), (4, 5)): 0, ((5, 5), (3, 4)): 0, ((6, 0), (0, 1)): 0, ((6, 0), (3, 0)): 0, ((6, 0), (3, 4)): 0, ((6, 0), (5, 4)): 0, ((6, 0), (4, 5)): 0, ((6, 6), (2, 5)): 3, ((6, 6), (4, 5)): 1, ((6, 6), (3, 4)): 1, ((7, 1), (0, 1)): 0, ((7, 1), (3, 0)): 0, ((7, 1), (3, 4)): 0, ((7, 1), (5, 4)): 0, ((7, 1), (4, 5)): 0} 
        turn off debug
        FULL example
        [2024-12-11 17:37:28,236] INFO day_10:372 > Num of Trailheads: 659 
        [2024-12-11 17:37:28,236] INFO day_10:373 > Trailheads: {((0, 2), (1, 2)): 0, ((0, 2), (1, 4)): 1, ((0, 17), (1, 15)): 0, ((0, 21), (4, 24)): 0, ((0, 21), (3, 23)): 0, ((0, 26), (2, 25)): 1, ((0, 26), (4, 27)): 0, ((0, 28), (2, 25)): 5, ((0, 28), (4, 27)): 2, ((0, 35), (1, 33)): 0, ((0, 45), (2, 42)): 0, ((0, 52), (6, 53)): 0, ((0, 52), (1, 48)): 0, ((0, 52), (3, 48)): 0, ((1, 14), (0, 12)): 0, ((1, 14), (1, 15)): 0, ((1, 38), (3, 37)): 2, ((1, 38), (4, 38)): 2, ((2, 6), (2, 9)): 4, ((2, 19), (1, 15)): 0, ((2, 19), (3, 23)): 7, ((2, 19), (4, 22)): 5, ((2, 19), (4, 24)): 13, ((2, 21), (3, 23)): 3, ((2, 21), (4, 22)): 2, ((2, 21), (4, 24)): 6, ((2, 31), (7, 29)): 5, ((2, 31), (5, 33)): 0, ((2, 35), (1, 33)): 0, ((2, 44), (5, 42)): 0, ((2, 44), (1, 46)): 5, ((2, 44), (1, 48)): 5, ((2, 44), (3, 48)): 2, ((2, 52), (6, 53)): 0, ((3, 10), (4, 6)): 2, ((3, 10), (4, 8)): 2, ((3, 14), (0, 12)): 0, ((3, 14), (1, 15)): 0, ((3, 15), (3, 12)): 0, ((3, 30), (7, 29)): 5, ((3, 30), (5, 33)): 0, ((3, 35), (5, 36)): 0, ((3, 35), (5, 38)): 1, ((3, 35), (7, 38)): 0, ((3, 38), (3, 37)): 0, ((3, 38), (4, 38)): 0, ((3, 49), (1, 48)): 0, ((3, 49), (3, 48)): 1, ((3, 49), (4, 47)): 0, ((4, 0), (1, 2)): 0, ((4, 0), (1, 4)): 1, ((4, 17), (1, 15)): 1, ((4, 17), (6, 20)): 0, ((4, 17), (3, 23)): 0, ((4, 17), (4, 22)): 0, ((4, 17), (4, 24)): 1, ((4, 19), (1, 15)): 1, ((4, 19), (3, 23)): 4, ((4, 19), (4, 22)): 3, ((4, 19), (4, 24)): 8, ((4, 19), (6, 20)): 0, ((4, 40), (1, 42)): 1, ((5, 3), (9, 2)): 0, ((5, 12), (4, 6)): 2, ((5, 12), (4, 8)): 2, ((5, 12), (6, 14)): 0, ((5, 32), (5, 33)): 0, ((5, 32), (7, 29)): 2, ((5, 35), (5, 36)): 0, ((5, 35), (5, 38)): 1, ((5, 35), (7, 38)): 0, ((5, 47), (1, 46)): 1, ((5, 47), (1, 48)): 1, ((5, 47), (3, 48)): 0, ((5, 47), (5, 42)): 0, ((6, 3), (4, 6)): 2, ((6, 16), (7, 12)): 0, ((6, 16), (7, 14)): 0, ((6, 24), (4, 27)): 1, ((6, 33), (8, 32)): 0, ((6, 33), (12, 34)): 1, ((6, 33), (12, 36)): 3, ((6, 33), (10, 36)): 1, ((6, 50), (3, 48)): 0, ((6, 50), (4, 47)): 0, ((7, 6), (10, 6)): 4, ((7, 6), (4, 6)): 0, ((7, 6), (4, 8)): 0, ((7, 7), (11, 6)): 0, ((7, 7), (12, 11)): 9, ((7, 7), (11, 12)): 7, ((7, 7), (7, 12)): 1, ((7, 7), (7, 14)): 1, ((7, 30), (10, 30)): 0, ((7, 30), (8, 32)): 0, ((7, 34), (8, 32)): 1, ((7, 34), (12, 34)): 3, ((7, 34), (12, 36)): 7, ((7, 34), (10, 36)): 3, ((7, 45), (1, 46)): 1, ((7, 45), (1, 48)): 1, ((7, 45), (3, 48)): 0, ((7, 45), (5, 42)): 5, ((7, 48), (11, 47)): 1, ((8, 7), (10, 6)): 2, ((8, 23), (6, 20)): 1, ((8, 23), (3, 23)): 0, ((8, 23), (4, 22)): 0, ((8, 23), (4, 24)): 1, ((8, 41), (4, 38)): 2, ((8, 41), (8, 40)): 2, ((8, 43), (4, 38)): 2, ((8, 43), (8, 40)): 2, ((9, 9), (12, 11)): 9, ((9, 9), (11, 12)): 7, ((9, 9), (7, 12)): 1, ((9, 9), (7, 14)): 1, ((9, 9), (11, 6)): 0, ((9, 19), (7, 12)): 0, ((9, 19), (7, 14)): 0, ((9, 19), (10, 21)): 0, ((9, 29), (14, 27)): 0, ((9, 29), (11, 30)): 0, ((9, 41), (11, 42)): 1, ((9, 52), (10, 50)): 0, ((10, 14), (7, 12)): 1, ((10, 14), (7, 14)): 1, ((10, 14), (12, 11)): 5, ((10, 14), (11, 12)): 5, ((10, 19), (9, 17)): 1, ((10, 22), (10, 21)): 0, ((10, 27), (10, 30)): 0, ((10, 27), (8, 32)): 0, ((10, 38), (5, 36)): 1, ((10, 38), (5, 38)): 3, ((10, 38), (7, 38)): 2, ((10, 44), (12, 45)): 0, ((10, 44), (11, 42)): 1, ((10, 53), (10, 50)): 0, ((11, 14), (9, 17)): 0, ((11, 27), (14, 27)): 0, ((11, 27), (11, 30)): 0, ((11, 43), (12, 45)): 0, ((11, 43), (11, 42)): 1, ((11, 48), (11, 47)): 0, ((11, 48), (10, 50)): 0, ((12, 3), (15, 3)): 1, ((12, 3), (8, 2)): 0, ((12, 3), (15, 1)): 0, ((12, 6), (11, 6)): 1, ((12, 17), (13, 21)): 0, ((12, 18), (13, 22)): 0, ((12, 25), (8, 24)): 1, ((12, 25), (10, 24)): 0, ((12, 48), (12, 51)): 1, ((12, 48), (13, 50)): 1, ((12, 50), (12, 51)): 0, ((12, 50), (13, 50)): 0, ((12, 50), (15, 52)): 0, ((13, 0), (8, 2)): 3, ((13, 0), (15, 1)): 0, ((13, 0), (15, 3)): 0, ((13, 33), (11, 30)): 2, ((13, 38), (15, 39)): 1, ((13, 38), (15, 41)): 0, ((13, 53), (12, 51)): 0, ((13, 53), (13, 50)): 0, ((13, 53), (15, 52)): 0, ((14, 3), (15, 3)): 0, ((14, 14), (14, 13)): 0, ((14, 14), (15, 18)): 0, ((14, 16), (14, 13)): 0, ((14, 16), (15, 18)): 0, ((14, 23), (8, 24)): 1, ((14, 23), (10, 24)): 0, ((14, 35), (10, 36)): 1, ((14, 35), (12, 36)): 3, ((14, 35), (12, 34)): 1, ((15, 8), (14, 10)): 1, ((15, 8), (15, 9)): 1, ((15, 12), (14, 10)): 0, ((15, 12), (15, 9)): 0, ((15, 12), (17, 15)): 0, ((15, 21), (13, 22)): 0, ((15, 21), (18, 23)): 0, ((15, 30), (19, 29)): 0, ((15, 30), (13, 27)): 0, ((15, 30), (16, 24)): 0, ((15, 32), (17, 35)): 1, ((16, 1), (15, 1)): 0, ((16, 1), (15, 3)): 0, ((16, 2), (18, 1)): 1, ((16, 2), (21, 2)): 0, ((16, 2), (19, 4)): 0, ((16, 9), (14, 10)): 1, ((16, 9), (15, 9)): 1, ((16, 19), (18, 20)): 1, ((16, 22), (18, 23)): 0, ((16, 22), (13, 22)): 0, ((16, 30), (13, 30)): 0, ((16, 35), (10, 36)): 3, ((16, 35), (12, 36)): 7, ((16, 35), (12, 34)): 3, ((16, 37), (10, 36)): 1, ((16, 37), (12, 36)): 3, ((16, 37), (12, 34)): 1, ((16, 41), (15, 39)): 0, ((16, 46), (12, 45)): 1, ((16, 46), (15, 48)): 1, ((16, 47), (20, 48)): 0, ((16, 47), (20, 50)): 0, ((16, 48), (12, 51)): 5, ((16, 48), (13, 50)): 5, ((16, 52), (17, 50)): 3, ((17, 5), (18, 1)): 0, ((17, 5), (21, 2)): 0, ((17, 5), (19, 4)): 0, ((17, 5), (16, 5)): 0, ((17, 5), (16, 7)): 0, ((17, 7), (20, 11)): 0, ((17, 7), (16, 5)): 0, ((17, 7), (16, 7)): 0, ((17, 38), (24, 40)): 1, ((17, 38), (22, 40)): 0, ((17, 38), (22, 42)): 0, ((17, 38), (17, 35)): 0, ((17, 41), (11, 42)): 0, ((17, 41), (15, 42)): 0, ((17, 41), (12, 45)): 2, ((17, 41), (15, 48)): 2, ((18, 10), (20, 11)): 0, ((18, 10), (16, 5)): 0, ((18, 10), (16, 7)): 0, ((18, 32), (22, 33)): 9, ((18, 32), (20, 37)): 1, ((18, 32), (19, 32)): 1, ((18, 39), (24, 40)): 5, ((18, 39), (22, 40)): 2, ((18, 39), (22, 42)): 2, ((18, 39), (17, 35)): 1, ((18, 39), (15, 39)): 0, ((19, 9), (20, 11)): 0, ((19, 9), (16, 5)): 0, ((19, 9), (16, 7)): 0, ((19, 24), (13, 27)): 5, ((19, 24), (16, 24)): 5, ((19, 24), (19, 29)): 7, ((19, 26), (22, 26)): 1, ((19, 26), (23, 25)): 1, ((19, 26), (20, 30)): 0, ((19, 26), (13, 27)): 2, ((19, 26), (16, 24)): 2, ((19, 26), (19, 29)): 3, ((19, 46), (19, 43)): 1, ((19, 46), (22, 42)): 1, ((20, 15), (18, 20)): 1, ((20, 15), (22, 18)): 0, ((20, 24), (26, 23)): 3, ((20, 24), (25, 24)): 5, ((20, 24), (23, 24)): 3, ((20, 27), (22, 26)): 1, ((20, 27), (23, 25)): 1, ((20, 27), (20, 30)): 0, ((21, 12), (20, 10)): 0, ((21, 12), (26, 10)): 0, ((21, 20), (18, 20)): 0, ((21, 20), (20, 20)): 0, ((21, 20), (25, 21)): 0, ((21, 23), (26, 23)): 3, ((21, 23), (25, 24)): 5, ((21, 23), (23, 24)): 3, ((21, 50), (20, 50)): 0, ((21, 50), (26, 52)): 0, ((21, 50), (20, 48)): 0, ((22, 1), (27, 1)): 2, ((22, 1), (27, 5)): 0, ((22, 25), (22, 26)): 1, ((22, 25), (23, 25)): 1, ((22, 25), (20, 30)): 0, ((22, 32), (19, 30)): 0, ((22, 48), (21, 46)): 0, ((22, 48), (22, 45)): 0, ((23, 0), (27, 1)): 2, ((23, 0), (27, 5)): 0, ((23, 3), (19, 4)): 1, ((23, 3), (21, 2)): 3, ((23, 8), (20, 6)): 0, ((23, 8), (22, 8)): 0, ((23, 12), (26, 10)): 0, ((23, 17), (23, 14)): 0, ((23, 31), (19, 30)): 0, ((23, 33), (22, 33)): 3, ((23, 33), (20, 37)): 3, ((23, 37), (22, 33)): 3, ((23, 37), (20, 37)): 3, ((23, 38), (24, 40)): 1, ((23, 38), (22, 40)): 0, ((23, 38), (22, 42)): 0, ((23, 43), (21, 46)): 1, ((23, 43), (22, 45)): 1, ((23, 44), (19, 43)): 1, ((23, 44), (22, 42)): 1, ((24, 3), (27, 1)): 2, ((24, 3), (27, 5)): 0, ((24, 19), (20, 20)): 0, ((24, 19), (25, 21)): 0, ((24, 27), (22, 26)): 0, ((24, 27), (23, 25)): 0, ((24, 32), (22, 33)): 3, ((24, 32), (20, 37)): 3, ((24, 49), (20, 50)): 1, ((24, 49), (26, 52)): 2, ((25, 6), (20, 6)): 1, ((25, 6), (22, 8)): 1, ((25, 13), (32, 13)): 0, ((25, 13), (25, 10)): 0, ((25, 13), (23, 14)): 0, ((25, 25), (28, 27)): 1, ((25, 28), (22, 26)): 1, ((25, 28), (23, 25)): 1, ((25, 28), (25, 31)): 1, ((25, 28), (25, 33)): 3, ((25, 28), (28, 34)): 1, ((25, 36), (25, 31)): 1, ((25, 36), (25, 33)): 3, ((25, 36), (28, 34)): 1, ((26, 6), (26, 7)): 1, ((26, 38), (25, 38)): 1, ((26, 38), (29, 34)): 0, ((26, 45), (27, 41)): 3, ((26, 45), (24, 40)): 1, ((26, 45), (24, 42)): 1, ((26, 48), (21, 46)): 2, ((26, 48), (22, 45)): 2, ((26, 48), (27, 48)): 1, ((26, 48), (29, 48)): 1, ((27, 4), (27, 5)): 1, ((27, 4), (27, 1)): 0, ((27, 4), (31, 3)): 1, ((27, 4), (31, 5)): 3, ((27, 14), (30, 16)): 1, ((27, 14), (25, 15)): 1, ((27, 17), (25, 20)): 3, ((27, 21), (26, 23)): 0, ((27, 28), (25, 31)): 2, ((27, 28), (25, 33)): 5, ((27, 28), (28, 34)): 2, ((27, 30), (25, 31)): 1, ((27, 30), (25, 33)): 3, ((27, 30), (28, 34)): 1, ((27, 37), (29, 34)): 0, ((27, 37), (25, 38)): 0, ((27, 42), (27, 41)): 3, ((27, 42), (24, 40)): 1, ((27, 42), (24, 42)): 1, ((28, 3), (27, 5)): 1, ((28, 3), (27, 1)): 0, ((28, 3), (31, 3)): 1, ((28, 3), (31, 5)): 3, ((28, 12), (25, 10)): 2, ((28, 12), (23, 14)): 2, ((28, 12), (29, 8)): 1, ((28, 12), (31, 8)): 1, ((28, 12), (32, 13)): 0, ((28, 15), (30, 16)): 0, ((28, 15), (25, 15)): 0, ((28, 50), (27, 48)): 0, ((28, 50), (29, 48)): 0, ((28, 51), (20, 50)): 0, ((28, 51), (26, 52)): 1, ((29, 0), (31, 3)): 1, ((29, 0), (31, 5)): 3, ((29, 5), (26, 7)): 1, ((29, 9), (29, 8)): 0, ((29, 9), (31, 8)): 0, ((29, 18), (35, 21)): 5, ((29, 18), (32, 16)): 11, ((29, 18), (29, 21)): 3, ((29, 22), (26, 24)): 2, ((29, 22), (30, 28)): 3, ((29, 32), (29, 31)): 3, ((29, 40), (32, 34)): 1, ((29, 40), (27, 41)): 0, ((29, 40), (29, 41)): 0, ((30, 17), (35, 21)): 2, ((30, 17), (32, 16)): 5, ((30, 17), (29, 21)): 1, ((31, 0), (35, 1)): 7, ((31, 0), (37, 1)): 7, ((31, 0), (31, 3)): 1, ((31, 0), (31, 5)): 3, ((31, 24), (35, 21)): 3, ((31, 24), (29, 21)): 3, ((31, 24), (30, 28)): 5, ((31, 24), (26, 24)): 2, ((31, 27), (32, 27)): 1, ((31, 36), (32, 34)): 1, ((31, 47), (29, 48)): 1, ((31, 48), (30, 52)): 0, ((31, 48), (33, 53)): 0, ((32, 8), (29, 8)): 1, ((32, 8), (31, 8)): 1, ((32, 8), (33, 12)): 1, ((32, 37), (32, 34)): 1, ((32, 37), (36, 38)): 2, ((32, 37), (38, 38)): 2, ((32, 37), (35, 35)): 0, ((32, 43), (27, 41)): 1, ((32, 43), (29, 41)): 1, ((32, 43), (29, 45)): 0, ((32, 53), (33, 53)): 0, ((33, 0), (35, 1)): 3, ((33, 0), (37, 1)): 3, ((33, 3), (36, 3)): 1, ((33, 24), (35, 21)): 2, ((33, 24), (29, 21)): 1, ((33, 24), (30, 28)): 1, ((33, 26), (30, 28)): 0, ((33, 31), (34, 29)): 0, ((33, 31), (35, 30)): 0, ((33, 31), (32, 27)): 0, ((33, 33), (34, 29)): 0, ((33, 33), (35, 30)): 0, ((33, 33), (32, 27)): 0, ((33, 38), (36, 38)): 7, ((33, 38), (38, 38)): 7, ((33, 38), (35, 35)): 1, ((33, 43), (32, 41)): 0, ((34, 10), (38, 7)): 2, ((34, 10), (29, 8)): 1, ((34, 10), (31, 8)): 1, ((34, 10), (33, 12)): 1, ((34, 14), (38, 13)): 2, ((34, 14), (39, 16)): 1, ((34, 14), (35, 16)): 0, ((34, 42), (32, 41)): 3, ((34, 49), (34, 48)): 0, ((34, 49), (33, 49)): 0, ((35, 13), (35, 16)): 0, ((35, 13), (38, 13)): 2, ((35, 13), (39, 16)): 1, ((35, 27), (37, 24)): 0, ((35, 27), (34, 25)): 0, ((36, 7), (31, 5)): 1, ((36, 7), (31, 7)): 0, ((36, 7), (31, 3)): 0, ((36, 16), (38, 13)): 2, ((36, 16), (39, 16)): 1, ((36, 20), (35, 16)): 1, ((36, 22), (37, 20)): 1, ((36, 22), (41, 22)): 1, ((36, 42), (32, 41)): 1, ((36, 42), (34, 43)): 1, ((36, 46), (32, 45)): 1, ((36, 46), (34, 43)): 0, ((36, 46), (40, 49)): 0, ((36, 46), (39, 44)): 1, ((36, 47), (34, 48)): 0, ((36, 47), (33, 49)): 0, ((36, 50), (40, 49)): 2, ((36, 50), (39, 44)): 4, ((37, 11), (38, 7)): 0, ((37, 27), (37, 24)): 0, ((37, 27), (34, 25)): 1, ((37, 31), (45, 30)): 0, ((37, 31), (42, 31)): 0, ((37, 41), (32, 41)): 0, ((37, 41), (34, 43)): 1, ((38, 4), (36, 3)): 0, ((38, 17), (35, 17)): 1, ((38, 17), (36, 18)): 1, ((38, 33), (35, 35)): 1, ((38, 46), (32, 45)): 1, ((38, 46), (34, 43)): 0, ((38, 46), (40, 49)): 0, ((38, 46), (39, 44)): 1, ((38, 53), (33, 53)): 1, ((38, 53), (37, 53)): 1, ((39, 0), (37, 1)): 1, ((39, 0), (40, 4)): 2, ((39, 6), (40, 6)): 0, ((39, 6), (41, 7)): 1, ((39, 20), (44, 18)): 0, ((39, 20), (35, 17)): 0, ((39, 20), (36, 18)): 0, ((39, 38), (36, 38)): 3, ((39, 38), (38, 38)): 3, ((39, 40), (36, 38)): 0, ((39, 40), (38, 38)): 0, ((39, 43), (34, 43)): 1, ((39, 43), (39, 44)): 0, ((39, 43), (41, 44)): 0, ((40, 14), (45, 14)): 0, ((40, 14), (43, 16)): 1, ((40, 14), (39, 16)): 0, ((40, 14), (38, 13)): 0, ((40, 18), (39, 16)): 1, ((40, 18), (38, 13)): 1, ((40, 25), (39, 27)): 0, ((40, 29), (39, 27)): 0, ((41, 12), (42, 10)): 1, ((41, 12), (41, 7)): 1, ((41, 18), (35, 17)): 0, ((41, 18), (36, 18)): 0, ((41, 18), (44, 18)): 0, ((41, 32), (39, 35)): 0, ((41, 33), (43, 36)): 5, ((41, 51), (41, 52)): 2, ((41, 51), (40, 53)): 2, ((42, 24), (37, 20)): 1, ((42, 24), (41, 22)): 1, ((42, 45), (40, 46)): 0, ((42, 45), (45, 43)): 0, ((42, 45), (44, 40)): 0, ((42, 48), (40, 53)): 3, ((42, 48), (41, 52)): 4, ((43, 2), (37, 1)): 3, ((43, 2), (40, 4)): 5, ((43, 2), (40, 6)): 0, ((43, 2), (41, 7)): 1, ((43, 6), (40, 6)): 1, ((43, 6), (41, 7)): 3, ((43, 11), (45, 14)): 0, ((43, 11), (43, 16)): 1, ((43, 17), (39, 16)): 1, ((43, 17), (38, 13)): 1, ((43, 27), (42, 29)): 1, ((43, 38), (45, 43)): 0, ((43, 38), (44, 40)): 0, ((43, 42), (45, 43)): 0, ((43, 42), (44, 40)): 0, ((43, 42), (40, 46)): 0, ((44, 8), (49, 8)): 2, ((44, 8), (48, 7)): 2, ((44, 11), (42, 10)): 0, ((44, 45), (40, 46)): 0, ((44, 45), (45, 43)): 1, ((44, 51), (48, 52)): 3, ((44, 51), (46, 52)): 1, ((45, 1), (42, 3)): 0, ((45, 20), (44, 18)): 1, ((45, 20), (43, 21)): 1, ((45, 22), (43, 21)): 0, ((45, 29), (45, 30)): 1, ((45, 29), (42, 31)): 0, ((45, 34), (45, 35)): 0, ((46, 4), (49, 8)): 4, ((46, 4), (48, 7)): 4, ((46, 5), (51, 3)): 1, ((46, 5), (50, 6)): 1, ((46, 5), (51, 7)): 1, ((46, 12), (51, 10)): 1, ((46, 12), (51, 12)): 0, ((46, 12), (49, 10)): 0, ((46, 14), (51, 10)): 1, ((46, 14), (51, 12)): 0, ((46, 14), (49, 10)): 0, ((46, 14), (43, 16)): 1, ((46, 16), (47, 14)): 1, ((46, 16), (43, 16)): 1, ((46, 26), (49, 28)): 1, ((46, 26), (49, 30)): 0, ((46, 26), (45, 30)): 1, ((46, 26), (42, 31)): 0, ((46, 37), (47, 39)): 5, ((46, 37), (44, 40)): 1, ((46, 46), (44, 49)): 0, ((47, 0), (49, 3)): 1, ((47, 0), (46, 2)): 0, ((47, 4), (51, 3)): 1, ((47, 4), (50, 6)): 1, ((47, 4), (51, 7)): 1, ((47, 6), (51, 3)): 4, ((47, 6), (50, 6)): 4, ((47, 6), (51, 7)): 4, ((47, 15), (43, 16)): 1, ((47, 15), (47, 14)): 1, ((47, 17), (47, 14)): 3, ((47, 23), (45, 26)): 1, ((47, 23), (50, 23)): 0, ((47, 25), (50, 23)): 1, ((47, 25), (49, 28)): 3, ((47, 25), (49, 30)): 1, ((47, 25), (45, 26)): 1, ((47, 36), (47, 39)): 4, ((47, 36), (44, 40)): 0, ((48, 12), (51, 10)): 1, ((48, 12), (51, 12)): 0, ((48, 12), (49, 10)): 0, ((48, 21), (46, 20)): 2, ((48, 21), (48, 20)): 1, ((48, 21), (51, 19)): 0, ((48, 34), (45, 30)): 1, ((48, 34), (45, 32)): 3, ((48, 34), (49, 28)): 3, ((48, 34), (49, 30)): 1, ((48, 34), (50, 33)): 0, ((48, 34), (51, 36)): 0, ((48, 43), (45, 43)): 0, ((48, 43), (47, 39)): 2, ((48, 43), (44, 40)): 0, ((49, 9), (49, 8)): 1, ((49, 9), (48, 7)): 1, ((49, 9), (51, 10)): 1, ((49, 9), (51, 12)): 0, ((49, 9), (49, 10)): 0, ((49, 20), (46, 20)): 2, ((49, 20), (48, 20)): 1, ((49, 20), (51, 19)): 0, ((49, 33), (45, 30)): 0, ((49, 33), (45, 32)): 1, ((49, 33), (49, 28)): 1, ((49, 33), (49, 30)): 0, ((49, 50), (48, 52)): 4, ((49, 50), (46, 52)): 1, ((49, 50), (53, 47)): 0, ((49, 50), (49, 53)): 2, ((50, 7), (51, 3)): 0, ((50, 7), (50, 6)): 0, ((50, 7), (51, 7)): 0, ((50, 13), (52, 14)): 0, ((50, 25), (50, 26)): 1, ((50, 28), (49, 30)): 5, ((50, 28), (53, 30)): 2, ((50, 42), (49, 40)): 1, ((50, 42), (50, 45)): 2, ((50, 42), (51, 36)): 0, ((50, 49), (48, 52)): 2, ((50, 49), (46, 52)): 0, ((50, 49), (53, 47)): 0, ((50, 49), (49, 53)): 2, ((51, 2), (49, 3)): 1, ((51, 2), (46, 2)): 0, ((51, 22), (46, 20)): 3, ((51, 22), (48, 20)): 2, ((51, 22), (51, 19)): 1, ((51, 45), (49, 40)): 0, ((51, 45), (50, 45)): 2, ((51, 46), (48, 48)): 3, ((51, 46), (53, 47)): 0, ((52, 3), (50, 0)): 1, ((52, 3), (50, 6)): 0, ((52, 3), (51, 7)): 0, ((52, 5), (50, 0)): 1, ((52, 5), (50, 6)): 0, ((52, 5), (51, 7)): 0, ((52, 13), (52, 14)): 0, ((52, 17), (52, 14)): 0, ((52, 17), (51, 19)): 1, ((52, 23), (50, 26)): 3, ((52, 40), (49, 40)): 1, ((52, 40), (51, 36)): 2, ((52, 40), (50, 45)): 2, ((52, 53), (48, 52)): 0, ((52, 53), (49, 53)): 2, ((53, 9), (51, 12)): 1, ((53, 29), (49, 30)): 5, ((53, 29), (53, 30)): 2, ((53, 35), (51, 36)): 0} 
        I looked at 02 to 12 and 02 to 14 and they are correct
        """
        #create a dictionary of trailheads 
        dst_trailhead = dict()
        #for all trails
        for ltnn_trail in self.glltnn_trails:
            #get the start and end coordnate
            st_trail = (ltnn_trail[0], ltnn_trail[-1])
            #
            if st_trail not in dst_trailhead:
                dst_trailhead[st_trail] = 1
            else:
                dst_trailhead[st_trail] += 1

        logging.info(f"Num of Trailheads: {len(dst_trailhead)}")
        logging.info(f"Trailheads: {dst_trailhead}")

        return False #OK

    def find_trails(self):
        b_fail, lltnn_trails = self.gcl_map.find_trails()
        if (b_fail):
            logging.error("ERROR: could not find trails")
        self.glltnn_trails = lltnn_trails
        logging.info(f"Trails found: {len(self.glltnn_trails)}")
        logging.info(f"{self.glltnn_trails}")
        return False #ok

#------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(
        filename="day10/day_10.log",
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin")

    cl_trail = Trail()
    #cl_trail.load_map_from_file( "day10\day_10_example_small.txt" )
    #cl_trail.load_map_from_file( "day10\day_10_example_medium.txt" )
    #cl_trail.load_map_from_file( "day10\day_10_map_critical.txt" )
    cl_trail.load_map_from_file( "day10\day_10_map.txt" )
    cl_trail.find_trails()
    cl_trail.compute_trailhead_score()