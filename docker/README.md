# Docker Setup for Grammar School

This directory contains Dockerfiles for reproducible builds and testing.

## Dockerfiles

- `python/Dockerfile` - Python development and testing environment
- `go/Dockerfile` - Go development and testing environment

## Usage

### Build Images

```bash
# Build Python image
docker build -f docker/python/Dockerfile -t grammar-school-python .

# Build Go image
docker build -f docker/go/Dockerfile -t grammar-school-go .
```

### Run Tests

```bash
# Python tests
docker run --rm -v $(pwd)/python:/app/python grammar-school-python pytest

# Go tests
docker run --rm -v $(pwd)/go:/app/go grammar-school-go go test ./...
```

### Using Docker Compose

```bash
# Run all tests
docker-compose run python-test
docker-compose run go-test

# Run linting
docker-compose run python-lint
docker-compose run go-lint
```

## CI Integration

The GitHub Actions workflows use these Docker images for reproducible CI builds. This ensures:

- Consistent environment across all CI runs
- Same dependencies and versions every time
- Isolated builds that don't affect the host system
- Faster builds with Docker layer caching

## Benefits

1. **Reproducibility** - Same environment every time
2. **Isolation** - No conflicts with host system
3. **Speed** - Docker layer caching speeds up builds
4. **Consistency** - Same setup locally and in CI

