# Contributing

Thank you for your interest in contributing to Grammar School! This document provides guidelines and instructions for contributing.

## Development Setup

See the main [CONTRIBUTING.md](../CONTRIBUTING.md) file in the repository root for complete setup instructions.

## Documentation

### Building Documentation

```bash
# Install dependencies
cd python
pip install -e ".[docs]"

# Serve locally
cd ../docs
mkdocs serve

# Build for production
mkdocs build

# Deploy to GitHub Pages (requires push access)
mkdocs gh-deploy
```

### Writing Documentation

- Use Markdown for all documentation
- Follow the existing structure
- Include code examples for both Python and Go when relevant
- Use the Material theme features (tabs, admonitions, etc.)

### API Documentation

- Python API docs are auto-generated using `mkdocstrings`
- Go API docs are manually written (can be enhanced with godoc integration)
- Keep API docs up to date with code changes

## Documentation Structure

```
docs/
├── index.md                 # Homepage
├── getting-started/         # Getting started guides
├── python/                  # Python API docs
├── go/                      # Go API docs
├── examples/                # Example DSLs
├── specification.md         # Framework specification
└── mkdocs.yml              # MkDocs configuration
```

## Style Guide

- Use clear, concise language
- Include code examples
- Use tabs for language-specific examples
- Add diagrams where helpful (Mermaid supported)

