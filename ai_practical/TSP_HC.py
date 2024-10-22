import random
from typing import List, Tuple

tsp = [
    [0, 400, 500, 300],
    [400, 0, 300, 500],
    [500, 300, 0, 400],
    [300, 500, 400, 0],
]


def randomSolution(tsp: List[List[int]]) -> List[int]:
    cities = list(range(len(tsp)))
    random.shuffle(cities)

    return cities


def routeLength(tsp: List[List[int]], solution: List[int]) -> int:
    routeLength = 0
    for i in range(len(solution)):
        routeLength += tsp[solution[i - 1]][solution[i]]

    return routeLength


def getNeighbours(solution: List[int]) -> List[List[int]]:
    neighbours: List[List[int]] = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbour = solution.copy()
            neighbour[i], neighbour[j] = solution[j], solution[i]
            neighbours.append(neighbour)

    return neighbours


def getBestNeighbour(
    tsp: List[List[int]], neighbours: List[List[int]]
) -> Tuple[List[int], int]:
    bestRouteLength = routeLength(tsp, neighbours[0])
    bestNeighbour = neighbours[0]

    for neighbour in neighbours:
        currentRouteLength = routeLength(tsp, neighbour)
        if currentRouteLength < bestRouteLength:
            bestRouteLength = currentRouteLength
            bestNeighbour = neighbour

    return bestNeighbour, bestRouteLength


def hillClimbing(tsp: List[List[int]]) -> Tuple[List[int], int]:
    currentSolution = randomSolution(tsp)
    currentRouteLength = routeLength(tsp, currentSolution)

    neighbours = getNeighbours(currentSolution)
    bestNeighbour, bestRouteLength = getBestNeighbour(tsp, neighbours)

    while bestRouteLength < currentRouteLength:
        currentSolution = bestNeighbour
        currentRouteLength = bestRouteLength
        neighbours = getNeighbours(currentSolution)
        bestNeighbour, bestRouteLength = getBestNeighbour(tsp, neighbours)

    return currentSolution, currentRouteLength


hill_climbing_solution, hill_climbing_route_length = hillClimbing(tsp)
hill_climbing_solution.append(hill_climbing_solution[0])
print("Hill Climbing Solution = ", hill_climbing_solution)
print("Hill Climbing Route Length = ", hill_climbing_route_length)
