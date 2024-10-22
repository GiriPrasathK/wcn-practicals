from dataclasses import dataclass
from typing import List, Tuple


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
        self.path: List[Jug] = []

    def dfs(self, state: Jug, target: int) -> bool:
        if (state.a, state.b) in self.visited:
            return False
        self.visited.add((state.a, state.b))

        if state.a == target or state.b == target:
            self.path.append(state)
            return True

        states = [
            Jug(self.jug1_cap, state.b),
            Jug(state.a, self.jug2_cap),
            Jug(0, state.b),
            Jug(state.a, 0),
            Jug(
                max(0, state.a - (self.jug2_cap - state.b)),
                min(self.jug2_cap, state.a + state.b),
            ),
            Jug(
                min(self.jug1_cap, state.a + state.b),
                max(0, state.b - (self.jug1_cap - state.a)),
            ),
        ]

        for state_ in states:
            if self.dfs(state_, target):
                self.path.append(state)
                return True

        return False

    def solution_path(self, target: int) -> None:
        self.dfs(Jug(0, 0), target)

        if self.path:
            self.path.reverse()
            print("Solution Found")
            for idx, step in enumerate(self.path, start=1):
                print(f"Step {idx} => {step}")
        else:
            print("Solution Not Found!")


if __name__ == "__main__":
    water_jug = WaterJug(4, 3)
    target = 2
    water_jug.solution_path(target)
