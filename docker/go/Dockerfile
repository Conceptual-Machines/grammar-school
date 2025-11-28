ARG GO_VERSION=1.21
FROM golang:${GO_VERSION}

WORKDIR /app

# Install system dependencies
# Note: git is required for pre-commit hooks
# Python and pip are required for pre-commit (pre-commit is a Python tool)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    ca-certificates \
    python3 \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv (required for pre-commit)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

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
