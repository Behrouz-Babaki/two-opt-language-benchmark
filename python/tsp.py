#! /usr/bin/env python3
import time
from typing import List, Tuple

def read_distances(filename: str) -> Tuple[List[List[float]], int]:
    """
    Reads distances from a text file and returns a distance matrix and the number of nodes.

    Args:
        filename: The name of the input file.

    Returns:
        A tuple containing a distance matrix and the number of nodes.
    """
    with open(filename, 'r') as f:
        n = int(f.readline().strip())
        distances: List[List[float]] = []
        for _ in range(n):
            row = list(map(float, f.readline().strip().split()))
            distances.append(row)
    return distances, n

def two_opt(tour: List[int], distances: List[List[float]], n: int) -> float:
    """
    Implements the two-opt move to improve a given TSP tour.

    Args:
        tour: A list representing the current TSP tour.
        distances: A distance matrix containing distances between cities.
        n: The number of nodes.

    Returns:
        The improvement in total distance, or 0 if no improvement was found.
    """
    for i in range(n-1):
        for j in range(i + 2, n):
            change = (
                -distances[tour[i]][tour[i+1]]
                -distances[tour[j]][tour[(j+1)%n]]
                +distances[tour[i]][tour[j]]
                +distances[tour[i+1]][tour[(j+1)%n]]
            )

            if change < -1e-10:  # Use a small threshold to account for floating-point precision
                # Apply the first improving move
                tour[i+1:j+1] = reversed(tour[i+1:j+1])
                return change

    return 0  # No improvement found

def optimize_tour(distances: List[List[float]], n: int) -> Tuple[List[int], float, int]:
    tour = list(range(n))
    total_improvement = 0.0
    iterations = 0
    MAX_ITERATIONS = 10000

    while iterations < MAX_ITERATIONS:
        improvement = two_opt(tour, distances, n)
        if improvement >= 0:
            break
        total_improvement += improvement
        iterations += 1

    return tour, total_improvement, iterations

def main() -> None:
    import sys
    if len(sys.argv) < 2:
        print("Please provide the filename as an argument.")
        return

    filename = sys.argv[1]
    distances, n = read_distances(filename)
    tour = list(range(n))  # Initialize tour from 0 to n-1

    num_runs = 10
    total_time = 0.0

    for run in range(num_runs):
        start_time = time.time()
        tour, total_improvement, iterations = optimize_tour(distances, n)
        end_time = time.time()
        time_spent = end_time - start_time
        total_time += time_spent

        if run == 0:
            print("Optimized tour:", " ".join(map(str, tour)))  # Format output to match C version
            print(f"Total improvement: {-total_improvement:.6f}")
            print(f"Iterations: {iterations}")

    average_time = total_time / num_runs
    print(f"Average time spent: {average_time:.6f} seconds")

if __name__ == '__main__':
    main()