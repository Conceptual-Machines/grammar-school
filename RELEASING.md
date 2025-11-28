# Releasing Grammar School

This document describes how to create a new release of Grammar School.

## Semantic Versioning

Grammar School follows [Semantic Versioning](https://semver.org/) (SemVer):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

## Release Process

### 1. Update Version

Update the version in the following files:

- `VERSION` - Main version file
- `python/pyproject.toml` - Python package version
- `python/grammar_school/version.py` - Python module version
- `go/gs/version.go` - Go package version

### 2. Create Git Tag

Create a git tag with the version (prefixed with `v`):

```bash
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

### 3. Automated Release

The GitHub Actions workflow will automatically:

- Extract version from the tag
- Update all version files
- Build Python package
- Run tests
- Create GitHub Release
- Upload Python distribution files

### 4. Manual Steps (if needed)

If you need to release manually:

#### Python

```bash
cd python
pip install build
python -m build
# Upload to PyPI (if configured)
# twine upload dist/*
```

#### Go

Go modules use git tags for versioning. Users can install specific versions:

```bash
go get github.com/Conceptual-Machines/grammar-school/go/gs@v0.1.0
```

## Version Files

- `VERSION` - Single source of truth for version
- `python/pyproject.toml` - Python package metadata
- `python/grammar_school/version.py` - Python `__version__` constant
- `go/gs/version.go` - Go `Version` constant

## Pre-release Checklist

- [ ] All tests pass
- [ ] Documentation is up to date
- [ ] CHANGELOG.md is updated (if maintained)
- [ ] Version numbers are updated
- [ ] Git tag is created and pushed
- [ ] GitHub Release is created (automated)

## Example Release

```bash
# 1. Update version files
echo "0.2.0" > VERSION
# Update other files...

# 2. Commit changes
git add VERSION python/pyproject.toml python/grammar_school/version.py go/gs/version.go
git commit -m "chore: prepare release v0.2.0"

# 3. Create and push tag
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin main
git push origin v0.2.0

# 4. GitHub Actions will handle the rest
```
