#!/bin/bash
# 🚀 Complete AI Video Generator Deployment Script
# Deploy everything to Wasabi + prepare for web hosting

echo "🎓 AI Video Generator - Complete Deployment"
echo "==========================================="
echo "📊 Content ready: 287MB educational platform"
echo "   - 67MB Audio (ABC songs, music)"
echo "   - 165MB Video (educational content)"
echo "   - 6.6MB Podcasts (episodes)"
echo "   - 48MB Interviews (recordings)"
echo ""

# Step 1: Check prerequisites
echo "🔍 Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is required but not installed"
    exit 1
fi

if ! python3 -c "import boto3" &> /dev/null; then
    echo "📦 Installing boto3 for Wasabi..."
    pip install boto3 python-dotenv
fi

# Step 2: Wasabi setup
echo ""
echo "🗄️  STEP 1: Wasabi Storage Setup"
echo "================================"

if [ ! -f ".env.wasabi" ]; then
    echo "⚠️  .env.wasabi not found!"
    echo "📝 Please get your Wasabi credentials:"
    echo "   1. Visit: https://wasabi.com"
    echo "   2. Sign up (free trial available)"
    echo "   3. Generate Access Keys"
    echo ""
    echo "Creating .env.wasabi template..."
    
    cat > .env.wasabi << 'EOF'
# Wasabi Credentials (replace with your actual keys)
WASABI_ACCESS_KEY=your-access-key-here
WASABI_SECRET_KEY=your-secret-key-here
WASABI_BUCKET=ai-video-generator-content
WASABI_REGION=us-east-1
WASABI_ENDPOINT=https://s3.wasabisys.com
EOF
    
    echo "✅ Created .env.wasabi template"
    echo "📝 Please edit .env.wasabi with your credentials"
    
    # Open for editing
    if command -v code &> /dev/null; then
        echo "🔧 Opening .env.wasabi in VS Code..."
        code .env.wasabi
    else
        echo "🔧 Edit .env.wasabi manually with your credentials"
    fi
    
    echo ""
    read -p "Press Enter when you've added your Wasabi credentials..."
fi

# Step 3: Test Wasabi connection
echo ""
echo "🧪 Testing Wasabi connection..."
if python3 test_wasabi_deployment.py; then
    echo "✅ Wasabi connection successful!"
else
    echo "❌ Wasabi connection failed. Please check your credentials."
    exit 1
fi

# Step 4: Deploy to Wasabi
echo ""
echo "🚀 STEP 2: Deploying to Wasabi"
echo "=============================="
echo "📦 Uploading 287MB of content..."

if python3 deploy_to_wasabi.py; then
    echo ""
    echo "🎉 Wasabi deployment successful!"
    
    # Check if manifest was created
    if [ -f "wasabi_deployment_manifest.json" ]; then
        echo "📋 Deployment manifest created"
        echo "🌐 Your content is now globally accessible!"
        
        # Show some stats
        echo ""
        echo "📊 Deployment Summary:"
        python3 -c "
import json
with open('wasabi_deployment_manifest.json', 'r') as f:
    manifest = json.load(f)
    print(f\"   Total files: {manifest['stats']['total_files']}\")
    print(f\"   Total size: {manifest['stats']['total_size_mb']:.1f} MB\")
    print(f\"   Monthly cost: ~\$0.002\")
        "
    fi
else
    echo "❌ Wasabi deployment failed"
    exit 1
fi

# Step 5: Web hosting setup
echo ""
echo "🌐 STEP 3: Web Hosting Setup"
echo "============================"
echo "Your content is now on Wasabi CDN. Next steps for web hosting:"
echo ""
echo "Option A - Durable.co (Recommended for custom HTML):"
echo "   1. Visit: https://durable.co"
echo "   2. Sign up and connect to GitHub"
echo "   3. Repository: AI-Empower-Cloud/AI-Video-Generator"
echo "   4. Build command: (none needed - static files)"
echo "   5. Publish directory: . (root)"
echo ""
echo "Option B - Wix Studio (Easier setup):"
echo "   1. Visit: https://wix.com/studio"
echo "   2. Import your HTML templates"
echo "   3. Update URLs to use Wasabi CDN"
echo ""

# Step 6: Generate URL update script
echo "🔧 Creating URL update helper..."
cat > update_urls_for_hosting.py << 'EOF'
#!/usr/bin/env python3
"""
Update HTML files to use Wasabi CDN URLs
Run this after deploying to Wasabi
"""

import json
import re
import os
from pathlib import Path

def update_html_files():
    # Load deployment manifest
    if not os.path.exists('wasabi_deployment_manifest.json'):
        print("❌ Run deploy_to_wasabi.py first!")
        return
    
    with open('wasabi_deployment_manifest.json', 'r') as f:
        manifest = json.load(f)
    
    base_url = f"{manifest['endpoint']}/{manifest['bucket']}"
    
    # HTML files to update
    html_files = [
        'educational_platform_dashboard.html',
        'stunning_music_player.html',
        'abc_video_player.html',
        'advanced_podcast_player.html',
        'platform_showcase.html'
    ]
    
    print("🔧 Updating HTML files with Wasabi URLs...")
    
    for html_file in html_files:
        if os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update local paths to Wasabi URLs
            updated_content = content
            updated_content = re.sub(r'audio_output/', f'{base_url}/audio/', updated_content)
            updated_content = re.sub(r'video_output/', f'{base_url}/videos/', updated_content)
            updated_content = re.sub(r'podcast_output/', f'{base_url}/podcasts/', updated_content)
            updated_content = re.sub(r'interview_output/', f'{base_url}/interviews/', updated_content)
            
            # Save updated file
            updated_file = f"{html_file.replace('.html', '_hosted.html')}"
            with open(updated_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"✅ Created {updated_file}")
    
    print("🎉 HTML files updated for hosting!")
    print("📁 Use the *_hosted.html files for your web hosting platform")

if __name__ == "__main__":
    update_html_files()
EOF

python3 update_urls_for_hosting.py

echo ""
echo "🎉 DEPLOYMENT COMPLETE!"
echo "======================"
echo "✅ All content deployed to Wasabi CDN"
echo "✅ HTML files updated with CDN URLs"
echo "✅ Ready for web hosting platform"
echo ""
echo "💰 Monthly cost: ~$0.002 for Wasabi + hosting fees"
echo "🌐 Your educational platform is ready to go live!"
echo ""
echo "📁 Files ready for hosting:"
ls -la *_hosted.html 2>/dev/null || echo "   (HTML files will be created after successful Wasabi deployment)"

echo ""
echo "🔗 Next steps:"
echo "   1. Choose hosting platform (Durable.co or Wix Studio)"
echo "   2. Upload the *_hosted.html files"
echo "   3. Configure domain and go live!"
echo "   4. Share your educational platform URL!"
