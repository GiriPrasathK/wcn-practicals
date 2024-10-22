class Jug:
    def __init__(self, capacityA, capacityB):
        self.capacityA = capacityA
        self.capacityB = capacityB

    def dfs(self, a, b, target, visited):
        if (a, b) in visited:
            return False
        visited.add((a, b))

        # If we reached the target amount
        if a == target or b == target:
            return True

        # Possible states to explore
        states = [
            (self.capacityA, b),  # Fill Jug A
            (a, self.capacityB),  # Fill Jug B
            (0, b),               # Empty Jug A
            (a, 0),               # Empty Jug B
            (0, a + b) if a + b <= self.capacityB else (a - (self.capacityB - b), self.capacityB),  # Pour A to B
            (a + b, 0) if a + b <= self.capacityA else (self.capacityA, b - (self.capacityA - a))   # Pour B to A
        ]

        # Explore each possible state
        for state in states:
            if self.dfs(state[0], state[1], target, visited):
                return True

        return False

    def can_measure(self, target):
        visited = set()
        return self.dfs(0, 0, target, visited)


# Example usage:
if __name__ == "__main__":
    jug = Jug(4, 3)  # Jug capacities
    target = 2       # Target amount
    if jug.can_measure(target):
        print("Yes, we can measure the target amount!")
    else:
        print("No, we cannot measure the target amount.")
