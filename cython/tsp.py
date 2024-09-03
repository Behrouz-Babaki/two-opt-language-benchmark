#! /usr/bin/env python3
import time
from typing import List, Tuple
import numpy as np
from tsp import optimize_tour  # Import the Cython function

def read_distances(filename: str) -> Tuple[np.ndarray, int]:
    """
    Reads distances from a text file and returns a distance matrix and the number of nodes.

    Args:
        filename: The name of the input file.

    Returns:
        A tuple containing a distance matrix and the number of nodes.
    """
    with open(filename, 'r') as f:
        n = int(f.readline().strip())
        distances = np.zeros((n, n), dtype=np.float64)
        for i in range(n):
            row = list(map(float, f.readline().strip().split()))
            distances[i, :] = row
    return distances, n

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