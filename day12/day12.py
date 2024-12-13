#------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#------------------------------------------------------------------------------------------------------------------------------

import logging

from typing import Set, Dict, List, Tuple

#import copy

from map_of_symbols import Map_of_symbols

#------------------------------------------------------------------------------------------------------------------------------
#   RULES
#------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------
#   ALGORITHM
#------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------
#   SOLUTION
#------------------------------------------------------------------------------------------------------------------------------

class Farm:
    def __init__(self):
        #
        self.gcl_map = Map_of_symbols()
        #
        self.gld_plots : List[Dict[Tuple[int,int]]] = list()
    
    def load_farm(self, is_filename: str) -> bool:
        b_fail = self.gcl_map.load_map_from_file( is_filename )
        if b_fail:
            logging.error(f"ERROR: failed to load {is_filename}")
        self.gcl_map.show_map()
        return b_fail



    def compute_plots(self) -> bool:
        """
        from a map of symbols
        use a coloring algorithm
        load all adjcent symbols to the dictionary of plot with coordinates
        add processed coordinates to a set to prevent recomputing them
        """

        #list of coordinates that have already been scanned
        dtnn_scanned : Set[Tuple[int,int]] = set()

        #use my map class as iterator to scan all coordinates
        for tnn_coordinate in self.gcl_map:
            #if a coordinate has already been scanned
            if tnn_coordinate in dtnn_scanned:
                #skip it
                pass
            else:
                #find the plot in this coordinate
                b_fail, dtnn_plot = self.process_plot( tnn_coordinate )
                if b_fail:
                    logging.error(f"ERROR: Could not process plot at: {tnn_coordinate}")
                    return True #FAIL
                #all the coordinates found must be exluded from the scan
                for tnn_exclude in dtnn_plot:
                    dtnn_scanned.add(tnn_exclude)
                #save the plot in the list of plots
                self.gld_plots.append(dtnn_plot)

        return False #OK

    def process_plot(self, itnn_start : Tuple[int,int] ) -> Tuple[ bool, Dict[Tuple[int,int], str] ]:
        """
        given a starting coordinate
        find all the symbols adjacent to that coordinate
        and add them to a dictionary
        taking care to list the number of same symbols adjacent to it
        
        """

        if self.gcl_map.is_coordinate_invalid( itnn_start ):
            logging.error(f"ERROR: Coordinate {itnn_start} is invalid")
            return True, dict() #FAIL
        #symbol common to all coordinates in the plot
        b_fail, s_plot_type = self.gcl_map.get_coordinate( itnn_start )
        if b_fail:
            logging.error(f"ERROR: Failed to get symbol {itnn_start}")
            return True, dict() #FAIL
        #dictionary of plot coodinates
        dtnn_plot : Dict[Tuple[int,int], str] = dict()
        #queue of coordinates
        ltnn_coordinate_queue : List[Tuple[int,int]] = list()
        #add the starting coordinate to the list of coordinates to be tested
        ltnn_coordinate_queue.append(itnn_start)
        logging.debug(f"Processing plot symbol >{s_plot_type}< starting from {itnn_start}")
        #while there are coordinates that are candidate to be part of the plot
        while len(ltnn_coordinate_queue) > 0:
            #get the next coordinate
            tnn_candidate = ltnn_coordinate_queue.pop()
            #find all the four connect to that coordinate
            b_fail, ltnn_four_connect = self.gcl_map.find_four_connect( tnn_candidate, s_plot_type )
            if b_fail:
                logging.error(f"ERROR: Failed four connect at coordinate {tnn_candidate}")
            #four connect is number of neighbours
            n_neighbour = len(ltnn_four_connect)
            #add the popped symbol to the plot
            dtnn_plot[tnn_candidate] = n_neighbour
            #scan all the four connect symbols found
            for tnn_four_connect in ltnn_four_connect:
                #if the coordinate is already in the dictionary, do not add it
                if tnn_four_connect in dtnn_plot:
                    pass
                else:
                    #add that symbol to the processing queue
                    ltnn_coordinate_queue.append(tnn_four_connect)
        logging.info(f"Plot Symbol: {s_plot_type} | Plot size: {len(dtnn_plot)}")
        logging.info(f"Plot:\n{dtnn_plot}")
        return False, dtnn_plot
    
    def compute_fence_price( self ):
        """
        I have a list of dictionaries
        holding the coordinate of the plot with their neighbour
        The price is PLOT.AREA * PLOT.PERIMETER
        PLOT.AREA = number of keys in the dictionary
        PLOT.PERIMETER is smart. each plot has 4-neighbour as perimeter :3
        """
        n_total_price = 0
        for dtnn_plot in self.gld_plots:
            n_area = len(dtnn_plot)
            #for all coordinates
            n_perimeter_total = 0
            for tnn_coordinate in dtnn_plot:
                n_perimeter = 4 -dtnn_plot[tnn_coordinate]
                n_perimeter_total += n_perimeter

            n_price = n_area*n_perimeter_total
            n_total_price += n_price

            logging.info(f"Plot Area: {n_area} | Plot Perimeter: {n_perimeter_total} | Fence Price {n_price}")

        logging.info(f"Total Fence Price: {n_total_price}")

#------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(
        filename="day12/day12.log",
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin")

    cl_farm = Farm()
    #cl_farm.load_farm("day12/day12-example-4x4.txt")
    #cl_farm.load_farm("day12/day12-example-5x5.txt")
    cl_farm.load_farm("day12/day12-data.txt")
    cl_farm.compute_plots()
    cl_farm.compute_fence_price()
    