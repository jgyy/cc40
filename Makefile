PYTHON = python3
PIP = pip3
REQUIREMENTS = requirements.txt
SRC_DIR = src
TEST_DIR = tests
JSON_DATA = restaurant_data.json
XLSX_DATA = Country-Code.xlsx
OUTPUT_DIR = output

all: setup
	$(PYTHON) $(SRC_DIR)/main.py

setup:
	$(PIP) install -r $(REQUIREMENTS)

clean:
	rm -rf $(OUTPUT_DIR)/*.csv
	rm -rf __pycache__
	rm -rf $(TEST_DIR)/__pycache__
	rm -rf $(SRC_DIR)/__pycache__

test:
	$(PYTHON) -m unittest discover $(TEST_DIR)

run:
	$(PYTHON) $(SRC_DIR)/main.py $(JSON_DATA) $(XLSX_DATA) $(OUTPUT_DIR)

.PHONY: all setup clean test
