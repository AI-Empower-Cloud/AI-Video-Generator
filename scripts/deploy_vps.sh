#!/bin/bash

# 🖥️ VPS Deployment Script
# Deploy to your own Virtual Private Server

set -e

SERVER_IP=${1:-"your-server-ip"}
SERVER_USER=${2:-"ubuntu"}
APP_DOMAIN=${3:-"your-domain.com"}

echo "🚀 Deploying AI Video Generator to VPS..."
echo "🖥️ Server: $SERVER_USER@$SERVER_IP"
echo "🌐 Domain: $APP_DOMAIN"

# Check if server IP is provided
if [ "$SERVER_IP" = "your-server-ip" ]; then
    echo "❌ Please provide server IP: ./deploy_vps.sh <server-ip> [user] [domain]"
    exit 1
fi

# Create deployment script for server
cat > deploy_server.sh << 'EOF'
#!/bin/bash

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker if not installed
if ! command -v docker &> /dev/null; then
    echo "📦 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
fi

# Install Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "📦 Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Create app directory
sudo mkdir -p /opt/ai-video-generator
sudo chown $USER:$USER /opt/ai-video-generator
cd /opt/ai-video-generator

# Clone repository
if [ ! -d ".git" ]; then
    git clone https://github.com/AI-Empower-Cloud/AI-Video-Generator.git .
else
    git pull origin main
fi

# Create production environment file
cat > .env << EOL
APP_ENV=production
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
EOL

# Build and start the application
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build

echo "✅ Deployment complete!"
echo "🌐 App should be available at: http://$(curl -s ifconfig.me):8503"
EOF

# Copy deployment script to server and execute
echo "📁 Copying deployment script to server..."
scp deploy_server.sh $SERVER_USER@$SERVER_IP:/tmp/

echo "🚀 Executing deployment on server..."
ssh $SERVER_USER@$SERVER_IP "chmod +x /tmp/deploy_server.sh && /tmp/deploy_server.sh"

# Clean up
rm deploy_server.sh

echo "✅ VPS Deployment complete!"
echo "🌐 Your app should be available at: http://$SERVER_IP:8503"

if [ "$APP_DOMAIN" != "your-domain.com" ]; then
    echo "🔧 To set up domain $APP_DOMAIN:"
    echo "   1. Point your domain's A record to $SERVER_IP"
    echo "   2. Set up reverse proxy (nginx) for SSL"
    echo "   3. Use Let's Encrypt for SSL certificate"
fi
