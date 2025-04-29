from othello import Othello
import copy
SIZE = 8

# Heuristic: 
def greedy_policy():
    return pick_move
    
def pick_move(pos):    
        #Player 1, Black
        if pos.actor() == 1:
            max_value = float('-inf')
            max_action = None

            #Check all possible squares for moves
            for row in range(SIZE):
                for col in range(SIZE):
                    #Squares to flip if we chose action (row, col)
                    flips = pos.retrieve_flips((row, col))
                    new_state = copy.deepcopy(pos)
                    new_state.update_state((row, col), flips)
                    
                    #If this was a valid move
                    if flips != []:
                        h = pos.heuristic()
                        if h > max_value:
                            max_value = h
                            max_action = (row, col)
            return max_action
        #Player 2, White
        elif pos.actor() == 2:
            min_value = float('inf')
            min_action = None
            
            #Check all possible squares for moves
            for row in range(SIZE):
                for col in range(SIZE):
                    flips = pos.retrieve_flips((row, col))
                    # print(flips)
                    new_state = copy.deepcopy(pos)
                    new_state.update_state((row, col), flips)
                    
                    if flips != []:
                        h = pos.heuristic()
                        if h < min_value:
                            min_value = h
                            min_action = (row, col)
                            # min_flips = flips
            return min_action