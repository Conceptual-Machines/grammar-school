# Installation

Install Grammar School for your preferred language.

## Python

### From Source

```bash
cd python
pip install -e .
```

### With Development Dependencies

```bash
cd python
pip install -e ".[dev]"
```

### With Documentation Dependencies

```bash
cd python
pip install -e ".[docs]"
```

### Requirements

- Python 3.9 or higher
- `lark>=1.1.0` (parsing library)

## Go

### Installation

```bash
cd go
go mod download
```

### Requirements

- Go 1.21 or higher

### Using in Your Project

```bash
go get github.com/Conceptual-Machines/grammar-school/go/gs
```

## Verification

=== "Python"

    ```python
    import grammar_school
    print(grammar_school.__version__)
    ```

=== "Go"

    ```go
    import "grammar-school/go/gs"
    // Check that package imports successfully
    ```
