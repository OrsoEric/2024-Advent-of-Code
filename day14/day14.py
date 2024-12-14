#------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#------------------------------------------------------------------------------------------------------------------------------

import numpy

import logging

from typing import Set, Dict, List, Tuple

#import copy

#enumeration support
from enum import Enum, auto

#------------------------------------------------------------------------------------------------------------------------------
#   RULES
#------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------
#   ALGORITHM
#------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------
#   SOLUTION
#------------------------------------------------------------------------------------------------------------------------------

class Robot_security:
    """
    Stores all the robot data and simulates robots.
    """

    class E_ROBOT( Enum ):
        PX = 0
        PY = auto()
        VX = auto()
        VY = auto()
        COLUMNS = auto()

    def __init__(self):
        self.gn_height : int = 0
        self.gn_width : int = 0
        self.gn_height_center : int = 0
        self.gn_width_center : int = 0
        self.gm_robot_data : numpy.array = numpy.array((0,0))

    def load_from_file(self, is_filename: str) -> bool:
        """
        Loads from file:
        - the room size
        - the robot positions and speeds
        """
        try:
            with open(is_filename, 'r') as file:
                ls_lines = file.readlines()
                # First line holds the room size
                self.gn_height, self.gn_width = tuple(map(int, ls_lines[0].strip()[2:].split(',')))
                logging.debug(f"Height: {self.gn_height} | Width: {self.gn_width}")
                n_num_robots = len(ls_lines) - 1
                # Allocate a matrix with n_num_robots rows and 4 columns
                self.gm_robot_data = numpy.zeros((n_num_robots, self.E_ROBOT.COLUMNS.value), dtype=int)
                # Fill the matrix line by line
                for n_index, s_line in enumerate(ls_lines[1:]):
                    ln_data = s_line.strip().replace('p=', '').replace('v=', '').split()
                    ln_position = ln_data[0].split(',')
                    ln_velocity = ln_data[1].split(',')
                    self.gm_robot_data[n_index] = numpy.array(ln_position + ln_velocity, dtype=int)
                    logging.debug(f"{self.gm_robot_data[n_index]}")
        except Exception as e:
            logging.error(f"Error loading file: {e}")
            return True # Error
        
        self.gn_center_height = (self.gn_height -1) // 2
        self.gn_center_width = (self.gn_width -1) // 2
        logging.debug(f"Center H: {self.gn_center_height} W: {self.gn_center_width}")

        self.show()
        logging.info(f"Loaded {len(self.gm_robot_data)} robots")
        return False # OK

    def show(self):
        """
        Prints the room size and the robot data.
        """
        s_lines = str()
        s_lines += f"Room Size:\nHeight={self.gn_height}, Width={self.gn_width}\n"
        for n_index, ln_robot in enumerate(self.gm_robot_data):
            s_lines += f"ROBOT {n_index:3} | P: {ln_robot[self.E_ROBOT.PX.value]:3}, {ln_robot[self.E_ROBOT.PY.value]:3} | V: {ln_robot[self.E_ROBOT.VX.value]:3}, {ln_robot[self.E_ROBOT.VY.value]:3}"
            if n_index < len(self.gm_robot_data) -1:
                s_lines += "\n"
        logging.info(s_lines)
        return False # OK
    
    def simulate_step(self):
        # Simulate a robot step
        #ADD the speed to the position
        #self.gm_robot_data[:,0:2] += self.gm_robot_data[:,2:4]
        #self.gm_robot_data[:, 0] = numpy.mod(self.gm_robot_data[:, 0], self.gn_width)
        #for each robot
        for ln_robot in self.gm_robot_data:
            #POS+=SPEED
            ln_robot[self.E_ROBOT.PX.value] += ln_robot[self.E_ROBOT.VX.value]
            ln_robot[self.E_ROBOT.PY.value] += ln_robot[self.E_ROBOT.VY.value]
            #Teleport X
            if ln_robot[self.E_ROBOT.PX.value] < 0:
                ln_robot[self.E_ROBOT.PX.value] += self.gn_width
            if ln_robot[self.E_ROBOT.PY.value] < 0:
                ln_robot[self.E_ROBOT.PY.value] += self.gn_height
            if ln_robot[self.E_ROBOT.PX.value] >= self.gn_width:
                ln_robot[self.E_ROBOT.PX.value] -= self.gn_width
            if ln_robot[self.E_ROBOT.PY.value] >= self.gn_height:
                ln_robot[self.E_ROBOT.PY.value] -= self.gn_height

        return False # OK

    def simulate(self, in_steps : int )->bool:
        """
        simulate a fixed number of steps
        """
        for n_step in range(in_steps):
            logging.info(f"STEP {n_step+1}")
            b_fail = self.simulate_step()
            if b_fail:
                return True #FAIL
            self.show()
            cl_robot_security.count_robots_in_quadrants()
        return False #OK
    
    def count_robots_in_quadrants(self) -> bool:
        """
        I divide the field in 4 sections plus a central cross
        7 hieght, 11 width
        0:3 3 4:7
        0 1 2 3 4 5 6
        . . . | . . . 
        I count all robots within that quadrant and inside the cross
        number should be conserved
        """

        n_top_left = 0
        n_top_right = 0
        n_bot_left = 0
        n_bot_right = 0
        n_center = 0

        for ln_robot in self.gm_robot_data:
            b_left = False
            b_right = False
            b_top = False
            b_bot = False
            b_center = False
            if ln_robot[self.E_ROBOT.PX.value] < 0:
                logging.error(f"ERROR: X WIDTH OOB {ln_robot[self.E_ROBOT.PX.value]}")
                return True #FAIL
            elif ln_robot[self.E_ROBOT.PX.value] < self.gn_center_width:
                b_left = True
            elif ln_robot[self.E_ROBOT.PX.value] == self.gn_center_width:
                b_center = True
            elif ln_robot[self.E_ROBOT.PX.value] < self.gn_width:
                b_right = True
            else:
                logging.error(f"ERROR: X WIDTH OOB {ln_robot[self.E_ROBOT.PX.value]}")
                return True #FAIL

            if ln_robot[self.E_ROBOT.PY.value] < 0:
                logging.error(f"ERROR: Y HEIGHT OOB {ln_robot[self.E_ROBOT.PY.value]}")
                return True #FAIL
            elif ln_robot[self.E_ROBOT.PY.value] < self.gn_center_height:
                b_top = True
            elif ln_robot[self.E_ROBOT.PY.value] == self.gn_center_height:
                b_center = True
            elif ln_robot[self.E_ROBOT.PY.value] < self.gn_height:
                b_bot = True
            else:
                logging.error(f"ERROR: Y HEIGHT OOB {ln_robot[self.E_ROBOT.PY.value]}")
                return True #FAIL

            if b_center:
                n_center += 1
            elif b_left:
                if b_top:
                    n_top_left += 1
                else:
                    n_bot_left += 1
            elif b_right:
                if b_top:
                    n_top_right += 1
                else:
                    n_bot_right += 1
            else:
                logging.error(f"ERROR: POSITION NOT DETECTED {ln_robot[self.E_ROBOT.PX.value]} {ln_robot[self.E_ROBOT.PY.value]}")
                return True #FAIL
            
        n_total = n_top_left+n_top_right+n_bot_left+n_bot_right+n_center
        logging.info(f"Top Left {n_top_left} | Top Right {n_top_right} | Bottom Left {n_bot_left} | Bottom Right {n_bot_right} | Center {n_center}")
        if (n_total != len(self.gm_robot_data)):
            logging.error(f"ERROR: ROBOT NUMBER NOT CONSERVED {n_total} expected {self.gm_robot_data}")
            return True #FAIL

        n_safety_factor = n_top_left * n_top_right * n_bot_left * n_bot_right
        logging.info(f"Safety Factor: {n_safety_factor}")
        return False #OK







#------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(
        filename="day14/day14.log",
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin")

    cl_robot_security = Robot_security()
    #cl_robot_security.load_from_file("day14/day14-example.txt")
    #cl_robot_security.load_from_file("day14/day14-example-simple.txt")
    cl_robot_security.load_from_file("day14/day14-data.txt")
    cl_robot_security.simulate(100)
    
    cl_robot_security.show()




