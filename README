# Othello AI Agent Comparison

This repository explores the performance of three computational intelligence methods for playing Othello:

1. MCTS (Monte Carlo Tree Search)
2. Minimax with Alpha-Beta Pruning
3. Minimax with Scout

We test these agents against a baseline Greedy agent and against each other to evaluate performance across time constraints and strategy depth.

---

## Running the Lightweight Tests

To run the lightweight version of the testing framework:

```bash
make
./Othello
```

This will generate the main results data files.

To also generate a result graph:

```bash
mkdir graph_results
mv scratch* graph_results
python3 parse_data.py
```

This will save the plot as `lightweight_results.png`.

---

## Othello Game Overview

- Played on an 8x8 board
- Players choose black or white; black moves first
- Initial board setup is a central 2x2 checker of black and white
- Moves must outflank the opponent's pieces
- If no outflanking move is possible, the turn is skipped
- Game ends when neither player can move
- Winner is the player with the most pieces of their color

---



RESEARCH QUESTION:

Under three computational intelligence methods used for games with large state spaces, 
including 1. MCTS 2. Minimax with Scout 3. Minimax with alpha/beta, which performs best when playing 
against a greedy agent, and which performs best when pitted against each other?

CODE BASE:

3. TESTING

FILES:
makefile
test_script.py
compare_agents.py
parse_data.py

run "make" to create an Othello "executable"
run "./Othello"

test_script.py is run by ./Othello. For a certain number of game playouts (determined by magic_number and time limit), 
runs full games for each of the specified a. agent matchups and b. time limits per move. 

For each specified agent matchup and time limit, this script outputs
a file that displays the NET win rate, the WIN rate, and DIFF, which is the average piece difference (calculated as black - white)
over all games played within the time limit. Note that this script may output many files into your current working directory. 

The output files will have the following naming convention: 
'{header}_{magic_number}_{matchup}_{time_limit}.txt'. The indexing convention for
matchups are specified in compare_agents.py. test_script.py uses Python multiprocessing to run
each of the time/matchup pairs in parallel. Each parallel process runs a number of playouts in sequence
as determined by magic_number / time limit.

compare_agents.py is called by test_script.py to run the playouts. Based on the magic_number
in test_sript.py compare_agents is passed in a number of playouts to perform. The order of the 
agents is swapped throughout the trials for equality: Player1 goes first, then Player2 goes first.
Note: we define Player1 as the same agent throughout the playouts and our results show the win
rate relative to Player1. For example, in a matchup of mcts vs. alpha/beta, mcts is always
"Player1" but Player1 alternates between going first and going second. And the results are displayed
with the mcts (Player1) win rate.

Finally, we wrote a script called parse_data to generate the graphs of the final results.

4. RESULTS

a. final_greedy_results.png

This graph displays the results of all 3 agent matchups versus the baseline greedy agent.
The results are the win rates relative to the comp intelligence agent. These preliminary 
results simply show that each of the computational intelligence methods requires a
very short amount of thinking time before it invariable defeats the greedy agent. This
was in line with what we expected, so below we move onto the next more interesting question
of pitting the agents against each other.

NOTE: we alternated who played first and who played second in our game testing

b. final_agents_results.png

This graph displays the results of all 3 agent matchups against eachother. The results
have the win rate relative to the first agent listed in the matchup. As noted above, 
we alternated who went first in our game testing.

Here are some of the conclusions we drew:

- scout almost always performed worse than alpha-beta. This can be seen both by the increasing
trend in the green alpha/beta vs. scout line, and by the increasing trend in the orange
mcts vs. scout line. This could likely be attributed to the fact that we needed to sort 
the children nodes by according to the heuristic  every time we traversed down another layer,
and this possibly reduced the speed advantage of the additional pruning by Scout.

- As more computational resources are provided, MCTS rapidly overtook both of the
pruning agents in performance.

- Although MCTS continues to improve linearly against scout at 50 seconds per move,
MCTS starts declining in its performance against alpha beta; it is sitll winning,
but at a different rate. If we extrapolate, we would expect that giving alpha beta
more and more computational resources would allow it to eventaully take over MCTS,
although it was infeasible to actually test this.

REPRODUCING RESULTS

Instructions were provided at the beginning fo the README for how to run a lightweight version
of the results. To reproduce the data for the 3 computational intelligence agents playing against
each other, one should follow these steps:

1. in parse_data.py uncomment the array of times for versus agents and comment out the 
one for lightweight testing
2. In test_script.py, modify the  magic number to 500. This will take around 500 minutes, or 8+hours
We personally did 500 (8+ hours) across multiple nodes to get all of our results. 




## Research Question

Which AI strategy performs best:
- When playing against a greedy baseline agent?
- When pitted against other AI agents?

---

## Code Structure

### `othello.py`  
Defines the game logic and board update rules.

### Agents
- `mcts.py`: UCT2-based Monte Carlo Tree Search
- `alpha_beta.py`: Alpha-beta pruning with heuristic and iterative deepening
- `scout.py`: Scout pruning with heuristic and iterative deepening
- `greedy.py`: Greedy agent using a simple heuristic

### Testing
- `makefile`: Builds the executable
- `test_script.py`: Runs parallelized matches for various agent matchups and time constraints
- `compare_agents.py`: Handles specific agent matchups and win rate calculations
- `parse_data.py`: Parses data and generates plots

---

## Results

### `final_greedy_results.png`

Displays win rates of each AI agent versus the greedy agent.  
All AI agents consistently outperform the greedy strategy with minimal compute time.

### `final_agents_results.png`

Compares AI agents head-to-head.  
Key observations:
- Scout performs worse than Alpha-Beta, likely due to node sorting overhead.
- MCTS rapidly improves with more time and eventually outperforms both pruning agents.
- Alpha-Beta shows signs of catching up to MCTS at higher time limits.

---

## Reproducing Full Results

To replicate the full experimental results:

1. In `parse_data.py`, uncomment the array of times for full testing and comment out the lightweight version.
2. In `test_script.py`, set `magic_number = 500`.

Note: This process takes 8 or more hours of

