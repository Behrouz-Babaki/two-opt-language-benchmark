import time
from typing import List, Tuple
cimport cython
from libc.stdlib cimport malloc, free

@cython.boundscheck(False)
@cython.wraparound(False)
def two_opt(int[:] tour, double[:, :] distances, int n) -> double:
    cdef int i, j, start, end, temp
    cdef double change

    for i in range(n-1):
        for j in range(i + 2, n):
            change = (
                -distances[tour[i], tour[i+1]]
                -distances[tour[j], tour[(j+1)%n]]
                +distances[tour[i], tour[j]]
                +distances[tour[i+1], tour[(j+1)%n]]
            )

            if change < -1e-10:  # Use a small threshold to account for floating-point precision
                # Apply the first improving move
                tour[i+1:j+1] = tour[i+1:j+1][::-1]
                return change

    return 0.0  # No improvement found

@cython.boundscheck(False)
@cython.wraparound(False)
def optimize_tour(double[:, :] distances, int n) -> Tuple[List[int], double, int]:
    cdef int[:] tour = cython.view.array(shape=(n,), itemsize=cython.sizeof(cython.int), format="i")
    cdef int i, iterations = 0
    cdef double total_improvement = 0.0
    cdef double improvement
    cdef int MAX_ITERATIONS = 10000

    for i in range(n):
        tour[i] = i

    while iterations < MAX_ITERATIONS:
        improvement = two_opt(tour, distances, n)
        if improvement >= 0:
            break
        total_improvement += improvement
        iterations += 1

    return list(tour), total_improvement, iterations
