# PyPI Publishing Setup

This document explains how to set up PyPI publishing for the Grammar School Python package.

## Prerequisites

1. Create a PyPI account at https://pypi.org/account/register/
2. Create an API token at https://pypi.org/manage/account/token/

## Setting up GitHub Secrets

1. Go to your repository: https://github.com/Conceptual-Machines/grammar-school
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add a secret named `PYPI_API_TOKEN` with your PyPI API token as the value

## How It Works

When you create a git tag with a version (e.g., `v0.1.0`), the release workflow will:

1. Extract the version from the tag
2. Update version numbers in all relevant files
3. Build the Python package (wheel and source distribution)
4. Run tests to ensure everything works
5. **Publish to PyPI** (if `PYPI_API_TOKEN` is set)
6. Create a GitHub Release with the built packages

## Publishing a New Version

1. Update the version in `VERSION` file
2. Create and push a git tag:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```
3. The workflow will automatically:
   - Build the package
   - Publish to PyPI
   - Create a GitHub Release

## Installing from PyPI

Once published, users can install the package with:

```bash
pip install grammar-school
```

Or with optional dependencies:

```bash
pip install grammar-school[dev]
pip install grammar-school[docs]
```

## Test PyPI (Optional)

For testing before publishing to production PyPI, you can use Test PyPI:

1. Create an account at https://test.pypi.org/
2. Add `TEST_PYPI_API_TOKEN` as a GitHub secret
3. Update the workflow to publish to Test PyPI first for testing
