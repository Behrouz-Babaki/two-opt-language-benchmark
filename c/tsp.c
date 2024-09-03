#include <stdio.h>
#include <stdlib.h>
#include <time.h>
typedef struct
{
    int *tour;
    double totalImprovement;
    int iterations;
} OptimizationResult;

int read_distances(const char *filename, double **distances, int *n)
{
    FILE *fp = fopen(filename, "r");
    if (fp == NULL)
    {
        perror("Error opening file");
        return 1;
    }

    if (fscanf(fp, "%d", n) != 1)
    {
        perror("Error reading number of nodes");
        fclose(fp);
        return 1;
    }

    *distances = malloc(sizeof(double) * (*n) * (*n));
    if (*distances == NULL)
    {
        perror("Error allocating memory for distances");
        fclose(fp);
        return 1;
    }

    for (int i = 0; i < *n; i++)
    {
        for (int j = 0; j < *n; j++)
        {
            if (fscanf(fp, "%lf", &(*distances)[i * (*n) + j]) != 1)
            {
                perror("Error reading distance");
                fclose(fp);
                free(*distances);
                return 1;
            }
        }
    }

    fclose(fp);
    return 0;
}

double two_opt(int *tour, double *distances, int n)
{
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = i + 2; j < n; j++)
        {
            double change =
                -distances[tour[i] * n + tour[i + 1]] - distances[tour[j] * n + tour[(j + 1) % n]] + distances[tour[i] * n + tour[j]] + distances[tour[i + 1] * n + tour[(j + 1) % n]];

            if (change < -1e-10) // Use a small threshold to account for floating-point precision
            {
                // Apply the first improving move
                int start = i + 1;
                int end = j;
                while (start < end)
                {
                    int temp = tour[start];
                    tour[start] = tour[end];
                    tour[end] = temp;
                    start++;
                    end--;
                }
                return change;
            }
        }
    }

    return 0; // No improvement found
}

OptimizationResult optimizeTour(double *distances, int n)
{
    int *tour = malloc(sizeof(int) * n);
    for (int i = 0; i < n; i++)
    {
        tour[i] = i;
    }

    double totalImprovement = 0;
    int iterations = 0;
    const int MAX_ITERATIONS = 10000;

    while (iterations < MAX_ITERATIONS)
    {
        double improvement = two_opt(tour, distances, n);
        if (improvement >= 0)
        {
            break;
        }
        totalImprovement += improvement;
        iterations++;
    }

    return (OptimizationResult){tour, totalImprovement, iterations};
}

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        fprintf(stderr, "Please provide the filename as an argument.\n");
        return 1;
    }

    const char *filename = argv[1];
    double *distances;
    int n;
    double improvement = 0;

    if (read_distances(filename, &distances, &n) != 0)
    {
        return 1;
    }

    const int numRuns = 10;
    double totalTime = 0;

    for (int run = 0; run < numRuns; run++)
    {
        clock_t start_time = clock();
        OptimizationResult result = optimizeTour(distances, n);
        clock_t end_time = clock();
        double time_spent = (double)(end_time - start_time) / CLOCKS_PER_SEC;
        totalTime += time_spent;

        if (run == 0)
        {
            printf("Optimized tour: ");
            for (int i = 0; i < n; i++)
            {
                printf("%d ", result.tour[i]);
            }
            printf("\nTotal improvement: %f\n", -result.totalImprovement);
            printf("Iterations: %d\n", result.iterations);
        }

        free(result.tour);
    }

    double averageTime = totalTime / numRuns;
    printf("Average time spent: %f seconds\n", averageTime);

    free(distances);

    return 0;
}