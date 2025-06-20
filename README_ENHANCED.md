# 🎬 AI Video Generator v2.0 - Enhanced with Audio & Animation

Transform your stories into engaging videos with AI-powered character detection, emotion analysis, advanced audio integration, and sophisticated character animations!

## ✨ New Features in v2.0

### 🎵 Advanced Audio Integration
- **Text-to-Speech (TTS)**: Multiple engines (pyttsx3, gTTS) with voice customization
- **Background Music**: Procedural music generation based on emotions
- **Audio Mixing**: Seamless integration of voice and music
- **Character Voices**: Unique voice profiles for different characters
- **Emotion-Based Audio**: Dynamic music and voice modulation

### 🎭 Advanced Character Animations
- **Facial Expressions**: Emotion-based facial animation templates
- **Gesture Patterns**: Wave, point, nod, and custom gesture animations
- **Walk Cycles**: Realistic character movement animations
- **Particle Effects**: Sparkles, magic effects, and environmental particles
- **Lip-Sync**: Improved mouth movement synchronization with audio

### 🎬 Enhanced Video Generation
- **Multi-Character Support**: Generate videos with multiple unique characters
- **Scene Transitions**: Smooth transitions between different scenes
- **Dynamic Backgrounds**: Scene-appropriate background generation
- **Audio-Visual Sync**: Synchronized audio and visual elements
- **Style Customization**: Multiple animation and visual styles

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Virtual environment (recommended)
- Git

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/AI-Video-Generator.git
   cd AI-Video-Generator
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

4. **Install system audio dependencies** (Linux/Ubuntu):
   ```bash
   sudo apt-get update
   sudo apt-get install espeak espeak-data libespeak1 libespeak-dev
   sudo apt-get install ffmpeg
   ```

### Run the Application

#### Web Interface (Recommended)
```bash
streamlit run streamlit_app.py
```
Access the web interface at `http://localhost:8501`

#### Command Line
```bash
python main.py --script "Your story here..." --output video.mp4
```

#### Docker (Production)
```bash
docker-compose up
```
Access at `http://localhost:8503`

## 🎛️ Usage Guide

### Web Interface Features

1. **📝 Story Input**: Enter your story script or upload a PDF
2. **⚙️ Video Settings**: Configure resolution, FPS, and duration
3. **🎵 Audio Controls**: 
   - Enable/disable audio generation
   - Choose voice type and settings
   - Select background music style
   - Adjust audio levels
4. **🎭 Animation Settings**:
   - Enable advanced animations
   - Choose animation style
   - Configure particle effects
   - Set character behavior

### Audio Features

#### Voice Synthesis
- **Multiple Engines**: Offline (pyttsx3) and online (gTTS) options
- **Voice Customization**: Rate, volume, pitch, and voice type
- **Character Voices**: Unique voice profiles for each character

#### Background Music
- **Emotion-Based**: Music adapts to story emotion (joy, sadness, excitement)
- **Multiple Styles**: Orchestral, electronic, piano, ambient
- **Dynamic Generation**: Procedural music creation

### Animation Features

#### Character Animation
- **Facial Expressions**: 15+ emotion-based expressions
- **Gestures**: Wave, point, nod, celebrate, think
- **Movement**: Walk cycles, idle animations, scene transitions

#### Visual Effects
- **Particle Systems**: Sparkles, magic effects, environmental particles
- **Scene Enhancement**: Dynamic backgrounds, lighting effects
- **Style Options**: Cartoon, realistic, minimalist

## 📁 Project Structure

```
AI-Video-Generator/
├── 🎬 Core Engine
│   ├── engine/core/               # Core video processing
│   ├── enhanced_video_generator.py # Main enhanced generator
│   └── main.py                    # CLI interface
├── 🎵 Audio System
│   └── audio_integration.py       # Advanced audio engine
├── 🎭 Animation System
│   └── advanced_animation.py      # Animation processing
├── 🌐 Web Interface
│   ├── streamlit_app.py          # Streamlit web app
│   └── app.py                    # Alternative web interface
├── 🐳 Deployment
│   ├── Dockerfile                # Container configuration
│   ├── docker-compose.yml        # Multi-service setup
│   └── requirements.txt          # Python dependencies
├── 📚 Documentation
│   ├── DOCUMENTATION.md           # Detailed technical docs
│   ├── USER_GUIDE.md             # User manual
│   ├── API_REFERENCE.md          # API documentation
│   └── use_cases/                # Example use cases
└── 🧪 Testing
    ├── tests/                     # Unit tests
    └── test_integrated_system.py  # Integration tests
```

