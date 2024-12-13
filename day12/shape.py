"""
This library is designed to operate on dictionaries of coordinates
Dict[Tuple[int, int], str]
Dict[Tuple[int, int], int]

It does topological operations on such list of coordinates
"""
import logging
from typing import Set, Dict, List, Tuple

class Shape:
    def __init__(self):
        self.cs_cardinal = "NESW"
        #shape parameters
        self.gn_area = 0
        self.gn_perimeter = 0
        self.gn_sides = 0
        #list of coordinates
        self.gdtnn_coordinates : Set[Tuple[int, int]] = set()
        self.gdtnns_walls : Set[Tuple[int, int, str]] = set()
        self.gdtnns_sides : Set[Tuple[Tuple[int, int],Tuple[int, int], str]] = set()

    def load_shape( self, iltnn_coordinates: List[Tuple[int, int]], ib_debug = True ) -> bool:
        """
        given a list of coordinates
        fill an internal set of coordinates
        """
        for tnn_coordinate in iltnn_coordinates:
            self.gdtnn_coordinates.add(tnn_coordinate)

        self.gn_area += len( self.gdtnn_coordinates)
        #TODO: detect four connect adjacency of all coordinates
        logging.debug(f"Imported {len(self.gdtnn_coordinates)} coordinates")
        logging.debug(f"{self.gdtnn_coordinates}")
        self.compute_walls()
        self.compute_sides()
        return False #OK
    
    def is_adjacent( self, itnn_a : Tuple[int, int], itnn_b : Tuple[int, int], b_debug = False) -> bool:
        n_distance = abs(itnn_a[0]-itnn_b[0])+abs(itnn_a[1]-itnn_b[1])
        if b_debug:
            logging.debug(f"A: {itnn_a} B: {itnn_b} Distance: {n_distance}")
        if n_distance == 1:
            return True
        else:
            return False

    def get_stats(self):
        return (self.gn_area, self.gn_perimeter, self.gn_sides)

    def compute_coordinate_cardinal( self, itnn_coordinate : Tuple[int, int], is_cardinal : str ) -> Tuple[bool, Tuple[int, int]]:
        """
        Given a coordinate
        Given a cardinal direction
        Compute the coordinate of that cardinal direction
        """

        (n_y, n_x) = itnn_coordinate
        if is_cardinal == 'N':
            return False, (n_y-1, n_x)
        elif is_cardinal == 'S':
            return False, (n_y+1, n_x)
        elif is_cardinal == 'E':
            return False, (n_y, n_x+1)
        elif is_cardinal == 'W':
            return False, (n_y, n_x-1)
        logging.error(f"invalid cardinal direction: {is_cardinal}")
        return True, (-1,-1) #FAIL

    def compute_walls(self) -> bool:
        """
        Given a list of coordinates, I want to compute all walls
        A wall is a tuple (Y, X, DIRECTION)
        with direction being North, East, South, West
        """

        #scan all coordinates of the shape
        for tnn_coordinate in self.gdtnn_coordinates:
            for s_cardinal in self.cs_cardinal:
                b_fail, tnn_coordinate_cardinal = self.compute_coordinate_cardinal(tnn_coordinate, s_cardinal)
                if b_fail:
                    logging.error(f"ERROR: failed to compute cardinal {tnn_coordinate} {s_cardinal}")
                    return True #FAIL
                #if the cardinal is within the shape
                if tnn_coordinate_cardinal in self.gdtnn_coordinates:
                    #this is NOT a wall
                    pass
                else:
                    self.gdtnns_walls.add( (tnn_coordinate[0], tnn_coordinate[1], s_cardinal) )
            
        logging.debug(f"Number of walls: {len(self.gdtnns_walls)}")
        logging.debug(f"Walls: {self.gdtnns_walls}")
        return False #OK

    def compute_sides(self) -> bool:
        """
        Given a list of walls YXD
        I want to group walls by their direction
        I want to group walls by their adjacency
        What's left is the list of sides
        """
        #separate walls by their cardinal direction, and strip the direction from the coordinate
        ds_cardinal : Dict[ str, Set[Tuple[int,int]]]= dict()
        #for each cardinal direction
        for s_cardinal in self.cs_cardinal:
            #allocate a set of coordinates
            ds_cardinal[s_cardinal] = set()

        #for each wall
        for tnn_wall in self.gdtnns_walls:
            #strip cardinal and put it in the dictionary of walls
            ds_cardinal[ tnn_wall[2] ].add( (tnn_wall[0], tnn_wall[1]) )

        logging.debug(f"Group walls: {ds_cardinal}")

        #Now that walls are grouped by their cardinal direction
        #I find all sides
        #A side is has a starting coordinate, an end coordinate, and a cardinal direction
        #I just need for each coordinate to find all adjacent and take that out from the set
        #when the set is empty, I created all walls

        #for each cardinal direction
        for s_cardinal in self.cs_cardinal:
            #get all the coordinates with a wall on that cardinal direction
            dtnn_wall = ds_cardinal[s_cardinal]
            #using clustering, I can find a list of walls adjacent to each others
            ldtnn_wall_adjacent = self.cluster_adjacent_coordinates(dtnn_wall)

            #TODO: I need to build a list of walls

            self.gn_sides += len(ldtnn_wall_adjacent)

        logging.debug(f"Sides: {self.gn_sides}")
        return False #OK


    def cluster_adjacent_coordinates(self, dtnn_coordinates : Set[Tuple[int, int]] ) -> List[Set[Tuple[int, int]]]:
        """
        Give a set of coordinates
        Return a list of sets of coordinates that are all adjacent in four connect

        
        Algorithm:
        pop a coordinate and put it in the first cluster
            Look for adjacent to an existing cluster
        when i find no adjacent
        pop a coordinate and create a new cluster


        """
        #create a list of sets (cluster)
        ldtnn_clusters = list()

        #startup: pop one coordinate and start the first cluster
        tnn_candidate = dtnn_coordinates.pop()
        dtnn_cluster : Set[Tuple[int, int]] = set()
        dtnn_cluster.add(tnn_candidate)
        
        b_continue = True
        #while I have coordinates to cluster
        while b_continue:
            ltnn_adjacent = list()
            #for all coordinates in the cluster
            for tnn_cluster_coordinate in dtnn_cluster:
                #for all coordinates that need to be clustered
                for tnn_coordinate_to_be_clustered in dtnn_coordinates:
                    #find all adjacents
                    if self.is_adjacent( tnn_cluster_coordinate, tnn_coordinate_to_be_clustered):
                        ltnn_adjacent.append(tnn_coordinate_to_be_clustered)
            logging.debug(f"Adjacents fund: {len(ltnn_adjacent)} | {ltnn_adjacent}")
            #if at least one adjacent coordinate was found
            if len(ltnn_adjacent) > 0:
                #now remove the coordinates to be clustered from the set and add them to the cluster
                for tnn_coordinate in ltnn_adjacent:
                    dtnn_coordinates.remove(tnn_coordinate)
                    dtnn_cluster.add(tnn_coordinate)
                #special case. If this has zeroed the cluster, I need to add the cluster to the list of found clusters
                if (len(dtnn_coordinates) == 0):
                    ldtnn_clusters.append(dtnn_cluster)
                    b_continue = False
            #add the cluster to the list of clusters and there are more coordinates
            elif len(dtnn_coordinates) > 0:
                ldtnn_clusters.append(dtnn_cluster)
                #pop next coordinate
                tnn_candidate = dtnn_coordinates.pop()
                #start a new cluster
                dtnn_cluster = set()
                dtnn_cluster.add(tnn_candidate)
                logging.debug(f"Start new cluster: {dtnn_cluster}")
            #this cluster closes the search
            else:
                ldtnn_clusters.append(dtnn_cluster)
                b_continue = False

        logging.debug(f"Found {len(ldtnn_clusters)} clusters")
        logging.debug(f"{ldtnn_clusters}")

        return ldtnn_clusters
