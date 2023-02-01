'''
Name(s): Zuo Wang, Charlie Norgaard
UW netid(s): zwang36, norgc52
'''

from game_engine import genmoves

class BackgammonPlayer:
    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()
        self.func = self.staticEval
        self.maxply = 2
        self.states = 0
        self.cutoffs = 0
        self.prune = False

    # Return a string containing your UW NETID(s)
    # For students in partnership: UWNETID + " " + UWNETID
    def nickname(self):
        return "1938164 1972609"

    # If prune==True, then your Move method should use Alpha-Beta Pruning
    # otherwise Minimax
    def useAlphaBetaPruning(self, prune=False):
        # Use the prune flag to indiciate what search alg to use
        self.prune = prune
        self.states = 0
        self.cutoffs = 0


    # Returns a tuple containing the number explored
    # states as well as the number of cutoffs.
    def statesAndCutoffsCounts(self):
        # Return a tuple containig states and cutoff
        return (self.states, self.cutoffs)

    # Given a ply, it sets a maximum for how far an agent
    # should go down in the search tree. maxply=2 indicates that
    # our search level will go two level deep.
    def setMaxPly(self, maxply=2):
        self.maxply = maxply

    # If not None, it update the internal static evaluation
    # function to be func
    def useSpecialStaticEval(self, func):
        if func != None: self.func = func

    # Given a state and a roll of dice, it returns the best move for
    # the state.whose_move.
    # Keep in mind: a player can only pass if the player cannot move any checker with that role
    def move(self, state, die1=1, die2=6):
        # Return a move for the current state and for the current player.
        # Hint: you can get the current player with state.whose_move
        bestMove = None
        bestScore = -1e9 + state.whose_move * 1e9 * 2    # -1e9 for white 1e9 for red
        for move in self.GenMoveInstance.gen_moves(state=state,
                                                    whose_move=state.whose_move,
                                                    die1=die1,
                                                    die2=die2):
            if self.prune:
                score = self.alphaBetaPruning(state=move[1], depth=self.maxply, alpha=-1e9, beta=1e9)
            else:
                score = self.miniMax(state=move[1], depth=self.maxply)
            if (state.whose_move == 0 and score > bestScore) or \
                (state.whose_move == 1 and score < bestScore):
                bestScore = score
                bestMove = move
        return bestMove[0]


    def alphaBetaPruning(self, state, depth, alpha, beta):
        # increment states
        self.states += 1

        # check if at leaf node or game is over
        if depth == 0 or len(state.white_off) == 15 or len(state.red_off) == 15:
            return self.func(state=state)

        # white's move (maximizing player)
        if state.whose_move == 0:
            maxEval = -1e9
            for move in self.GenMoveInstance.gen_moves(state=state, whose_move=state.whose_move, die1=1, die2=6):
                eval = self.alphaBetaPruning(move[1], depth - 1, alpha, beta)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha: # prune
                    self.cutoffs += 1 # increment cutoffs
                    break
            return maxEval

        # red's move (minimizing player)
        if state.whose_move ==1:
            minEval = 1e9
            for move in self.GenMoveInstance.gen_moves(state=state, whose_move=state.whose_move, die1=1, die2=6):
                eval = self.alphaBetaPruning(move[1], depth - 1, alpha, beta)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha: # prune
                    self.cutoffs += 1 # increment cutoffs
                    break
            return minEval


    def miniMax(self, state, depth):
        # increment states
        self.states += 1

        # check if at leaf node or game is over
        if depth == 0 or len(state.white_off) == 15 or len(state.red_off) == 15:
            return self.func(state=state)

        # white's move (maximizing player)
        if state.whose_move == 0:
            maxEval = -1e9
            for move in self.GenMoveInstance.gen_moves(state=state, whose_move=state.whose_move, die1=1, die2=6):
                eval = self.miniMax(move[1], depth - 1)
                maxEval = max(maxEval, eval)
            return maxEval

        # red's move (minimizing player)
        if state.whose_move ==1:
            minEval = 1e9
            for move in self.GenMoveInstance.gen_moves(state=state, whose_move=state.whose_move, die1=1, die2=6):
                eval = self.miniMax(move[1], depth - 1)
                minEval = min(minEval, eval)
            return minEval


    # Hint: Look at game_engine/boardState.py for a board state properties you can use.
    def staticEval(self, state):
        # Return a number for the given state
        # The static evaluation is as followed:
        #   Each white checker off the board counts as 100
        #   Each red chekcer off the board counts as -100
        #   Ecah white checker on the bar counts as -5
        #   Each red chekcer on the bar counts as 5
        #   Each white checker on the board counts as it's distance from point 24
        #   Each red checker on the board counts as (it's distance from point 24) * -1
        eval = 100 * (len(state.white_off) - len(state.red_off))
        for checker in state.bar:
            if checker == 0: eval -= 5
            else: eval += 5
        for index, point in enumerate(state.pointLists):
            for checker in point:
                if checker == 0: eval += index + 1  # This is a white checker
                else: eval -= (24 - index)          # This is a red checker

        return eval