# 🎬 AI Video Generator

> Transform your stories into engaging animated videos using advanced AI technology

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.46+-red.svg)](https://streamlit.io/)
[![spaCy](https://img.shields.io/badge/spaCy-3.8+-green.svg)](https://spacy.io/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## ✨ Features

🧠 **Advanced NLP Processing**
- Character extraction and coreference resolution
- Emotion detection and scene analysis
- Multi-language support with spaCy and Transformers

🎨 **Enhanced Video Generation**
- Procedural character avatar creation
- Scene-appropriate background generation
- Multiple visual styles (Cartoon, Realistic, Minimalist)
- Animated lip-sync and character movement

🌐 **Interactive Web Interface**
- Real-time video generation and preview
- Drag-and-drop file uploads (PDF, text)
- Customizable video settings and styles
- Instant download and sharing capabilities

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/your-username/AI-Video-Generator.git
cd AI-Video-Generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### 2. Launch the Application

```bash
streamlit run streamlit_app.py --server.port 8503
```

Open your browser to: http://localhost:8503

### 3. Create Your First Video

1. **Enter your story** in the text area:
   ```
   Alice walked through the enchanted forest when she met Bob. 
   He was sitting by a crystal stream, looking worried. 
   "What's wrong?" Alice asked with concern.
   ```

2. **Adjust settings** in the sidebar:
   - Resolution: 640x480 to 1920x1080
   - Style: Cartoon, Realistic, or Minimalist
   - Duration: 3-30 seconds

3. **Click "Generate Video"** and watch the magic happen!

4. **Preview and download** your AI-generated MP4 video

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [📋 Complete Documentation](DOCUMENTATION.md) | Comprehensive system overview and guides |
| [🔧 API Reference](API_REFERENCE.md) | Detailed API documentation and examples |
| [👤 User Guide](USER_GUIDE.md) | Step-by-step usage instructions |
| [⚙️ Technical Specifications](TECHNICAL_SPECS.md) | System architecture and requirements |

## 🎯 Use Cases

### 📚 Educational Content
- Convert textbook stories into engaging visual content
- Create animated explanations for complex concepts
- Generate character-driven educational videos

### 🎭 Creative Storytelling
- Bring short stories and poems to life
- Prototype video content for larger productions
- Create social media content from text posts

### 💼 Business Presentations
- Transform case studies into visual narratives
- Create engaging product demonstration videos
- Generate training content from written materials

## 🎨 Example Outputs

### Fairy Tale (Cartoon Style)
**Input:** "The little princess found a magic mirror in the castle tower..."

**Output:** Bright, colorful animation with:
- Cartoon princess character with expressive features
- Magical castle tower background with glowing effects
- Animated mirror with sparkle effects
- Joyful emotions reflected in character expressions

### Adventure Story (Realistic Style)
**Input:** "Captain Sarah navigated through the storm, determined to reach safety..."

**Output:** Dramatic, realistic animation featuring:
- Detailed captain character with weather-appropriate clothing
- Stormy ocean background with dynamic waves
- Determined facial expressions and body language
- Dark, moody color palette matching the scene

### Science Fiction (Minimalist Style)
**Input:** "The astronaut discovered a strange signal from deep space..."

**Output:** Clean, geometric animation with:
- Simplified astronaut figure in space suit
- Abstract space background with geometric patterns
- Minimal color palette focused on blues and whites
- Smooth, flowing animations

## 🔧 Advanced Usage

### Command Line Interface

```python
from enhanced_video_generator import AdvancedVideoGenerator
from main import parse_characters_and_scenes

# Generate video programmatically
generator = AdvancedVideoGenerator()
story = "Your story here..."
characters, scenes = parse_characters_and_scenes(story)

video_path = generator.generate_story_video(
    script=story,
    characters=characters,
    scenes=scenes,
    output_path="my_video.mp4",
    width=1280,
    height=720,
    fps=30,
    duration=10
)
```

### Batch Processing

```python
import asyncio
from main import process_video_generation

stories = ["Story 1...", "Story 2...", "Story 3..."]
videos = []

for i, story in enumerate(stories):
    video_path, title, tags = await process_video_generation(
        script=story,
        headline=f"Story {i+1}",
        config=VideoConfig(width=640, height=480)
    )
    videos.append(video_path)
```

## 🏗️ Architecture

```
AI Video Generator
├── 📖 NLP Pipeline
│   ├── spaCy (text processing)
│   ├── Coreferee (coreference resolution)
│   ├── Transformers (emotion detection)
│   └── PDF extraction
├── 🎨 Video Generation
│   ├── Character avatar creation
│   ├── Scene background rendering
│   ├── Animation engine
│   └── MP4 export
├── 🌐 Web Interface
│   ├── Streamlit UI components
│   ├── File upload handling
│   ├── Real-time preview
│   └── Download management
└── 🔧 Core Engine
    ├── Video processing pipeline
    ├── Memory management
    └── Error handling
```

## 📊 Performance

### Generation Speed
- **320x240**: ~2 seconds per second of video
- **640x480**: ~4 seconds per second of video  
- **1280x720**: ~8 seconds per second of video
- **1920x1080**: ~15 seconds per second of video

### System Requirements
- **Minimum**: 2GB RAM, Python 3.8+
- **Recommended**: 4GB RAM, Python 3.10+
- **Optimal**: 8GB RAM, multi-core CPU

### Output Quality
- **File sizes**: 50-400 KB per second of video
- **Formats**: MP4 (H.264), WebM (optional)
- **Quality levels**: Draft, Standard, High, Maximum

## 🛠️ Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Check code quality
black . --check
flake8 .
mypy .

# Generate documentation
sphinx-build -b html docs docs/_build
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 🐛 Troubleshooting

### Common Issues

**spaCy Model Not Found**
```bash
python -m spacy download en_core_web_sm
```

**Memory Issues**
- Reduce video resolution or duration
- Close other applications
- Restart the browser

**Slow Processing**
- Use CPU-only mode if GPU causes issues
- Try smaller video dimensions for testing
- Check available system memory

**Import Errors**
- Verify all dependencies are installed
- Check Python version compatibility
- Try recreating the virtual environment

For more help, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or open an issue.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **spaCy**: Industrial-strength Natural Language Processing
- **Transformers**: State-of-the-art Machine Learning for PyTorch and TensorFlow
- **Streamlit**: The fastest way to build and share data apps
- **PIL/Pillow**: Python Imaging Library for image processing
- **imageio**: Library for reading and writing various image formats

## 📞 Support

- 📧 **Email**: support@ai-video-generator.com
- 💬 **Discord**: [Join our community](https://discord.gg/ai-video-gen)
- 📖 **Documentation**: [Full documentation](DOCUMENTATION.md)
- 🐛 **Issues**: [GitHub Issues](https://github.com/your-username/AI-Video-Generator/issues)

## 🌟 Star History

If this project helps you, please consider giving it a star! ⭐

---

**Made with ❤️ by the AI Video Generator Team**

*Transform your imagination into reality, one story at a time.*
