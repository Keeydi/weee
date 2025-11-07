#!/bin/bash
# Production startup script for SmartHire
# Make this file executable: chmod +x start_production.sh

# Navigate to project directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Create logs directory if it doesn't exist
mkdir -p logs

# Start Gunicorn with configuration file
gunicorn -c gunicorn_config.py wsgi:app

