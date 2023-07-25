import math

def draw_board(board):
    print("-------------")
    for i in range(3):
        print("|", end=" ")
        for j in range(3):
            print(board[i * 3 + j], "|", end=" ")
        print("\n-------------")

def check_winner(board):
    # All possible winning combinations
    win_positions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Cols
        [0, 4, 8], [2, 4, 6] # Diagonals
    ]

    for pos in win_positions:
        if board[pos[0]] == board[pos[1]] == board[pos[2]] != " ":
            return board[pos[0]]

    if " " not in board:
        return "draw"

    return None

# Evaluate the board state
def evaluate(board):
    scores = {"X": 1, "O": -1, "draw": 0}

    winner = check_winner(board)
    if winner is not None:
        return scores[winner]

    return 0
   
def minimax(board, depth, maximizing_player, alpha, beta):
    '''
    Minimax algorithm with alpha-beta pruning

    Parameters:
        board (list): The current board state
        depth (int): The depth of the tree
        maximizing_player (bool): True if the current player is the maximizing player
        alpha (int): The alpha value
        beta (int): The beta value

    Returns:
        int: The score of the current board state

    How it works:
        1. If the game is over or depth reached, evaluate the score
        2. If it's the maximizing player's turn
            1. Traverse all cells
            2. If the cell is empty, make the move and call minimax recursively
            3. Undo the move
            4. Update the max_score
        3. If it's the minimizing player's turn
            1. Traverse all cells
            2. If the cell is empty, make the move and call minimax recursively
            3. Undo the move
            4. Update the min_score
        4. Return the max_score if it's the maximizing player's turn, else return the min_score

    Alpha-beta pruning:
        1. If the current player is the maximizing player
            1. Update the alpha value
            2. If alpha is greater than or equal to beta, break
        2. If the current player is the minimizing player
            1. Update the beta value
            2. If alpha is greater than or equal to beta, break
        This will reduce the number of nodes that need to be evaluated.

    Maximizing player is the AI (X)
    Minimizing player is the human (O)
    '''
    scores = {"X": 1, "O": -1, "draw": 0}

    # If the game is over or depth reached, evaluate the score
    winner = check_winner(board)
    if (depth == 0 and winner is not None) or (winner is not None):
        return scores[winner]

    # If it's the maximizing player's turn
    if maximizing_player:
        max_score = -math.inf

        # Traverse all cells
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, depth - 1, False, alpha, beta)
                board[i] = " "
                max_score = max(max_score, score)
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
        return max_score
    else:
        # If it's the minimizing player's turn
        min_score = math.inf

        # Traverse all cells
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, depth - 1, True, alpha, beta)
                board[i] = " "
                min_score = min(min_score, score)
                beta = min(beta, score)
                if alpha >= beta:
                    break
        return min_score

# Get the best move for the AI
def get_best_move(board):
    best_score = -math.inf
    best_move = -1
    for i in range(9):
        if board[i] == " ":
            board[i] = "X"
            score = minimax(board, 5, False, -math.inf, math.inf) # The depth is chosen arbitrarily
            board[i] = " "
            if score > best_score:
                best_score = score
                best_move = i
    return best_move

# Main driver
def play_game():
    # Initialize the board and current player
    board = [" " for _ in range(9)]
    current_player = "O"

    while True:
        draw_board(board)
        if current_player == "O":
            move = int(input("Enter position (0-8): "))
            if board[move] != " " or move < 0 or move > 8 or not isinstance(move, int):
                print("Invalid position, please try again.")
                continue
        else:
            move = get_best_move(board)

        board[move] = current_player
        winner = check_winner(board)

        if winner is not None:
            draw_board(board)
            if winner == "draw":
                print("Its a draw!")
            else:
                print("Winner: " + winner)
            break

        current_player = "X" if current_player == "O" else "O"

# Driver code
if __name__ == "__main__":
    play_game()
