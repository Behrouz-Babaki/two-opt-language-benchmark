#!/bin/bash

# Check if an input file is provided
if [[ $# -ne 1 ]]; then
    echo "Usage: ./run_tsp.sh <input_file>"
    exit 1
fi

# Compile the Java file
make

# Run the compiled class with the input file and optimizations
java -server \
    -XX:+UnlockExperimentalVMOptions \
    -XX:+UseEpsilonGC \
    -XX:+AlwaysPreTouch \
    -Xms2G -Xmx2G \
    TSPTwoOpt "$1"


