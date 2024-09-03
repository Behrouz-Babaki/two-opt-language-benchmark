# Specify the C++ compiler
CXX = g++

# Optimization flags
OPTFLAGS = -O3 -march=native -mtune=native -fomit-frame-pointer -flto

# Additional performance flags
PERFFLAGS = -ffast-math -funroll-loops -fpeel-loops -ftracer

# Debugging and warning flags
DEBUGFLAGS = -g -Wall -Wextra

# Set the target (the name of the compiled executable)
TARGET = tsp

# Define the source file
SOURCES = tsp.cpp

# Default to release build
CXXFLAGS = $(OPTFLAGS) $(PERFFLAGS)

# Build rules
all: release

release: CXXFLAGS = $(OPTFLAGS) $(PERFFLAGS)
release: $(TARGET)

debug: CXXFLAGS = $(DEBUGFLAGS)
debug: $(TARGET)_debug

$(TARGET): $(SOURCES)
	$(CXX) $(CXXFLAGS) $(SOURCES) -o $(TARGET)

$(TARGET)_debug: $(SOURCES)
	$(CXX) $(CXXFLAGS) $(SOURCES) -o $(TARGET)_debug

# Clean rule
clean:
	rm -f $(TARGET) $(TARGET)_debug