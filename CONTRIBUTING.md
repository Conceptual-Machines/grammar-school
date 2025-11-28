# Contributing to Grammar School

Thank you for your interest in contributing to Grammar School! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites

- **Python 3.9+** for the Python implementation
- **Go 1.21+** for the Go implementation
- **Git** for version control

### Initial Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Conceptual-Machines/grammar-school.git
   cd grammar-school
   ```

2. Install dependencies:
   ```bash
   make install
   # Or manually:
   # cd python && pip install -e ".[dev]"
   # cd go && go mod download
   ```

3. Install pre-commit hooks:
   ```bash
   make pre-commit-install
   # Or: pre-commit install
   ```

## Development Workflow

### Running Tests

```bash
# Run all tests
make test

# Run Python tests only
make python-test

# Run Go tests only
make go-test
```

### Linting and Formatting

```bash
# Check formatting and linting for all languages
make all

# Format code (auto-fix)
make format

# Check formatting without modifying files
make format-check

# Run linters
make lint
```

### Pre-commit Hooks

Pre-commit hooks automatically run checks before each commit. They ensure:
- Code is properly formatted
- Linting passes
- Tests pass
- No large files are committed

To run pre-commit manually on all files:
```bash
make pre-commit-run
```

## Code Style

### Python

- **Formatter**: Ruff (replaces Black)
- **Linter**: Ruff
- **Type Checker**: mypy
- **Line Length**: 100 characters
- **Python Version**: 3.9+

Run formatting:
```bash
make python-format
```

### Go

- **Formatter**: `gofmt`
- **Linter**: `golangci-lint`
- **Style**: Follow Go standard conventions

Run formatting:
```bash
make go-format
```

## Writing Tests

### Python Tests

- Place tests in `python/tests/`
- Use `pytest` for testing
- Follow naming convention: `test_*.py` or `*_test.py`
- Aim for good test coverage

Example:
```python
def test_my_feature():
    result = my_function()
    assert result == expected
```

### Go Tests

- Place tests in `*_test.go` files alongside source files
- Use Go's standard `testing` package
- Follow naming convention: `Test*` functions

Example:
```go
func TestMyFeature(t *testing.T) {
    result := MyFunction()
    if result != expected {
        t.Errorf("expected %v, got %v", expected, result)
    }
}
```

## Pull Request Process

1. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make your changes** and ensure:
   - Code is formatted (`make format`)
   - Linting passes (`make lint`)
   - Tests pass (`make test`)
   - Pre-commit hooks pass

3. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

4. **Push and create a PR**:
   ```bash
   git push origin feature/my-feature
   ```

5. **Wait for CI** - GitHub Actions will automatically:
   - Run tests on multiple platforms
   - Check formatting and linting
   - Verify type checking

## CI/CD

The project uses GitHub Actions for continuous integration:

- **Python CI**: Tests on Ubuntu, macOS, Windows with Python 3.9-3.12
- **Go CI**: Tests on Ubuntu, macOS, Windows with Go 1.21-1.22
- **Pre-commit**: Runs on all PRs to ensure code quality

All checks must pass before merging.

## Project Structure

```
grammar-school/
├── .github/
│   └── workflows/     # CI/CD workflows
├── python/            # Python implementation
│   ├── grammar_school/
│   ├── tests/
│   └── pyproject.toml
├── go/                # Go implementation
│   ├── gs/
│   └── go.mod
├── .pre-commit-config.yaml
├── Makefile
└── README.md
```

## Questions?

Feel free to open an issue for questions or discussions!
