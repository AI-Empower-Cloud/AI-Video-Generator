#!/bin/bash
# 🚀 One-Click Wasabi Setup for Educational Platform

echo "🗄️  Educational Platform - Wasabi Setup"
echo "======================================="

# Check if .env.wasabi exists
if [ ! -f ".env.wasabi" ]; then
    echo "📝 Creating .env.wasabi configuration file..."
    echo "⚠️  You need to add your Wasabi credentials!"
    echo ""
    echo "📋 Please:"
    echo "1. Sign up at https://wasabi.com (free trial)"
    echo "2. Generate Access Keys in Wasabi console"
    echo "3. Edit .env.wasabi with your credentials"
    echo ""
    read -p "Press Enter when you have your Wasabi credentials ready..."
    
    # Open .env.wasabi for editing
    if command -v code &> /dev/null; then
        code .env.wasabi
    else
        nano .env.wasabi
    fi
fi

echo ""
echo "🧪 Testing Wasabi connection..."
python test_wasabi_deployment.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🚀 Ready to deploy! Run deployment now? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "🚀 Starting deployment..."
        python deploy_to_wasabi.py
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "🎉 SUCCESS! Your educational platform is now on Wasabi!"
            echo "📊 Content deployed:"
            echo "   - 🎵 Audio files (ABC songs, music)"
            echo "   - 🎬 Video files (educational videos)"
            echo "   - 🎙️ Podcast episodes"
            echo "   - 📻 Interview recordings"
            echo ""
            echo "💰 Monthly cost: ~$0.002 (under 1 cent!)"
            echo "🌐 All files are publicly accessible"
            echo "📋 Check wasabi_deployment_manifest.json for URLs"
        fi
    fi
else
    echo "❌ Please fix the connection issues first"
fi
