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
                    
        logging.info(f"Found {len(lltnn_solution)} solutions")
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
        the trailhead score is the number of unique pars
        of LOW coordinates that connect with HIGH coordinates
        The number I add to the dictionary is jusst the number of dfferent ways you
        can get from LOW to HIGH
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
    #cl_trail.load_map_from_file( "day10\day_10_map_critical.txt" )
    #cl_trail.load_map_from_file( "day10\day_10_example_small.txt" )
    #cl_trail.load_map_from_file( "day10\day_10_example_medium.txt" )
    cl_trail.load_map_from_file( "day10\day_10_map.txt" )
    cl_trail.find_trails()
    cl_trail.compute_trailhead_score()