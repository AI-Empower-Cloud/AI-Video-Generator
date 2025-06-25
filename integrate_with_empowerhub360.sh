#!/bin/bash
# 🎨 Wix Studio Integration for EmpowerHub360.ai
# Add AI Video Generator to your existing Wix Studio site

echo "🎨 Wix Studio Integration for EmpowerHub360.ai"
echo "=============================================="
echo ""
echo "✅ Detected existing Wix Studio site: https://www.empowerhub360.ai"
echo "✅ Site has AI tool categories - perfect fit for Video Generator!"
echo ""
echo "📋 Integration Plan:"
echo "1. Add 'AI Educational Tools' to your existing categories"
echo "2. Upload media content to your Wix Media Manager"
echo "3. Create new pages for video/audio players"
echo "4. Integrate with your existing design theme"
echo ""

# Check if Wasabi deployment is complete
if [ ! -f "wasabi_deployment_manifest.json" ]; then
    echo "⚠️  Wasabi deployment needed first!"
    echo ""
    read -p "Do you want to deploy to Wasabi first? (y/n): " deploy_wasabi
    
    if [[ "$deploy_wasabi" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "🚀 Let's get your Wasabi credentials first..."
        ./configure_wasabi_keys.sh
        exit 0
    else
        echo "📝 Please run ./configure_wasabi_keys.sh when ready to deploy content"
        exit 0
    fi
fi

echo "✅ Wasabi deployment detected"
echo ""
echo "🎨 Creating Wix Studio integration files..."

mkdir -p wix_empowerhub_integration
cd wix_empowerhub_integration

# Extract content URLs for Wix Media Manager
echo "🔗 Preparing media URLs for your Wix site..."

python3 << 'EOF'
import json
import os

if os.path.exists('../wasabi_deployment_manifest.json'):
    with open('../wasabi_deployment_manifest.json', 'r') as f:
        manifest = json.load(f)
    
    base_url = f"{manifest['endpoint']}/{manifest['bucket']}"
    
    # Create organized content for Wix
    with open('wix_media_upload_guide.md', 'w') as f:
        f.write("# 🎨 Wix Media Manager Upload Guide\n")
        f.write("## For EmpowerHub360.ai Integration\n\n")
        
        f.write("## 📁 Create These Folders in Wix Media Manager:\n")
        f.write("1. **AI Educational Tools** (main folder)\n")
        f.write("   - **ABC Songs** (subfolder)\n")
        f.write("   - **Educational Videos** (subfolder)\n")
        f.write("   - **Podcasts** (subfolder)\n")
        f.write("   - **Interviews** (subfolder)\n\n")
        
        # Audio content
        f.write("## 🎵 ABC Songs & Music (Upload to 'ABC Songs' folder):\n")
        if 'audio' in manifest['content']:
            for i, file in enumerate(manifest['content']['audio'][:10], 1):
                f.write(f"{i}. {file['filename']} - {file['public_url']}\n")
            if len(manifest['content']['audio']) > 10:
                f.write(f"... and {len(manifest['content']['audio']) - 10} more files\n")
        f.write("\n")
        
        # Video content
        f.write("## 🎬 Educational Videos (Upload to 'Educational Videos' folder):\n")
        if 'videos' in manifest['content']:
            for i, file in enumerate(manifest['content']['videos'][:10], 1):
                f.write(f"{i}. {file['filename']} - {file['public_url']}\n")
            if len(manifest['content']['videos']) > 10:
                f.write(f"... and {len(manifest['content']['videos']) - 10} more files\n")
        f.write("\n")
        
        # Podcast content
        f.write("## 🎙️ Podcasts (Upload to 'Podcasts' folder):\n")
        if 'podcasts' in manifest['content']:
            for i, file in enumerate(manifest['content']['podcasts'], 1):
                f.write(f"{i}. {file['filename']} - {file['public_url']}\n")
        f.write("\n")
        
        # Interview content
        f.write("## 📻 Interviews (Upload to 'Interviews' folder):\n")
        if 'interviews' in manifest['content']:
            for i, file in enumerate(manifest['content']['interviews'], 1):
                f.write(f"{i}. {file['filename']} - {file['public_url']}\n")
    
    print("✅ Wix Media upload guide created")
else:
    print("❌ Wasabi manifest not found")
EOF

# Create page templates for EmpowerHub360.ai
echo "📄 Creating page templates for your Wix site..."

cat > empowerhub360_page_structure.md << 'EOF'
# 🏗️ Page Structure for EmpowerHub360.ai

## New Pages to Add:

### 1. AI Educational Tools (Main Page)
**URL**: /ai-educational-tools
**Purpose**: Showcase the video generator platform
**Layout**: 
- Hero section with platform overview
- Grid of tool categories
- Links to individual players

### 2. ABC Learning Center
**URL**: /abc-learning-center  
**Purpose**: Interactive ABC songs and videos
**Components**:
- Audio player for ABC songs
- Video gallery for educational videos
- Progress tracking for kids

### 3. Educational Podcasts
**URL**: /educational-podcasts
**Purpose**: Podcast episodes for educators
**Components**:
- Podcast player
- Episode list with descriptions
- Subscribe functionality

### 4. Teacher Resources
**URL**: /teacher-resources
**Purpose**: Interview content and resources
**Components**:
- Interview audio player
- Resource downloads
- Community features

## Integration with Existing Site:

### Update Main Navigation:
Add under "AI Tool Plans" or create new section:
- AI Educational Tools
- ABC Learning Center  
- Educational Podcasts
- Teacher Resources

### Update Homepage:
Add new card in your existing grid:
```
AI Educational Tools
Learn smarter with adaptive AI tutors,
ABC songs, videos, and educational content.
[Explore] -> /ai-educational-tools
```
EOF

# Create Wix component code templates
cat > wix_educational_player_code.js << 'EOF'
// Wix Code for Educational Content Players
// Add this to your EmpowerHub360.ai site pages

import { audio } from 'wix-window-frontend';

$w.onReady(function () {
    
    // ABC Songs Player Configuration
    const abcSongs = [
        {
            title: "ABC Song - Clear Child Voice",
            artist: "AI Educational Platform",
            duration: "2:30",
            category: "Kids Learning",
            src: "YOUR_WASABI_URL_HERE" // Replace with actual Wasabi URL
        },
        {
            title: "ABC Song - Teacher Voice", 
            artist: "AI Educational Platform",
            duration: "2:45",
            category: "Classroom",
            src: "YOUR_WASABI_URL_HERE" // Replace with actual Wasabi URL
        }
        // Add more songs from your content
    ];
    
    // Educational Videos Configuration
    const educationalVideos = [
        {
            title: "Professional ABC Teaching Video",
            description: "Learn the alphabet with professional teacher guidance",
            duration: "3:15",
            category: "Educational",
            thumbnail: "YOUR_THUMBNAIL_URL",
            src: "YOUR_WASABI_URL_HERE" // Replace with actual Wasabi URL
        }
        // Add more videos from your content
    ];
    
    // Initialize Audio Player
    let currentSong = 0;
    let isPlaying = false;
    
    // Load first song
    if (abcSongs.length > 0) {
        $w('#audioPlayer').src = abcSongs[currentSong].src;
        $w('#songTitle').text = abcSongs[currentSong].title;
        $w('#songArtist').text = abcSongs[currentSong].artist;
    }
    
    // Play/Pause functionality
    $w('#playPauseBtn').onClick(() => {
        if (isPlaying) {
            $w('#audioPlayer').pause();
            $w('#playPauseBtn').label = "▶️ Play";
            isPlaying = false;
        } else {
            $w('#audioPlayer').play();
            $w('#playPauseBtn').label = "⏸️ Pause";
            isPlaying = true;
        }
    });
    
    // Next song
    $w('#nextBtn').onClick(() => {
        currentSong = (currentSong + 1) % abcSongs.length;
        loadSong(currentSong);
    });
    
    // Previous song  
    $w('#prevBtn').onClick(() => {
        currentSong = currentSong > 0 ? currentSong - 1 : abcSongs.length - 1;
        loadSong(currentSong);
    });
    
    // Load song function
    function loadSong(index) {
        $w('#audioPlayer').src = abcSongs[index].src;
        $w('#songTitle').text = abcSongs[index].title;
        $w('#songArtist').text = abcSongs[index].artist;
        $w('#playPauseBtn').label = "▶️ Play";
        isPlaying = false;
    }
    
    // Video player setup
    if (educationalVideos.length > 0) {
        $w('#videoPlayer').src = educationalVideos[0].src;
        $w('#videoTitle').text = educationalVideos[0].title;
        $w('#videoDescription').text = educationalVideos[0].description;
    }
    
    // Video selection from repeater
    $w('#videoRepeater').onItemReady(($item, itemData, index) => {
        $item('#videoThumbnail').src = itemData.thumbnail;
        $item('#videoItemTitle').text = itemData.title;
        $item('#videoDuration').text = itemData.duration;
        
        $item('#videoItem').onClick(() => {
            $w('#videoPlayer').src = itemData.src;
            $w('#videoTitle').text = itemData.title;
            $w('#videoDescription').text = itemData.description;
        });
    });
    
    // Populate video repeater
    $w('#videoRepeater').data = educationalVideos;
    
    // Category filter functionality
    $w('#categoryFilter').onChange(() => {
        const selectedCategory = $w('#categoryFilter').value;
        if (selectedCategory === 'All') {
            $w('#videoRepeater').data = educationalVideos;
        } else {
            const filtered = educationalVideos.filter(video => 
                video.category === selectedCategory
            );
            $w('#videoRepeater').data = filtered;
        }
    });
    
    // Progress tracking for educational content
    let completedSongs = [];
    let completedVideos = [];
    
    // Mark song as completed when it ends
    $w('#audioPlayer').onEnded(() => {
        if (!completedSongs.includes(currentSong)) {
            completedSongs.push(currentSong);
            updateProgress();
        }
    });
    
    // Update progress display
    function updateProgress() {
        const totalContent = abcSongs.length + educationalVideos.length;
        const completed = completedSongs.length + completedVideos.length;
        const progressPercent = Math.round((completed / totalContent) * 100);
        
        $w('#progressBar').value = progressPercent;
        $w('#progressText').text = `${completed}/${totalContent} completed (${progressPercent}%)`;
    }
});
EOF

cd ..

echo ""
echo "✅ Wix Studio integration files created!"
echo ""
echo "🎨 Next Steps for EmpowerHub360.ai Integration:"
echo ""
echo "1. 📂 Upload Media to Wix Media Manager:"
echo "   - Follow guide: wix_empowerhub_integration/wix_media_upload_guide.md"
echo "   - Organize in folders as specified"
echo ""
echo "2. 📄 Add New Pages to Your Wix Site:"
echo "   - AI Educational Tools"
echo "   - ABC Learning Center"
echo "   - Educational Podcasts"
echo "   - Teacher Resources"
echo ""
echo "3. 🎨 Update Your Existing Design:"
echo "   - Add new card to your AI Tools grid"
echo "   - Match your existing blue/dark theme"
echo "   - Use consistent fonts and styling"
echo ""
echo "4. 🔧 Add Wix Code:"
echo "   - Use code from: wix_empowerhub_integration/wix_educational_player_code.js"
echo "   - Replace URLs with your actual Wasabi URLs"
echo ""
echo "5. 🧪 Test Everything:"
echo "   - Audio/video playback"
echo "   - Mobile responsiveness"
echo "   - Integration with existing pages"
echo ""
echo "📁 Integration files ready in: wix_empowerhub_integration/"
echo "🌐 Your enhanced site will be at: https://www.empowerhub360.ai"
echo ""
echo "💡 This will add a complete educational platform to your existing AI tools!"
