.PHONY: all init install build deploy destroy venv clean fclean re

VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
CDK := cdk

all: install build

init:
	$(CDK) init app --language python

venv:
	$(PYTHON) -m venv $(VENV_NAME)
	$(VENV_NAME)/bin/$(PIP) install -r $(REQUIREMENTS)

install:
	$(PIP) install -r requirements.txt

build:
	$(CDK) synth

deploy: build
	$(CDK) deploy --require-approval never

destroy:
	$(CDK) destroy --force

clean:
	rm -rf cdk.out/

fclean: clean
	rm -rf $(VENV)/
	rm -rf **/__pycache__/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf coverage.xml

re: fclean all
