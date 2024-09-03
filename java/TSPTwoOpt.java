import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.ArrayList;
import java.util.Collections;

public class TSPTwoOpt {

    static class OptimizationResult {
        ArrayList<Integer> tour;
        double totalImprovement;
        int iterations;

        OptimizationResult(ArrayList<Integer> tour, double totalImprovement, int iterations) {
            this.tour = tour;
            this.totalImprovement = totalImprovement;
            this.iterations = iterations;
        }
    }

    public static void main(String[] args) {
        if (args.length < 1) {
            System.err.println("Please provide the filename as an argument.");
            System.exit(1);
        }
        String filename = args[0];
        double[][] distanceMatrix;
        int n;
        
        try {
            distanceMatrix = readDistances(filename);
            n = distanceMatrix.length;
        } catch (FileNotFoundException e) {
            System.err.println("Error opening file: " + filename);
            return;
        }

        final int numRuns = 10;
        double totalTime = 0;

        for (int run = 0; run < numRuns; run++) {
            long startTime = System.currentTimeMillis();
            OptimizationResult result = optimizeTour(distanceMatrix);
            long endTime = System.currentTimeMillis();
            double timeSpent = (endTime - startTime) / 1000.0;
            totalTime += timeSpent;

            if (run == 0) {
                System.out.print("Optimized tour: ");
                for (int i = 0; i < n; i++) {
                    System.out.print(result.tour.get(i) + " ");
                }
                System.out.println("\nTotal improvement: " + (-result.totalImprovement));
                System.out.println("Iterations: " + result.iterations);
            }
        }

        double averageTime = totalTime / numRuns;
        System.out.printf("Average time spent: %.3f seconds%n", averageTime);
    }

    private static OptimizationResult optimizeTour(double[][] distanceMatrix) {
        int n = distanceMatrix.length;
        ArrayList<Integer> tour = new ArrayList<>(n);
        for (int i = 0; i < n; i++) {
            tour.add(i);
        }

        double totalImprovement = 0;
        int iterations = 0;
        final int MAX_ITERATIONS = 10000;

        while (iterations < MAX_ITERATIONS) {
            double improvement = twoOpt(tour, distanceMatrix);
            if (improvement >= 0) {
                break;
            }
            totalImprovement += improvement;
            iterations++;
        }

        return new OptimizationResult(tour, totalImprovement, iterations);
    }

    private static double twoOpt(ArrayList<Integer> tour, double[][] distances) {
        int n = tour.size();
        for (int i = 0; i < n - 1; i++) {
            for (int j = i + 2; j < n; j++) {
                double change =
                    -distances[tour.get(i)][tour.get(i + 1)]
                    -distances[tour.get(j)][tour.get((j + 1) % n)]
                    +distances[tour.get(i)][tour.get(j)]
                    +distances[tour.get(i + 1)][tour.get((j + 1) % n)];

                if (change < -1e-10) {  // Use a small threshold to account for floating-point precision
                    // Apply the first improving move
                    Collections.reverse(tour.subList(i + 1, j + 1));
                    return change;
                }
            }
        }

        return 0; // No improvement found
    }

    private static void reverseSegment(ArrayList<Integer> tour, int start, int end) {
        while (start < end) {
            int temp = tour.get(start);
            tour.set(start, tour.get(end));
            tour.set(end, temp);
            start++;
            end--;
        }
    }

    private static double[][] readDistances(String filename) throws FileNotFoundException {
        Scanner scanner = new Scanner(new File(filename));
        int n = scanner.nextInt();
        double[][] distances = new double[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                distances[i][j] = scanner.nextDouble();
            }
        }
        scanner.close();
        return distances;
    }
}
