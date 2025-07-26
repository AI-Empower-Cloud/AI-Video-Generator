#!/bin/bash

# AI Video Generator Development Startup Script

set -e

echo "🚀 Starting AI Video Generator Development Server..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export PYTHONPATH="$(pwd):$PYTHONPATH"
export APP_ENV=development
export APP_DEBUG=true

# Create required directories
mkdir -p output temp static logs models

echo "📁 Created required directories"

# Check if essential packages are installed
python -c "import pydub, moviepy, fastapi" 2>/dev/null || {
    echo "❌ Essential packages not installed. Installing..."
    pip install pydub moviepy fastapi uvicorn[standard]
}

echo "✅ Essential packages verified"

# Start the FastAPI server in development mode
echo "🌐 Starting server at http://localhost:8000"
echo "📚 API docs available at http://localhost:8000/docs"
echo "🔧 Development mode with auto-reload enabled"
echo ""

uvicorn fastapi_ai_video_controller:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload \
    --log-level info \
    --access-log \
    --use-colors
