.PHONY: help install test lint clean coverage report docs

# Default target
help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test      - Run tests"
	@echo "  make coverage  - Run tests with coverage"
	@echo "  make lint      - Run linting checks"
	@echo "  make clean     - Clean up build artifacts"
	@echo "  make report    - Generate test reports"
	@echo "  make docs      - Generate documentation"
	@echo "  make all       - Run all checks (lint, test, coverage)"

# Install dependencies
install:
	pip install -r requirements.txt

# Run tests
test:
	python run_tests.py

# Run tests with coverage
coverage:
	python run_tests.py --coverage

# Run linting
lint:
	flake8 .
	black --check .
	isort --check-only .

# Clean up build artifacts
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name ".eggs" -exec rm -rf {} +
	find . -type d -name "test_reports" -exec rm -rf {} +

# Generate test reports
report:
	python run_tests.py --coverage --report

# Generate documentation
docs:
	mkdocs build

# Run all checks
all: lint test coverage

# Development setup
dev-setup: install
	pip install -r requirements-dev.txt
	pre-commit install

# Run tests in parallel
test-parallel:
	python run_tests.py --parallel

# Run specific test file
test-file:
	@if [ "$(file)" = "" ]; then \
		echo "Please specify a test file: make test-file file=tests/test_file.py"; \
	else \
		python run_tests.py --test-path $(file); \
	fi

# Run tests with specific marker
test-marked:
	@if [ "$(marker)" = "" ]; then \
		echo "Please specify a marker: make test-marked marker='not slow'"; \
	else \
		python run_tests.py --markers "$(marker)"; \
	fi

# Create virtual environment
venv:
	python -m venv venv
	@echo "Virtual environment created. Activate it with:"
	@echo "  source venv/bin/activate (Linux/Mac)"
	@echo "  .\\venv\\Scripts\\activate (Windows)"

# Security checks
security:
	bandit -r .
	safety check

# Type checking
type-check:
	mypy .

# Code quality checks
quality: lint type-check security

# Continuous Integration checks
ci: quality test coverage

# Database setup (if needed)
db-setup:
	python -c "from user_auth import UserAuth; UserAuth().create_users_directory()"

# Run development server
run:
	python main.py

# Create distribution
dist: clean
	python setup.py sdist bdist_wheel

# Install in development mode
dev: clean
	pip install -e .

# Update dependencies
update-deps:
	pip install --upgrade pip
	pip install --upgrade -r requirements.txt
	@if [ -f requirements-dev.txt ]; then \
		pip install --upgrade -r requirements-dev.txt; \
	fi

# Format code
format:
	isort .
	black .

# Check code style without making changes
check-style:
	isort --check-only .
	black --check .
	flake8 .

# Create necessary directories
init:
	mkdir -p data
	mkdir -p tests/data
	mkdir -p reports
	mkdir -p docs
