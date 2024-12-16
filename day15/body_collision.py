#------------------------------------------------------------------------------------------------------------------------------
#   Body_collision
#------------------------------------------------------------------------------------------------------------------------------
#   Meant as base class for physics simulation
#   Stores generic Body objects, allowing this class to be extended by all kind of simulations

#------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#------------------------------------------------------------------------------------------------------------------------------

import logging

from typing import Set, Dict, List, Tuple

import itertools 

#------------------------------------------------------------------------------------------------------------------------------
#   BOX
#------------------------------------------------------------------------------------------------------------------------------

class Box:
    """
    Stores a box.
    Internally uses center and size representation.
    Provides methods to set and retrieve box properties with different offsets for flexibility.
    """

    # Type of the body
    gs_type: str = str()
    # Center of the box
    gtnn_center: Tuple[float, float] = (0, 0)
    # Size of the box (width, height)
    gtnn_size: Tuple[float, float] = (0, 0)
    # Buffered motion. `apply()` will make the new center permanent. `discard()` will clear any motion.
    # This is meant to allow the caller to test positions.
    gtnn_center_next: Tuple[float, float] = (0, 0)

    def is_invalid(self) -> bool:
        """
        Determines if the box dimensions are invalid.
        A box is invalid if its size is negative in any dimension.

        Returns:
            bool: True if the box is invalid, False otherwise.
        """
        if (self.gtnn_size[0] <= 0) or (self.gtnn_size[1] <= 0):
            logging.error(f"Invalid box dimensions {self.gtnn_size}")
            return True  # FAIL
        return False  # OK

    def get_top_left(self) -> Tuple[float, float]:
        """
        Compute the top left corner
        """
        return (self.gtnn_center[0]-self.gtnn_size[0]* 0.5, self.gtnn_center[1]-self.gtnn_size[1]* 0.5)


    def set_center_size(self, itnn_center: Tuple[float, float], itnn_size: Tuple[float, float], is_type: str) -> bool:
        """
        Sets the box using center and size.

        Args:
            itnn_center (Tuple[float, float]): The center of the box (x, y).
            itnn_size (Tuple[float, float]): The size of the box (width, height).
            is_type (str): The type of the box.

        Returns:
            bool: True if the resulting box is invalid, False otherwise.
        """
        self.gtnn_center = itnn_center
        self.gtnn_size = itnn_size
        self.gtnn_center_next = itnn_center  # Initialize next center as the current center
        self.gs_type = is_type
        return self.is_invalid()

    def set_top_left_size(self, itnn_top_left: Tuple[float, float], itnn_size: Tuple[float, float], is_type: str) -> bool:
        """
        Sets the box using top-left corner and size.

        Args:
            itnn_top_left (Tuple[float, float]): The top-left corner of the box (x, y).
            itnn_size (Tuple[float, float]): The size of the box (width, height).
            is_type (str): The type of the box.

        Returns:
            bool: Always returns False (box validity is not checked here).
        """
        # Compute center by adding half the size to the top-left corner
        tnn_center = (itnn_top_left[0]+itnn_size[0]* 0.5, itnn_top_left[1]+itnn_size[1]* 0.5)
        self.gtnn_center = tnn_center
        self.gtnn_size = itnn_size
        self.gtnn_center_next = tnn_center  # Initialize next center as the current center
        self.gs_type = is_type
        return False  # OK

    def set_top_left_bot_right(self, itnn_top_left: Tuple[float, float], itnn_bot_right: Tuple[float, float], is_type: str) -> bool:
        """
        Sets the box using top-left and bottom-right corners.

        Args:
            itnn_top_left (Tuple[float, float]): The top-left corner of the box (x, y).
            itnn_bot_right (Tuple[float, float]): The bottom-right corner of the box (x, y).
            is_type (str): The type of the box.

        Returns:
            bool: True if the resulting box is invalid, False otherwise.
        """
        # Compute size as the difference between bottom-right and top-left
        tnn_size = (itnn_bot_right[0] - itnn_top_left[0], itnn_bot_right[1] - itnn_top_left[1])
        # Compute center as the midpoint between top-left and bottom-right
        tnn_center = (itnn_top_left[0]+tnn_size[0]* 0.5, itnn_top_left[1]+tnn_size[1]* 0.5)
        self.gtnn_center = tnn_center
        self.gtnn_size = tnn_size
        self.gtnn_center_next = tnn_center  # Initialize next center as the current center
        self.gs_type = is_type
        return self.is_invalid()

    def is_colliding(self, it_other: "Box") -> bool:
        """
        Checks if this box is colliding with another box.
        Two boxes are considered colliding if their boundaries overlap.

        Args:
            it_other (Box): Another box to check for collision.

        Returns:
            bool: True if the boxes collide, False otherwise.
        """
        # Calculate half-dimensions of self and other box
        tnn_half_size_self = (self.gtnn_size[0] / 2, self.gtnn_size[1] / 2)
        tnn_half_size_other = (it_other.gtnn_size[0] / 2, it_other.gtnn_size[1] / 2)

        # Extract centers for comparison
        tnn_center_self = self.gtnn_center
        tnn_center_other = it_other.gtnn_center

        # Check overlap along x-axis
        b_overlap_x = abs(tnn_center_self[0] - tnn_center_other[0]) < (tnn_half_size_self[0] + tnn_half_size_other[0])
        # Check overlap along y-axis
        b_overlap_y = abs(tnn_center_self[1] - tnn_center_other[1]) < (tnn_half_size_self[1] + tnn_half_size_other[1])

        # Collide if both x and y overlap
        return b_overlap_x and b_overlap_y

    def is_colliding_next(self, it_other: "Box") -> bool:
        """
        Checks if this box is colliding with another box based on its buffered motion (gtnn_center_next).
        Two boxes are considered colliding if their boundaries overlap.

        Args:
            it_other (Box): Another box to check for collision.

        Returns:
            bool: True if the boxes collide in their next positions, False otherwise.
        """
        # Calculate half-dimensions of self and other box
        tnn_half_size_self = (self.gtnn_size[0] / 2, self.gtnn_size[1] / 2)
        tnn_half_size_other = (it_other.gtnn_size[0] / 2, it_other.gtnn_size[1] / 2)

        # Extract next centers for comparison
        tnn_center_self_next = self.gtnn_center_next
        tnn_center_other = it_other.gtnn_center_next

        # Check overlap along x-axis
        b_overlap_x = abs(tnn_center_self_next[0] - tnn_center_other[0]) < (tnn_half_size_self[0] + tnn_half_size_other[0])
        # Check overlap along y-axis
        b_overlap_y = abs(tnn_center_self_next[1] - tnn_center_other[1]) < (tnn_half_size_self[1] + tnn_half_size_other[1])

        # Collide if both x and y overlap
        return b_overlap_x and b_overlap_y

    def is_moving(self)->bool:
        """
        Returns true if the next position is not the same as current position
        It means someone is trying to move it, waiting for apply()
        """
        return self.gtnn_center_next != self.gtnn_center


    def move(self, itnn_move_distance : Tuple[float, float] ) -> bool:
        """
        Increase the next position by the move distance
        """

        self.gtnn_center_next = (self.gtnn_center_next[0] +itnn_move_distance[0], self.gtnn_center_next[1] +itnn_move_distance[1])

        return False #OK

    def apply(self) -> bool:
        """
        Applies the buffered motion by assigning `gtnn_center_next` to `gtnn_center`.
        This makes the next position permanent.
        """

        if (self.gtnn_center != self.gtnn_center_next):
            self.gtnn_center = self.gtnn_center_next
            return True #UPDATED
        return False #NOT UPDATED
        

    def discard(self) -> bool:
        """
        Discards the buffered motion by assigning `gtnn_center` back to `gtnn_center_next`.
        This clears the next position.
        """
        if (self.gtnn_center_next != self.gtnn_center):
            self.gtnn_center_next = self.gtnn_center
            return True #DISCARDED
        return False

    def __repr__(self) -> str:
        """
        Provides a string representation of the box for debugging.

        Returns:
            str: A string describing the box's current center, next center, size, and type.
        """
        return (
            f"Center {self.gtnn_center} | Next Center {self.gtnn_center_next} "
            f"| Size {self.gtnn_size} | Type {self.gs_type}"
        )

