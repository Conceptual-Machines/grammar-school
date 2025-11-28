# Grammar School

*A multi-language framework for building tiny LLM-friendly DSLs*

Grammar School is a lightweight, multi-language framework for creating small, precise, LLM-friendly domain-specific languages (DSLs). It provides:

- A way to **define grammar rules** (via strings or structured combinators)
- A way to **map DSL verbs to semantic handlers**
- A **parser → AST → interpreter → actions → runtime** pipeline
- Independent implementations in **Python** and **Go** (and potentially TypeScript)

## Quick Start

### Python

```bash
cd python
pip install -e .
```

### Go

```bash
cd go
go mod init grammar-school
go build ./...
```

## Repository Structure

```
grammar-school/
  README.md          # This file
  SPEC.md            # Shared conceptual specification
  
  python/            # Python implementation
    grammar_school/
    examples/
    
  go/                # Go implementation
    gs/
    examples/
    
  docs/              # Additional documentation
```

## Core Concepts

All implementations follow the same conceptual design:

1. **DSL Program**: Plain string input (typically LLM-generated)
2. **AST**: Abstract Syntax Tree (CallChain → Call → Arg → Value)
3. **Actions**: Semantic evaluation output (runtime instructions)
4. **Pipeline**: Parse → Interpret → Execute

See [SPEC.md](./SPEC.md) for the complete specification.

## License

TBD

