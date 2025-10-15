FROM python:3.12-slim

# Create non-root user early
RUN useradd -m appuser

# Install CA certs and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    gnupg \
    build-essential \
    openssl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 🔐 Add Zscaler cert (from build context)
COPY zscaler-root.crt /usr/local/share/ca-certificates/zscaler-root.crt
RUN update-ca-certificates

# Force Python/pip/requests to use system certs
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV PIP_CERT=/etc/ssl/certs/ca-certificates.crt

# Install certifi to satisfy some Python packages, even if not used directly
RUN pip install --upgrade pip setuptools && pip install certifi

# Install Hatch and Hatchling
RUN pip install --no-cache-dir hatch hatchling uv

# Switch to non-root user and setup app dir
USER appuser
WORKDIR /home/appuser/app

# Copy project files
COPY --chown=appuser:appuser pyproject.toml ./pyproject.toml
COPY --chown=appuser:appuser src/ ./src

# Default command: run dev server
CMD ["hatch", "run", "dev:serve"]
