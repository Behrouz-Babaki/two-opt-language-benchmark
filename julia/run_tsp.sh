#!/bin/bash

# Check if an input file is provided
if [[ $# -ne 1 ]]; then
    echo "Usage: ./run_tsp.sh <input_file>"
    exit 1
fi

julia tsp.julia "$1"