## 🔧 Configuration

### Audio Settings
```python
audio_settings = {
    'enable_audio': True,
    'enable_background_music': True,
    'music_style': 'orchestral',  # orchestral, electronic, piano, ambient
    'voice_settings': {
        'rate': 150,      # Speech rate (words per minute)
        'volume': 0.9,    # Voice volume (0.0-1.0)
        'voice_id': 0,    # Voice type selection
        'pitch': 1.0      # Voice pitch multiplier
    }
}
```

### Animation Settings
```python
animation_settings = {
    'enable_advanced_animation': True,
    'animation_style': 'cartoon',     # cartoon, realistic, minimalist
    'enable_particle_effects': True,
    'animation_speed': 1.0           # Speed multiplier
}
```

## 🎯 Use Cases

- **📚 Educational Content**: Create engaging educational videos
- **📱 Social Media**: Generate content for TikTok, Instagram, YouTube
- **📈 Marketing**: Product demos and promotional videos
- **📖 Storytelling**: Bring written stories to life
- **🎓 Training**: Corporate training and tutorial videos

## 🛠️ API Reference

### AdvancedVideoGenerator Class
```python
from enhanced_video_generator import AdvancedVideoGenerator

generator = AdvancedVideoGenerator()

# Generate video with audio and animation
video_path = generator.generate_story_video(
    script="Your story...",
    characters=[{'name': 'Alice', 'gender': 'female'}],
    scenes=[{'description': 'Scene 1', 'emotion': 'joy'}],
    output_path="output.mp4",
    audio_settings=audio_settings,
    animation_settings=animation_settings
)
```

### Audio Engine
```python
from audio_integration import AdvancedAudioEngine

audio_engine = AdvancedAudioEngine()

# Generate character voice
voice_path = audio_engine.text_to_speech(
    text="Hello, I'm Alice!",
    voice_settings={'rate': 150, 'volume': 0.9}
)

# Generate background music
music_path = audio_engine.generate_background_music(
    emotion='joy',
    duration=30,
    style='orchestral'
)
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
# Run integration tests
python test_integrated_system.py

# Run specific component tests
python -m pytest tests/
```

## 🐳 Docker Deployment

### Development
```bash
docker build -t ai-video-generator .
docker run -p 8503:8503 ai-video-generator
```

### Production
```bash
docker-compose up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **spaCy**: Natural language processing
- **Transformers**: Emotion detection and NLP
- **Streamlit**: Web interface framework
- **PIL/Pillow**: Image processing
- **NumPy**: Numerical computations
- **librosa**: Audio processing
- **pyttsx3**: Text-to-speech synthesis
- **gTTS**: Google Text-to-Speech
- **imageio**: Video generation

## 📞 Support

- **Documentation**: Check the documentation files in the repository
- **Issues**: Report bugs on GitHub Issues
- **Wiki**: Check the project wiki for detailed guides

---

**🎬 AI Video Generator v2.0** - Bringing stories to life with AI-powered audio and animation!

## 🎥 Demo

Try the web interface to see the AI Video Generator in action:

1. Enter a story like: "Alice walked through the magical forest. She felt curious and excited about the adventure ahead."
2. Configure your audio and animation preferences
3. Click "Generate Video" and watch your story come to life!

### Example Output Features:
- ✅ Automatically detected character "Alice"
- ✅ Generated unique avatar and voice for Alice
- ✅ Created emotion-appropriate background music
- ✅ Applied facial expressions and gestures
- ✅ Synchronized audio with visual elements
- ✅ Added particle effects for magical scenes
