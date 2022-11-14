VENV = ~/venv-cc
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

run: $(VENV)/bin/activate
	$(PIP) install -r ./src/requirements.txt
	$(PYTHON) ./src/main.py

tests: $(VENV)/bin/activate
	$(PIP) install -r ./src/requirements.txt
	$(PYTHON) -m pytest

clean:
	rm -rf __pycache__