#------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#------------------------------------------------------------------------------------------------------------------------------

import logging

from typing import Set, Dict, List, Tuple

from coordinates import Coordinates

from map_of_symbols import Map_of_symbols

from body_collision import Box

from body_collision import Body_collision

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
        self.cs_robot_name = "robot"
        self.cs_wall = '#'
        self.cs_wall_name = "wall"
        self.cs_box = 'O'
        self.cs_box_name = "pallet"
        #robot instructions
        self.cs_commands = "^>v<"
        #class to handle maps
        self.gcl_map = Map_of_symbols()
        self.gltnn_instruction_speed : List[List[Tuple[float, float]]] = list()
        #Constant for Map->Collision conversion
        self.ctnn_tile_offset = (0.5, 0.5)
        self.ctnn_tile_size = (0.99, 0.99)
        #HALF SIZE ROBOT
        self.ctnn_robot_offset = (0.5, 0.25)
        self.ctnn_robot_size = (0.99, 0.49)
        self.ctnn_robot_speed = (1.0, 0.5)
        #FULL SIZE ROBOT
        #self.ctnn_robot_offset = (0.5, 0.5)
        #self.ctnn_robot_size = (0.99, 0.99)
        #self.ctnn_robot_speed = (1.0, 1.0)
        #Constant for the robot speed

        #True uses the slow collision algorithm, i estimate 66 minutes for the excercise
        #False uses a fast collision algorithm. I avoid doing the full N^2 collision detection, and just do MOVED*N
        self.cb_slow_collision = False
        
        #ID of the robot in the Collision class
        self.gn_id_robot = -1

        self.gcl_box_collision : Body_collision = Body_collision()

    def load_map_and_instructions_from_file(self, is_filename: str ) -> bool:
        """
        The file has two sections
        First a map
        Then instructions
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
        
        #translate instructions to cartesian
        b_fail, ltnn_instruction_speed = self.translate_instructions( s_instructions )
        if b_fail:
            logging.error("ERROR: failed to translate command instructions")
            return True #FAIL
        self.gltnn_instruction_speed = ltnn_instruction_speed
        logging.info(f"Number of commands: {len(self.gltnn_instruction_speed)}")
        logging.info(f"Commands:\n{self.gltnn_instruction_speed}")
        
        return False #OK

    def translate_instructions(self, is_instructions : str ) -> Tuple[bool, str]:
        """
        Given instructions in the format ^>v< translate them to move distance
        """

        #build the dictionary
        d_translate_to_speed = dict()
        
        d_translate_to_speed['^'] = (-self.ctnn_robot_speed[0], 0)  #NORTH
        d_translate_to_speed['>'] = (0, self.ctnn_robot_speed[1])   #EAST
        d_translate_to_speed['v'] = (self.ctnn_robot_speed[0], 0)   #SOUTH
        d_translate_to_speed['<'] = (0, -self.ctnn_robot_speed[1])   #WEST

        
        logging.debug(f"Dictionary to translate to cartesian: {d_translate_to_speed}")

        ltnn_instructions_speed = list()
        for s_command in is_instructions:
            if s_command not in d_translate_to_speed:
                logging.error(f"Translation error {s_command}")
                return True, list() #ERROR
            ltnn_instructions_speed.append( d_translate_to_speed[s_command])
        return False, ltnn_instructions_speed #OK

    def translate_map_to_body_collision(self) -> bool:
        """
        I have a map
        """
        tnn_start = (0,0)
        tnn_size = self.gcl_map.get_size()
        logging.info(f"Bounding box | Start {tnn_start} End {tnn_size}")

        #create the Body collision class
        cl_collision = Body_collision()
        #add the field
        b_fail, ln_id = cl_collision.add_field_top_left_size( tnn_start, tnn_size, "wall")
        if b_fail:
            logging.error("ERROR: failed to set boundary size")
            return True #FAIL
        
        # ADD WALLS TO COLLISION

        b_fail, ltnn_walls = self.gcl_map.find_symbol(self.cs_wall)
        logging.info(f"Number of walls: {len(ltnn_walls)} | Walls:\n{ltnn_walls}")

        for tnn_wall in ltnn_walls:
            tnn_center = Coordinates.sum( tnn_wall, self.ctnn_tile_offset )
            b_fail, n_id = cl_collision.add_box_center_size( tnn_center, self.ctnn_tile_size, self.cs_wall_name )
            if b_fail:
                logging.error("ERROR: failed to add wall")
                return True #FAIL
            b_fail, st_box = cl_collision.get_box(n_id)
            if b_fail:
                logging.error("ERROR: failed to address wall")
                return True #FAIL
            logging.info(f"ID: {n_id:5} | {st_box}")

        # ADD PALLETS TO COLLISION

        b_fail, ltnn_pallet = self.gcl_map.find_symbol(self.cs_box)
        logging.info(f"Number of pallets: {len(ltnn_pallet)} | Pallets:\n{ltnn_pallet}")

        for tnn_pallet in ltnn_pallet:
            tnn_center = Coordinates.sum( tnn_pallet, self.ctnn_tile_offset )
            b_fail, n_id = cl_collision.add_box_center_size( tnn_center, self.ctnn_tile_size, self.cs_box_name )
            if b_fail:
                logging.error("ERROR: failed to add pallet")
                return True #FAIL
            b_fail, st_box = cl_collision.get_box(n_id)
            if b_fail:
                logging.error("ERROR: failed to address pallet")
                return True #FAIL
            logging.info(f"ID: {n_id:5} | {st_box}")

        #ADD ROBOT TO COLLISION

        b_fail, tnn_robot = self.find_robot_in_map()
        if b_fail:
            logging.error("ERROR: failed to find robot")
            return True #FAIL
        else:
            tnn_center = Coordinates.sum( tnn_robot, self.ctnn_robot_offset )
            b_fail, n_id = cl_collision.add_box_center_size( tnn_center, self.ctnn_robot_size, self.cs_robot_name )
            if b_fail:
                logging.error("ERROR: failed to add pallet")
                return True #FAIL
            b_fail, st_box = cl_collision.get_box(n_id)
            if b_fail:
                logging.error("ERROR: failed to address pallet")
                return True #FAIL
            self.gn_id_robot = n_id
            logging.info(f"Robot {st_box} ID: {self.gn_id_robot}")    
        
        self.gcl_box_collision = cl_collision

        return False #OK

    
    def translate_body_collision_to_map(self) -> bool:
        """
        Updates the map (gcl_map) based on the Body_collision instance.
        Extracts objects from Body_collision and maps them back to symbols in the map.

        Returns:
            bool: True if an error occurs during the process, False otherwise.
        """
        if not hasattr(self, "gcl_box_collision") or self.gcl_box_collision is None:
            logging.error("ERROR: No collision object found to translate")
            return True  # FAIL

        # Reset the map
        b_fail = self.gcl_map.clear_map(self.cs_void)
        if b_fail:
            logging.error("ERROR: Failed to clear map")
            return True  # FAIL

        # Process all boxes in the collision object
        ltnn_boxes = self.gcl_box_collision.get_boxes()
        if b_fail:
            logging.error("ERROR: Failed to retrieve boxes from collision object")
            return True  # FAIL

        for st_box in ltnn_boxes:
            # Check the type of the box and map it back to a symbol
            tnn_top_left = Coordinates.sub(st_box.gtnn_center, self.ctnn_tile_offset)
            tnn_top_left = (round(tnn_top_left[0]), round(tnn_top_left[1]))
            if st_box.gs_type == self.cs_wall_name:
            
                b_fail = self.gcl_map.set_coordinate(tnn_top_left, self.cs_wall)
            elif st_box.gs_type == self.cs_box_name:
                
                b_fail = self.gcl_map.set_coordinate(tnn_top_left, self.cs_box)
            elif st_box.gs_type == self.cs_robot_name:
                
                b_fail = self.gcl_map.set_coordinate(tnn_top_left, self.cs_robot)
            else:
                logging.warning(f"Unknown box type: {st_box.gs_type}, skipping...")
                continue

            if b_fail:
                logging.error(f"ERROR: Failed to update map for box ID:")
                return True  # FAIL

        logging.info("Map updated successfully from collision data")
        return False  # OK


    def find_robot_in_map( self ) -> Tuple[bool, Tuple[int,int]]:

        #find the robot
        b_fail, ltnn_robots = self.gcl_map.find_symbol(self.cs_robot)
        if b_fail:
            logging.error("ERROR: could not find robot")
            return True #FAIL
        elif len(ltnn_robots) <= 0:
            logging.error("ERROR: Robot not found...")
            return True #FAIL
        elif len(ltnn_robots) > 1:
            logging.error(f"ERROR: too many robots! {len(ltnn_robots)}")
            return True #FAIL
            
        return False, ltnn_robots[0] #OK
    

    def simulate_step(self, itnn_move : Tuple[float,float], ib_debug = True) -> bool:
        """
        Move the robot
        """
    
        b_fail = self.gcl_box_collision.move( self.gn_id_robot, itnn_move )
        if b_fail:
            logging.error(f"Failed to move robot")
            return True #FAIL
        #list of items that have been moved
        #used to restrict the collision search
        ln_id_moved = list()
        ln_id_moved.append(self.gn_id_robot)

        ln_collision_id = self.gcl_box_collision.detect_box_collision( self.gn_id_robot )
        if ib_debug:
            logging.debug(f"Num Collisions: {len(ln_collision_id)} | Collisions: {ln_collision_id}")
        #CHAIN OF COLLISION ALGORITHM
        b_allow_move = True
        b_continue = True
        while b_continue:
            #no collision
            if len(ln_collision_id) == 0:
                b_continue = False
            #collision
            else:
                b_fail, d_id_type = self.gcl_box_collision.get_types(ln_collision_id)
                if b_fail:
                    logging.error(f"ERROR: could not get collision ID types. IDs:\n{ln_collision_id}")
                    return True #FAIL
                #If there is at least a wall in the collision
                if self.cs_wall_name in d_id_type:
                    b_continue = False
                    b_allow_move = False
                    if ib_debug:
                        logging.debug("WALL. Forbidden from moving")
                else:
                    
                    #Try to move everything that I just collided with
                    for n_id in ln_collision_id:
                        b_fail, st_box = self.gcl_box_collision.get_box(n_id)
                        if st_box.is_moving():
                            if ib_debug:
                                logging.debug(f"Box {n_id} is moving, don't move it further")
                            
                        else:
                            st_box.move(itnn_move)

                        if n_id not in ln_id_moved:
                            #remember the items that moved
                            ln_id_moved.append(n_id)

                    if self.cb_slow_collision:
                        #detect all collisions
                        #this is too expensive.  
                        ln_collision_id = self.gcl_box_collision.detect_collision()
                    else:
                        #to make the collision detection cheaper
                        #I know I have no collisions before moving the robot
                        #I keep a list of everything that moves
                        #I just consider collisions against that which has moved


                        ln_collision_id = list()
                        #for each item moved
                        for n_id_moved in ln_id_moved:
                            #find all the collisions
                            ln_id_sub_collision = self.gcl_box_collision.detect_box_collision( n_id_moved )
                            logging.debug(f"sub collision {ln_id_sub_collision}")
                            #if the collision is not yet recorded
                            for n_id_collision in ln_id_sub_collision:
                                if n_id_collision not in ln_collision_id:
                                    ln_collision_id.append(n_id_collision)
                    if ib_debug:
                        logging.debug(f"Moved: {ln_id_moved} | collisions: {ln_collision_id}")


                    #ln_collision_id = list()

        if b_allow_move:
            n_updated = self.gcl_box_collision.apply()
            if ib_debug:
                logging.debug(f"Boxes updated: {n_updated}")
        else:
            n_discarded = self.gcl_box_collision.discard()
            if ib_debug:
                logging.debug(f"Boxes whose update has been discarded: {n_discarded}")

        if ib_debug:
            self.translate_body_collision_to_map()
            self.gcl_map.show_map()


        b_fail, st_robot = self.gcl_box_collision.get_box( self.gn_id_robot )
        logging.info(f"New Robot position: {st_robot}")
        return False #OK

    def simulate(self) -> bool:
        """
        Ask the robot to execute the instruction
        """

        for n_index, tnn_instruction_speed in enumerate(self.gltnn_instruction_speed):
            print(f"STEP: {n_index+1:4} of {len(self.gltnn_instruction_speed)}")
            logging.info(f"STEP: {n_index+1:4} | Command: {tnn_instruction_speed}")
            b_fail = self.simulate_step(tnn_instruction_speed, False)
            if b_fail:
                logging.error(f"Failed to simulate")
                return True #FAIL  
    
        self.compute_part_2_result( )

        

        return False #OK

    def compute_part_2_result(self, ib_debug = False) -> bool:
        """
        Get the coordinates of all boxes
        From that, compute GPS coordinate and final score
        """

        lst_boxes = self.gcl_box_collision.get_boxes()
        logging.info(f"Found {len(lst_boxes)} boxes")
        n_gps_total = 0
        for st_box in lst_boxes:
            if st_box.gs_type == self.cs_box_name:
                st_box.gtnn_size=(1,1)
                tnn_top_left= st_box.get_top_left()
                n_gps = 100*tnn_top_left[0] +2*tnn_top_left[1]
                n_gps_total += n_gps
                logging.debug(f"Coordinate: {tnn_top_left} | GPS: {n_gps} | Total GPS: {n_gps_total}")
        
        logging.info(f"Sum of all GPS coordinates: {n_gps_total}")

        self.gcl_map.show_map()

        return False #OK


def solution() -> bool:
    cl_warehouse = Robot_instruction()
    #cl_warehouse.load_map_and_instructions_from_file("day15/day15-example-small.txt")
    #cl_warehouse.load_map_and_instructions_from_file("day15/day15-example-small-b.txt")
    #cl_warehouse.load_map_and_instructions_from_file("day15/day15-example-simple.txt")
    #cl_warehouse.load_map_and_instructions_from_file("day15/day15-example.txt")
    cl_warehouse.load_map_and_instructions_from_file("day15/day15-data.txt")

    cl_warehouse.translate_map_to_body_collision()

    cl_warehouse.simulate()
    

    #cl_collision.add_line( )

    

    return False #OK

#------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(
        filename="day15/day15.log",
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin")

    solution()
