# Makefile

# Variables
CYTHON = cython
PYTHON = python
SETUP = setup.py
TARGET = tsp.cpython-*.so

# Default target
all: build

# Build target
build:
	$(PYTHON) $(SETUP) build_ext --inplace

# Clean target
clean:
	rm -rf build
	rm -f $(TARGET)
	rm -f tsp.c

# Phony targets
.PHONY: all build clean