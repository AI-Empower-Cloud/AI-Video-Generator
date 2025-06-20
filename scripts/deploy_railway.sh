#!/bin/bash

# 🚀 Railway Deployment Script
# This script helps you deploy to Railway platform

set -e

echo "🚀 Deploying AI Video Generator to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Login to Railway (if not already logged in)
echo "🔐 Logging into Railway..."
railway login

# Link to project (or create new one)
if [ ! -f .railway ]; then
    echo "🔗 Creating new Railway project..."
    railway init
else
    echo "🔗 Using existing Railway project..."
fi

# Set environment variables
echo "⚙️ Setting environment variables..."
railway variables set APP_ENV=production
railway variables set PYTHONUNBUFFERED=1
railway variables set PYTHONDONTWRITEBYTECODE=1

# Deploy the application
echo "🚀 Deploying application..."
railway up

echo "✅ Deployment complete!"
echo "🌐 Your app will be available at the Railway-provided URL"
echo "📊 Check deployment status: railway status"
echo "📝 View logs: railway logs"
