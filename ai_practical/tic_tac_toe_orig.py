from typing import List, Optional, Tuple, Union

# Define the player symbols
Player = str  # 'X' or 'O'
EMPTY = "-"
AI_PLAYER = "O"
HUMAN_PLAYER = "X"


def print_board(board: List[List[Player]]) -> None:
    """Prints the Tic-Tac-Toe board."""
    for row in board:
        print(" | ".join(row))
    print()


def check_winner(board: List[List[Player]]) -> Optional[Player]:
    """Check if there's a winner on the board."""
    # Check rows, columns, and diagonals
    win_conditions = [
        # Rows
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        # Columns
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        # Diagonals
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]

    for condition in win_conditions:
        a, b, c = condition
        if board[a[0]][a[1]] == board[b[0]][b[1]] == board[c[0]][c[1]] != EMPTY:
            return board[a[0]][a[1]]

    return None


def is_moves_left(board: List[List[Player]]) -> bool:
    """Check if there are any moves left on the board."""
    for row in board:
        if EMPTY in row:
            return True
    return False


def evaluate(board: List[List[Player]]) -> int:
    """Evaluate the board and return a score."""
    winner = check_winner(board)
    if winner == AI_PLAYER:
        return 10
    elif winner == HUMAN_PLAYER:
        return -10
    return 0


def minimax(board: List[List[Player]], depth: int, is_max: bool) -> Union[int, float]:
    """Minimax function to calculate the best move."""
    score = evaluate(board)

    # If the game is over, return the score
    if score == 10 or score == -10:
        return score

    if not is_moves_left(board):
        return 0

    if is_max:
        best = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = AI_PLAYER
                    best = max(best, minimax(board, depth + 1, not is_max))
                    board[i][j] = EMPTY
        return best
    else:
        best = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = HUMAN_PLAYER
                    best = min(best, minimax(board, depth + 1, not is_max))
                    board[i][j] = EMPTY
        return best


def find_best_move(board: List[List[Player]]) -> Tuple[int, int]:
    """Find the best move for the AI player."""
    best_val = -float("inf")
    best_move: Tuple[int, int] = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI_PLAYER
                move_val = minimax(board, 0, False)
                board[i][j] = EMPTY

                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val

    return best_move


def main() -> None:
    """Main function to run the Tic-Tac-Toe game with Minimax AI."""
    board: List[List[Player]] = [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
    ]

    while True:
        print_board(board)
        if not is_moves_left(board) or check_winner(board):
            break

        # Human move
        row, col = map(int, input("Enter your move (row and column 0-2): ").split())
        if board[row][col] == EMPTY:
            board[row][col] = HUMAN_PLAYER
        else:
            print("Invalid move, try again.")
            continue

        if check_winner(board) or not is_moves_left(board):
            break

        # AI move
        best_move = find_best_move(board)
        board[best_move[0]][best_move[1]] = AI_PLAYER
        print(f"AI chooses move: {best_move}")

    winner = check_winner(board)
    print_board(board)
    if winner:
        print(f"Winner is: {winner}")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    print(f"Player symbol is {HUMAN_PLAYER}")
    print(f"AI symbol is {AI_PLAYER}")
    main()
