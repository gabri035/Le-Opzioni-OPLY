#!/bin/bash

# Production startup script for FastAPI app

echo "Starting application..."
echo "PORT: $PORT"
echo "Environment: $RENDER"

# Set default values - Render provides PORT automatically
export PORT=${PORT:-10000}
export HOST=${HOST:-0.0.0.0}

echo "Using HOST: $HOST"
echo "Using PORT: $PORT"

# Health check before starting
echo "Starting FastAPI application..."

# Start the application with minimal configuration for faster startup
exec uvicorn main:app --host $HOST --port $PORT --log-level info 