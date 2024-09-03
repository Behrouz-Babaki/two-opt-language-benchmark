#!/usr/bin/env python3

import sys
import random
import math

def generate_points(n):
    points = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]
    return points

def calculate_distances(points):
    n = len(points)
    distances = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                distances[i][j] = math.sqrt((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2)
    return distances

def write_distances_to_file(filename, distances):
    n = len(distances)
    with open(filename, 'w') as f:
        f.write(f"{n}\n")
        for row in distances:
            f.write(" ".join(map(str, row)) + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate.py <number_of_nodes> <output_file>")
        sys.exit(1)

    n = int(sys.argv[1])
    output_file = sys.argv[2]

    points = generate_points(n)
    distances = calculate_distances(points)
    write_distances_to_file(output_file, distances)
