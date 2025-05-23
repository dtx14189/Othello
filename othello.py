import copy

SIZE = 8
# N: (-1, 0)
# NE: (-1, 1)
# E: (0, 1)
# SE: (1, 1)
# S: (1, 0)
# SW: (1, -1)
# W: (0, -1)
# NW: (-1, -1)

DIRECTIONS = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

def find_total_heuristic():
    temp_game = Othello()
    total = 0
    for row in range(SIZE):
        for col in range(SIZE):
            temp_game.board[row][col] = 1

    return temp_game.heuristic()

class Othello:
    def __init__(self):
        ''' Creates an s by s board to represent the Othello game
        '''
        if SIZE < 2:
            raise ValueError('Size of the board must be at least 2x2: %d' % SIZE)

        # BOARD INFORMATION:
        # 0 means square is empty
        # 1 means black
        # 2 means white

        # clockwise around the board
        self.board = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
        # Storing which player moves next
        self.turn = 1
        # Storing the number of active white/black pieces
        self.piece_nums = [0 for _ in range(2)]

        # Storing the number of forfeits in a row
        self.forfeits = 0
        self.terminal = False
        
        # Compute the preliminary hash
        self._compute_hash()
    
    def board_init(self):
        # Setting up the initial middle pieces
        self.board[SIZE // 2 - 1][SIZE // 2 - 1] = 2
        self.board[SIZE // 2][SIZE // 2 - 1] = 1
        self.board[SIZE // 2 - 1][SIZE // 2] = 1
        self.board[SIZE // 2][SIZE // 2] = 2

        self.piece_nums[0] = 2
        self.piece_nums[1] = 2

    # Update the state based on the current move
    # and the squares to flip
    def update_state(self, move, to_flip):
        # If the player cannot make a move
        if to_flip == []:
            self.turn = 3 - self.turn
            self.forfeits += 1
            if self.forfeits == 2:
                self.terminal = True
            self._compute_hash()
            return

        # If the player CAN make a move
        self.board[move[0]][move[1]] = self.turn
        self.piece_nums[self.turn - 1] += len(to_flip) + 1
        self.piece_nums[(3 - self.turn) - 1] -= len(to_flip)
        if sum(self.piece_nums) == SIZE * SIZE:
            self.terminal = True

        for coord in to_flip:
            self.board[coord[0]][coord[1]] = 3 - self.board[coord[0]][coord[1]] 

        self.turn = 3 - self.turn
        self.forfeits = 0

        # RECOMPUTING THE HASH BECAUSE THE STATE CHANGED
        self._compute_hash()

    def reverse_state(self, last_move, last_flip):
        self.turn = 3 - self.turn # change turn back to old turn
        if last_flip == []:
            return
        
        self.board[last_move[0]][last_move[1]] = 0
        self.piece_nums[self.turn - 1] -= len(last_flip) + 1
        self.piece_nums[(3 - self.turn) - 1] += len(last_flip)

        for coord in last_flip:
            self.board[coord[0]][coord[1]] = 3 - self.board[coord[0]][coord[1]] 
        
    
    def update_state_move(self, move):
        flips = self.retrieve_flips(move)
        new_state = copy.deepcopy(self)
        new_state.update_state(move, flips)
        return new_state

    # GET THE CURRENT POSSIBLE ACTIONS
    def get_actions(self):
        # To store the possible actions
        actions = []
        
        # Loop through all squares on the baord
        for i in range(SIZE):
            for j in range(SIZE):
                # If that square can outflank, then add it
                # to the actions list
                if self.is_outflank((i, j)):
                    actions.append((i, j))
        
        if actions == []:
            return [None]
                    
        return actions
    

    # Takes in an x and a y position
    # Returns a list of pieces that are flanked if the move is valid
    # Otherwise, returns an empty list
    def retrieve_flips(self, move):
        if move is None:
            return []
        
        player = self.turn
        
        row_y = move[0]
        col_x = move[1]
        
        # Sanity check on the variables passed in
        if row_y >= SIZE or col_x >= SIZE or row_y < 0 or col_x < 0:
            raise ValueError('Out of bounds row or column value %d' % SIZE)

        # Check to see if there is already a piece there
        if self.board[row_y][col_x] != 0:
            return []

        flip = []

        for dir in DIRECTIONS:
            y = row_y + dir[0]
            x = col_x + dir[1]

            sandwich = False
            if self.in_bounds(y, x) and self.board[y][x] == (3 - self.turn):
                sandwich = True

            # while the piece played is not the same as the neighbor
            
            # We terminate if we do not run into an empty square, and we 
            # we do not run into an edge
            terminates = False
            dir_flip = []
            if sandwich:
                while self.in_bounds(y, x) and self.board[y][x] != 0:
                    if self.board[y][x] == player:
                        terminates = True
                        break
                    
                    dir_flip.append((y, x))

                    y += dir[0]
                    x += dir[1]

                # if valid, then flip
                if terminates:
                    flip.extend(dir_flip)
                    
        return flip
    
    def is_outflank(self, move):
        row_y = move[0]
        col_x = move[1]

        # Check to see if the square is currently occupied
        if self.board[row_y][col_x] != 0:
            return False

        # If the square is empty
        for dir in DIRECTIONS:
            y = row_y + dir[0]
            x = col_x + dir[1]

            sandwich = False
            if self.in_bounds(y, x) and self.board[y][x] == (3 - self.turn):
                sandwich = True
            
            if sandwich:
                while self.in_bounds(y, x) and self.board[y][x] != 0:
                    if self.board[y][x] == self.turn:
                        return True
                    y += dir[0]
                    x += dir[1]
        return False
    
    def in_bounds(self, row, col):
        return (row >= 0 and row < SIZE and col >= 0 and col < SIZE)
    
    def payoff(self):
        difference = self.piece_nums[0] - self.piece_nums[1] 
        return (difference > 0) - (difference < 0)
    
    def __hash__(self):
        return self.hash
    
    def _compute_hash(self):
        # faster hash computation; thanks to CF
        self.hash = hash(tuple(tuple(line) for line in self.board)) * 9 + self.turn * 3 + self.forfeits 

    def actor(self):
        return self.turn
    def is_terminal(self):
        return self.terminal
                
    def heuristic(self):
        value = 0
        for row in range(SIZE):
            for col in range(SIZE):
                if self.board[row][col] == 1:
                    value += self.coord_value(row, col)
                elif self.board[row][col] == 2:
                    value -= self.coord_value(row, col)
        return value
    
    def coord_value(self, row, col):
        if self.is_corner(row, col):
            return 3
        elif self.is_edge(row, col):
            return 2
        elif self.is_inner_ring(row, col):
            return 0
        else:
            return 1

    def is_corner(self, row, col):
        if row == 0 or row == SIZE - 1:
            return (col == 0 or col == SIZE - 1)
        return False
    
    def is_edge(self, row, col):  
        if row == 0 or row == SIZE - 1:
            if col >= 0 and col <= SIZE - 1:
                return True
        if col == 0 or col == SIZE - 1:
            if row >= 0 and row <= SIZE - 1:
                return True
        return False
        
    def is_inner_ring(self, row, col): 
        if row == 1 or row == SIZE - 2:
            if col >= 1 and col <= SIZE - 2:
                return True    
        if col == 1 or col == SIZE - 2:
            if row >= 1 and row <= SIZE - 2:
                return True
        return False

