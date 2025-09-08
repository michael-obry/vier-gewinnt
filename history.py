import numpy as np
import math
import os
import random
os.system('color')

# Size of the playing field is determined and function for new playing
# field defined
m = 8
n = 8

sign_arrow = b'\xE2\x86\x93'.decode('utf8')

def create_board():
    """Creates a new empty playing field consisting of a matrix of m rows and
    n columns"""
    board = np.empty(m * n)
    board[:] = 0
    board = board.reshape(m, n)
    return board


##########################
###### class state #######
##########################

class State:
    """The State class is used to create instances that manage data on the
    current game state and form the elements of the History class"""
    def __init__(self, board):
        self.__board = board

    def get_board(self):
        """Returns a copy of the game board of a state"""
        return self.__board.copy()

    def control_win(self):
        """Checks whether the current board is a winning position. This is the
        case when four of the same tiles form a row, column or diagonal.
        Returns True if there is a winner, otherwise False."""
        board = self.__board
        for row in range(0, m):
            for col in range(0, n):
                if board[row, col] != 0:
                    # Check rows
                    if ((col + 3) < n and board[row, col] == board[row, col+1]
                            == board[row, col+2] == board[row, col+3]):
                        return True
                    # Check columns
                    if ((row + 3) < m and board[row, col] == board[row+1, col]
                            == board[row+2, col] == board[row+3, col]):
                        return True
                    # Check diagonal
                    if ((row + 3) < m and (col + 3) < n
                            and board[row, col] == board[row+1, col+1]
                            == board[row+2, col+2] == board[row+3, col+3]):
                        return True
                    # Check counter diagonal
                    if ((row + 3) < m and (col - 3) >= 0
                            and board[row, col] == board[row+1, col-1] ==
                            board[row+2, col-2] == board[row+3, col-3]):
                        return True
        return False

    def control_draw(self):
        """Checks whether the current board has a draw position. This is the
        case if no further tile can be placed on the board. Returns True if
        there is a draw, otherwise False."""
        board = self.__board
        draw = True
        for row in range(0, m):
            for col in range(0, n):
                if board[row, col] == 0:
                    draw = False
        return draw

    def get_heuristic(self):
        """
        Calculates a heuristic for the current game state to evaluate the
        advantage of a player.

        - Positive values indicate an advantage for the starting
            player (yellow).
        - Negative values indicate an advantage for the challenger (red).

        Points are awarded based on the following patterns:
        - Two consecutive stones in a row column, or diagonal: 10 points.
        - Three consecutive stones in a row, column, or diagonal: 15 points.
        - More complex patterns (e.g., staggered or broken rows) receive higher
          scores, such as 24 points for two stones with a gap in between.

        The heuristic also considers proximity to the center of the board to
        reward strategic positions.

        Returns:
            A positive value indicates an advantage for the starting player,
            while a negative value indicates an advantage for the challenger.
        """
        board = self.__board
        result = 0
        for row in range(0, m):
            for col in range(0, n):
                patterns = list()
                ## Tendency towards the middle
                if 2 <= col < n - 2 and board[row, col] != 0:
                    result += board[row, col]
                ## Check rows for patterns
                if (col+ 3) < n:
                    patterns.append((board[row, col],
                                     board[row, col+1],
                                     board[row, col+2],
                                     board[row, col+3]))
                ## Check columns for patterns
                if (row + 3) < m:
                     patterns.append((board[row, col],
                                      board[row+1, col],
                                      board[row+2, col],
                                      board[row+3, col]))
                ## Check diagonals for patterns
                if (col + 3) < n and (row + 3) < m:
                     patterns.append((board[row, col],
                                      board[row+1, col+1],
                                      board[row+2, col+2],
                                      board[row+3, col+3]))
                ## Check counter diagonals for patterns
                if (col - 3) >= 0 and (row + 3) < m:
                     patterns.append((board[row, col],
                                      board[row+1, col-1],
                                      board[row+2, col-2],
                                      board[row+3, col-3]))
                ## Reward for specific patterns
                for pat in patterns:
                    if (pat != (0, 0, 0, 0)
                            and (not (1 in pat) or not (-1 in pat))
                            and -1 < sum(pat) > 1):
                        if (pat == (1, 1, 0, 0)
                                or pat == (-1, -1, 0, 0)
                                or pat == (0, 1, 1, 0)
                                or pat == (0, -1, -1, 0)
                                or pat == (0, 0, 1, 1)
                                or pat == (0, 0, -1, -1)):
                            result += sum(pat) * 5
                        elif (pat == (1, 0, 0, 1)
                              or pat == (-1, 0, 0, -1)
                              or pat == (1 ,0 ,1 ,0)
                              or pat == (-1 ,0, -1 ,0)
                              or pat == (0, 1, 0, 1)
                              or pat == (0, -1, 0, -1)):
                            result += sum(pat) * 12
                        elif (pat == (1, 1, 1, 0)
                              or pat == (-1, -1, -1, 0)
                              or pat == (0, 1, 1, 1)
                              or pat == (0, -1, -1, -1)):
                            result += sum(pat) * 5
                        elif (pat == (1, 0, 1, 1)
                              or pat == (-1, 0, -1, -1)
                              or pat == (1, 1, 0, 1)
                              or pat == (-1, -1, 0, -1)):
                            result += sum(pat) * 10
                del patterns
        return result

