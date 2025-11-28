ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION}-slim

WORKDIR /app

# Install system dependencies
# Note: git is required for pre-commit hooks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && git --version

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Copy project files
COPY python/ /app/python/

WORKDIR /app/python

# Install dependencies
RUN uv pip install --system -e ".[dev]"

# Default command
CMD ["pytest"]
