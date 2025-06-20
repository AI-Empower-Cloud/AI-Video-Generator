#!/bin/bash

# Testing Environment Setup and Test Runner
# This script sets up the testing environment and runs all tests

set -e  # Exit on any error

echo "🧪 Setting up AI Video Generator Testing Environment..."

# Load testing environment
if [ -f ".env.testing" ]; then
    export $(cat .env.testing | grep -v '^#' | xargs)
    echo "✅ Loaded testing environment variables"
else
    echo "❌ .env.testing file not found!"
    exit 1
fi

# Create test directories
echo "📁 Creating test directories..."
mkdir -p test_output
mkdir -p test_temp
mkdir -p test_logs

# Clean previous test files
echo "🧹 Cleaning previous test files..."
rm -rf test_output/*
rm -rf test_temp/*
rm -rf test_logs/*

# Run integrated system tests
echo "🔬 Running integrated system tests..."
python test_integrated_system.py

# Run specific component tests
echo "🔬 Running component tests..."

# Test audio integration
if [ -f "audio_integration.py" ]; then
    echo "🎵 Testing audio integration..."
    python -c "
from audio_integration import AdvancedAudioEngine
engine = AdvancedAudioEngine()
print('✅ Audio engine initialized successfully')
"
fi

# Test animation integration
if [ -f "advanced_animation.py" ]; then
    echo "🎭 Testing animation integration..."
    python -c "
from advanced_animation import AdvancedAnimationEngine
engine = AdvancedAnimationEngine()
print('✅ Animation engine initialized successfully')
"
fi

# Test enhanced video generator
echo "🎬 Testing enhanced video generator..."
python -c "
from enhanced_video_generator import AdvancedVideoGenerator
generator = AdvancedVideoGenerator()
print('✅ Enhanced video generator initialized successfully')
"

# Test Streamlit imports
echo "🌐 Testing Streamlit imports..."
python -c "
import sys
sys.path.append('.')
from streamlit_app import main
print('✅ Streamlit app imports successful')
"

# Run performance tests (if they exist)
if [ -f "test_performance.py" ]; then
    echo "⚡ Running performance tests..."
    python test_performance.py
fi

# Generate test report
echo "📊 Generating test report..."
echo "Test Report - $(date)" > test_logs/test_report.txt
echo "===========================================" >> test_logs/test_report.txt
echo "Environment: Testing" >> test_logs/test_report.txt
echo "Python Version: $(python --version)" >> test_logs/test_report.txt
echo "All tests completed successfully" >> test_logs/test_report.txt

# Clean up test files
if [ "${CLEANUP_TEMP_FILES:-true}" = "true" ]; then
    echo "🧹 Cleaning up test files..."
    rm -rf test_output/*
    rm -rf test_temp/*
fi

echo "✅ All tests completed successfully!"
echo "📊 Test report saved to test_logs/test_report.txt"
