const fs = require('fs');

function readDistances(filename) {
  const data = fs.readFileSync(filename, 'utf8').trim().split('\n');
  const n = parseInt(data.shift());
  return data.map(line => line.split(' ').map(Number));
}

function twoOpt(tour, distances) {
  const n = tour.length;
  
  for (let i = 0; i < n - 1; i++) {
    for (let j = i + 2; j < n; j++) {
      const change =
        -distances[tour[i]][tour[i+1]]
        -distances[tour[j]][tour[(j+1)%n]]
        +distances[tour[i]][tour[j]]
        +distances[tour[i+1]][tour[(j+1)%n]];

      if (change < -1e-10) {  // Use a small threshold to account for floating-point precision
        // Apply the first improving move
        tour.splice(i + 1, j - i, ...tour.slice(i + 1, j + 1).reverse());
        return change;
      }
    }
  }

  return 0; // No improvement found
}

function optimizeTour(distances) {
  const n = distances.length;
  const tour = Array.from({ length: n }, (_, i) => i);

  let totalImprovement = 0;
  let iterations = 0;
  const MAX_ITERATIONS = 10000;

  while (iterations < MAX_ITERATIONS) {
    const improvement = twoOpt(tour, distances);
    if (improvement >= 0) {
      break;
    }
    totalImprovement += improvement;
    iterations++;
  }

  return { tour, totalImprovement, iterations };
}

function main(filename) {
  const distances = readDistances(filename);
  const numRuns = 10;
  let totalTime = 0;

  for (let run = 0; run < numRuns; run++) {
    const startTime = process.hrtime();
    const { tour, totalImprovement, iterations } = optimizeTour(distances);
    const endTime = process.hrtime(startTime);
    const timeSpent = endTime[0] + endTime[1] / 1e9;
    totalTime += timeSpent;

    if (run === 0) {
      console.log(`Optimized tour: ${tour.join(' ')}`);
      console.log(`Total improvement: ${(-totalImprovement).toFixed(6)}`);
      console.log(`Iterations: ${iterations}`);
    }
  }

  const averageTime = totalTime / numRuns;
  console.log(`Average time spent: ${averageTime.toFixed(6)} seconds`);
}

// If this script is run directly (not imported as a module)
if (require.main === module) {
  if (process.argv.length < 3) {
    console.error('Please provide the filename as an argument.');
    process.exit(1);
  }
  main(process.argv[2]);
}

module.exports = { main };
