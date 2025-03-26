# Backend Dockerfile - Optimized for caching
FROM python:3.12-slim AS base

# Set working directory
WORKDIR /app

# Install system dependencies in a separate layer for better caching
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    libmagic1 \
    libmagic-dev \
    && rm -rf /var/lib/apt/lists/*

# Dependencies stage - this layer gets cached if requirements don't change
FROM base AS dependencies

# Copy only requirements file first for better Docker layer caching
COPY config/requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Final stage - copy application code
FROM dependencies AS application

# Copy backend source code
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app && \
    mkdir -p /app/data/vector_db && \
    chown -R app:app /app

USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Run the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]