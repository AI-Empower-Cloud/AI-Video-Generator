#!/bin/bash

# Development Environment Setup Script
# This script sets up the development environment for the AI Video Generator

set -e  # Exit on any error

echo "🚀 Setting up AI Video Generator Development Environment..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✅ Python $python_version is compatible"
else
    echo "❌ Python $python_version is not compatible. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Install spaCy models
echo "🧠 Installing spaCy models..."
python -m spacy download en_core_web_sm

# Install coreferee models
echo "🔗 Installing coreferee models..."
python -m coreferee install en

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p generated_videos
mkdir -p temp
mkdir -p logs
mkdir -p test_output
mkdir -p test_temp
mkdir -p test_logs

# Copy environment file
if [ ! -f ".env" ]; then
    echo "⚙️ Setting up environment variables..."
    cp .env.example .env
    echo "✅ Created .env file from .env.example"
    echo "📝 Please edit .env file with your specific settings"
else
    echo "✅ .env file already exists"
fi

# Set permissions
chmod +x scripts/*.sh 2>/dev/null || true

echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Edit .env file with your settings"
echo "3. Run the application: streamlit run streamlit_app.py"
echo "4. Or run tests: python test_integrated_system.py"
echo ""
echo "For Docker deployment:"
echo "1. Build: docker build -t ai-video-generator ."
echo "2. Run: docker run -p 8503:8503 ai-video-generator"
