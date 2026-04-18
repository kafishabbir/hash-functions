# Variables
VENV_DIR = venv
PYTHON_SCRIPT = plot_data.py  # or whatever your plotting script is named
BUILD_DIR = build

all: setup run_cpp run_python

# Create build directory if it doesn't exist
$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)
	@echo "✓ Created $(BUILD_DIR) directory"

# Setup virtual environment and dependencies
setup: $(VENV_DIR)/bin/activate

$(VENV_DIR)/bin/activate:
	@echo "Creating virtual environment..."
	@python3 -m venv $(VENV_DIR)
	@echo "Installing matplotlib and pandas..."
	@. $(VENV_DIR)/bin/activate && pip install matplotlib pandas
	@echo "✓ Environment ready"

# Compile and run C++ program (ensures build dir exists)
run_cpp: $(BUILD_DIR)
	g++ hash-functions-experiment.cpp -std=c++17 -Wall -o $(BUILD_DIR)/hash-functions-experiment.exe
	./$(BUILD_DIR)/hash-functions-experiment.exe

# Run Python plotting with venv activation
run_python: $(VENV_DIR)/bin/activate
	@echo "Plotting data with Python..."
	@. $(VENV_DIR)/bin/activate && python $(PYTHON_SCRIPT)

# Clean everything
clean:
	rm -rf $(BUILD_DIR)
	rm -f data.txt
	@echo "✓ Cleaned build directory and data files"

clean-all: clean
	rm -rf $(VENV_DIR)
	@echo "✓ Virtual environment removed"

.PHONY: all setup run_cpp run_python clean clean-all
