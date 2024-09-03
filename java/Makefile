# Specify the Java compiler
CC = javac

# Set the target (the name of the compiled class file)
TARGET = TSPTwoOpt

# Define the source files
SOURCES = TSPTwoOpt.java

# Compiler flags
CFLAGS = -g:none

# Build rule
$(TARGET).class: $(SOURCES)
	$(CC) $(CFLAGS) $(SOURCES)

# Clean rule
clean:
	rm -f *.class