# Grammar School Documentation

This directory contains the documentation for Grammar School, built with [MkDocs](https://www.mkdocs.org/) and the [Material theme](https://squidfunk.github.io/mkdocs-material/).

## Local Development

### Prerequisites

- Python 3.9+
- pip

### Setup

```bash
# Install documentation dependencies
cd python
pip install -e ".[docs]"

# Or install directly
pip install mkdocs mkdocs-material mkdocstrings[python] pymdown-extensions
```

### Serve Locally

```bash
cd docs
mkdocs serve
```

The documentation will be available at `http://127.0.0.1:8000`

### Build

```bash
cd docs
mkdocs build
```

This creates a `site/` directory with the static HTML files.

## Deployment

Documentation is automatically deployed to GitHub Pages via GitHub Actions when changes are pushed to the `main` branch.

### Manual Deployment

If you need to deploy manually:

```bash
cd docs
mkdocs gh-deploy
```

This will build the documentation and push it to the `gh-pages` branch.

## Structure

```
docs/
├── mkdocs.yml          # MkDocs configuration
├── index.md            # Homepage
├── getting-started/    # Getting started guides
├── python/             # Python API documentation
├── go/                 # Go API documentation
├── examples/           # Example DSLs
├── specification.md    # Framework specification
└── contributing.md     # Contributing guide
```

## Adding New Documentation

1. Create a new Markdown file in the appropriate directory
2. Add it to the `nav` section in `mkdocs.yml`
3. Follow the existing documentation style
4. Use code tabs for language-specific examples

## API Documentation

- Python API docs are auto-generated using `mkdocstrings`
- Go API docs are manually written (can be enhanced with godoc integration)
