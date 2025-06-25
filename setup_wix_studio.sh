#!/bin/bash
# 🎨 Wix Studio Setup Helper Script

echo "🎨 Wix Studio Deployment Setup"
echo "=============================="

# Check if Wasabi deployment is complete
if [ ! -f "wasabi_deployment_manifest.json" ]; then
    echo "❌ Please run Wasabi deployment first!"
    echo "   Run: python deploy_to_wasabi.py"
    exit 1
fi

echo "✅ Wasabi deployment detected"

# Create Wix-compatible files
echo ""
echo "📁 Preparing files for Wix Studio..."

mkdir -p wix_studio_setup
cd wix_studio_setup

# Extract Wasabi URLs for easy copy-paste
echo "🔗 Extracting media URLs from Wasabi..."
python3 << 'EOF'
import json
import os

if os.path.exists('../wasabi_deployment_manifest.json'):
    with open('../wasabi_deployment_manifest.json', 'r') as f:
        manifest = json.load(f)
    
    base_url = f"{manifest['endpoint']}/{manifest['bucket']}"
    
    # Create URL lists for Wix Media Manager
    with open('audio_urls.txt', 'w') as f:
        f.write("# Audio URLs for Wix Media Manager\n")
        f.write("# Copy these URLs and upload to Wix Audio folder\n\n")
        if 'audio' in manifest['content']:
            for file in manifest['content']['audio']:
                f.write(f"{file['public_url']}\n")
    
    with open('video_urls.txt', 'w') as f:
        f.write("# Video URLs for Wix Media Manager\n")
        f.write("# Copy these URLs and upload to Wix Video folder\n\n")
        if 'videos' in manifest['content']:
            for file in manifest['content']['videos']:
                f.write(f"{file['public_url']}\n")
    
    with open('podcast_urls.txt', 'w') as f:
        f.write("# Podcast URLs for Wix Media Manager\n")
        f.write("# Copy these URLs and upload to Wix Audio folder\n\n")
        if 'podcasts' in manifest['content']:
            for file in manifest['content']['podcasts']:
                f.write(f"{file['public_url']}\n")
    
    with open('interview_urls.txt', 'w') as f:
        f.write("# Interview URLs for Wix Media Manager\n")
        f.write("# Copy these URLs and upload to Wix Audio folder\n\n")
        if 'interviews' in manifest['content']:
            for file in manifest['content']['interviews']:
                f.write(f"{file['public_url']}\n")
    
    print("✅ URL lists created for Wix Media Manager")
else:
    print("❌ Wasabi manifest not found")
EOF

# Create Wix component templates
echo "🎨 Creating Wix component templates..."

# Audio Player Component Template
cat > wix_audio_player_template.js << 'EOF'
// Wix Audio Player Component Template
// Add this to your Wix Studio page

import { audio } from 'wix-window-frontend';

$w.onReady(function () {
    // Audio playlist data - replace URLs with your Wasabi URLs
    const audioPlaylist = [
        {
            title: "ABC Song - Clear Child Boy",
            artist: "Educational Platform",
            src: "https://s3.wasabisys.com/your-bucket/audio/abc_clear_child_boy_excited.wav"
        },
        {
            title: "ABC Song - Sweet Girl",
            artist: "Educational Platform", 
            src: "https://s3.wasabisys.com/your-bucket/audio/abc_clear_child_girl_sweet.wav"
        }
        // Add more songs from audio_urls.txt
    ];
    
    let currentTrack = 0;
    
    // Initialize audio player
    $w('#audioPlayer').src = audioPlaylist[currentTrack].src;
    $w('#trackTitle').text = audioPlaylist[currentTrack].title;
    
    // Play/Pause button
    $w('#playButton').onClick(() => {
        if ($w('#audioPlayer').isPlaying) {
            $w('#audioPlayer').pause();
            $w('#playButton').label = "Play";
        } else {
            $w('#audioPlayer').play();
            $w('#playButton').label = "Pause";
        }
    });
    
    // Next track
    $w('#nextButton').onClick(() => {
        currentTrack = (currentTrack + 1) % audioPlaylist.length;
        $w('#audioPlayer').src = audioPlaylist[currentTrack].src;
        $w('#trackTitle').text = audioPlaylist[currentTrack].title;
    });
    
    // Previous track
    $w('#prevButton').onClick(() => {
        currentTrack = currentTrack > 0 ? currentTrack - 1 : audioPlaylist.length - 1;
        $w('#audioPlayer').src = audioPlaylist[currentTrack].src;
        $w('#trackTitle').text = audioPlaylist[currentTrack].title;
    });
});
EOF

# Video Player Component Template
cat > wix_video_player_template.js << 'EOF'
// Wix Video Player Component Template
// Add this to your Wix Studio page

