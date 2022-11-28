VENV = /venv-cc
PYTHON = $(VENV)/bin/python3.8
PIP = $(VENV)/bin/pip

run: $(VENV)/bin/activate
	$(PYTHON) ./src/main.py

tests: $(VENV)/bin/activate
	$(PYTHON) -m pytest

clean:
	rm -rf __pycache__