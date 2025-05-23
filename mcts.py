from othello import Othello
import math
import random
import time

class Node:
    def __init__(self, state):
        self.state = state
        self.edges = []
        self.n = 0
        self.reward = 0
    
class Edge:
    def __init__(self, action, child):
        self.action = action
        self.child = child
        self.n = 0

def mcts_policy(timeLimit):
    def traverse(node, path):
        while node.edges: # while non-leaf
            bestEdge = best_edge(node)
            path.append(bestEdge)
            node = bestEdge.child  
        return node
    
    def best_edge(node):
        if(node.state.actor() == 1): # P0
            max = float('-inf')
            bestEdge = None
            for edge in node.edges:
                if(edge.n == 0):
                    return edge
                edge_val = edge.child.reward/edge.child.n + UCB(edge.n, node.n - 1) 
                if(edge_val > max):
                    max = edge_val
                    bestEdge = edge
            return bestEdge
        else: # P1
            min = float('inf')
            bestEdge = None
            for edge in node.edges:
                if edge.n == 0:
                    return edge
                edge_val = edge.child.reward/edge.child.n - UCB(edge.n, node.n - 1) 
                if(edge_val < min):
                    min = edge_val
                    bestEdge = edge
            return bestEdge
    
    def UCB(edge_n, T):
        return math.sqrt(2 * math.log(T)/edge_n)

    def simulate(state):
        while not state.is_terminal():
            random_action = random.choice(state.get_actions())
            state = state.update_state_move(random_action)
        return state.payoff()
   
    def mcts(pos):
        start_time = time.time()
        state_to_node = {} 
        root = Node(pos)

        # Add the root to dictionary storing states and nodes
        state_to_node[pos] = root

        #While there is still time to grow the tree
        while(time.time() - start_time < timeLimit):
            path = []
            leaf = traverse(root, path) # path has all nodes excluding root including leaf

            # expand leaf if nonterminal and visited
            if not leaf.state.is_terminal() and leaf.n > 0: 
                for action in leaf.state.get_actions():
                    succ = leaf.state.update_state_move(action)
                    if succ in state_to_node: 
                        leaf.edges.append(Edge(action, state_to_node[succ])) 
                    else: 
                        new_node = Node(succ) 

                        # This is to check if the node already exists in the graph 
                        state_to_node[succ] = new_node

                        leaf.edges.append(Edge(action, new_node)) 
                random_edge = random.choice(leaf.edges)
                path.append(random_edge)
                leaf = random_edge.child

            payoff = simulate(leaf.state)
            root.n += 1 
            
            # propogate
            for edge in path:
                edge.n += 1
                edge.child.reward += payoff
                edge.child.n += 1
                
        if root.state.is_terminal():
            return None
        else:
            max = float('-inf')
            bestAction = None
            for edge in root.edges:
                if edge.n > max:
                    max = edge.n
                    bestAction = edge.action
            return bestAction

    return mcts
