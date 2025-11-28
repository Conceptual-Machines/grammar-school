FROM golang:1.21-alpine

WORKDIR /app

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
