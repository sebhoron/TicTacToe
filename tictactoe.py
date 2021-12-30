"""
Tic Tac Toe Player
"""

import copy


X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board): 
    """
    Returns player who has the next turn on a board.
    """
    SumX = 0
    SumO = 0
    for row in board:
        SumX += row.count(X)
        SumO += row.count(O)
    if (board == initial_state() or SumX == SumO):
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Initialize a set.
    PossibleActions = set()
    height = len(board)
    width = max(len(row) for row in board)
    # Iterate over board's cells.
    for i in range(height):
        for j in range(width):
            # If cell is empty, add it to possible moves.
            if board[i][j] == EMPTY:
                PossibleActions.add((i, j))
    return PossibleActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i = action[0]
    j = action[1]
    # Test for move's validity.
    if board[i][j] is not EMPTY:
        raise Exception("invalid action")

    # Create a deep copy of the current board.
    BoardCopy = copy.deepcopy(board)
    BoardCopy[i][j] = player(board)
    return BoardCopy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Initialize board's height and width for iteration.
    height = len(board)
    width = max(len(row) for row in board)
    h = height - 1
    w = width - 1

    # Establish winning conditions.
    WinCon = [[O, O, O], [X, X, X]]

    # Iterate over board's cells.
    for i in range(height):
        for j in range(width):
            # Skip corners.
            if (i == 0 and j == 0) or (i == 0 and j == w) or (i == h and j == 0) or (i == h and j == w):
                continue
            MainEl = board[i][j]
            # Skip empty cells.
            if MainEl == EMPTY:
                continue
            
            neighbours = []
                        
            # If on the top or bottom border, check only for the horizontal win.
            if i == 0 or i == h:
                neighbours = [board[i][j-1], MainEl, board[i][j+1]]
                if neighbours in WinCon:
                    return MainEl
            # If on the left or right border, check only for the vertical win.
            elif j == 0 or j == w:
                neighbours = [board[i-1][j], MainEl, board[i+1][j]]
                if neighbours in WinCon:
                    return MainEl
            # Check for win.
            else:
                neighbours = [[board[i-1][j-1], MainEl, board[i+1][j+1]],
                [board[i][j-1], MainEl, board[i][j+1]],
                [board[i+1][j-1], MainEl, board[i-1][j+1]],
                [board[i-1][j], MainEl, board[i+1][j]]]
                for list in neighbours:
                    if list in WinCon:
                        return MainEl
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Test if there's no empty cells left or if there's a winner.
    if winner(board) is not None:
        return True
    Cells = [cell for row in board for cell in row]
    if EMPTY not in Cells:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    state = winner(board)
    if state == X:
        return 1
    elif state == O:
        return -1
    else:
        return 0

def MaxValue(board, alpha, beta):
    if terminal(board):
        return utility(board)

    val = -2

    for action in actions(board):
        # Find the maximal value.
        val = max(val, MinValue(result(board, action), alpha, beta))
        alpha = max(alpha, val)
        if beta <= val:
            break
    return val
            
def MinValue(board, alpha, beta):
    if terminal(board):
        return utility(board)

    val = 2

    for action in actions(board):
        
        # Find the minimal value.
        val = min(val, MaxValue(result(board, action), alpha, beta))
        beta = min(beta, val)
        if beta <= alpha:
            break
    return val

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Return None if board is a terminal board.
    if terminal(board) == True:
        return None
    
    ActVal = {}
    alpha = -2
    beta = 2

    if player(board) == X:
        for action in actions(board):
            # Find the maximal value.
            MaxVal = max(alpha, MinValue(result(board, action), alpha, beta))
            ActVal.update({action: MaxVal})
            alpha = max(alpha, MaxVal)
            if beta <= alpha:
                break
            
        
        # Make lists of keys and values to find the best action.
        k = list(ActVal.keys())
        v = list(ActVal.values())
        return k[v.index(max(v))]
    
    else:
        for action in actions(board):
            # Find the minimal value.
            MinVal = min(beta, MaxValue(result(board, action), alpha, beta))
            ActVal.update({action: MinVal})
            beta = min(beta, MinVal)
            if beta <= alpha:
                break
            
        
        # Make lists of keys and values to find the best action.
        k = list(ActVal.keys())
        v = list(ActVal.values())
        return k[v.index(min(v))]
