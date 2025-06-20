#!/bin/bash

# Production Deployment Script
# This script sets up the production environment for the AI Video Generator

set -e  # Exit on any error

echo "🚀 Setting up AI Video Generator Production Environment..."

# Load production environment
if [ -f ".env.production" ]; then
    export $(cat .env.production | grep -v '^#' | xargs)
    echo "✅ Loaded production environment variables"
else
    echo "❌ .env.production file not found!"
    exit 1
fi

# Create production directories
echo "📁 Creating production directories..."
mkdir -p /app/generated_videos
mkdir -p /app/temp
mkdir -p /app/logs
mkdir -p /app/data

# Set proper permissions
chmod 755 /app/generated_videos
chmod 755 /app/temp
chmod 755 /app/logs
chmod 755 /app/data

# Install system dependencies (if not in Docker)
if [ ! -f "/.dockerenv" ]; then
    echo "🔧 Installing system dependencies..."
    apt-get update
    apt-get install -y gcc g++ wget ffmpeg
    apt-get clean
    rm -rf /var/lib/apt/lists/*
fi

# Health check
echo "🏥 Running health checks..."

# Check Python dependencies
python3 -c "import streamlit, spacy, transformers, librosa, pydub" || {
    echo "❌ Missing Python dependencies"
    exit 1
}

# Check spaCy model
python3 -c "import spacy; nlp = spacy.load('en_core_web_sm')" || {
    echo "❌ spaCy model not found"
    exit 1
}

# Check write permissions
touch /app/generated_videos/test_file && rm /app/generated_videos/test_file || {
    echo "❌ Cannot write to output directory"
    exit 1
}

echo "✅ All health checks passed"

# Start the application
echo "🎬 Starting AI Video Generator..."
exec streamlit run streamlit_app.py \
    --server.port=${PORT:-8503} \
    --server.address=${HOST:-0.0.0.0} \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false
