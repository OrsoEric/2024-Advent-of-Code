"""
--- Day 6: Guard Gallivant ---

The Historians use their fancy device again, this time to whisk you all away to the North Pole prototype suit manufacturing lab...
in the year 1518! It turns out that having direct access to history is very convenient for a group of historians.

You still have to be careful of time paradoxes, and so it will be important to avoid anyone from 1518 while The Historians search for the Chief.
Unfortunately, a single guard is patrolling this part of the lab.

Maybe you can work out where the guard will go ahead of time so that The Historians can search safely?

You start by making a map (your puzzle input) of the situation. For example:

....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...

The map shows the current position of the guard with ^ (to indicate the guard is currently facing up from the perspective of the map).
Any obstructions - crates, desks, alchemical reactors, etc. - are shown as #.

Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:

    If there is something directly in front of you, turn right 90 degrees.
    Otherwise, take a step forward.

Following the above protocol, the guard moves up several times until she reaches an obstacle (in this case, a pile of failed suit prototypes):

....#.....
....^....#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...

Because there is now an obstacle in front of the guard, she turns right before continuing straight in her new facing direction:

....#.....
........>#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...

Reaching another obstacle (a spool of several very long polymers), she turns right again and continues downward:

....#.....
.........#
..........
..#.......
.......#..
..........
.#......v.
........#.
#.........
......#...

This process continues for a while, but the guard eventually leaves the mapped area (after walking past a tank of universal solvent):

....#.....
.........#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#v..

By predicting the guard's route, you can determine which specific positions in the lab will be in the patrol path. Including the guard's starting position, the positions visited by the guard before leaving the area are marked with an X:

....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X..

In this example, the guard will visit 41 distinct positions on your map.

Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?
"""



import logging

import itertools

from typing import Dict, Tuple, List

class Patrol_route:
    class Coordinate:
        n_x, n_y, s_dir = -1, -1, "?"
        def show_position(self) -> None:
            logging.info(f"X: {self.n_x} Y: {self.n_y} Direction: {self.s_dir}")
        def get_xy(self) -> Tuple[int,int]:
            return (self.n_x, self.n_y)
        def get_xyd(self) -> Tuple[int,int,str]:
            return (self.n_x, self.n_y, self.s_dir)
        def __str__(self):
            return f"X: {self.n_x} Y: {self.n_y} Direction: {self.s_dir}"
            
    def __init__(self):
        """
        Initialize the Patrol_route class
        """
        self.gn_width = -1
        self.gn_height = -1
        self.gd_obstacle = dict()
        self.gst_guard_position = self.Coordinate()
        self.gltn_patrol_path = list()

    def load_map_from_file(self, is_filename: str) -> bool:
        """
        Load the coordinate of obstacles in a dictionary from a file and set guard position.

        Parameters:
        is_filename (str): The filename of the map to be loaded

        Returns:
        bool: True if fail
        """
        try:
            with open(is_filename, 'r') as file:
                lines = file.readlines()
                self.gn_height = len(lines)
                self.gn_width = len(lines[0].strip())
                
                for y, line in enumerate(lines):
                    for x, char in enumerate(line.strip()):
                        if char == '#':
                            self.gd_obstacle[(x, y)] = True
                        elif char == '^':
                            self.gst_guard_position.n_x = x
                            self.gst_guard_position.n_y = y
                            self.gst_guard_position.s_dir = char
        except Exception as e:
            logging.error(f"Failed to load map: {e}")
            return True #fail
        self.show_map(gs_filename_output)

    def show_map(self, output_filename: str) -> None:
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

    def is_oob(self, ist_coordinate: Coordinate ) -> bool:
        """
        return true if a coordinate is Out of Boundary
        """
        if (ist_coordinate.n_x < 0):
            return True #OOB
        if (ist_coordinate.n_y < 0):
            return True #OOB
        if (ist_coordinate.n_x >= self.gn_width):
            return True #OOB
        if (ist_coordinate.n_y >= self.gn_height):
            return True #OOB
        return False

    def compute_position_in_front_of_the_guard( self ) -> Coordinate:
        """
        Given a guard position XY and a guard direction ^>v<
        Compute the position in front of the guard, and what the right turn is
        """

        st_coordinate = self.Coordinate()

        #UP
        if (self.gst_guard_position.s_dir == "^"):
            st_coordinate.n_x = self.gst_guard_position.n_x
            st_coordinate.n_y = self.gst_guard_position.n_y -1
            st_coordinate.s_dir = ">"
        #RIGHT
        elif (self.gst_guard_position.s_dir == ">"):
            st_coordinate.n_x = self.gst_guard_position.n_x +1
            st_coordinate.n_y = self.gst_guard_position.n_y
            st_coordinate.s_dir = "v"
        #DOWN
        elif (self.gst_guard_position.s_dir == "v"):
            st_coordinate.n_x = self.gst_guard_position.n_x
            st_coordinate.n_y = self.gst_guard_position.n_y +1
            st_coordinate.s_dir = "<"
        #LEFT
        elif (self.gst_guard_position.s_dir == "<"):
            st_coordinate.n_x = self.gst_guard_position.n_x -1
            st_coordinate.n_y = self.gst_guard_position.n_y
            st_coordinate.s_dir = "^"
        else:
            logging.error("ERROR: Invalid guard direction: {self.gst_guard_position.s_dir}")
        st_coordinate.show_position()
        return st_coordinate

    def simulate(self):
        """
        Simulate the path of the guard
        RULE:
        -directions are ^>v<
        -guard advance 1 in the direction if there are no obstacles
        -guard turn 90° to the right if there are obstacles
        """
        
        lst_path = [self.gst_guard_position.get_xyd()]

        b_continue = True
        while b_continue:
            #where is the guard looking?
            st_coordinate = self.compute_position_in_front_of_the_guard()
            #is the position OOB?
            if self.is_oob(st_coordinate):
                logging.debug("guard is OOB")
                #The guard left the room. End.
                b_continue = False
            #is there an obstacle in that position?
            elif (st_coordinate.get_xy() in self.gd_obstacle):
                logging.debug("guard found obstacle, turn right")
                #the guard turns right
                self.gst_guard_position.s_dir = st_coordinate.s_dir
            #no obstacles
            else:
                logging.debug("guard moves forward")
                #the gurad moves forward
                self.gst_guard_position.n_x = st_coordinate.n_x
                self.gst_guard_position.n_y = st_coordinate.n_y
            lst_path.append(self.gst_guard_position.get_xyd())

        logging.info(f"Path length: {len(lst_path)} | Path: {lst_path}")
        self.gltn_patrol_path = lst_path
        return False #OK

    def count_unique_cell_visited(self) -> bool:
        """
        Given a guard path, count the number of unique cells visited
        """
        #create a dictionary of visited cells
        d_patrol_cell = dict()
        #for each coordinate visited by the guard
        for n_index, tn_xyd in enumerate(self.gltn_patrol_path):
            #extract XY and get rid of direction
            tn_xy = (tn_xyd[0],tn_xyd[1])
            #if coordinate is new
            if (tn_xy not in d_patrol_cell):
                #save the index where this coordinate appeared
                d_patrol_cell[tn_xy] = [n_index]
            else:
                #append coordinate
                d_patrol_cell[tn_xy].append(n_index)

        n_unique_cells = len(d_patrol_cell.keys())

        logging.info(f"Unique Cells: {n_unique_cells} | Cells: {d_patrol_cell}")

        return False #OK



