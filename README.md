# Othello AI Agent Comparison

This project explores the performance of three computational intelligence methods for playing Othello:

1. MCTS (Monte Carlo Tree Search)
2. Minimax with Alpha-Beta Pruning
3. Minimax with Scout

We test these agents against a baseline Greedy agent and against each other to evaluate performance across time constraints.

## Research Question

Which AI strategy performs best when playing against a greedy baseline agent?
Which AI strategy performs best when pitted against each other?

## Othello Game Overview

- Played on an 8x8 board
- Players choose black or white; black moves first
- Initial board setup is a central 2x2 checker of black and white
- Moves must outflank the opponent's pieces
- If no outflanking move is possible, the turn is skipped
- Game ends when neither player can move
- Winner is the player with the most pieces of their color

[Official Othello Rules](https://www.worldothello.org/about/about-othello/othello-rules/official-rules/english)

## Agents
- `mcts.py`: UCT2-based Monte Carlo Tree Search
- `alpha_beta.py`: Alpha-beta pruning with heuristic and iterative deepening
- `scout.py`: Scout pruning with heuristic and iterative deepening
- `greedy.py`: Greedy agent using a simple heuristic

## Results
### `final_greedy_results.png`

This graph shows the performance of all three AI agents against a baseline greedy agent. The win rates are reported relative to the AI agent.

The results indicate that each of the AI agents quickly outperforms the greedy agent, even with minimal computation time. This aligns with our expectations and serves as a baseline before moving on to more complex agent-vs-agent matchups.

**Note:** In all matchups, we alternated which agent played first to avoid first-move bias.

---

### `final_agents_results.png`

This graph compares the performance of the three AI agents against one another. Win rates are shown relative to the first agent listed in each matchup. As before, we alternated the starting player across games.

**Key Findings:**

- **Scout vs. Alpha-Beta:**  
  Scout consistently performed worse than Alpha-Beta. This is evident from the upward trend in both the Alpha-Beta vs. Scout and MCTS vs. Scout lines. One likely reason is that Scout required sorting child nodes by heuristic value at every depth, which reduced the speed advantage typically gained from its pruning strategy.

- **MCTS vs. Both Pruning Agents:**  
  MCTS outperformed both Alpha-Beta and Scout as more computational time was allotted. Its performance improved rapidly with increased resources.

- **MCTS vs. Alpha-Beta at High Time Limits:**  
  While MCTS continued to improve against Scout at 50 seconds per move, its performance against Alpha-Beta began to decline slightly (though MCTS was still winning). This suggests that with enough time, Alpha-Beta could eventually surpass MCTS. However, due to runtime constraints, we were unable to test this hypothesis at longer time intervals.

These results highlight the trade-offs between tree search strategies and how computational resources can shift the performance balance among them.

