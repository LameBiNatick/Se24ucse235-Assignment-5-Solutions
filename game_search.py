from math import sqrt, log
import random


# TIC TAC TOE STATE

class TicTacToeState:

    def __init__(self, board=None, player='X'):
        if board is None:
            self.board = [' '] * 9
        else:
            self.board = board

        self.player = player

    def available_moves(self):
        return [i for i in range(9) if self.board[i] == ' ']

    def make_move(self, pos):

        new_board = self.board[:]
        new_board[pos] = self.player

        next_player = 'O' if self.player == 'X' else 'X'

        return TicTacToeState(new_board, next_player)

    def winner(self):

        lines = [
            [0,1,2],
            [3,4,5],
            [6,7,8],
            [0,3,6],
            [1,4,7],
            [2,5,8],
            [0,4,8],
            [2,4,6]
        ]

        for line in lines:

            a,b,c = line

            if self.board[a] != ' ' and \
               self.board[a] == self.board[b] == self.board[c]:

                return self.board[a]

        return None

    def terminal(self):

        return self.winner() is not None or ' ' not in self.board

    def utility(self):

        w = self.winner()

        if w == 'X':
            return 1

        if w == 'O':
            return -1

        return 0

    def display(self):

        print()

        for i in range(0,9,3):

            print(
                self.board[i],
                "|",
                self.board[i+1],
                "|",
                self.board[i+2]
            )

        print()


# HEURISTIC FUNCTION

def heuristic(state):

    score = 0

    lines = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
        [0,3,6],
        [1,4,7],
        [2,5,8],
        [0,4,8],
        [2,4,6]
    ]

    for line in lines:

        values = [state.board[i] for i in line]

        if values.count('X') == 2 and values.count(' ') == 1:
            score += 5

        if values.count('O') == 2 and values.count(' ') == 1:
            score -= 5

    return score


# MINIMAX

def minimax(state, depth, maximizing):

    if depth == 0 or state.terminal():
        return heuristic(state)

    if maximizing:

        best = -999

        for move in state.available_moves():

            value = minimax(
                state.make_move(move),
                depth - 1,
                False
            )

            best = max(best, value)

        return best

    else:

        best = 999

        for move in state.available_moves():

            value = minimax(
                state.make_move(move),
                depth - 1,
                True
            )

            best = min(best, value)

        return best


def minimax_best_move(state, depth):

    best_value = -999
    best_move = None

    for move in state.available_moves():

        value = minimax(
            state.make_move(move),
            depth - 1,
            False
        )

        if value > best_value:

            best_value = value
            best_move = move

    return best_move, best_value


# ALPHA BETA

def alphabeta(state, depth, alpha, beta, maximizing):

    if depth == 0 or state.terminal():
        return heuristic(state)

    if maximizing:

        value = -999

        for move in state.available_moves():

            value = max(
                value,
                alphabeta(
                    state.make_move(move),
                    depth - 1,
                    alpha,
                    beta,
                    False
                )
            )

            alpha = max(alpha, value)

            if alpha >= beta:
                break

        return value

    else:

        value = 999

        for move in state.available_moves():

            value = min(
                value,
                alphabeta(
                    state.make_move(move),
                    depth - 1,
                    alpha,
                    beta,
                    True
                )
            )

            beta = min(beta, value)

            if alpha >= beta:
                break

        return value


def alphabeta_best_move(state, depth):

    best_move = None
    best_value = -999

    for move in state.available_moves():

        value = alphabeta(
            state.make_move(move),
            depth - 1,
            -999,
            999,
            False
        )

        if value > best_value:

            best_value = value
            best_move = move

    return best_move, best_value


# HEURISTIC ALPHA BETA

def heuristic_alphabeta_best_move(state):

    return alphabeta_best_move(state, 3)



# MCTS

class MCTS:

    def __init__(self, simulations=1000):

        self.simulations = simulations

    def rollout(self, state):

        current = state

        while not current.terminal():

            moves = current.available_moves()

            move = random.choice(moves)

            current = current.make_move(move)

        return current.utility()

    def best_move(self, state):

        moves = state.available_moves()

        scores = {}

        for move in moves:

            scores[move] = 0

            for _ in range(self.simulations):

                result = self.rollout(
                    state.make_move(move)
                )

                scores[move] += result

        return max(scores, key=scores.get)


# TEST CASES

if __name__ == "__main__":

    print("="*50)
    print("AI SEARCH ALGORITHMS ASSIGNMENT")
    print("="*50)

    state = TicTacToeState()

    print("\nInitial Board")

    state.display()

    print("MINIMAX")

    move, value = minimax_best_move(
        state,
        4
    )

    print("Best Move =", move)
    print("Value =", value)

    print("\nALPHA BETA")

    move, value = alphabeta_best_move(
        state,
        4
    )

    print("Best Move =", move)
    print("Value =", value)

    print("\nHEURISTIC ALPHA BETA")

    move, value = heuristic_alphabeta_best_move(
        state
    )

    print("Best Move =", move)
    print("Value =", value)

    print("\nMCTS")

    mcts = MCTS(500)

    move = mcts.best_move(state)

    print("Best Move =", move)

    print("\n" + "="*50)
    print("SECOND TEST CASE")
    print("="*50)

    board = [
        'X','O',' ',
        ' ','X',' ',
        'O',' ',' '
    ]

    state2 = TicTacToeState(
        board,
        'X'
    )

    state2.display()

    move, value = alphabeta_best_move(
        state2,
        4
    )

    print("Best Move =", move)
    print("Value =", value)

    print("\nProgram Executed Successfully")