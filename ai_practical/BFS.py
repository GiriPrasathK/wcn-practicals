from collections import deque

class Jug:
    def __init__(self, capacityA, capacityB):
        self.capacityA = capacityA
        self.capacityB = capacityB

    def bfs(self, target):
        visited = set()
        queue = deque([(0, 0)])  # Start with both jugs empty

        while queue:
            a, b = queue.popleft()

            # If we reached the target amount
            if a == target or b == target:
                return True

            if (a, b) in visited:
                continue
            visited.add((a, b))

            # Possible states to explore
            states = [
                (self.capacityA, b),  # Fill Jug A
                (a, self.capacityB),  # Fill Jug B
                (0, b),               # Empty Jug A
                (a, 0),               # Empty Jug B
                (0, a + b) if a + b <= self.capacityB else
                (a - (self.capacityB - b), self.capacityB),  # Pour A to B
                (a + b, 0) if a + b <= self.capacityA else
                (self.capacityA, b - (self.capacityA - a))   # Pour B to A
            ]

            # Add new states to the queue
            for state in states:
                if state not in visited:
                    queue.append(state)

        return False

    def can_measure(self, target):
        return self.bfs(target)


# Example usage:
if __name__ == "__main__":
    jug = Jug(4, 3)  # Jug capacities
    target = 2       # Target amount
    if jug.can_measure(target):
        print("Yes, we can measure the target amount!")
    else:
        print("No, we cannot measure the target amount.")
