from collections import deque
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class Jug:
    a: int
    b: int

    def __repr__(self) -> str:
        return f"{self.a, self.b}"


class WaterJug:
    def __init__(self, jug1_cap: int, jug2_cap: int) -> None:
        self.jug1_cap = jug1_cap
        self.jug2_cap = jug2_cap
        self.visited: set[Tuple[int, int]] = set()
        self.queue: deque[Tuple[Jug, List[Jug]]] = deque()

    def is_visited(self, state: Jug):
        return (state.a, state.b) in self.visited

    def bfs(self, target: int) -> Optional[List[Jug]]:
        init_state = Jug(0, 0)
        self.queue.append((init_state, []))
        self.visited.add((init_state.a, init_state.b))

        while self.queue:
            curr_state, path = self.queue.popleft()

            if curr_state.a == target or curr_state.b == target:
                path.append(curr_state)
                return path

            states = [
                Jug(self.jug1_cap, curr_state.b),
                Jug(curr_state.a, self.jug2_cap),
                Jug(0, curr_state.b),
                Jug(curr_state.a, 0),
                Jug(
                    min(self.jug1_cap, curr_state.a + curr_state.b),
                    max(0, curr_state.b - (self.jug1_cap - curr_state.a)),
                ),
                Jug(
                    max(0, curr_state.a - (self.jug2_cap - curr_state.b)),
                    min(self.jug2_cap, curr_state.a + curr_state.b),
                ),
            ]

            for state in states:
                if not self.is_visited(state):
                    self.visited.add((state.a, state.b))
                    self.queue.append((state, path + [curr_state]))

        return None

    def solution_path(self, target: int):
        sol_path = self.bfs(target)

        if sol_path:
            print("Solution Found")
            for step in sol_path:
                print(step)
        else:
            print(f"Soltion for target amount = {target} not found")


if __name__ == "__main__":
    water_jug = WaterJug(4, 3)
    target = 2
    water_jug.solution_path(2)
