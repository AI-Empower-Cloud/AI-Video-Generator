#!/bin/bash

# 🌐 Quick Web Service Setup
# Choose your deployment platform

echo "🌐 AI Video Generator - Web Service Setup"
echo "=========================================="
echo ""
echo "Choose your deployment platform:"
echo ""
echo "1. 🚂 Railway (Recommended - Easiest)"
echo "2. 🟣 Heroku (Traditional PaaS)"
echo "3. 🌊 Digital Ocean (App Platform)"
echo "4. 🎨 Render (Modern Alternative)"
echo "5. 🖥️  Custom VPS (Your own server)"
echo "6. ☁️  Manual setup instructions"
echo ""

read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo "🚂 Setting up Railway deployment..."
        echo "📋 Instructions:"
        echo "1. Go to: https://railway.app"
        echo "2. Sign up with GitHub"
        echo "3. Click 'Deploy from GitHub repo'"
        echo "4. Select: AI-Empower-Cloud/AI-Video-Generator"
        echo "5. Click 'Deploy'"
        echo ""
        echo "🤖 Or use the automated script:"
        echo "   ./scripts/deploy_railway.sh"
        ;;
    2)
        echo "🟣 Setting up Heroku deployment..."
        read -p "Enter your app name (or press Enter for auto-generated): " app_name
        if [ -z "$app_name" ]; then
            ./scripts/deploy_heroku.sh
        else
            ./scripts/deploy_heroku.sh "$app_name"
        fi
        ;;
    3)
        echo "🌊 Setting up Digital Ocean deployment..."
        ./scripts/deploy_digitalocean.sh
        ;;
    4)
        echo "🎨 Setting up Render deployment..."
        echo "📋 Instructions:"
        echo "1. Go to: https://render.com"
        echo "2. Connect your GitHub account"
        echo "3. Select 'Web Service'"
        echo "4. Choose your AI-Video-Generator repository"
        echo "5. Render will auto-detect the configuration"
        echo ""
        echo "Your render.yaml is already configured!"
        ;;
    5)
        echo "🖥️ Setting up custom VPS deployment..."
        read -p "Enter your server IP: " server_ip
        read -p "Enter username (default: ubuntu): " server_user
        read -p "Enter domain (optional): " domain
        
        server_user=${server_user:-ubuntu}
        domain=${domain:-your-domain.com}
        
        ./scripts/deploy_vps.sh "$server_ip" "$server_user" "$domain"
        ;;
    6)
        echo "📖 Manual setup instructions:"
        echo "See: web-service-setup.md"
        echo ""
        echo "Quick links:"
        echo "• Railway: https://railway.app"
        echo "• Heroku: https://heroku.com"
        echo "• Render: https://render.com"
        echo "• Digital Ocean: https://cloud.digitalocean.com"
        echo ""
        echo "Your repository: https://github.com/AI-Empower-Cloud/AI-Video-Generator"
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "🎉 Setup complete!"
echo "📚 Documentation: https://ai-empower-cloud.github.io/AI-Video-Generator/"
echo "📊 GitHub Actions: https://github.com/AI-Empower-Cloud/AI-Video-Generator/actions"
