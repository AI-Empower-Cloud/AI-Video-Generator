# 🎓 Educational Video Generator

Create 10-40 minute educational videos with automatic YouTube upload, specifically designed for teaching slokas, mantras, and educational content.

## ✨ Features

### 🕉️ **Sanskrit & Spiritual Content**
- **Gayatri Mantra** complete teaching videos
- **Custom Slokas** with pronunciation guides
- **Mantras** with meditation guidance
- **Sanskrit syllable breakdown** for proper pronunciation
- **Spiritual benefits** explanation

### 📚 **Educational Content**
- **Long-form lectures** (10-40 minutes)
- **Interactive teaching** with examples
- **Multi-segment structure** (intro, explanation, practice, conclusion)
- **Custom topics** and course content

### 🎬 **Advanced Video Features**
- **High-quality output** (720p to 4K)
- **Professional audio** with clear pronunciation
- **Background music** (spiritual/classical/ambient)
- **Text overlays** with Sanskrit/Devanagari support
- **Animated characters** and visual effects

### 📤 **YouTube Integration**
- **Automatic upload** to YouTube
- **Custom thumbnails** generation
- **SEO-optimized titles** and descriptions
- **Proper tagging** for discoverability
- **Educational category** optimization

## 🚀 Quick Start

### 1. **Web Interface (Recommended)**
```bash
# Launch the educational video creator
./run_educational.sh

# Or directly:
streamlit run educational_app.py --server.port 8504
```

### 2. **Command Line**
```bash
# Create Gayatri Mantra video
python3 educational_video_generator.py

# Batch create series
python3 batch_educational_creator.py --series sanskrit
```

### 3. **Custom Script**
```python
from educational_video_generator import EducationalVideoGenerator

generator = EducationalVideoGenerator()

# Create custom sloka video
content_data = {
    'text': 'ॐ गं गणपतये नमः',
    'meaning': 'Salutations to Lord Ganesha, remover of obstacles',
    'benefits': 'Removes obstacles, brings success and wisdom',
    'title': 'Ganesh Mantra Teaching'
}

video_path, metadata = generator.generate_educational_video(
    'mantra_teaching', content_data, {'duration': 900}
)
```

## 📋 Content Types Supported

### 🕉️ **Mantras & Slokas**
- **Gayatri Mantra** - The most sacred Vedic mantra
- **Maha Mantra** - Hare Krishna chanting
- **Ganesh Mantra** - Obstacle removal
- **Shanti Mantra** - Universal peace
- **Custom Slokas** - Any Sanskrit verse

### 📚 **Educational Topics**
- **Sanskrit Language** basics and grammar
- **Vedic Mathematics** calculations and techniques
- **Yoga Philosophy** and practice
- **Hindu Scriptures** explanations
- **Meditation Techniques** and guidance
- **Custom Educational Content**

## ⚙️ Configuration

### 📺 **YouTube API Setup**
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create project and enable YouTube Data API v3
3. Create OAuth 2.0 credentials
4. Download `client_secrets.json` to project root
5. Run first upload to authenticate

### 🎬 **Video Settings**
```json
{
  "duration": 1200,    // 20 minutes
  "width": 1920,       // 1080p HD
  "height": 1080,
  "fps": 30,
  "voice_speed": 120,  // Slower for teaching
  "music_style": "spiritual"
}
```

### 🎵 **Audio Options**
- **Voice Speed**: 80-150 WPM (slower for learning)
- **Music Styles**: Spiritual, Classical, Ambient, Meditation
- **Multiple Voices**: Male, Female, Neutral
- **Clear Pronunciation** optimized for Sanskrit

## 📖 **Video Structure**

### 🕉️ **Sloka/Mantra Teaching** (15-25 minutes)
1. **Introduction** (2 min) - Welcome and context
2. **Pronunciation** (5-8 min) - Syllable-by-syllable breakdown
3. **Meaning** (3-5 min) - Word-by-word translation
4. **Repetition** (5-10 min) - Guided chanting practice
5. **Conclusion** (2 min) - Benefits and closing

