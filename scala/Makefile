# Makefile for Scala TSP project

# Variables
SBT := sbt
BUILD_DIR := target
PROJECT_DIR := project

# Default target
all: compile

# Compile the project
compile:
	$(SBT) compile

# Clean build artifacts
clean:
	rm -rf $(BUILD_DIR) $(PROJECT_DIR)

.PHONY: all compile clean run
