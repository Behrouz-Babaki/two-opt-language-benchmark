#!/bin/bash

# Save the current working directory
current_dir=$(pwd)

# Change directory to the script directory
script_dir=$(dirname "$0")
cd "$script_dir"

# Check if an input file is provided
if [[ $# -ne 1 ]]; then
    echo "Usage: ./run_tsp.sh <input_file>"
    exit 1
fi

julia tsp.jl "$1"

cd "$current_dir"
