from othello import Othello
import time
import sys


heuristic_value = 76

def scout_policy(timeLimit):
    def scout_iterative_deepening(pos):
        start_time = time.time()
        alpha = float('-inf')
        beta = float('inf')
        depth = 2
        move = None
        while(time.time() - start_time < timeLimit):
            #If our acout throws a timeout error, terminate the search
            try:
                #F CHANGE
                value, move = scout(pos, depth, alpha, beta, start_time, timeLimit)
                depth = depth + 1
            except TimeoutError:
                break
            
        #FOR LOGGING PURPOSES (F CHANGE)
        # print(depth)
        # print("scout")
        return move

    #F CHANGE
    def scout(pos, depth, alpha_bound, beta_bound, t_start, t_limit):
        #Check if the time is out each time alpha beta is called
        if time.time() - t_start >= t_limit:
            raise TimeoutError("Time limit exceeded during search.")
        
        if pos.is_terminal():
            return pos.payoff(), None
        
        if depth == 0:
            return pos.heuristic() / heuristic_value, None
        
        alpha = alpha_bound
        beta = beta_bound
        best_move = None

        # order moves from best to worst
        actions = pos.get_actions()
        num_actions = len(actions)
        action_state_pairs = [0 for _ in range(num_actions)]
        for i in range(num_actions):
            next_pos = pos.update_state_move(actions[i])
            action_state_pairs[i] = (actions[i], next_pos)

        sorted_pairs = sorted(action_state_pairs, key=lambda state: state[1].heuristic(), reverse=True)

        if(pos.actor() == 1):
            a = float('-inf')
            first_child = True
            score = None
            for pair in sorted_pairs:
                if alpha >= beta:
                    break 
                if first_child:
                    first_child = False
                    score, move = scout(pair[1], depth - 1, alpha, beta, t_start, t_limit)
                else:
                    #F CHANGE
                    #Making the null window with 1 / heuristic_value
                    score, move = scout(pair[1], depth - 1, alpha, alpha + 1 / heuristic_value, t_start, t_limit)
                    if alpha + 1 <= score <= beta:
                        score, move = scout(pair[1], depth - 1, score, beta, t_start, t_limit)
                if score > a:
                    a = score
                    best_move = pair[0]
                alpha = max(alpha, a)
            return a, best_move
        elif(pos.actor() == 2):
            b = float('inf')
            first_child = True
            score = None
            for pair in sorted_pairs:
                if alpha >= beta:
                    break 
                if first_child:
                    first_child = False
                    score, move = scout(pair[1], depth - 1, alpha, beta, t_start, t_limit)
                else:
                    #F CHANGE
                    #making the null window with 1 / heuristic_value
                    score, move = scout(pair[1], depth - 1, beta - 1 / heuristic_value, beta, t_start, t_limit)
                    if alpha <= score <= beta - 1:
                        score, move = scout(pair[1], depth - 1, alpha, score, t_start, t_limit)
                if score < b:
                    b = score
                    best_move = pair[0]
                beta = min(beta, b)
            return b, best_move
    return scout_iterative_deepening
