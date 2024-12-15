#------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#------------------------------------------------------------------------------------------------------------------------------

import logging

from typing import Set, Dict, List, Tuple

#import copy

#from map_of_symbols import Map_of_symbols

from map_cartesian import Map_cartesian

#------------------------------------------------------------------------------------------------------------------------------
#   RULES
#------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------
#   ALGORITHM
#------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------
#   SOLUTION
#------------------------------------------------------------------------------------------------------------------------------

class Robot_instruction:
    def __init__(self):
        #map symbols
        self.cs_void = '.'
        self.cs_robot = '@'
        self.cs_wall = '#'
        self.cs_box = 'O'
        #robot can be moved into half position (start fefault west/left)
        self.cs_robot_half_west = '<'
        self.cs_robot_half_east = '>'
        #boxes can be moved half position
        self.cs_box_half_west = '['
        self.cs_box_half_east = ']'
        self.cs_box_double_half = 'X'
        #robot instructions
        self.cs_commands = "^>v<"
        #class to handle maps
        self.gcl_map = Map_cartesian()
        self.gs_instructions = str()
        #position of the robot in the map
        self.gtnn_robot_coordinates = [-1, -1]
        

    def load_map_and_instructions_from_file(self, is_filename: str ) -> bool:
        """
        The file has two sections
        First a map
        Then instructions

        HORIZONTAL COMBOS
        R.  BB
        >   O

        .R  BB
        >   O

        .R  .B  B.
        >   [   ]

        Devilish. The robot is touching a half box
        ..  RB  B.
        .   >   ]

        ..  RB  BB  B.
        .   >   X   ]
        
        

        """

        s_instructions = str()

        try:
            with open(is_filename, 'r') as file:
                ls_lines = file.readlines()
                
                # Split the lines based on the first newline
                n_split_index = ls_lines.index('\n') if '\n' in ls_lines else len(ls_lines)
                s_map = ls_lines[:n_split_index]
                s_instructions = ls_lines[n_split_index + 1:]  # Exclude the newline itself
                ls_instructions = [s_line.strip() for s_line in s_instructions]
                #take the string out of the list
                s_instructions = str()
                for s_instruction in ls_instructions:
                    s_instructions+=s_instruction
                #Use the Map class to load the map
                self.gcl_map.load_map_from_list( s_map )
                self.gcl_map.show_map()                

                logging.info(f"Number of instructions: {len(s_instructions)}")
                logging.info(f"Instructions:\n{s_instructions}")

        except Exception as e:
            logging.error(f"Error loading file: {e}")
            return True # Error
        
        #Find the coordinates of the robot
        b_fail = self.find_robot_in_map()
        if b_fail:
            logging.error("ERROR: failed to find robot")
            return True #FAIL
        
        logging.info(f"Robot position: {self.gtnn_robot_coordinates}")

        #translate instructions to cartesian
        b_fail, s_instructions_cartesian = self.translate_instructions( s_instructions )
        if b_fail:
            logging.error("ERROR: failed to translate command instructions")
            return True #FAIL
        self.gs_instructions = s_instructions_cartesian
        logging.info(f"Number of commands: {len(self.gs_instructions)}")
        logging.info(f"Commands:\n{self.gs_instructions}")
        
        return False #OK

    def translate_instructions(self, is_instructions : str ) -> Tuple[bool, str]:
        """
        Given instructions in the format ^>v< translate them to cartesian NESW
        """

        #build the dictionary
        d_translate_to_cartesian = dict()
        for n_index, s_command in enumerate(self.cs_commands):
            s_command_cartesian = Map_cartesian.cs_cartesian[n_index]
            d_translate_to_cartesian[s_command] = s_command_cartesian
        logging.debug(f"Dictionary to translate to cartesian: {d_translate_to_cartesian}")

        s_instructions_cartesian = str()

        #translate commands
        s_instructions_cartesian = ''.join([d_translate_to_cartesian[s_command] for s_command in is_instructions])

        return False, s_instructions_cartesian #OK


    def find_robot_in_map( self ) -> Tuple[bool, Tuple[int,int]]:

        #find the robot
        b_fail, ltnn_robots = self.gcl_map.find_symbol(self.cs_robot_half_west)
        if b_fail:
            logging.error("ERROR: could not find robot")
            return True #FAIL
        elif len(ltnn_robots) <= 0:
            logging.error("ERROR: Robot not found...")
            return True #FAIL
        elif len(ltnn_robots) > 1:
            logging.error(f"ERROR: too many robots! {len(ltnn_robots)}")
            return True #FAIL
        else:
            self.gtnn_robot_coordinates = ltnn_robots[0]
            
        return False #OK

    def simulate_step(self, s_instruction : str) -> bool:
        """
        Simulate one instruction step
        """
        b_fail, s_robot_symbol = self.gcl_map.get_coordinate(self.gtnn_robot_coordinates)
        if b_fail or s_robot_symbol != self.cs_robot:
            logging.error(f"ERROR: robot coordinate {self.gtnn_robot_coordinates} is NOT a robot >{s_robot_symbol}<")
            return True #FAIL

        #try to move the robot in the given direction
        b_fail, tnn_next = self.gcl_map.get_coordinate_cartesian( self.gtnn_robot_coordinates, s_instruction )
        if b_fail:
            logging.error("ERROR: could not move robot...")
            return True #FAIL
        b_fail, s_symbol = self.gcl_map.get_coordinate(tnn_next)
        #if I hit a wall
        if s_symbol == self.cs_wall:
            #robot does not move
            logging.info(f"{tnn_next} is a wall >{s_symbol}< Do not move")
            pass
        #move into a void
        elif s_symbol == self.cs_void:
            #robot moves in the void
            logging.info(f"{tnn_next} is a void >{s_symbol}< Robot moves from {self.gtnn_robot_coordinates} to {tnn_next}")
            b_fail = False
            b_fail = b_fail or self.gcl_map.set_coordinate(self.gtnn_robot_coordinates, self.cs_void)
            b_fail = b_fail or self.gcl_map.set_coordinate(tnn_next, self.cs_robot)
            if b_fail:
                logging.error(f"ERROR: failed to set the map coordinates {self.gtnn_robot_coordinates} or {tnn_next} to new symbols {self.cs_void} {self.cs_robot}")
                return True #FAIL
            self.gtnn_robot_coordinates = tnn_next
        #move into a box
        elif s_symbol == self.cs_box:
            #I'm expecting a sequence of any number of >O< followed by a void
            b_robot_advances = True
            n_boxes = 1
            ltnn_boxes = list()
            #as long as I see a box
            while s_symbol == self.cs_box:
                #increase distance by 1
                n_boxes += 1
                #compute next position
                b_fail, tnn_next_box = self.gcl_map.get_coordinate_cartesian(self.gtnn_robot_coordinates, s_instruction,n_boxes)
                if b_fail:
                    #it means that there is a wall or it's OOB and robot can't advance
                    b_robot_advances = False
                    s_symbol = self.cs_wall
                else:
                    #add the coordinate to the list of what needs to be turned into a box
                    ltnn_boxes.append(tnn_next_box)
                    bool, s_symbol = self.gcl_map.get_coordinate(tnn_next_box)
                    if b_fail:
                        b_robot_advances = False
                        s_symbol = self.cs_wall

            #if I get to the end, and the symbol is a void
            if s_symbol == self.cs_void:
                #it means the robot advances into the box
                #it means all boxes advances into the void
                b_fail = False
                b_fail = b_fail or self.gcl_map.set_coordinate(self.gtnn_robot_coordinates, self.cs_void)
                b_fail = b_fail or self.gcl_map.set_coordinate(tnn_next, self.cs_robot)
                if b_fail:
                    logging.error(f"ERROR: failed to set the map coordinates {self.gtnn_robot_coordinates} or {tnn_next} to new symbols {self.cs_void} {self.cs_robot}")
                    return True #FAIL
                self.gtnn_robot_coordinates = tnn_next
                #for all the boxes found
                for tnn_box in ltnn_boxes:
                    b_fail = b_fail or self.gcl_map.set_coordinate(tnn_box, self.cs_box)
                    if b_fail:
                        logging.error(f"ERROR: failed to set the map coordinate {tnn_box} to box {self.cs_box}")
                        return True #FAIL
                logging.info(f"Robot advanced into {n_boxes-1} boxes")
            else:
                logging.info(f"Robot tried to advanced into {n_boxes-1} boxes but a wall blocks it")
        else:
            logging.error(f"ERROR: invalid symbol >{s_symbol}<")
            return True #FAIL
                    
        b_continue = False
        while b_continue:
            b_fail, tnn_cursor = self.gcl_map.get_coordinate_cartesian()

        return False #OK

    def simulate(self) -> bool:
        """
        Ask the robot to execute the instruction
        """

        for n_index, s_command in enumerate(self.gs_instructions):
            logging.info(f"STEP: {n_index+1:4} | Command: {s_command} | Position {self.gtnn_robot_coordinates}")
            self.simulate_step(s_command)
        
        self.gcl_map.show_map()

        return False #OK
    
    def simulate_step_half_width(self, s_instruction : str) -> bool:
        """
        Simulate one instruction step
        """
        b_fail, s_robot_symbol = self.gcl_map.get_coordinate(self.gtnn_robot_coordinates)
        if b_fail or (s_robot_symbol != self.cs_robot_half_west and s_robot_symbol != self.cs_robot_half_east):
            logging.error(f"ERROR: robot coordinate {self.gtnn_robot_coordinates} is NOT a robot >{s_robot_symbol}<")
            return True #FAIL
        #try to move the robot in the given direction
        b_fail, tnn_next = self.gcl_map.get_coordinate_cartesian( self.gtnn_robot_coordinates, s_instruction )
        if b_fail:
            logging.error("ERROR: could not move robot...")
            return True #FAIL+
        b_fail, s_next_symbol = self.gcl_map.get_coordinate(tnn_next)
        logging.debug(f"Symbol at coordinate {tnn_next} is {s_next_symbol}")

        #-------------------------------------------------------------------------
        # HALF ROBOT MOVES INTO OPPOSITE DIRECTION
        #-------------------------------------------------------------------------
        #   BUT I need to exclude the devilish conditions <] <X [> X>
        
        if (
            (
                #moving east with half robot west
                (s_instruction == 'E' and s_robot_symbol == '<') or  
                #moving west with half robot east
                (s_instruction == 'W' and s_robot_symbol == '>')
            ) and not
            (
                #moving east with Wrobot pressed against west half box
                (s_instruction == 'E' and s_robot_symbol == '<' and s_next_symbol==']') or
                #moving east with Wrobot pressed against double half box
                (s_instruction == 'E' and s_robot_symbol == '<' and s_next_symbol=='X') or
                #moving west with east robot pressed against east half box
                (s_instruction == 'W' and s_robot_symbol == '>' and s_next_symbol=='[') or
                #moving west with east robot pressed against double half box
                (s_instruction == 'W' and s_robot_symbol == '>' and s_next_symbol=='X')
            )
        ):
            if s_robot_symbol == self.cs_robot_half_west:
                s_robot_symbol_new = self.cs_robot_half_east
            elif s_robot_symbol == self.cs_robot_half_east:
                s_robot_symbol_new = self.cs_robot_half_west
            b_fail = self.gcl_map.set_coordinate(self.gtnn_robot_coordinates, s_robot_symbol_new)
            if b_fail:
                logging.error(f"ERROR: could not set robot {self.gtnn_robot_coordinates} to {s_robot_symbol_new}")
                return True #FAIL
            logging.info(f"Half robot {s_robot_symbol} moves {s_instruction} and becomes half robot {s_robot_symbol_new}")

        #-------------------------------------------------------------------------
        # MOVE INTO WALL >#<  
        #-------------------------------------------------------------------------

        #if I hit a wall
        elif s_next_symbol == self.cs_wall:
            logging.info(f"{tnn_next} is a wall >{s_next_symbol}< Do not move")
        
        #move into a void
        elif s_next_symbol == self.cs_void:

            #-------------------------------------------------------------------------
            # MOVE INTO VOID >.<  vertically
            #-------------------------------------------------------------------------

            b_move_robot = False
            b_flip_robot = False

            #if I'm moving vertically
            if s_instruction == 'N' or s_instruction == 'S':
                #always update symbols
                b_move_robot = True

            #-------------------------------------------------------------------------
            # MOVE INTO VOID >.<  horizontally
            #-------------------------------------------------------------------------

            #I'm moving horizontally
            elif s_instruction == 'E' or s_instruction == 'W':
                #moving east with half robot west
                if s_instruction == 'E' and s_robot_symbol==self.cs_robot_half_west:
                    b_flip_robot = True

                #moving west with half robot east
                elif s_instruction == 'W' and s_robot_symbol==self.cs_robot_half_east:
                    b_flip_robot = True

                else:
                    b_flip_robot = True
                    b_move_robot = True

                    s_new_robot = self.cs_robot_half_west
                    b_fail = self.gcl_map.set_coordinate(self.gtnn_robot_coordinates, s_new_robot)
                    if b_fail:
                        logging.error(f"ERROR: could not set robot {self.gtnn_robot_coordinates} to {s_new_robot}")
                        return True #FAIL
                    logging.info(f"Half robot {s_robot_symbol} moves {s_instruction} and becomes half robot {s_new_robot}")

                if b_flip_robot:
                    if s_robot_symbol == self.cs_robot_half_west:
                        s_robot_symbol = self.cs_robot_half_east
                    elif s_robot_symbol == self.cs_robot_half_east:
                        s_robot_symbol = self.cs_robot_half_west
                    else:
                        logging.error(f"Bad robot symbol: {s_robot_symbol}")
                        return True #FAIL

            else:
                logging.error(f"ERROR: invalid Symbol {s_instruction}")
                return True #FAIL
            
            #PROCESS MOTION
            b_fail = False

            if b_move_robot == False:
                tnn_next = self.gtnn_robot_coordinates
            else:
                b_fail = b_fail or self.gcl_map.set_coordinate(self.gtnn_robot_coordinates, self.cs_void)

            b_fail = self.gcl_map.set_coordinate(tnn_next, s_robot_symbol)
            if b_fail:
                logging.error(f"ERROR: could not set robot {self.gtnn_robot_coordinates} to {s_robot_symbol}")
                return True #FAIL
            self.gtnn_robot_coordinates = tnn_next
            logging.info(f"Half robot moves {s_instruction} to from {self.gtnn_robot_coordinates} to {tnn_next} and becomes {s_robot_symbol}")

        #-------------------------------------------------------------------------
        # MOVE INTO A WHOLE BOX >O<  or an half moved box >[< >]< or two half boxes >X<
        #-------------------------------------------------------------------------

        elif s_next_symbol == self.cs_box or s_next_symbol == self.cs_box_half_west or s_next_symbol == self.cs_box_half_east or self.cs_box_double_half:
            return True #FAIL  


        else:
            logging.error(f"ERROR: invalid symbol >{s_next_symbol}<")
            return True #FAIL          
        return False #OK
        """
        #-------------------------------------------------------------------------
        # MOVE INTO A WHOLE BOX >O<  or an half moved box >[< >]< or two half boxes >X<
        #-------------------------------------------------------------------------

        elif s_symbol == self.cs_box or s_symbol == self.cs_box_half_west or s_symbol == self.cs_box_half_east or self.cs_box_double_half:

            #-------------------------------------------------------------------------
            # MOVE INTO A WHOLE BOX >O<  WHILE GOING North or South
            #-------------------------------------------------------------------------

            if s_symbol == self.cs_box and (s_instruction == 'N' or s_instruction == 'S'):
                b_robot_advances = True
                n_boxes = 1
                ltnn_boxes = list()
                #as long as I see a box
                while s_symbol == self.cs_box:
                    #increase distance by 1
                    n_boxes += 1
                    #compute next position
                    b_fail, tnn_next_box = self.gcl_map.get_coordinate_cartesian(self.gtnn_robot_coordinates, s_instruction,n_boxes)
                    if b_fail:
                        #it means that there is a wall or it's OOB and robot can't advance
                        b_robot_advances = False
                        s_symbol = self.cs_wall
                    else:
                        #add the coordinate to the list of what needs to be turned into a box
                        ltnn_boxes.append(tnn_next_box)
                        bool, s_symbol = self.gcl_map.get_coordinate(tnn_next_box)
                        if b_fail:
                            b_robot_advances = False
                            s_symbol = self.cs_wall

                #if I get to the end, and the symbol is a void
                if s_symbol == self.cs_void:
                    #it means the robot advances into the box
                    #it means all boxes advances into the void
                    b_fail = False
                    b_fail = b_fail or self.gcl_map.set_coordinate(self.gtnn_robot_coordinates, self.cs_void)
                    b_fail = b_fail or self.gcl_map.set_coordinate(tnn_next, self.cs_robot)
                    if b_fail:
                        logging.error(f"ERROR: failed to set the map coordinates {self.gtnn_robot_coordinates} or {tnn_next} to new symbols {self.cs_void} {self.cs_robot}")
                        return True #FAIL
                    self.gtnn_robot_coordinates = tnn_next
                    #for all the boxes found
                    for tnn_box in ltnn_boxes:
                        b_fail = b_fail or self.gcl_map.set_coordinate(tnn_box, self.cs_box)
                        if b_fail:
                            logging.error(f"ERROR: failed to set the map coordinate {tnn_box} to box {self.cs_box}")
                            return True #FAIL
                    logging.info(f"Robot advanced into {n_boxes-1} boxes")
                else:
                    logging.info(f"Robot tried to advanced into {n_boxes-1} boxes but a wall blocks it")

            #-------------------------------------------------------------------------
            # MOVE INTO A HALF BOX >[< >]< or DOUBLE HALF BOX >X< WHILE GOING North or South
            #-------------------------------------------------------------------------
            # this is difficult, because I can push a whole pyramid of boxes
            #

            elif (s_instruction == 'E' or s_instruction == 'W'):

                #-------------------------------------------------------------------------
                # MOVE INTO A WHOLE BOX >O< WHILE GOING East or West
                #-------------------------------------------------------------------------

                if s_symbol == self.cs_box:
                    #moving east but not yet +1/2
                    if self.gn_robot_position_half_width != 



                #-------------------------------------------------------------------------
                # MOVE INTO A HALF BOX >[< >]< WHILE GOING East or West
                #-------------------------------------------------------------------------

                elif s_symbol == self.cs_box_half_west or s_symbol == self.cs_box_half_east:
                    pass

                elif s_symbol == self.cs_box_double_half:
                    logging.error(f"ERROR: I can never encounter double half while going E or W!")
                    return True #FAIL    
                else:
                    logging.error(f"ERROR: invalid symbol >{s_symbol}<")
                    return True #FAIL 

            else:
                logging.error(f"ERROR: ALGORIGHM NOT FINISHED | Symbol {s_symbol}")

        """     

        """

        #move into a box
        elif s_symbol == self.cs_box:
            #I'm expecting a sequence of any number of >O< followed by a void
            b_robot_advances = True
            n_boxes = 1
            ltnn_boxes = list()
            #as long as I see a box
            while s_symbol == self.cs_box:
                #increase distance by 1
                n_boxes += 1
                #compute next position
                b_fail, tnn_next_box = self.gcl_map.get_coordinate_cartesian(self.gtnn_robot_coordinates, s_instruction,n_boxes)
                if b_fail:
                    #it means that there is a wall or it's OOB and robot can't advance
                    b_robot_advances = False
                    s_symbol = self.cs_wall
                else:
                    #add the coordinate to the list of what needs to be turned into a box
                    ltnn_boxes.append(tnn_next_box)
                    bool, s_symbol = self.gcl_map.get_coordinate(tnn_next_box)
                    if b_fail:
                        b_robot_advances = False
                        s_symbol = self.cs_wall

            #if I get to the end, and the symbol is a void
            if s_symbol == self.cs_void:
                #it means the robot advances into the box
                #it means all boxes advances into the void
                b_fail = False
                b_fail = b_fail or self.gcl_map.set_coordinate(self.gtnn_robot_coordinates, self.cs_void)
                b_fail = b_fail or self.gcl_map.set_coordinate(tnn_next, self.cs_robot)
                if b_fail:
                    logging.error(f"ERROR: failed to set the map coordinates {self.gtnn_robot_coordinates} or {tnn_next} to new symbols {self.cs_void} {self.cs_robot}")
                    return True #FAIL
                self.gtnn_robot_coordinates = tnn_next
                #for all the boxes found
                for tnn_box in ltnn_boxes:
                    b_fail = b_fail or self.gcl_map.set_coordinate(tnn_box, self.cs_box)
                    if b_fail:
                        logging.error(f"ERROR: failed to set the map coordinate {tnn_box} to box {self.cs_box}")
                        return True #FAIL
                logging.info(f"Robot advanced into {n_boxes-1} boxes")
            else:
                logging.info(f"Robot tried to advanced into {n_boxes-1} boxes but a wall blocks it")
        else:
            logging.error(f"ERROR: invalid symbol >{s_symbol}<")
            return True #FAIL
                    
        b_continue = False
        while b_continue:
            b_fail, tnn_cursor = self.gcl_map.get_coordinate_cartesian()
        """
        return False #OK
    
    def simulate_half_width(self, ib_debug = False) -> bool:
        """
        Ask the robot to execute the instruction
        """

        for n_index, s_command in enumerate(self.gs_instructions):
            logging.info(f"STEP: {n_index+1:4} | Command: {s_command} | Position {self.gtnn_robot_coordinates}")
            self.simulate_step_half_width(s_command)
            if ib_debug:
                self.gcl_map.show_map()
        if not ib_debug:
            self.gcl_map.show_map()
        return False #OK

    def compute_part_1_result(self, ib_debug = False) -> bool:
        """
        Get the coordinates of all boxes
        From that, compute GPS coordinate and final score
        """

        b_fail, ltnn_box = self.gcl_map.find_symbol(self.cs_box)
        if b_fail:
            logging.error("ERROR: could not get list of boxes")
            return True #FAIL

        n_gps_total = 0
        logging.info(f"Found {len(ltnn_box)} boxes")
        for tnn_box in ltnn_box:
            n_gps = 100*tnn_box[0] +tnn_box[1]
            n_gps_total += n_gps
            logging.debug(f"Coordinate: {tnn_box} | GPS: {n_gps} | Total GPS: {n_gps_total}")
        logging.info(f"Sum of all GPS coordinates: {n_gps_total}")

        return False #OK


#------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(
        filename="day15/day15.log",
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin")

    cl_warehouse = Robot_instruction()
    #cl_warehouse.load_map_and_instructions_from_file("day15/day15-example-small.txt")
    #cl_warehouse.load_map_and_instructions_from_file("day15/day15-example-small-b.txt")
    cl_warehouse.load_map_and_instructions_from_file("day15/day15-example-simple.txt")
    #cl_warehouse.load_map_and_instructions_from_file("day15/day15-example.txt")
    #cl_warehouse.load_map_and_instructions_from_file("day15/day15-data.txt")
    #cl_warehouse.simulate()
    cl_warehouse.simulate_half_width(True)
    cl_warehouse.compute_part_1_result()