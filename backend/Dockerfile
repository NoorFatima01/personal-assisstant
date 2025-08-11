# Build stage
FROM python:3.10-slim as builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install build dependencies and Python packages in one layer
COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --user --no-warn-script-location -r requirements.txt

# Runtime stage
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/home/appuser/.local/bin:$PATH

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install only runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Set working directory and switch to non-root user
WORKDIR /app
RUN chown -R appuser:appuser /app
USER appuser

# Copy application code
COPY --chown=appuser:appuser . .

# Expose port
EXPOSE 8080

# Health check (optional but recommended)
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Use exec form (JSON array) for proper signal handling
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

# CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