###########################
###### class history ######
###########################

class History:    
    def __init__(self):
        """The state class is used to create instances that manage data on the
        current game state and form the elements of the history class. Every
        state in history has a unique id. There is also the information if
        the game is still active and which state refers to which player."""
        self.__hist = [State(create_board())]
        self.__id = 0
        # Indicates whether the current game is still active
        self.__active = True
        self.__current_player = 1

    def get_current_player(self):
        """Returns 1 if the first player has to make a move, otherwise -1 (the
        challenger has to make a move)."""
        return self.__current_player

    def get_winner(self):
        """Returns the color of the winner as string. The first player has the
        colour yellow, the challenger the colour red."""
        winner = self.__current_player * (-1)
        if winner == 1:
            return "yellow"
        else:
            return "red"

    def get_current_board(self):
        """Returns the current board of history."""
        return self.__hist[self.__id].get_board()

    def get_current_state(self):
        """Returns the current state id"""
        return self.__hist[self.__id]

    def player_input(self):
        """
        Handles the input for the human player, checks for validity, and
        updates the game state accordingly.

        The player is prompted to select a column, undo a move, or progress
        through game history. The input is validated, and the game state is
        updated based on the player's move. Invalid moves are handled with
        appropriate feedback.

        Special inputs:
        - 'q': Quit the game.
        - 'b': Go back to a previous state in history.
        - 'f': Move forward to a future state in history.

        Raises:
            ValueError: If the player input is not a valid column number.
    """
        while True:
            userinput = input("Choose a number between 1 and " + str(n) + ": ")
            # Game can be quit by 'q'
            if userinput == "q":
                self.__active = False
                break
            # Returns to the previous state of the current player
            if userinput == "b" and (self.__id - 2 >= 0):
               self.__id = self.__id - 2
               board = self.__hist[self.__id].get_board()
               print()
               self.print_board(board)
            elif userinput == "b" and (self.__id - 2 < 0):
                print("You can't go back any further, you've reached the "
                      "beginning of the game")
            # Returns to the next state in the game history of the
            # current player
            elif userinput == "f" and ((self.__id + 3) <= len(self.__hist)):
               self.__id = self.__id + 2
               board = self.__hist[self.__id].get_board()
               print()
               self.print_board(board)
            elif userinput == "f" and ((self.__id + 3) > len(self.__hist)):
                print("You cannot go any further, you have reached the"
                      " current game state")
            # Checking the validity of the input and managing the scores
            # in History
            else:
                try:
                        userinput = int(userinput)
                except ValueError:
                        print("Please enter a (natural) number from 1 to "
                              + str(n))
                else:
                    if 1 <= userinput <= n:
                        player = self.get_current_player()
                        board = self.get_current_board()
                        # The columns of the user and the indices of the
                        # matrix differ from the value 1.
                        row = self.__is_legal_move(userinput - 1, board)
                        # Check whether it was a legal move,
                        # otherwise row == -1
                        if row >= 0:
                            # Delete more advanced scores if an older score
                            # has been changed in history
                            while (self.__id + 1) < len(self.__hist):
                                self.__hist.pop(self.__id + 1)
                            board[row, userinput-1] = player
                            self.__current_player \
                                = self.__change_player(self.__current_player)
                            new_move = State(board)
                            self.__id = self.__id + 1
                            self.__hist.append(new_move)
                            return
                        else:
                            print("The column you chose is full, please "
                                  "choose another column")
                    else:
                        print("The number must be between 1 and " + str(n))

    def ki_input(self):
        """
        Handles the input for the AI player using the alpha-beta pruning
        algorithm.

        The AI calculates the best possible move by evaluating future game
        states and updating the game history accordingly. The search depth is
        limited to a set number of branches to balance decision-making time and
        performance.

        Uses:
            Alpha-beta pruning algorithm to evaluate possible future game
            states and select the optimal move for the AI.
        """
        player = self.get_current_player()
        state = self.get_current_state()
        depth = 5
        result = self.alpha_beta(state, player, -math.inf, math.inf, depth)
        self.__id = self.__id + 1
        self.__current_player = self.__change_player(self.__current_player)
        self.__hist.append(result[1])
                   
    def is_game_active(self):
        """Returns True if the game is still active, otherwise false"""
        return self.__active

    #### AlphaBeta auxiliary methods ####
    def expand_state(self, state, player):
        """
        Generates all possible next game states for the given player by
        simulating all legal moves.

        This function examines the current game state and calculates the board
        positions that can be reached by placing a new tile in any valid
        column.
        It returns a list of all possible new states.

        Args:
            state (State): The current game state.
            player (int): The current player (1 for the starting player, -1 for
                the challenger).

        Returns:
            list: A list of new possible game states resulting from valid
                moves.
        """
        new_states = []
        if not (state.control_win() or state.control_draw()):
            for j in range(0, n):
                new_board = state.get_board()
                row = self.__is_legal_move(j, new_board)
                if row >= 0:
                    new_board[row, j] = player
                    new_state = State(new_board)
                    new_states.insert(j, new_state)
        return new_states

    def get_reward(self, state, player):
        """
        Calculates the reward for a specific game state based on the current
        player's advantage.

        The reward is determined by evaluating the game's heuristic and
        checking if the current state results in a win for either player.

        Args:
            state (State): The current game state.
            player (int): The current player (1 for the starting player, -1 for
                the challenger).

        Returns:
            int: A positive reward if the state favors the starting player,
            a negative reward if it favors the challenger, or 0 if the state
            is neutral. Winning states provide a high reward of 1000 points.
        """
        result = 0
        win = state.control_win()
        # reward patterns
        result += state.get_heuristic()
        if win and player == -1:
            result += 1000
        elif win and player == 1:
            result -= 1000
        return result

    def alpha_beta(self, state, player, alpha, beta, depth):
        """
        Recursively implements the alpha-beta pruning algorithm to evaluate
        possible game states and determine the best move.

        This algorithm searches through possible future game states and
        prunes branches that cannot result in a better outcome for the
        current player, improving efficiency.

        Args:
            state (State): The current game state.
            player (int): The current player (1 for the starting player, -1 for
                the challenger).
            alpha (float): The best score the maximizing player
                (starting player) can achieve.
            beta (float): The best score the minimizing player (challenger) can
                achieve.
            depth (int): The maximum depth for the search tree (controls how
                far ahead the AI looks).

        Returns:
            tuple: A tuple containing the best score and the best state (State)
            for the current player.
        """
        children = self.expand_state(state, player)
        if not children or depth == 0:
            return self.get_reward(state, player), state
        else:
            if player == 1:
                v = -math.inf
                for c in children:
                    if alpha < beta:
                        res = self.alpha_beta(c,
                                              self.__change_player(player),
                                              alpha,
                                              beta,
                                              depth - 1)
                        if res[0] > v:
                            best_state = c
                        v = max(res[0], v)
                        alpha = max(alpha, v)
                    else:
                        break
            elif player == -1:
                v = math.inf
                for c in children:
                    if alpha < beta:
                        res = self.alpha_beta(c,
                                              self.__change_player(player),
                                              alpha,
                                              beta,
                                              depth - 1)
                        if res[0] < v:
                            best_state = c
                        v = min(res[0], v)
                        beta = min(beta, v)
                    else:
                        break
        return v, best_state
                
    #### Auxiliary methods ####
    def print_board(self, board):
        """Auxiliary function to print game field 'human-readable'. For the
        number 1 (first player) in the gaming matrix a yellow tile
        (string zero), for the number -1 (challenger) a red tile and for the
        number 0 (empty field) an empty space is printed."""
        numb = " "
        arrow = " "
        for col in range(n):
            numb += str(col + 1) + " "
            arrow += sign_arrow + " "
        print(numb)
        print(arrow)
        for row in range(m):
            elem = "|"
            for col in range(n):
                elem += self.__output_console(board[row, col]) + "|"
            print(elem)
        numb = " "
        for col in range(n):
            numb += str(col + 1) + " "
        print(numb)
        
    def __output_console(self, elem):
        """Auxiliary function to display game pieces as colored and empty
        playing fields as blank spaces"""
        if elem == 1:
            return "\033[93mO\033[00m"
        elif elem == -1:
            return "\033[91mO\033[00m"
        else:
            return " "

    def __change_player(self, player):
        """Changes the current player"""
        return player * (-1)

    def __is_legal_move(self, move, board):
        """
        Checks if a move is legal. E.g. if a player wants to insert a tile in
        the third column of the matrix where two tiles are already placed,
        the method places the next tile on the two previous tiles.

        Args:
            move (int): The column number of the board where the tile shall
                be inserted.
            board (matrix): The game field from a state (State).

        Returns:
            int: If the move is legal (the column is not full), the row number
                according to the move in which the next tile can be “placed” on
                the previous one is returned. If the move is not legal -1 is
                returned.
        """
        r = m - 1
        while board[r, move] == 1 or board[r, move] == -1:
            r -= 1
            if r < 0:
                break
        return r