### 📚 **Educational Lecture** (20-40 minutes)
1. **Introduction** (3-5 min) - Topic overview
2. **Concept Explanation** (10-15 min) - Core teaching
3. **Examples** (5-10 min) - Practical applications
4. **Practice** (5-10 min) - Interactive exercises
5. **Summary** (2-3 min) - Key takeaways

## 🎯 **Use Cases**

### 👨‍🏫 **For Teachers**
- Create **course content** for online platforms
- **Sanskrit pronunciation** guides for students
- **Spiritual teachings** for communities
- **Educational series** for YouTube channels

### 🙏 **For Spiritual Practitioners**
- **Daily mantra practice** videos
- **Meditation guidance** with mantras
- **Devotional content** for sharing
- **Learning Sanskrit** slokas properly

### 📚 **For Educators**
- **Hindu philosophy** courses
- **Sanskrit language** tutorials
- **Vedic mathematics** lessons
- **Cultural education** content

## 📊 **Batch Processing**

### Create Multiple Videos Automatically
```bash
# Create Sanskrit learning series (4-5 videos)
python3 batch_educational_creator.py --series sanskrit

# Create educational content series  
python3 batch_educational_creator.py --series educational

# Create both series
python3 batch_educational_creator.py --series both

# Auto-upload to YouTube
python3 batch_educational_creator.py --series sanskrit --upload
```

### **Predefined Series Available**
- **Sanskrit Learning Series** (Gayatri, Maha Mantra, Shanti, Ganesh)
- **Educational Content Series** (Sanskrit basics, Vedic Math, Yoga)
- **Custom Series** from JSON configuration

## 🌐 **YouTube Optimization**

### 📝 **Auto-Generated Content**
- **SEO-optimized titles** with keywords
- **Detailed descriptions** with chapters and benefits
- **Proper tags** for Sanskrit, Education, Spirituality
- **Educational category** for better reach
- **Custom thumbnails** with Sanskrit text

### 📊 **Example Generated Metadata**
```
Title: "Learn Sanskrit Sloka: Gayatri Mantra | Pronunciation, Meaning & Benefits"

Description: 
🕉️ Welcome to our Sanskrit Learning Series!
✨ Correct pronunciation guide
📚 Deep meaning and significance  
🙏 Spiritual benefits explanation
🎵 Proper chanting technique

Tags: Sanskrit, Mantra, Education, Spirituality, Gayatri, Meditation
```

## 🔧 **Advanced Features**

### 🎨 **Visual Enhancements**
- **Sanskrit text overlays** in Devanagari script
- **Pronunciation guides** with syllable highlighting
- **Spiritual backgrounds** (temples, nature, meditation)
- **Character animations** for teaching
- **Particle effects** for spiritual ambiance

### 🎵 **Audio Enhancements**
- **Multiple voice engines** (pyttsx3, gTTS)
- **Background music generation** based on emotion
- **Audio mixing** and synchronization
- **Clear pronunciation** optimized for Sanskrit phonetics

### 📱 **Multi-Platform Ready**
- **Multiple resolutions** (720p, 1080p, 4K)
- **Various aspect ratios** (16:9, 4:3, 1:1)
- **Mobile-optimized** layouts
- **Subtitle generation** (.srt files)

## 📈 **Example Output**

### 🕉️ **Gayatri Mantra Video** (20 minutes)
1. **Introduction** - History and significance
2. **Pronunciation** - "Om Bhur Bhuva Swaha..."
3. **Meaning** - "We meditate upon divine light..."
4. **Benefits** - Spiritual awakening, peace, wisdom
5. **Practice** - Guided chanting with repetition
6. **Conclusion** - Daily practice recommendations

**Result**: Professional 1080p video with clear audio, Sanskrit text overlay, spiritual background music, and automatic YouTube upload.

## 🎯 **Next Steps**

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Setup YouTube API**: Follow configuration guide
3. **Create first video**: `./run_educational.sh`
4. **Share your teachings**: Auto-upload to YouTube
5. **Build your channel**: Create series and playlists

## 📞 **Support**

- 📚 **Full Documentation**: `web-service-setup.md`
- 🎬 **Video Examples**: Check generated videos
- 🔧 **Configuration**: `educational_config.json`
- 🐛 **Issues**: GitHub Issues

---

**Transform your spiritual and educational knowledge into professional videos with automatic YouTube distribution!** 🎓✨
