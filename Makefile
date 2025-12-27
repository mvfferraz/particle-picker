.PHONY: help venv install install-dev test test-cov lint format clean build run-dashboard run-cli

VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

help:
	@echo "Particle Picker Dashboard - Makefile Commands"
	@echo "=============================================="
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make venv           - Create virtual environment"
	@echo "  make install        - Create venv and install package"
	@echo "  make install-dev    - Create venv and install with dev dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test           - Run all tests"
	@echo "  make test-cov       - Run tests with coverage report"
	@echo "  make test-unit      - Run unit tests only"
	@echo "  make test-integration - Run integration tests only"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint           - Run flake8 and mypy"
	@echo "  make format         - Format code with black and isort"
	@echo "  make check-format   - Check if code is formatted"
	@echo ""
	@echo "Build & Distribution:"
	@echo "  make build          - Build package distribution"
	@echo "  make clean          - Remove build artifacts and venv"
	@echo ""
	@echo "Run Application:"
	@echo "  make run-dashboard  - Start web dashboard"
	@echo "  make run-cli        - Show CLI help"
	@echo ""
	@echo "Examples:"
	@echo "  make analyze FILE=data/particles.star TYPE=star"
	@echo "  make compare FILES='file1.star file2.star' TYPE=star"

venv:
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV)
	@echo "Virtual environment created at ./$(VENV)"
	@echo "Activate with: source $(VENV)/bin/activate"

install: venv
	@echo "Installing package..."
	$(PIP) install --upgrade pip
	$(PIP) install -e .
	@echo ""
	@echo "Installation complete!"
	@echo "Activate environment: source $(VENV)/bin/activate"

install-dev: venv
	@echo "Installing package with dev dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"
	@echo ""
	@echo "Development installation complete!"
	@echo "Activate environment: source $(VENV)/bin/activate"

test:
	$(PYTHON) -m pytest

test-cov:
	$(PYTHON) -m pytest --cov=particle_picker --cov-report=html --cov-report=term

test-unit:
	$(PYTHON) -m pytest tests/unit/

test-integration:
	$(PYTHON) -m pytest tests/integration/

lint:
	$(PYTHON) -m flake8 particle_picker tests
	$(PYTHON) -m mypy particle_picker

format:
	$(PYTHON) -m black particle_picker tests
	$(PYTHON) -m isort particle_picker tests

check-format:
	$(PYTHON) -m black --check particle_picker tests
	$(PYTHON) -m isort --check particle_picker tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache
	rm -rf $(VENV)
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Cleaned build artifacts and virtual environment"

build: clean
	python -m build

run-dashboard:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	$(PYTHON) -m particle_picker.dashboard.app

run-cli:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	$(VENV)/bin/particle-picker --help

analyze:
	@if [ -z "$(FILE)" ] || [ -z "$(TYPE)" ]; then \
		echo "Usage: make analyze FILE=path/to/file TYPE=star|csv|box"; \
	elif [ ! -d "$(VENV)" ]; then \
		echo "Virtual environment not found. Run 'make install' first."; \
	else \
		$(VENV)/bin/particle-picker analyze -i $(FILE) -t $(TYPE) -v; \
	fi

compare:
	@if [ -z "$(FILES)" ] || [ -z "$(TYPE)" ]; then \
		echo "Usage: make compare FILES='file1 file2' TYPE=star|csv|box"; \
	elif [ ! -d "$(VENV)" ]; then \
		echo "Virtual environment not found. Run 'make install' first."; \
	else \
		$(VENV)/bin/particle-picker compare -i $(FILES) -t $(TYPE); \
	fi

list:
	@if [ -z "$(FILE)" ] || [ -z "$(TYPE)" ]; then \
		echo "Usage: make list FILE=path/to/file TYPE=star|csv|box"; \
	elif [ ! -d "$(VENV)" ]; then \
		echo "Virtual environment not found. Run 'make install' first."; \
	else \
		$(VENV)/bin/particle-picker list -i $(FILE) -t $(TYPE); \
	fi

export:
	@if [ -z "$(FILE)" ] || [ -z "$(TYPE)" ] || [ -z "$(OUTPUT)" ]; then \
		echo "Usage: make export FILE=input TYPE=star|csv|box OUTPUT=output.csv"; \
	elif [ ! -d "$(VENV)" ]; then \
		echo "Virtual environment not found. Run 'make install' first."; \
	else \
		$(VENV)/bin/particle-picker export -i $(FILE) -t $(TYPE) -o $(OUTPUT); \
	fi
