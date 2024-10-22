import heapq
from typing import List, Tuple

State = List[List[int]]

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0],
]

directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def find_blank_pos(state: State) -> Tuple[int, int]:
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return (i, j)
    return -1, -1


def manhattan_dist(state: State) -> int:
    dist = 0
    for i in range(3):
        for j in range(3):
            goal_row, goal_col = divmod(state[i][j] - 1, 3)
            dist += abs(goal_row - i) + abs(goal_col - j)
    return dist


def get_neighbours(state: State) -> List[State]:
    neighbours: List[State] = []
    blank_row, blank_col = find_blank_pos(state)

    for dr, dc in directions:
        new_row, new_col = blank_row + dr, blank_col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = [row[:] for row in state]
            new_state[blank_row][blank_col], new_state[new_row][new_col] = (
                new_state[new_row][new_col],
                new_state[blank_row][blank_col],
            )
            neighbours.append(new_state)

    return neighbours


def is_goal(state: State) -> bool:
    return state == goal_state


def reconstruct_path(came_from: dict[str, State], current: State) -> List[State]:
    path = [current]
    for curr in came_from:
        current = came_from[curr]
        path.append(current)
    path.reverse()
    return path


def a_star(start: State):
    open_list: List[Tuple[int, int, State]] = []
    heapq.heappush(open_list, (manhattan_dist(goal_state), 0, start))

    came_from: dict[str, State] = {}
    g_score: dict[str, int] = {str(start): 0}

    while open_list:
        _, current_g, current_state = heapq.heappop(open_list)

        if is_goal(current_state):
            return reconstruct_path(came_from, current_state)

        for neighbour in get_neighbours(current_state):
            tentative_g = current_g + 1
            neighbour_str = str(neighbour)

            if neighbour_str not in g_score or tentative_g < g_score[neighbour_str]:
                came_from[neighbour_str] = current_state
                g_score[neighbour_str] = tentative_g
                f_score = tentative_g + manhattan_dist(neighbour)
                heapq.heappush(open_list, (f_score, tentative_g, neighbour))

    return None


def print_puzzle(state: State) -> None:
    for row in state:
        print(row)
    print()


def main():
    start_state = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8],
    ]

    print_puzzle(start_state)

    solution_path = a_star(start_state)

    if solution_path:
        print(f"Solution found in {len(solution_path) - 1} moves: ")
        for state in solution_path:
            print_puzzle(state)
    else:
        print("No Solution Found!")


if __name__ == "__main__":
    main()
