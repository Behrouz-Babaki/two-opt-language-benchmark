# Specify the C compiler with enhanced optimization flags
CC = gcc
CFLAGS = -O3 -march=native -mtune=native -fomit-frame-pointer -flto -ffast-math -funroll-loops

# Set the target (the name of the compiled executable)
TARGET = tsp

# Define the source file
SOURCES = tsp.c

# Build rule
$(TARGET): $(SOURCES)
	$(CC) $(CFLAGS) $(SOURCES) -o $(TARGET)

# Clean rule
clean:
	rm -f $(TARGET)