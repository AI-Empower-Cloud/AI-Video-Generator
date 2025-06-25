#!/bin/bash
# 🚀 Durable.co Deployment Helper Script

echo "🌐 Durable.co Deployment Setup"
echo "=============================="

# Check if Wasabi deployment is complete
if [ ! -f "wasabi_deployment_manifest.json" ]; then
    echo "❌ Please run Wasabi deployment first!"
    echo "   Run: python deploy_to_wasabi.py"
    exit 1
fi

echo "✅ Wasabi deployment detected"

# Step 1: Prepare files for Durable.co
echo ""
echo "📁 Preparing files for Durable.co..."

# Create a deployment directory
mkdir -p durable_deployment
cd durable_deployment

# Copy essential files
echo "📋 Copying essential files..."
cp ../*_hosted.html . 2>/dev/null || echo "⚠️  No hosted HTML files found"
cp ../educational_platform_dashboard.html ./index.html
cp ../README.md .
cp ../DEPLOYMENT_PLAN.md .

# Create a simple index.html if none exists
if [ ! -f "index.html" ]; then
    echo "🏠 Creating index.html..."
    cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Video Generator - Educational Platform</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .apps { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 30px; }
        .app-card { background: #4CAF50; color: white; padding: 20px; border-radius: 8px; text-decoration: none; transition: transform 0.2s; }
        .app-card:hover { transform: translateY(-2px); }
        .app-card h3 { margin: 0 0 10px 0; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
        .stat { background: #e8f5e8; padding: 15px; border-radius: 8px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 AI Video Generator</h1>
            <p>Complete Educational Platform with Voice, Video & Audio Content</p>
        </div>
        
        <div class="stats">
            <div class="stat">
                <h3>🎵 Audio Files</h3>
                <p>47 ABC Songs & Music</p>
            </div>
            <div class="stat">
                <h3>🎬 Video Content</h3>
                <p>40 Educational Videos</p>
            </div>
            <div class="stat">
                <h3>🎙️ Podcasts</h3>
                <p>12 Educational Episodes</p>
            </div>
            <div class="stat">
                <h3>📻 Interviews</h3>
                <p>19 Live Recordings</p>
            </div>
        </div>
        
        <div class="apps">
            <a href="educational_platform_dashboard.html" class="app-card">
                <h3>🏠 Main Dashboard</h3>
                <p>Central hub for all educational content</p>
            </a>
            
            <a href="stunning_music_player.html" class="app-card">
                <h3>🎵 Music Player</h3>
                <p>ABC songs and musical content</p>
            </a>
            
            <a href="abc_video_player.html" class="app-card">
                <h3>🎬 Video Player</h3>
                <p>Educational videos and content</p>
            </a>
            
            <a href="advanced_podcast_player.html" class="app-card">
                <h3>🎙️ Podcast Player</h3>
                <p>Educational podcasts and episodes</p>
            </a>
            
            <a href="platform_showcase.html" class="app-card">
                <h3>✨ Platform Showcase</h3>
                <p>Explore all features and capabilities</p>
            </a>
        </div>
        
        <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px;">
            <h3>🚀 About This Platform</h3>
            <p>This educational platform features advanced AI-powered content generation, including:</p>
            <ul>
                <li>✅ Local TTS (Text-to-Speech) with multiple voices</li>
                <li>✅ Video generation with synchronized audio</li>
                <li>✅ Musical content creation and playback</li>
                <li>✅ Podcast and interview generation</li>
                <li>✅ Cloud storage integration (Wasabi CDN)</li>
                <li>✅ Responsive web applications</li>
            </ul>
        </div>
    </div>
</body>
</html>
EOF
fi

# Create package.json for better Durable.co compatibility
echo "📦 Creating package.json..."
cat > package.json << 'EOF'
{
  "name": "ai-video-generator",
  "version": "1.0.0",
  "description": "Complete Educational Platform with AI-powered content generation",
  "main": "index.html",
  "scripts": {
    "start": "python -m http.server 8000",
    "build": "echo 'Static site - no build needed'"
  },
  "keywords": ["education", "ai", "video", "audio", "tts", "platform"],
  "author": "AI-Empower-Cloud",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/AI-Empower-Cloud/AI-Video-Generator"
  }
}
EOF

# Create .gitignore for deployment
echo "📝 Creating .gitignore..."
cat > .gitignore << 'EOF'
# Deployment files
*.log
.env*
node_modules/
.DS_Store
*.tmp
EOF

cd ..

echo ""
echo "✅ Durable.co files prepared!"
echo ""
echo "🌐 Next Steps for Durable.co:"
echo "1. Visit: https://durable.co"
echo "2. Sign up with GitHub account"
echo "3. Import repository: AI-Empower-Cloud/AI-Video-Generator"
echo "4. Configure settings:"
echo "   - Framework: Static Site"
echo "   - Build Command: (empty)"
echo "   - Output Directory: ."
echo "   - Root Directory: (empty)"
echo "5. Deploy and test!"
echo ""
echo "📁 Deployment files ready in: durable_deployment/"
echo "🌍 Your platform will be live at: https://your-project.durable.co"
echo ""
echo "💡 Pro tip: Use 'durable_deployment' as root directory if needed"
