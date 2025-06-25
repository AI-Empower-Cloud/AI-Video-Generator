#!/bin/bash
# 🔑 Wasabi Access Key Setup Helper

echo "🔑 Wasabi Access Key Configuration"
echo "=================================="
echo ""
echo "I can see you have your Wasabi account ready!"
echo "Account: admin@empowerhub360.org (ID: 100000405343)"
echo ""
echo "📋 To get your Access Keys:"
echo "1. In your Wasabi console, click 'Access Keys' in the left menu"
echo "2. Click 'Create New Access Key'"
echo "3. Copy the Access Key ID and Secret Access Key"
echo ""
echo "🔧 Now let's configure your credentials..."
echo ""

# Prompt for Access Key
read -p "Enter your Wasabi Access Key ID: " access_key
read -p "Enter your Wasabi Secret Access Key: " secret_key

# Validate inputs
if [ -z "$access_key" ] || [ -z "$secret_key" ]; then
    echo "❌ Both Access Key ID and Secret Access Key are required!"
    exit 1
fi

# Update .env.wasabi file
echo "📝 Updating .env.wasabi with your credentials..."

cat > .env.wasabi << EOF
# Wasabi Cloud Storage Configuration
# Account: admin@empowerhub360.org (ID: 100000405343)

# Required: Your Wasabi Access Keys
WASABI_ACCESS_KEY=$access_key
WASABI_SECRET_KEY=$secret_key

# Required: Your Wasabi Bucket Name
WASABI_BUCKET=ai-video-generator-content

# Optional: Wasabi Region (default: us-east-1)
WASABI_REGION=us-east-1

# Optional: Wasabi Endpoint (default: s3.wasabisys.com)
WASABI_ENDPOINT=https://s3.wasabisys.com

# Optional: Custom CDN Domain (if you set up CloudFlare)
CDN_DOMAIN=https://cdn.yourdomain.com

# Deployment Settings
DEPLOY_AUDIO=true
DEPLOY_VIDEO=true
DEPLOY_PODCASTS=true
DEPLOY_INTERVIEWS=true
EOF

echo "✅ Credentials configured successfully!"
echo ""
echo "🧪 Testing connection to Wasabi..."
python3 test_wasabi_deployment.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🚀 Ready to deploy! Your content summary:"
    echo "   📊 Total: 287MB of educational content"
    echo "   🎵 Audio: 67MB (47 ABC songs, music tracks)"
    echo "   🎬 Video: 165MB (40 educational videos)"  
    echo "   🎙️ Podcasts: 6.6MB (12 episodes)"
    echo "   📻 Interviews: 48MB (19 recordings)"
    echo ""
    echo "💰 Monthly cost: ~$0.002 (practically free!)"
    echo ""
    read -p "Deploy all content to Wasabi now? (y/n): " deploy_now
    
    if [[ "$deploy_now" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo ""
        echo "🚀 Starting deployment..."
        python3 deploy_to_wasabi.py
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "🎉 SUCCESS! Your educational platform is now on Wasabi!"
            echo ""
            echo "📋 Next steps:"
            echo "1. Choose hosting platform (Durable.co recommended)"
            echo "2. Run: ./setup_durable.sh"
            echo "3. Go live with your platform!"
            echo ""
            echo "🌐 Content URLs available in: wasabi_deployment_manifest.json"
        else
            echo "❌ Deployment failed. Please check the error messages above."
        fi
    else
        echo "⏸️  Deployment skipped. Run 'python3 deploy_to_wasabi.py' when ready."
    fi
else
    echo "❌ Connection test failed. Please check your credentials."
fi
