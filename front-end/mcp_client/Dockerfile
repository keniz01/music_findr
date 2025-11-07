# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Install Hatch
RUN pip install --no-cache-dir hatch

# Copy project files
COPY . /app

# Install dependencies using Hatch
RUN hatch env create dev

# Expose port for FastAPI
EXPOSE 8001

# Default command to run the FastAPI app using uvicorn
CMD ["hatch", "run", "dev:serve"]
