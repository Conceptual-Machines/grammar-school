.PHONY: help install test lint format pre-commit clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Python targets
python-install: ## Install Python dependencies
	cd python && pip install -e ".[dev]"

python-test: ## Run Python tests
	cd python && pytest

python-lint: ## Run Python linter (ruff check)
	cd python && ruff check .

python-format: ## Format Python code (ruff format)
	cd python && ruff format .

python-format-check: ## Check Python formatting without modifying files
	cd python && ruff format --check .

python-type-check: ## Run Python type checker (mypy)
	cd python && mypy grammar_school || true

python-all: python-lint python-format-check python-type-check python-test ## Run all Python checks

# Go targets
go-install: ## Download Go dependencies
	cd go && go mod download

go-test: ## Run Go tests
	cd go && go test -v -race -coverprofile=coverage.out ./...

go-lint: ## Run Go linter (golangci-lint)
	cd go && golangci-lint run

go-format: ## Format Go code (gofmt)
	cd go && gofmt -s -w .

go-format-check: ## Check Go formatting without modifying files
	cd go && gofmt -s -l . | grep -q . && exit 1 || exit 0

go-vet: ## Run go vet
	cd go && go vet ./...

go-all: go-format-check go-vet go-lint go-test ## Run all Go checks

# Pre-commit
pre-commit-install: ## Install pre-commit hooks
	pip install pre-commit
	pre-commit install

pre-commit-run: ## Run pre-commit on all files
	pre-commit run --all-files

# Combined targets
install: python-install go-install ## Install all dependencies

test: python-test go-test ## Run all tests

lint: python-lint go-lint ## Run all linters

format: python-format go-format ## Format all code

format-check: python-format-check go-format-check ## Check formatting for all code

type-check: python-type-check ## Run type checkers

all: python-all go-all ## Run all checks for all languages

# Documentation
docs-install: ## Install documentation dependencies
	cd python && pip install -e ".[docs]"

docs-serve: ## Serve documentation locally
	cd docs && mkdocs serve

docs-build: ## Build documentation
	cd docs && mkdocs build

docs-deploy: ## Deploy documentation to GitHub Pages
	cd docs && mkdocs gh-deploy --force

clean: ## Clean build artifacts
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -r {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -r {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "coverage.out" -delete
	find . -type f -name "coverage.xml" -delete
	find . -type d -name "htmlcov" -exec rm -r {} + 2>/dev/null || true

