#!/bin/bash

echo "🚀 Setting up AI Video Generator Frontend..."

# Navigate to frontend directory
cd /workspaces/AI-Video-Generator/frontend

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Install additional dependencies
echo "📦 Installing additional packages..."
npm install next-themes@^0.2.1

echo "✅ Frontend setup complete!"
echo ""
echo "To start the development server, run:"
echo "cd /workspaces/AI-Video-Generator/frontend && npm run dev"
