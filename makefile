VENV = /venv-cc
PYTHON = $(VENV)/bin/python3.8
PIP = $(VENV)/bin/pip

run:
	docker-compose up -d

tests: $(VENV)/bin/activate
	$(PYTHON) -m pytest

clean:
	rm -rf __pycache__