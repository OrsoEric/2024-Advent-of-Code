#------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#------------------------------------------------------------------------------------------------------------------------------

import logging

from typing import Set, Dict, List, Tuple

from map_of_symbols import Map_of_symbols

class Labirinth:
    class Agent:
        #agent always start ooking east
        gs_name = ""
        gs_symbol = '>'
        gn_dir = 1
        gtnn_position : Tuple[int, int] = (-1,-1)

        def set( self, is_name : str, is_symbol : str, is_dir: str, itnn_start : Tuple[int, int] ) -> bool:
            self.gs_name = is_name
            self.gs_symbol = is_symbol
            self.gn_dir = is_dir
            self.gtnn_position = itnn_start
            return False #OK
        
        def __repr__(self):
            return f"Name: {self.gs_name} | Position: {self.gtnn_position} | Direction: {self.gn_dir}"

    def __init__(self):
        #labirinth symbol map
        self.gcl_map = Map_of_symbols()
        self.cs_wall = '#'
        self.cs_void = '.'
        #labirinth number map
        self.cn_wall = 0
        self.cn_void = 1
        #agent
        self.st_agent = self.Agent()
        self.st_agent.set("Start",">",1,(-1,-1))
        self.st_goal = self.Agent()
        self.st_goal.set("Goal","+",1,(-1,-1))
        #COST of moves
        self.cn_price_forward = 1
        self.cn_price_turn = 1000

        self.gn_best_score = -1
        #optimization metrics
        self.gn_stack_max = 0
        self.gn_iterations = 0

    def invert_start_goal(self, in_goal_dir : int)->bool:
        self.st_agent, self.st_goal = self.st_goal, self.st_agent
        self.st_agent.gn_dir = in_goal_dir
        logging.info(f"INVERSION! Agent: {self.st_agent} | Goal: {self.st_goal}")
        return False #OK

    def get_score(self) -> int:
        logging.info(f"Total Iterations: {self.gn_iterations} Maximum Stack: {self.gn_stack_max} Best Score {self.gn_best_score}")
        return self.gn_best_score

    def get_map(self) -> Map_of_symbols:
        """
        Return a copy of the labirinth
        """
        return self.gcl_map

    def set_size(self, in_size : Tuple[int, int] ) -> bool:
        """
        clears and resize the symbol map of the labirinth
        """
        return self.gcl_map.set_size( in_size, self.cs_void )

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
    
    def load_walls_from_list( self, iltnn_walls : List[Tuple[int,int]] ) -> bool:
        """
        From a list of coordinates Y X
        Put walls in the lanbirinth
        """

        b_fail = False
        for tnn_wall in iltnn_walls:
            b_fail |= self.gcl_map.set_coordinate( tnn_wall, self.cs_wall )
        if b_fail:
            logging.error(f"ERROR: Failed to load walls {iltnn_walls}")
            return True #FAIL

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
        d_translate_symbol_to_int[self.cs_wall] = self.cn_wall
        d_translate_symbol_to_int[self.cs_void] = self.cn_void
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

    @staticmethod
    def compute_turns( in_arrival_direction : int, in_departing_direction: int ) -> Tuple[bool,int]:
        """
        0(N) 0(N) -> no change
        1(E) 1(E) -> no change
        0(N) 1(E) -> 90°
        1(N) 2(E) -> 90°
        3[W] 1(N) -> 90° !
        
        """
        n_turns = abs(in_arrival_direction -in_departing_direction)
        if n_turns > 2:
            n_turns = 4-n_turns
        return n_turns

    def color_labirinth(self, ib_debug=True) -> bool:
        """
        The agent is placed in the start
        Available moves are executed, coloring the tiles with their cost
        adjacency is 4 connect
        cost is 1000 for a rotation
        cost is 1 for moving
        use a queue
        """

        n_cnt_iterations = 0

        class Token:
            """
            My queue needs to know the orientation going in
            """
            gtnn_pos : Tuple[int,int] = (-1,-1)
            gn_dir : str = '>'
            gn_score : int = 0

            def __repr__(self):
                return f"TOKEN | Position: {self.gtnn_pos} | Direction: {self.gn_dir} | Score: {self.gn_score}"

        lst_queue_of_tokens : List[Token] = list()

        @staticmethod
        def add_best_token_to_queue( ilst_tokens : List[Token], ist_token : Token ):
            """
            given a Token
            I want only the cheapest token in a given coordinate to be present in the queue
            THERE SHOULD BE ONE IF I USE THIS
            """

            b_add = False

            ln_id_same_position : List[int] = list()
            #scan the queue
            for n_index, st_token_in_queue in enumerate(ilst_tokens):
                if st_token_in_queue.gtnn_pos == ist_token.gtnn_pos:
                    #list of IDs with the best position
                    ln_id_same_position.append(n_index)

            n_num_same_position = len(ln_id_same_position)
            #if unique position
            if n_num_same_position == 0:
                #append new token
                ilst_tokens.append(ist_token)
            #if duplicate
            elif n_num_same_position == 1:
                n_id = ln_id_same_position[0]
                #if the token in the queue is WORSE than the token I want to push
                if ilst_tokens[n_id].gn_score > ist_token.gn_score:
                    #remove the worse token
                    del ilst_tokens[n_id]
                    #append new token
                    ilst_tokens.append(ist_token)
                #if I want to add a worse token
                else:
                    #already optimal
                    pass
            else:
                logging.error(f"ERROR: There is more than one duplicate token in the queue. {ilst_tokens}")
                return True #FAIL

            return False #OK

        #GOAL SCORE
        #when I reach the goal, I can safely stop all WRITE operations more expensive then the GOAL
        n_goal_score = -1

        #build first token
        st_token = Token()
        st_token.gtnn_pos = self.st_agent.gtnn_position
        st_token.gn_dir = self.st_agent.gn_dir
        st_token.gn_score = self.cn_void +1
        #push the first token inside the queue
        lst_queue_of_tokens.append( st_token )
        
        #Token processor
        b_continue = True
        while b_continue == True:
            n_stack_size = len(lst_queue_of_tokens)
            if n_stack_size > self.gn_stack_max:
                self.gn_stack_max = n_stack_size
            #queue is empty
            if n_stack_size <= 0:
                #exploration is complete
                b_continue = False
            else:
                #get the next token from the front
                st_token : Token = lst_queue_of_tokens.pop(0)
                if ib_debug:
                    logging.debug(f"PROCESSING: {st_token}")
                #score of the tile being processed
                n_score_origin = st_token.gn_score
                tnn_origin = st_token.gtnn_pos

                #initialize list of four connect
                ltnnn_four_connect_direction = list()

                #IF the goal has been found, and I'm trying to write something more expensive than the goal
                if n_goal_score != -1 and n_score_origin > n_goal_score:
                    #STOP in the track
                    pass
                else:
                    #write down the score
                    self.gcl_map.set_coordinate(tnn_origin, n_score_origin)
                    if ib_debug:
                        logging.debug(f"Tile {tnn_origin} | Color {n_score_origin}") 
                        self.gcl_map.show_map()

                    #If I reached the GOAL
                    if (tnn_origin == self.st_goal.gtnn_position):
                        logging.info(f"Agent reached the GOAL with score: {n_score_origin}")
                        n_goal_score = n_score_origin
                        self.gn_best_score = n_goal_score
                        #DO NOT PROPAGATE FURTHER
                    #I have not reached the goal, keep exploring
                    else:                        
                        #get all adjacent tiles
                        ltnnn_four_connect_direction = self.gcl_map.get_four_connect_direction( st_token.gtnn_pos )

                #scan all adjacent tiles
                for tnnn_four_connect_direction in ltnnn_four_connect_direction:
                    n_y,n_x,n_dir = tnnn_four_connect_direction
                    tnn_four_connect = (n_y,n_x)

                    b_spawn_new_token = False
                    #get the content of the four connect coorinate
                    b_fail, n_score_current = self.gcl_map.get_coordinate(tnn_four_connect)
                    if b_fail == True:
                        logging.error(f"ERROR: cannot read {tnn_four_connect}")
                        return True #FAIL
                    
                    #add 1000 points for each 90° turn
                    n_turns = self.compute_turns( st_token.gn_dir, n_dir )
                    #compute color score of the next four connect tile
                    n_price = self.cn_price_forward + n_turns *self.cn_price_turn
                    n_score_next = n_score_origin +n_price
                    if ib_debug:
                        logging.debug(f"arrival direction: {st_token.gn_dir} | departing direction: {n_dir} | Turns: {n_turns} | Price: {n_price}")
                    #do not reverse direction
                    if n_turns == 2:
                        #no effect, already takes care by score
                        pass
                    #do not propagate into walls
                    elif n_score_current == self.cn_wall:
                        #cannot color walls
                        b_spawn_new_token = False
                        if ib_debug:
                            logging.debug(f"Position {tnn_four_connect} Value {n_score_current} | is a WALL")
                    #if it's the first time the tile is colored
                    elif n_score_current == self.cn_void:
                        #I can color in that direction
                        b_spawn_new_token = True
                        if ib_debug:
                            logging.debug(f"Position {tnn_four_connect} Value {n_score_current} | is a VIRGIN: ADD")
                    #if it's already colored, with a lower number that I'm trying to add
                    elif n_score_next >= n_score_current:
                        #there is a cheaper path to get here
                        b_spawn_new_token = False
                        if ib_debug:
                            logging.debug(f"Position {tnn_four_connect} Value {n_score_current} | is a worse than current {n_score_current}")
                    #I found a cheaper way to get here
                    else:
                        #color in that direction
                        b_spawn_new_token = True
                        if ib_debug:
                            logging.debug(f"Position {tnn_four_connect} Value {n_score_current} | is a BETTER than {n_score_next}, ADD")

                    if b_spawn_new_token:
                        #create a new Token
                        st_new_token = Token()
                        #save the coordinate of that tile
                        st_new_token.gtnn_pos = tnn_four_connect
                        #save the departing direction
                        st_new_token.gn_dir = n_dir
                        #save the score that token will have
                        st_new_token.gn_score = n_score_next
                        #do NOT just add the token to the queue
                        #lst_queue_of_tokens.append(st_new_token)
                        #I need to look for tokens in the same position, and I only need to keep the cheapest
                        b_fail = add_best_token_to_queue( lst_queue_of_tokens, st_new_token)
                        if b_fail:
                            logging.error("ERROR: Failed to add token to queue")
                            return True #FAIL
            #
            n_cnt_iterations += 1
            if n_cnt_iterations%50 == 0 or b_continue == False:
                print(f"iteration: {n_cnt_iterations} stack: {len(lst_queue_of_tokens)} Goal Reached: {self.gn_best_score}")
        #save iterations
        self.gn_iterations = n_cnt_iterations
        #Correct the score to reflect the point system
        for tnn_cursor in self.gcl_map:
            b_fail, n_value = self.gcl_map.get_coordinate(tnn_cursor)
            if n_value == self.cn_wall:
                pass
            #this is a tile that has never been explored
            elif n_value == self.cn_void:
                self.gcl_map.set_coordinate(tnn_cursor,self.cn_wall)
            else:
                n_value = n_value -self.cn_void -self.cn_price_forward
                self.gcl_map.set_coordinate(tnn_cursor,n_value)

        #correct the score
        self.gn_best_score += -self.cn_void -self.cn_price_forward


        return False #OK



    def show_map(self) ->bool:
        self.gcl_map.show_map()
        return False #OK
