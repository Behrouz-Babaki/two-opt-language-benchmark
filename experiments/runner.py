#!/usr/bin/env python

import subprocess
import csv
import os
import sys

def run_tsp(language, input_file):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    runners = {
        'c': f'{script_dir}/../c/tsp',
        'cpp': f'{script_dir}/../cpp/tsp',
        'python': f'{script_dir}/../python/tsp.py',
        'cython': f'{script_dir}/../cython/tsp.py',
        'java': f'{script_dir}/../java/run_tsp.sh',
        'julia': f'{script_dir}/../julia/run_tsp.sh',
        'js': f'{script_dir}/../js/run_tsp.sh',
        'scala': f'{script_dir}/../scala/run_tsp.sh',
        'go': f'{script_dir}/../go/run_tsp.sh'
    }

    command = f"{runners[language]} {input_file}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.stderr:
        print(f"Error output for {language}:")
        print(result.stderr)
    
    for line in result.stdout.split('\n'):
        if "Average time spent:" in line:
            return float(line.split(":")[1].strip().split()[0])
    
    return None

def run_all_languages(input_file):
    languages = ['c', 'cpp', 'cython', 'java', 'julia', 'js', 'scala', 'go']
    results = {}

    for lang in languages:
        print(f"Running {lang} implementation...")
        runtime = run_tsp(lang, input_file)
        if runtime is not None:
            results[lang] = runtime
        else:
            print(f"Failed to get runtime for {lang}")
    
    return results

def main():
    if len(sys.argv) != 2:
        print("Usage: python runner.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    num_repeats = 10

    # Write results to CSV
    output_file = 'tsp_runtimes.csv'
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        languages = ['c', 'cpp', 'cython', 'java', 'julia', 'js', 'scala', 'go']
        writer.writerow(['Run'] + languages)
        for run in range(num_repeats):
            results = run_all_languages(input_file)
            row = [run + 1]  # Start with the run number
            for lang in languages:
                runtime = results.get(lang, '')  # Use empty string if language not in results
                row.append(runtime)
            writer.writerow(row)

    print(f"Results written to {output_file}")

if __name__ == "__main__":
    main()
