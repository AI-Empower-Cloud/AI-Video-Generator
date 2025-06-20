#!/bin/bash

# 🌊 Digital Ocean App Platform Deployment
# This script helps you deploy to Digital Ocean

set -e

echo "🚀 Deploying AI Video Generator to Digital Ocean..."

# Check if doctl is installed
if ! command -v doctl &> /dev/null; then
    echo "📦 Installing Digital Ocean CLI..."
    echo "Please install doctl from: https://docs.digitalocean.com/reference/doctl/how-to/install/"
    exit 1
fi

# Create app spec
cat > app-spec.yaml << EOF
name: ai-video-generator
services:
- name: web
  source_dir: /
  github:
    repo: AI-Empower-Cloud/AI-Video-Generator
    branch: main
  run_command: streamlit run streamlit_app.py --server.port=\$PORT --server.address=0.0.0.0 --server.headless=true
  environment_slug: docker
  instance_count: 1
  instance_size_slug: basic-xxs
  http_port: 8503
  routes:
  - path: /
  health_check:
    http_path: /_stcore/health
  envs:
  - key: APP_ENV
    value: production
  - key: PYTHONUNBUFFERED
    value: "1"
  - key: PYTHONDONTWRITEBYTECODE
    value: "1"
EOF

# Deploy to Digital Ocean
echo "🚀 Creating Digital Ocean app..."
doctl apps create app-spec.yaml

echo "✅ Deployment initiated!"
echo "🌐 Check your apps: doctl apps list"
echo "📊 Monitor deployment: doctl apps list"