$w.onReady(function () {
    // Video playlist data - replace URLs with your Wasabi URLs
    const videoPlaylist = [
        {
            title: "ABC Video - Professional Teacher",
            description: "Educational ABC video with professional teacher voice",
            src: "https://s3.wasabisys.com/your-bucket/videos/youtube_professional_professional_teacher_female.mp4"
        },
        {
            title: "ABC Video - Sweet Girl Lily",
            description: "Fun ABC video with child voice",
            src: "https://s3.wasabisys.com/your-bucket/videos/youtube_professional_sweet_girl_lily.mp4"
        }
        // Add more videos from video_urls.txt
    ];
    
    let currentVideo = 0;
    
    // Initialize video player
    $w('#videoPlayer').src = videoPlaylist[currentVideo].src;
    $w('#videoTitle').text = videoPlaylist[currentVideo].title;
    $w('#videoDescription').text = videoPlaylist[currentVideo].description;
    
    // Video selection
    $w('#videoRepeater').onItemReady(($item, itemData, index) => {
        $item('#videoItem').onClick(() => {
            currentVideo = index;
            $w('#videoPlayer').src = videoPlaylist[currentVideo].src;
            $w('#videoTitle').text = videoPlaylist[currentVideo].title;
            $w('#videoDescription').text = videoPlaylist[currentVideo].description;
        });
    });
    
    // Populate video list
    $w('#videoRepeater').data = videoPlaylist;
});
EOF

# Create Wix setup instructions
cat > WIX_STUDIO_SETUP.md << 'EOF'
# 🎨 Wix Studio Setup Instructions

## Step 1: Create Wix Studio Account
1. Visit: https://www.wix.com/studio
2. Sign up for Wix Studio (not regular Wix)
3. Choose "Start Creating" → "Blank Template"

## Step 2: Set Up Media Manager
1. Go to Media Manager in Wix Studio
2. Create folders:
   - 📁 Audio (for ABC songs, music)
   - 📁 Videos (for educational content)
   - 📁 Podcasts (for episodes)
   - 📁 Interviews (for recordings)

## Step 3: Upload Media Files
Use the URL lists provided:
- Copy URLs from `audio_urls.txt` → Upload to Audio folder
- Copy URLs from `video_urls.txt` → Upload to Videos folder
- Copy URLs from `podcast_urls.txt` → Upload to Podcasts folder
- Copy URLs from `interview_urls.txt` → Upload to Interviews folder

## Step 4: Create Pages
Create these pages in Wix Studio:
1. **Home Page** - Platform overview
2. **Music Player** - Audio content
3. **Video Player** - Educational videos
4. **Podcast Player** - Podcast episodes
5. **About** - Platform information

## Step 5: Add Components
For each page, add these Wix components:

### Music Player Page:
- Audio Player component
- Repeater for playlist
- Text elements for titles
- Buttons for controls

### Video Player Page:
- Video Player component
- Repeater for video list
- Text elements for descriptions
- Navigation buttons

### Podcast Player Page:
- Audio Player component
- Repeater for episodes
- Text for descriptions
- Subscribe button

## Step 6: Add Custom Code
1. Go to Code Files in Wix Studio
2. Add the provided template files:
   - `wix_audio_player_template.js`
   - `wix_video_player_template.js`
3. Update URLs with your actual Wasabi URLs
4. Connect code to page elements

## Step 7: Design & Style
1. Use Wix Studio design tools
2. Apply consistent color scheme
3. Make responsive for mobile
4. Add animations and effects

## Step 8: SEO & Settings
1. Set page titles and descriptions
2. Add meta tags for SEO
3. Configure social media sharing
4. Set up analytics tracking

## Step 9: Publish
1. Preview your site
2. Test all functionality
3. Connect custom domain (optional)
4. Publish your site

## 📊 Expected Timeline:
- Media upload: 30-60 minutes
- Page creation: 2-3 hours
- Code integration: 1-2 hours
- Design & styling: 2-4 hours
- Testing & publish: 1 hour

## ⚠️ Limitations with Wix:
- Cannot directly embed custom HTML players
- Need to recreate functionality using Wix components
- Less flexibility than Durable.co
- Higher monthly cost

## 💡 Pro Tips:
1. Use Wix's drag-and-drop interface
2. Preview on mobile frequently
3. Test audio/video playback thoroughly
4. Use Wix SEO tools for better ranking
5. Enable Wix Analytics for visitor tracking
EOF

cd ..

echo ""
echo "✅ Wix Studio files prepared!"
echo ""
echo "🎨 Next Steps for Wix Studio:"
echo "1. Visit: https://www.wix.com/studio"
echo "2. Create account and choose blank template"
echo "3. Follow instructions in: wix_studio_setup/WIX_STUDIO_SETUP.md"
echo "4. Upload media using the provided URL lists"
echo "5. Create pages and add components"
echo "6. Integrate custom code templates"
echo "7. Design, test, and publish!"
echo ""
echo "📁 Setup files ready in: wix_studio_setup/"
echo "🌍 Your platform will be live at: https://your-site.wixsite.com"
echo ""
echo "⚠️  Note: Wix requires more manual work but offers easier visual editing"
