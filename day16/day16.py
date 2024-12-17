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

class Labirinth:
    class Agent:
        #agent always start ooking east
        gs_name = ""
        gs_symbol = '>'
        gs_dir = '>'
        gtnn_position : Tuple[int, int] = (-1,-1)

        def set( self, is_name : str, is_symbol : str, is_dir: str, itnn_start : Tuple[int, int] ) -> bool:
            self.gs_name = is_name
            self.gs_symbol = is_symbol
            self.gs_dir = is_dir
            self.gtnn_position = itnn_start
            return False #OK
        
        def __repr__(self):
            return f"Name: {self.gs_name} | Position: {self.gtnn_position} | Direction: {self.gs_dir}"

    def __init__(self):
        #labirinth symbol map
        self.gcl_map = Map_of_symbols()
        self.cs_wall = '#'
        self.cs_void = '.'
        #labirinth number map
        self.cn_wall = -1
        self.cn_void = 0
        #agent
        self.st_agent = self.Agent()
        self.st_agent.set("Start",">",">",(-1,-1))
        self.st_goal = self.Agent()
        self.st_goal.set("Goal","+",">",(-1,-1))

    def load_from_file( self, is_filename : str ) -> bool:
        #Load Map
        b_fail = self.gcl_map.load_map_from_file(is_filename)
        if b_fail:
            logging.error(f"ERROR: could not load labirinth from file {is_filename}")
            return True #FAIL

        #Load Agent Start
        b_fail, ltnn_start = self.gcl_map.find_symbol(self.st_agent.gs_symbol)
        if b_fail or len(ltnn_start) != 1:
            logging.error(f"ERROR: agent not found")
            return True #FAIL
        else:
            tnn_start = ltnn_start[0]
            self.st_agent.gtnn_position = tnn_start
            #replace symbol with void
            b_fail = self.gcl_map.set_coordinate( tnn_start, self.cs_void )
            logging.info(f"Agent {self.st_agent}")

        #Load Goal End
        b_fail, ltnn_goal = self.gcl_map.find_symbol(self.st_goal.gs_symbol)
        if b_fail or len(ltnn_goal) != 1:
            logging.error(f"ERROR: goal not found")
            return True #FAIL
        else:
            tnn_goal = ltnn_goal[0]
            self.st_goal.gtnn_position = tnn_goal
            #replace symbol with void
            b_fail = self.gcl_map.set_coordinate( tnn_goal, self.cs_void )
            logging.info(f"Goal {self.st_goal}")

        self.gcl_map.show_map()
        
        return False #OK
    
    def translate_symbols_to_int(self) -> bool:
        """
        I need to translate the map for the coloring algorithm
        -1 means impassable
        0 means uncolored
        1 and above are colors that will be painted by the algorithm
        """

        #build translation
        d_translate_symbol_to_int = dict()
        d_translate_symbol_to_int[self.cs_wall] = -1
        d_translate_symbol_to_int[self.cs_void] = 0
        #scan the map
        for tnn_cursor in self.gcl_map:
            #fetch existing symbol
            b_fail, s_symbol = self.gcl_map.get_coordinate( tnn_cursor )
            if b_fail:
                logging.error(f"ERROR: cannot read {tnn_cursor}")
                return True #FAIL
            if s_symbol not in d_translate_symbol_to_int:
                logging.error(f"ERROR: symbol {s_symbol} not in translation {d_translate_symbol_to_int}")
                return True #FAIL
            n_value = d_translate_symbol_to_int[s_symbol]
            b_fail = self.gcl_map.set_coordinate( tnn_cursor, n_value )
            if b_fail:
                logging.error(f"ERROR: cannot write {tnn_cursor} {n_value}")
                return True #FAIL
        logging.info("Translate map from string to int")
        self.gcl_map.show_map()
        return False #OK

    def color_labirinth(self) -> bool:
        """
        The agent is placed in the start
        Available moves are executed, coloring the tiles with their cost
        adjacency is 4 connect
        cost is 1000 for a rotation
        cost is 1 for moving
        use a queue
        """

        class Token:
            """
            My queue needs to know the orientation going in
            """
            gtnn_pos : Tuple[int,int] = (-1,-1)
            gs_dir : str = '>'
            gn_score : int = 0

        lst_queue_of_tokens = List[Token] = list()

        #build first token
        st_token = Token()
        st_token.gtnn_pos = self.st_agent.gtnn_position
        st_token.gs_dir = self.st_agent.gs_dir
        st_token.gn_score = 1
        #push the first token inside the queue
        lst_queue_of_tokens.append( st_token )
        
        #Token processor
        b_continue = True
        while b_continue == True:
            #queue is empty
            if len(lst_queue_of_tokens) < 0:
                b_continue = False
            else:
                #get the next token from the front
                st_token : Token = lst_queue_of_tokens.pop(0)
                #write down the score
                self.gcl_map.set_coordinate(st_token.gtnn_pos, 1)
                


        


        #get 
        ltnn_four_connect = self.gcl_map.get_four_connect( self.st_agent.gtnn_position )
        for tnn_four_connect in ltnn_four_connect:
            b_fail, n_value = self.gcl_map.get_coordinate(tnn_four_connect)
            if b_fail == True:
                logging.error(f"ERROR: cannot read {tnn_four_connect}")
                return True #FAIL
            #do not propagate into walls
            if n_value == self.cn_wall:
                pass
            #if it's the first time the tile is colored
            elif n_value == self.cn_void:
                self.gcl_map.set_coordinate(tnn_four_connect, n_value+1)

        logging.debug(f"{ltnn_four_connect}")
        self.gcl_map.show_map()


        return False #OK



    def find_agent(self) -> bool:
        """
        The agent is looking east
        """



        return False #OK




#------------------------------------------------------------------------------------------------------------------------------
#   SOLUTION
#------------------------------------------------------------------------------------------------------------------------------

def solution() -> bool:

    cl_labirinth = Labirinth()
    b_fail = cl_labirinth.load_from_file("day16/day16-example-15x15.txt")
    if b_fail:
        logging.error(f"ERROR: could not load labirinth from file")
        return True #FAIL
    
    cl_labirinth.translate_symbols_to_int()
    cl_labirinth.color_labirinth()
    

    return False #OK
    return True #FAIL

#------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(
        filename="day16/day16.log",
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin")

    solution()
