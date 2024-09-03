#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <cmath>

using namespace std;

struct OptimizationResult
{
    vector<int> tour;
    double totalImprovement;
    int iterations;
};

int read_distances(const string &filename, vector<vector<double>> &distances)
{
    ifstream file(filename);
    if (!file.is_open())
    {
        cerr << "Error opening file: " << filename << endl;
        return 1;
    }

    int n;
    file >> n;

    distances.resize(n, vector<double>(n));
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            if (!(file >> distances[i][j]))
            {
                cerr << "Error reading distance" << endl;
                return 1;
            }
        }
    }

    return 0;
}

double two_opt(vector<int> &tour, const vector<vector<double>> &distances)
{
    int n = tour.size();
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = i + 2; j < n; j++)
        {
            double change =
                -distances[tour[i]][tour[i + 1]] - distances[tour[j]][tour[(j + 1) % n]] + distances[tour[i]][tour[j]] + distances[tour[i + 1]][tour[(j + 1) % n]];

            if (change < -1e-10)
            { // Use a small threshold to account for floating-point precision
                // Apply the first improving move
                reverse(tour.begin() + i + 1, tour.begin() + j + 1);
                return change;
            }
        }
    }

    return 0; // No improvement found
}

OptimizationResult optimizeTour(const vector<vector<double>> &distances)
{
    int n = distances.size();
    vector<int> tour(n);
    for (int i = 0; i < n; i++)
    {
        tour[i] = i;
    }

    double totalImprovement = 0;
    int iterations = 0;
    const int MAX_ITERATIONS = 10000;

    while (iterations < MAX_ITERATIONS)
    {
        double improvement = two_opt(tour, distances);
        if (improvement >= 0)
        {
            break;
        }
        totalImprovement += improvement;
        iterations++;
    }

    return {tour, totalImprovement, iterations};
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        cerr << "Usage: " << argv[0] << " <filename>" << endl;
        return 1;
    }

    const string filename = argv[1];
    vector<vector<double>> distances;

    if (read_distances(filename, distances) != 0)
    {
        return 1;
    }

    const int numRuns = 10;
    double totalTime = 0;

    for (int run = 0; run < numRuns; run++)
    {
        auto start_time = chrono::high_resolution_clock::now();
        auto result = optimizeTour(distances);
        auto end_time = chrono::high_resolution_clock::now();
        chrono::duration<double> time_spent = end_time - start_time;
        totalTime += time_spent.count();

        if (run == 0)
        {
            cout << "Optimized tour: ";
            for (int i : result.tour)
            {
                cout << i << " ";
            }
            cout << "\nTotal improvement: " << -result.totalImprovement << endl;
            cout << "Iterations: " << result.iterations << endl;
        }
    }

    double averageTime = totalTime / numRuns;
    cout << "Average time spent: " << averageTime << " seconds" << endl;

    return 0;
}
