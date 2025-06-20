#!/bin/bash

# 🌐 Heroku Deployment Script
# This script helps you deploy to Heroku platform

set -e

echo "🚀 Deploying AI Video Generator to Heroku..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "📦 Installing Heroku CLI..."
    curl https://cli-assets.heroku.com/install.sh | sh
fi

# Login to Heroku
echo "🔐 Logging into Heroku..."
heroku login

# Create Heroku app (or use existing)
APP_NAME=${1:-ai-video-generator-$(date +%s)}
echo "🔗 Creating Heroku app: $APP_NAME"

if heroku apps:info $APP_NAME &> /dev/null; then
    echo "📱 Using existing app: $APP_NAME"
else
    heroku create $APP_NAME
fi

# Set stack to container
echo "🐳 Setting stack to container..."
heroku stack:set container -a $APP_NAME

# Set environment variables
echo "⚙️ Setting environment variables..."
heroku config:set APP_ENV=production -a $APP_NAME
heroku config:set PYTHONUNBUFFERED=1 -a $APP_NAME
heroku config:set PYTHONDONTWRITEBYTECODE=1 -a $APP_NAME

# Add Heroku remote
heroku git:remote -a $APP_NAME

# Deploy
echo "🚀 Deploying to Heroku..."
git push heroku main

echo "✅ Deployment complete!"
echo "🌐 Your app is available at: https://$APP_NAME.herokuapp.com"
echo "📊 Check app status: heroku ps -a $APP_NAME"
echo "📝 View logs: heroku logs --tail -a $APP_NAME"
