import heapq
from typing import List, Optional, Tuple

# 3x3 puzzle board
State = List[List[int]]

# Goal state for 8-puzzle problem
goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0],
]

# Directions for tile movement (up, down, left, right)
directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]


# Helper function to find the position of 0 (blank space) in the puzzle
def find_blank_position(state: State) -> Tuple[int, int]:
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return -1, -1


# Function to calculate the Manhattan distance heuristic
def manhattan_distance(state: State) -> int:
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                goal_row, goal_col = divmod(state[i][j] - 1, 3)
                distance += abs(i - goal_row) + abs(j - goal_col)
    return distance


# Function to generate the possible new states by sliding tiles
def get_neighbors(state: State) -> List[State]:
    neighbors = []
    blank_row, blank_col = find_blank_position(state)

    for dr, dc in directions:
        new_row, new_col = blank_row + dr, blank_col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = [row[:] for row in state]
            new_state[blank_row][blank_col], new_state[new_row][new_col] = (
                new_state[new_row][new_col],
                new_state[blank_row][blank_col],
            )
            neighbors.append(new_state)

    return neighbors


# Function to check if the state is the goal state
def is_goal(state: State) -> bool:
    return state == goal_state


# Function to reconstruct the path to the solution
def reconstruct_path(came_from: dict, current: State) -> List[State]:
    path = [current]
    for curr in came_from:
        current = came_from[curr]
        path.append(current)
    path.reverse()
    return path


# A* algorithm for solving the 8-puzzle problem
def a_star(start: State) -> Optional[List[State]]:
    # Priority queue (min-heap) for nodes to explore
    open_list = []
    heapq.heappush(open_list, (manhattan_distance(start), 0, start))

    # Dictionary to store the path
    came_from = {}

    # g_score: cost of getting from start to the node
    g_score = {str(start): 0}

    while open_list:
        _, current_g, current_state = heapq.heappop(open_list)

        if is_goal(current_state):
            return reconstruct_path(came_from, current_state)

        for neighbor in get_neighbors(current_state):
            tentative_g = current_g + 1
            neighbor_str = str(neighbor)

            if neighbor_str not in g_score or tentative_g < g_score[neighbor_str]:
                came_from[neighbor_str] = current_state
                g_score[neighbor_str] = tentative_g
                f_score = tentative_g + manhattan_distance(neighbor)
                heapq.heappush(open_list, (f_score, tentative_g, neighbor))

    return None


# Function to print the puzzle state
def print_puzzle(state: State) -> None:
    for row in state:
        print(row)
    print()


# Example usage
if __name__ == "__main__":
    # Initial state of the 8-puzzle
    start_state = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8],
    ]

    print("Starting puzzle:")
    print_puzzle(start_state)

    solution_path = a_star(start_state)

    if solution_path:
        print("Solution found in", len(solution_path) - 1, "moves:")
        for state in solution_path:
            print_puzzle(state)
    else:
        print("No solution found!")
