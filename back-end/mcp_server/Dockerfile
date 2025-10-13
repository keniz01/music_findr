# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY README.md .
COPY src ./src

# If data_accessor is in a sibling directory during build,
# you'll need to copy it in. Modify as needed.
COPY ../data_accessor ./data_accessor

# Install Hatch and pip tools
RUN pip install --upgrade pip hatch

# Install project + local dependency (data_accessor)
RUN pip install -e ./data_accessor
RUN pip install .

# Expose port (adjust as needed)
EXPOSE 8000

# Command to run the app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
