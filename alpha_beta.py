from othello import Othello
import time
import sys

def alpha_beta_policy(timeLimit):
    def alpha_beta_iterative_deepening(pos):
        start_time = time.time()
        alpha = float('-inf')
        beta = float('inf')
        depth = 2
        move = None
        while((time.time() - start_time) < timeLimit):
            # If our alpha beta throws a timeout error, terminate the search
            try:
                value, move = alpha_beta(pos, depth, alpha, beta, start_time, timeLimit)
                depth = depth + 1
            except TimeoutError:
                break
        return move
    
    def alpha_beta(pos, depth, alpha_bound, beta_bound, t_start, t_limit):
        # Check if the time is out each time alpha beta is called
        if time.time() - t_start >= t_limit:
            raise TimeoutError("Time limit exceeded during search.")
        
        if pos.is_terminal():
            return pos.payoff(), None
        
        if depth == 0:
            return pos.heuristic() / 76, None
        
        alpha = alpha_bound
        beta = beta_bound
        best_move = None
        actions = pos.get_actions()
        if pos.actor() == 1:
            a = float('-inf')
            for action in actions:
                if alpha >= beta:
                    break

                next_pos = pos.update_state_move(action)
                value, move = alpha_beta(next_pos, depth - 1, alpha, beta, t_start, t_limit)
                if value > a:
                    a = value
                    best_move = action
                alpha = max(alpha, a)

            return a, best_move
        elif pos.actor() == 2:
            b = float('inf')
            for action in actions:
                if alpha >= beta:
                    break

                next_pos = pos.update_state_move(action)
                value, move = alpha_beta(next_pos, depth - 1, alpha, beta, t_start, t_limit)
                if value < b:
                    b = value
                    best_move = action
                beta = min(beta, b)

            return b, best_move
    return alpha_beta_iterative_deepening
