'''
Name(s): Zuo Wang, Charlie Norgaard
UW netid(s): zwang36, norgc52
'''

from game_engine import genmoves
import random

class BackgammonPlayer:
    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()
        self.func = self.staticEval
        self.maxply = 2

    # Return a string containing your UW NETID(s)
    # For students in partnership: UWNETID + " " + UWNETID
    def nickname(self):
        return "1938164 1972609"

    # Given a ply, it sets a maximum for how far an agent
    # should go down in the search tree. Count the chance nodes
    # as a ply too!
    def setMaxPly(self, maxply=2):
        self.maxply = maxply

    # If not None, it update the internal static evaluation
    # function to be func
    def useSpecialStaticEval(self, func):
        if func != None: self.func = func

    # Given a state and a roll of dice, it returns the best move for
    # the state.whose_move
    # Keep in mind: a player can only pass if the player cannot move any checker with that role
    def move(self, state, die1, die2):
        bestMove = None
        bestScore = -1e9 + state.whose_move * 1e9 * 2    # -1e9 for white 1e9 for red
        for move in self.GenMoveInstance.gen_moves(state=state,
                                                    whose_move=state.whose_move,
                                                    die1=die1,
                                                    die2=die2):
            score = self.expectimax(state=move[1], depth=self.maxply)
            if (state.whose_move == 0 and score > bestScore) or \
                (state.whose_move == 1 and score < bestScore):
                bestScore = score
                bestMove = move
        return bestMove[0]


    def expectimax(self, state, depth):
        # check if at leaf node or game is over
        if depth == 0 or len(state.white_off) == 15 or len(state.red_off) == 15:
            return self.func(state=state)

        # randomly generate dice rolls
        die1 = random.randint(1,6)
        die2 = random.randint(1,6)

        num_states = 0
        # generate moves
        moves = self.GenMoveInstance.gen_moves(state=state, whose_move=state.whose_move, die1=die1, die2=die2)
        for move in moves:
            num_states += 1

        # white's move (maximizing player)
        if state.whose_move == 0:
            maxEval = -1e9
            for move in moves:
                eval = self.expectimax(move[1], depth - 1)
                maxEval = max(maxEval, eval)
            return maxEval

        # red's move (minimizing player)
        if state.whose_move == 1:
            minEval = 0
            for move in moves:
                # minimizing player is assumed to play randomly, each move has an equal probability of being chosen
                # probability of each move is 1 / number of successors
                minEval += (1 / num_states) * self.expectimax(move[1], depth - 1)
            return minEval


    # Hint: Look at game_engine/boardState.py for a board state properties you can use.
    def staticEval(self, state):
        # Return a number for the given state
        # The static evaluation is as followed:
        #   Each white checker off the board counts as 100 points
        #   Each red chekcer off the board counts as -100 points
        #   Ecah white checker on the bar counts as -5 points
        #   Each red chekcer on the bar counts as 5 points
        #   Each white checker on the board counts as (its’ point number) points
        #       For instance, if a white checker is on point 6, it is worth 6 points
        #   Each red checker on the board counts as (it's distance from point 24) * -1 points
        #       For instance, if a red checker is on point 8, it is worth (24 - 8) * -1 = -16 points

        eval = 100 * (len(state.white_off) - len(state.red_off))
        for checker in state.bar:
            if checker == 0: eval -= 5
            else: eval += 5
        for index, point in enumerate(state.pointLists):
            for checker in point:
                if checker == 0: eval += index + 1  # This is a white checker
                else: eval -= (24 - index)          # This is a red checker
        return eval
