from typing import List, Optional, Tuple, Union

Player = str
EMPTY = "-"
HUMAN_PLAYER = "X"
AI_PLAYER = "O"


def print_board(board: List[List[Player]]) -> None:
    for row in board:
        print(" | ".join(row))
    print()


def check_winner(board: List[List[Player]]) -> Optional[Player]:
    win_conditions = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]

    for condition in win_conditions:
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
    if winner == AI_PLAYER:
        return 10
    elif winner == HUMAN_PLAYER:
        return -10
    return 0


def minmax(board: List[List[Player]], depth: int, is_max: bool) -> Union[int, float]:
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
                    board[i][j] = AI_PLAYER
                    best = max(best, minmax(board, depth + 1, not is_max))
                    board[i][j] = EMPTY
        return best
    else:
        best = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = HUMAN_PLAYER
                    best = min(best, minmax(board, depth + 1, not is_max))
                    board[i][j] = EMPTY
        return best


def find_best_move(board: List[List[Player]]) -> Tuple[int, int]:
    best_val = -float("inf")
    best_move: Tuple[int, int] = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI_PLAYER
                move_val = minmax(board, 0, False)
                board[i][j] = EMPTY

                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val

    return best_move


def main():
    board: List[List[Player]] = [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
    ]

    print(f"Player symbol is {HUMAN_PLAYER}")
    print(f"AI symbol is {AI_PLAYER}")

    while True:
        print_board(board)
        if not is_moves_left(board) or check_winner(board):
            break

        row, col = map(int, input("Enter your move (row and column 1-3): ").split())
        row, col = row - 1, col - 1

        if board[row][col] == EMPTY:
            board[row][col] = HUMAN_PLAYER
        else:
            print("Invalid Move, try again")
            continue

        if check_winner(board) or not is_moves_left(board):
            break

        r, c = find_best_move(board)
        board[r][c] = AI_PLAYER
        print(f"AI chooses to move: {(r+1, c+1)}")

    winner = check_winner(board)

    if winner:
        print(f"Winner is: {winner}")
    else:
        print("It's a draw")


if __name__ == "__main__":
    main()
