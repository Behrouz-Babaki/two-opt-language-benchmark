package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

type OptimizationResult struct {
	Tour             []int
	TotalImprovement float64
	Iterations       int
}

func readDistances(filename string) ([][]float64, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, fmt.Errorf("error opening file: %w", err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	scanner.Scan()
	n, err := strconv.Atoi(scanner.Text())
	if err != nil {
		return nil, fmt.Errorf("error reading number of nodes: %w", err)
	}

	distances := make([][]float64, n)
	for i := range distances {
		distances[i] = make([]float64, n)
	}

	for i := 0; i < n; i++ {
		scanner.Scan()
		values := strings.Fields(scanner.Text())
		if len(values) != n {
			return nil, fmt.Errorf("invalid number of distances in row %d", i)
		}
		for j, val := range values {
			distances[i][j], err = strconv.ParseFloat(val, 64)
			if err != nil {
				return nil, fmt.Errorf("error parsing distance at (%d, %d): %w", i, j, err)
			}
		}
	}

	return distances, nil
}

func twoOpt(tour []int, distances [][]float64) float64 {
	n := len(tour)
	for i := 0; i < n-1; i++ {
		for j := i + 2; j < n; j++ {
			change := -distances[tour[i]][tour[i+1]] - distances[tour[j]][tour[(j+1)%n]] +
				distances[tour[i]][tour[j]] + distances[tour[i+1]][tour[(j+1)%n]]

			if change < -1e-10 {
				// Apply the first improving move
				reverse(tour[i+1 : j+1])
				return change
			}
		}
	}
	return 0 // No improvement found
}

func reverse(s []int) {
	for i, j := 0, len(s)-1; i < j; i, j = i+1, j-1 {
		s[i], s[j] = s[j], s[i]
	}
}

func optimizeTour(distances [][]float64) OptimizationResult {
	n := len(distances)
	tour := make([]int, n)
	for i := range tour {
		tour[i] = i
	}

	var totalImprovement float64
	iterations := 0
	const maxIterations = 10000

	for iterations < maxIterations {
		improvement := twoOpt(tour, distances)
		if improvement >= 0 {
			break
		}
		totalImprovement += improvement
		iterations++
	}

	return OptimizationResult{
		Tour:             tour,
		TotalImprovement: totalImprovement,
		Iterations:       iterations,
	}
}

func main() {
	if len(os.Args) < 2 {
		fmt.Fprintln(os.Stderr, "Please provide the filename as an argument.")
		os.Exit(1)
	}

	filename := os.Args[1]
	distances, err := readDistances(filename)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error reading distances: %v\n", err)
		os.Exit(1)
	}

	const numRuns = 10
	var totalTime time.Duration

	for run := 0; run < numRuns; run++ {
		startTime := time.Now()
		result := optimizeTour(distances)
		elapsedTime := time.Since(startTime)
		totalTime += elapsedTime

		if run == 0 {
			fmt.Print("Optimized tour: ")
			for _, city := range result.Tour {
				fmt.Printf("%d ", city)
			}
			fmt.Printf("\nTotal improvement: %f\n", -result.TotalImprovement)
			fmt.Printf("Iterations: %d\n", result.Iterations)
		}
	}

	averageTimeSeconds := totalTime.Seconds() / float64(numRuns)
	fmt.Printf("Average time spent: %.6f seconds\n", averageTimeSeconds)
}