#--------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#--------------------------------------------------------------------------------------------------------------------------------

# Example usage
gs_filename_output = 'day06\day_6_map_output.txt'
gs_filename_example = 'day06\day_6_map_example.txt'
gs_filename = 'day06\day_6_map.txt'
#   if interpreter has the intent of executing this file
if __name__ == "__main__":
    logging.basicConfig(
        filename='day06\day_6.log',
        # Specify the log file name
        level=logging.DEBUG,
        # Set the level of debug to show
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin") 

    cl_patrol = Patrol_route()
    #cl_patrol.load_map_from_file(gs_filename_example)
    cl_patrol.load_map_from_file(gs_filename)
    cl_patrol.simulate()
    cl_patrol.count_unique_cell_visited()
    #works for example
    #[2024-12-07 14:15:46,472] INFO day_6:292 > Unique Cells: 41 | Cells: {(4, 6): [0, 21], (4, 5): [1], (4, 4): [2, 29], (4, 3): [3], (4, 2): [4], (4, 1): [5, 6], (5, 1): [7], (6, 1): [8], (7, 1): [9], (8, 1): [10, 11], (8, 2): [12], (8, 3): [13], (8, 4): [14], (8, 5): [15], (8, 6): [16, 17], (7, 6): [18], (6, 6): [19, 34], (5, 6): [20], (3, 6): [22], (2, 6): [23, 24], (2, 5): [25], (2, 4): [26, 27], (3, 4): [28], (5, 4): [30], (6, 4): [31, 32], (6, 5): [33], (6, 7): [35, 50], (6, 8): [36, 37], (5, 8): [38], (4, 8): [39], (3, 8): [40], (2, 8): [41], (1, 8): [42, 43], (1, 7): [44, 45], (2, 7): [46], (3, 7): [47], (4, 7): [48], (5, 7): [49], (7, 7): [51, 52], (7, 8): [53], (7, 9): [54, 55]} 
    #SUCCESS PART 1
    #Unique Cells: 4656


