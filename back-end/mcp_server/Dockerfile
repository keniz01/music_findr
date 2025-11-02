# Use official Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Install Hatch
RUN pip install --upgrade pip hatch

# Copy project metadata first (so Docker cache isn’t invalidated by code changes)
COPY pyproject.toml README.md ./

# Create Hatch dev environment inside the container
RUN hatch env create dev

# Copy in lockfile (if you’re using it for dependency resolution)
COPY uv.lock ./

# Expose app port
EXPOSE 8002

# Default command: run the dev server
CMD ["hatch", "run", "dev:serve"]
