#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# Load environment variables from .env file with variable expansion
if [ -f .env ]; then
    # Source the .env file to enable variable expansion
    set -a  # automatically export all variables
    source .env
    set +a  # turn off automatic export
fi

# Install dependencies
echo "Installing dependencies..."
uv sync

# Run the Streamlit app
echo "Starting Data Insights Assistant UI..."
streamlit run src/app.py --server.port=8501 