# Frontend Dockerfile - Optimized for caching
FROM python:3.12-slim AS base

# Set working directory
WORKDIR /app

# Install system dependencies in a separate layer for better caching
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Dependencies stage - this layer gets cached if requirements don't change
FROM base AS dependencies

# Copy only requirements file first for better Docker layer caching
COPY config/requirements.txt ./requirements.txt

# Install Python dependencies (frontend has minimal deps, so this should be fast)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Final stage - copy application code
FROM dependencies AS application

# Copy frontend source code
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
CMD ["streamlit", "run", "ui/streamlit_app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]