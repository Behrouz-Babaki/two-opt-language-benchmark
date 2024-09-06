#!/bin/bash

# Save the current working directory
current_dir=$(pwd)

# Change directory to the script directory
script_dir=$(dirname "$0")
cd "$script_dir"

# Check if the input file is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

# Run the Go program
go run tsp.go $1

cd "$current_dir"