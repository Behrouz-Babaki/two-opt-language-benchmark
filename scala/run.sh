#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Please provide the input file path as an argument."
    exit 1
fi

input_file="$1"

# Build the project
sbt compile

# Run the project
sbt "run $input_file"
