#!/bin/bash

# Production startup script for FastAPI app

# Set default values
export PORT=${PORT:-8000}
export HOST=${HOST:-0.0.0.0}

# Start the application with Gunicorn for better production performance
exec uvicorn main:app --host $HOST --port $PORT --workers 4 