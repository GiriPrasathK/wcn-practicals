from typing import List, Optional, Tuple, Union

Player = str
EMPTY = "-"
HUMAN = "X"
AI = "O"


def print_board(board: List[List[Player]]) -> None:
    for row in board:
        print(" | ".join(row))
    print()


def check_winner(board: List[List[Player]]) -> Optional[Player]:
    winner_conditions = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]

    for condition in winner_conditions:
        a, b, c = condition
        if board[a[0]][a[1]] == board[b[0]][b[1]] == board[c[0]][c[1]] != EMPTY:
            return board[a[0]][a[1]]
    return None


def is_moves_left(board: List[List[Player]]) -> bool:
    for row in board:
        if EMPTY in row:
            return True
    return False


def evaluate(board: List[List[Player]]) -> int:
    winner = check_winner(board)
    if winner == AI:
        return 10
    elif winner == HUMAN:
        return -10
    else:
        return 0


def minimax(board: List[List[Player]], depth: int, is_max: bool) -> Union[int, float]:
    score = evaluate(board)

    if abs(score) == 10:
        return score

    if not is_moves_left(board):
        return 0

    if is_max:
        best = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = AI
                    best = max(best, minimax(board, depth + 1, not is_max))
                    board[i][j] = EMPTY
        return best
    else:
        best = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = HUMAN
                    best = min(best, minimax(board, depth + 1, not is_max))
                    board[i][j] = EMPTY
        return best


def find_best_move(board: List[List[Player]]):
    best_val = -float("inf")
    best_move: Tuple[int, int] = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI
                move_val = minimax(board, 0, False)
                board[i][j] = EMPTY

                if move_val > best_val:
                    best_val = move_val
                    best_move = (i, j)

    return best_move


def main():
    board: List[List[Player]] = [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
    ]

    while True:
        print_board(board)
        if not is_moves_left(board) or check_winner(board):
            break

        row, col = map(int, input("Enter your move (row/col 1-3): ").split())
        row, col = row - 1, col - 1
        if board[row][col] == EMPTY:
            board[row][col] = HUMAN
        else:
            print("Invalid Move")
            continue

        if check_winner(board) or not is_moves_left(board):
            break

        best_move = find_best_move(board)
        board[best_move[0]][best_move[1]] = AI
        print(f"AI chooses {(best_move[0]+1, best_move[1]+1)}")

    winner = check_winner(board)
    print(winner)


if __name__ == "__main__":
    main()
