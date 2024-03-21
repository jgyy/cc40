PYTHON = python3.11
PIP = pip
VENV_NAME = venv
REQUIREMENTS = requirements.txt
SRC_DIR = src
TEST_DIR = tests

.PHONY: all setup clean fclean test venv re

all: venv setup
	$(VENV_NAME)/bin/$(PYTHON) $(SRC_DIR)/main.py

setup:
	$(VENV_NAME)/bin/$(PIP) install -r $(REQUIREMENTS)

clean:
	rm -rf $(OUTPUT_DIR)/*.csv
	rm -rf __pycache__
	rm -rf $(TEST_DIR)/__pycache__
	rm -rf $(SRC_DIR)/__pycache__

fclean: clean
	rm -rf $(VENV_NAME)

test:
	$(VENV_NAME)/bin/$(PYTHON) -m unittest discover $(TEST_DIR)

run:
	$(VENV_NAME)/bin/$(PYTHON) $(SRC_DIR)/main.py

venv:
	$(PYTHON) -m venv $(VENV_NAME)

re: fclean all
