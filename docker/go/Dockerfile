ARG GO_VERSION=1.21
FROM golang:${GO_VERSION}-alpine

WORKDIR /app

# Install system dependencies
# Note: git is required for pre-commit hooks
RUN apk add --no-cache git ca-certificates

# Install golangci-lint
RUN wget -O- -nv https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s latest
RUN mv ./bin/golangci-lint /usr/local/bin/golangci-lint

# Copy project files
COPY go/ /app/go/

WORKDIR /app/go

# Download dependencies
RUN go mod download

# Default command
CMD ["go", "test", "./..."]
