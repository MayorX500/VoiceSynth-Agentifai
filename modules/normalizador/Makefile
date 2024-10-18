# Makefile for Normalization Programs

# Compiler and Linker
CXX = g++
LD = g++

# Directories
SRC_DIR = src
BIN_DIR = bin
BUILD_DIR = build
INCLUDE_DIR = include

# Source files (assuming all source files are .cpp in the src directory)
SRC = $(wildcard $(SRC_DIR)/*.cpp)
OBJ = $(patsubst $(SRC_DIR)/%.cpp,$(BUILD_DIR)/%.o,$(SRC))

# Executable names
MAIN_BIN_NAME = mainNormalizer
DATE_BIN_NAME = date_normalizer

# Compiler flags
CXXFLAGS = -O3 -g -std=c++11 -I$(INCLUDE_DIR)  # Add custom include directory
LDFLAGS = -lcurl   # Linker flags

# Targets
.PHONY: all clean run

# Default target: Build both executables
all: checkdirs $(BIN_DIR)/$(MAIN_BIN_NAME) $(BIN_DIR)/$(DATE_BIN_NAME)

# Rule for building object files
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Rule for linking the main normalizer executable
$(BIN_DIR)/$(MAIN_BIN_NAME): $(BUILD_DIR)/mainNormalizer.o $(BUILD_DIR)/numNormalizer.o $(BUILD_DIR)/dateNormalization.o
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

# Rule for linking the date normalizer executable
$(BIN_DIR)/$(DATE_BIN_NAME): $(BUILD_DIR)/dateNormalization.o
	$(CXX) -o $@ $^ $(LDFLAGS) $(CXXFLAGS)

# Create necessary directories
checkdirs:
	@mkdir -p $(BUILD_DIR) $(BIN_DIR)

# Clean up
clean:
	rm -f $(BUILD_DIR)/* $(BIN_DIR)/*

# Run the executable with multiple arguments
run: all
	$(BIN_DIR)/$(MAIN_BIN_NAME) $(args)

# Automatic dependency generation
DEPS = $(OBJ:.o=.d)

-include $(DEPS)

$(BUILD_DIR)/%.d: $(SRC_DIR)/%.cpp
	@set -e; rm -f $@; \
	$(CXX) -MM $(CXXFLAGS) $< > $@.$$$$; \
	sed 's,\($*\)\.o[ :]*,$(BUILD_DIR)/\1.o $@ : ,g' < $@.$$$$ > $@; \
	rm -f $@.$$$$