#------------------------------------------------------------------------------------------------------------------------------
#   CLASS
#------------------------------------------------------------------------------------------------------------------------------


"""
Data structure.
dict():
Using position as KEY has the issue that possition is immutable. Moving an item means deleting and adding a new one
I could do a combination of body ID and body name. Using object ID as KEY is just doing list() but worse

list():
I can use a list of Body structure

"""

class Body_collision:
    """
    Base class for physics simulation
    Handles a dictionary of bodies
    Key is the XY coordinate
    Box
    """


    def __init__(self):
        #list of boxes that make the field
        self.glst_field : List[Box] = list()
        #list of boxes inside the field
        self.glst_boxes : List[Box] = list()
        pass

    def is_box_id_invalid(self, in_id : int) -> bool:
        if in_id >= len(self.glst_boxes):
            logging.error(f"Trying to access box OOB {in_id} | Limit {len(self.glst_boxes)}")
            return True #FAIL
        return False #OK
    
    def add_field_top_left_size(self,  itnn_top_left : Tuple[float, float], itnn_size : Tuple[float, float] , is_name : str ) -> Tuple[bool, int]:
        """
        Add a field to the body collision
        """

        cl_box = Box()
        b_fail = cl_box.set_top_left_size( itnn_top_left, itnn_size, is_name )
        if b_fail:
            logging.error(f"Failed to set field: {cl_box}")
            return True # Error
        n_box_index = len(self.glst_field)
        #add the box to the fields
        self.glst_field.append( cl_box )
        if (n_box_index+1 != len(self.glst_field)):
            logging.error(f"Append did not increase index {len(self.glst_field)} | Expected: {n_box_index+1}")
            return True # Error

        return False, n_box_index # Error
        
    def add_box_center_size(self,  itnn_center : Tuple[float, float], itnn_size : Tuple[float, float] , is_name : str) -> Tuple[bool, int]:
        """
        Add a field to the body collision
        """

        cl_box = Box()
        b_fail = cl_box.set_center_size( itnn_center, itnn_size, is_name )
        if b_fail:
            logging.error(f"Failed to set field: {cl_box}")
            return True # Error
        n_box_index = len(self.glst_boxes)
        #add the box to the fields
        self.glst_boxes.append( cl_box )
        if (n_box_index+1 != len(self.glst_boxes)):
            logging.error(f"Append did not increase index {len(self.glst_boxes)} | Expected: {n_box_index+1}")
            return True # Error

        return False, n_box_index # Error

    def get_box(self, in_id : int ) -> Tuple[bool,Box]:
        if self.is_box_id_invalid(in_id):
            logging.error(f"Box ID {in_id} invalid")
            return True, Box()
        return False, self.glst_boxes[in_id]

    def get_types(self, iln_ids : List[int] ) -> Tuple[bool, Dict[str, int] ]:
        """
        Given a list of box IDs
        Return a dictionary with the types in those IDs, and the number of those types
        
        """

        d_id_type = dict()

        for n_id in iln_ids:
            if self.is_box_id_invalid(n_id):
                logging.error(f"Box ID {n_id} invalid")
                return True, dict() #ERROR
            s_type = self.glst_boxes[n_id].gs_type
            if s_type not in d_id_type:
                d_id_type[s_type] = 1
            else:
                d_id_type[s_type] += 1

        return False, d_id_type #OK

    def get_boxes(self) -> List[Box]:
        return self.glst_boxes

    def move( self, in_id : int, itnn_move_distance : Tuple[float, float] ) -> bool:
        """
        Move box ID by the given distance
        """
        if self.is_box_id_invalid(in_id):
            logging.error(f"Box ID {in_id} invalid")
            return True #FAIL
        b_fail = self.glst_boxes[in_id].move(itnn_move_distance)
        if b_fail:
            logging.error(f"ERROR: failed to move ID {in_id} by {itnn_move_distance}")

        return False #OK

    def detect_box_collision( self, in_id : int ) -> List[int]:
        """
        detect collision of this box against all other boxes
        return a list of all detected collisions
        empty list means no collisions detected
        """

        if self.is_box_id_invalid(in_id):
            logging.error(f"Box ID {in_id} invalid")
            return True #FAIL

        cl_box = self.glst_boxes[in_id]
        ln_collision_id : List[int] = list()

        for n_target_id in range(len(self.glst_boxes)):
            if n_target_id == in_id:
                pass
            else:
                b_collides = cl_box.is_colliding_next( self.glst_boxes[n_target_id] )
                if b_collides:
                    ln_collision_id.append(n_target_id)

        return ln_collision_id
    
    def detect_collision(self) -> List[int]:
        """
        detect everything that is colliding with something
        """
        ln_collision_id : List[int] = list()
        #for each unique pair of IDs
        for n_id_a, n_id_b in itertools.permutations(range(len(self.glst_boxes)),2):
            if self.glst_boxes[n_id_a].is_colliding_next( self.glst_boxes[n_id_b] ):
                if n_id_a not in ln_collision_id:
                    ln_collision_id.append(n_id_a)
                if n_id_b not in ln_collision_id:
                    ln_collision_id.append(n_id_b)
        return ln_collision_id
    
    def apply(self) -> int:
        """
        ask the boxes to update their position
        return the number of boxes that have been updated
        """
        ln_id_updated = list()
        n_updated = 0
        for n_index, cl_box in enumerate(self.glst_boxes):
            b_updated = cl_box.apply()
            if b_updated:
                n_updated += 1
                ln_id_updated.append(n_index)

        logging.info(f"Apply: {len(ln_id_updated)} | ID: {ln_id_updated}")
        return n_updated

    def discard(self) -> int:
        """
        ask the boxes to update their position
        return the number of boxes that have been updated
        """
        ln_id_updated = list()
        n_discarded = 0
        for n_index,cl_box in enumerate(self.glst_boxes):
            b_updated = cl_box.discard()
            if b_updated:
                n_discarded += 1
                ln_id_updated.append(n_index)
        logging.info(f"Discard: {len(ln_id_updated)} | ID: {ln_id_updated}")
        return n_discarded
    
    def show_position(self) -> bool:
        for n_id, cl_box in enumerate(self.glst_boxes):
            logging.info(f"ID: {n_id} | Box: {cl_box}")

