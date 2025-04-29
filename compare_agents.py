import time
import random
import argparse

import greedy
import mcts
import alpha_beta
import scout 

import copy

from othello import Othello

SIZE = 8

def random_move(position):
    moves = position.get_actions()
    return random.choice(moves)

def compare_policies(p1, p2, games, prob, time_limit_1, time_limit_2):
    p1_wins = 0
    p2_wins = 0
    p1_score = 0
    p1_time = 0.0
    p2_time = 0.0
    piece_diff = 0

    game = Othello()
    game.board_init()

    for i in range(games):
        p1_policy = p1()
        p2_policy = p2()
        position = copy.deepcopy(game)

        while not position.is_terminal():
            if random.random() < prob:
                move = random_move(position)
            else:
                if position.actor() == (i % 2) + 1:
                    start = time.time()
                    move = p1_policy(position)
                    p1_time = max(p1_time, time.time() - start)

                    #FOR TESTING PURPOSES (F CHANGE)
                    # print(move)
                    # print()
                else:
                    start = time.time()
                    move = p2_policy(position)
                    p2_time = max(p2_time, time.time() - start)

                    #FOR TESTING PURPOSES (F CHANGE)
                    # print(move)
                    # print()
            
            flips = position.retrieve_flips(move)
            position.update_state(move, flips)
        
        p1_score += position.payoff() * (1 if i % 2 == 0 else -1)
        #F CHANGE
        piece_diff += (position.piece_nums[0] - position.piece_nums[1]) * (1 if i % 2 == 0 else -1)

        if position.payoff() == 0:
            p1_wins += 0.5
            p2_wins += 0.5
        elif (position.payoff() > 0 and i % 2 == 0) or (position.payoff() < 0 and i % 2 == 1):
            p1_wins += 1
        else:
            p2_wins += 1

        #PRINT OUT THE BOARD FOR TESTING PURPOSES (F CHANGE)
        # for line in position.board:
        #     for piece in line:
        #         print(piece, end="")
        #     print("")
        # print("")

        # print("///////////////////////////////////////////////////////////////////")

    #GIVE A BIT OF LENIENCY ON THE TIME LIMITS (F CHANGE)
    if p1_time > time_limit_1 * 1.1:
        print("WARNING: max time for P1 =", p1_time)
    if p2_time > time_limit_2 * 1.1:
        print("WARNING: max time for P2 =", p2_time)
    
    margin = p1_score / games
    wins = p1_wins / games
    #F CHANGE
    piece_avg = piece_diff / games
    
    # for row in range(SIZE):
    #     for col in range(SIZE):
    #         if position.board[row][col] == 1:
    #             piece_diff += 1
    #         elif position.board[row][col] == 2:
    #             piece_diff -= 1
    
    #F CHANGE
    print("NET: ", margin, "; WINS: ", wins, "; DIFF: ", piece_avg, sep="")

if __name__ == '__main__':

    # print(args.count)
    # print(args.p_random)
    # print(args.time)

    # 0 = mcts vs greedy
    # 1 = alpha/beta vs greedy
    # 2 = scout vs greedy
    # 3 = mcts vs alpha/beta
    # 4 = mcts vs scout
    # 5 = alpha/beta vs scout

    parser = argparse.ArgumentParser(description="Compare Agents that Play Othello")
    parser.add_argument('--count', dest='count', type=int, action="store", default=2, help='number of games to play (default=2')
    parser.add_argument('--time', dest='time', type=float, action="store", default=0.1, help='time for MCTS per move')
    parser.add_argument('--random', dest="p_random", type=float, action="store", default = 0.0, help="p(random instead of minimax) (default=0.0)")
    parser.add_argument('--matchup', dest="matchup", type=int, action="store", default = 0, help="agent matchup for Othello (default=0)")

    args = parser.parse_args()

    agent_matchup = args.matchup

    if agent_matchup == 0:
        compare_policies(lambda: mcts.mcts_policy(args.time),
                         lambda: greedy.greedy_policy(),
                         args.count,
                         args.p_random,
                         args.time,
                         float("inf"))
    elif agent_matchup == 1:
        compare_policies(lambda: alpha_beta.alpha_beta_policy(args.time),
                         lambda: greedy.greedy_policy(),
                         args.count,
                         args.p_random,
                         args.time,
                         float("inf"))
    elif agent_matchup == 2:
        compare_policies(lambda: scout.scout_policy(args.time),
                         lambda: greedy.greedy_policy(),
                         args.count,
                         args.p_random,
                         args.time,
                         float("inf"))
    elif agent_matchup == 3:
        compare_policies(lambda: mcts.mcts_policy(args.time),
                         lambda: alpha_beta.alpha_beta_policy(args.time),
                         args.count,
                         args.p_random,
                         args.time,
                         args.time)
    elif agent_matchup == 4:
        compare_policies(lambda: mcts.mcts_policy(args.time),
                         lambda: scout.scout_policy(args.time),
                         args.count,
                         args.p_random,
                         args.time,
                         args.time)
    elif agent_matchup == 5:
        compare_policies(lambda: alpha_beta.alpha_beta_policy(args.time),
                         lambda: scout.scout_policy(args.time),
                         args.count,
                         args.p_random,
                         args.time,
                         args.time)
