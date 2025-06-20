# AI Video Generator - Complete Documentation

## 🎬 Overview

The AI Video Generator is a sophisticated Python-based system that transforms text stories into engaging animated videos using advanced Natural Language Processing (NLP) and computer vision techniques. The system automatically extracts characters, analyzes emotions, and generates custom videos with animated avatars and scene-appropriate backgrounds.

## 📋 Table of Contents

1. [System Architecture](#system-architecture)
2. [Core Features](#core-features)
3. [Installation & Setup](#installation--setup)
4. [Usage Guide](#usage-guide)
5. [API Reference](#api-reference)
6. [Video Generation Pipeline](#video-generation-pipeline)
7. [NLP Processing](#nlp-processing)
8. [Web Interface](#web-interface)
9. [Configuration Options](#configuration-options)
10. [Troubleshooting](#troubleshooting)
11. [Performance Optimization](#performance-optimization)
12. [Extension & Customization](#extension--customization)

## 🏗️ System Architecture

```
AI Video Generator
├── 📖 NLP Pipeline (main.py)
│   ├── spaCy Text Processing
│   ├── Coreferee Resolution
│   ├── Character Extraction
│   └── Emotion Detection
├── 🎨 Video Generation (enhanced_video_generator.py)
│   ├── Character Avatar Creation
│   ├── Scene Background Generation
│   ├── Animation & Lip-sync
│   └── Video Export (MP4)
├── 🌐 Web Interface (streamlit_app.py)
│   ├── User Input Forms
│   ├── Real-time Preview
│   ├── Download Management
│   └── Settings Configuration
└── 🔧 Core Engine (engine/core/)
    ├── Video Processing
    ├── Neural Networks
    └── Render Pipeline
```

## ⭐ Core Features

### 📖 Natural Language Processing
- **Text Analysis**: Advanced parsing using spaCy
- **Character Extraction**: Automatic detection of story characters
- **Coreference Resolution**: Links pronouns to characters using coreferee
- **Emotion Detection**: Scene-by-scene emotion analysis
- **PDF Support**: Extract text from uploaded PDF files

### 🎨 Video Generation
- **Procedural Avatars**: Unique character generation based on attributes
- **Dynamic Backgrounds**: Scene-appropriate environments
- **Animation System**: Lip-sync and character movement
- **Multiple Styles**: Cartoon, Realistic, and Minimalist options
- **High Quality Output**: MP4 export with customizable settings

### 🌐 Web Interface
- **Interactive UI**: Streamlit-based web application
- **Real-time Processing**: Live video generation and preview
- **File Management**: Upload, download, and preview capabilities
- **Advanced Settings**: Full control over video parameters

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- 2GB+ RAM
- 1GB+ storage space

### Quick Installation
```bash
# Clone the repository
git clone <repository-url>
cd AI-Video-Generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### Dependencies
```
spacy>=3.8.0
transformers>=4.52.0
streamlit>=1.46.0
pillow>=11.0.0
imageio>=2.37.0
numpy>=1.24.0
coreferee>=1.4.0
torch>=2.0.0
```

## 📖 Usage Guide

### 1. Web Interface (Recommended)
```bash
streamlit run streamlit_app.py --server.port 8503
```
Then open http://localhost:8503 in your browser.

### 2. Command Line Interface
```python
from main import process_video_generation
from engine.core.video_engine import VideoConfig

config = VideoConfig(width=640, height=480, fps=24, duration=5)
video_path, title, tags = await process_video_generation(
    script="Your story here...",
    config=config
)
```

### 3. Enhanced Video Generation
```python
from enhanced_video_generator import AdvancedVideoGenerator

generator = AdvancedVideoGenerator()
generator.generate_story_video(
    script="Alice met Bob in the forest...",
    characters=[{'name': 'Alice', 'gender': 'female'}],
    scenes=[{'description': 'Forest scene', 'emotion': 'joy'}],
    output_path="output.mp4",
    width=640, height=480, fps=24, duration=5
)
```

## 🔧 API Reference

### Main Processing Functions

#### `parse_characters_and_scenes(text)`
Extracts characters and scenes from text input.

**Parameters:**
- `text` (str): Input story text

**Returns:**
- `characters` (list): List of character dictionaries
- `scenes` (list): List of scene dictionaries

**Example:**
```python
characters, scenes = parse_characters_and_scenes("Alice met Bob...")
# characters: [{'name': 'Alice', 'gender': 'female'}, ...]
# scenes: [{'description': '...', 'emotion': 'joy'}, ...]
```

#### `detect_emotion(text)`
Analyzes emotion in text using transformer models.

**Parameters:**
- `text` (str): Text to analyze

**Returns:**
- `emotion` (str): Detected emotion (joy, sadness, anger, fear, surprise, neutral)

#### `AdvancedVideoGenerator.generate_story_video()`
Generates enhanced video with characters and scenes.

**Parameters:**
- `script` (str): Story text
- `characters` (list): Character data
- `scenes` (list): Scene data
- `output_path` (str): Output file path
- `width` (int): Video width
- `height` (int): Video height
- `fps` (int): Frames per second
- `duration` (int): Video duration in seconds
- `style_settings` (dict): Visual style options

## 🎬 Video Generation Pipeline

### 1. Text Processing
```
Input Text → spaCy Analysis → Character Extraction → Scene Segmentation → Emotion Analysis
```

### 2. Character Generation
```
Character Data → Attribute Selection → Avatar Creation → Animation Setup
```

### 3. Scene Creation
```
Scene Description → Background Generation → Lighting Setup → Composition
```

### 4. Video Assembly
```
Frames Generation → Animation Application → Scene Transitions → MP4 Export
```

### Visual Styles

#### Cartoon Style
- Bright, vibrant colors
- Simplified character features
- Animated expressions
- Playful backgrounds

#### Realistic Style
- Natural color palettes
- Detailed character features
- Subtle animations
- Photorealistic backgrounds

#### Minimalist Style
- Clean, simple designs
- Limited color palette
- Geometric shapes
- Abstract backgrounds

## 🧠 NLP Processing

### Character Extraction Process
1. **Named Entity Recognition**: Identifies person names using spaCy
2. **Coreference Resolution**: Links pronouns to characters using coreferee
3. **Gender Detection**: Analyzes context and pronouns for gender assignment
4. **Character Validation**: Removes duplicates and validates character data

### Emotion Detection Pipeline
1. **Text Preprocessing**: Tokenization and cleaning
2. **Transformer Analysis**: Uses pre-trained emotion models
3. **Context Awareness**: Considers surrounding text for accuracy
4. **Emotion Mapping**: Maps to standard emotion categories

### Scene Segmentation
1. **Sentence Boundary Detection**: Identifies scene boundaries
2. **Semantic Grouping**: Groups related sentences
3. **Character Tracking**: Maintains character presence across scenes
4. **Emotion Assignment**: Assigns dominant emotion to each scene

## 🌐 Web Interface

### Main Features
- **Story Input**: Text area for story input with syntax highlighting
- **File Upload**: PDF and image file support
- **Video Settings**: Resolution, FPS, duration controls
- **Style Selection**: Visual style and animation speed options
- **Real-time Preview**: Instant video preview and playback
- **Download Management**: Direct download with proper file naming

### User Interface Components

#### Sidebar Settings
```python
# Video Quality
width = st.selectbox("Width", [640, 1280, 1920])
height = st.selectbox("Height", [480, 720, 1080])
fps = st.slider("FPS", 24, 60, 30)
duration = st.slider("Duration", 3, 30, 5)

# Visual Style
character_style = st.selectbox("Character Style", 
    ["Cartoon", "Realistic", "Minimalist"])
background_style = st.selectbox("Background Style", 
    ["Gradient", "Scene-based", "Solid Color"])
```

#### Main Interface
```python
# Story Input
script = st.text_area("📝 Script or Story:", height=150)

# File Uploads
pdf_file = st.file_uploader("📚 Upload Story PDF:", type=["pdf"])
image_path = st.text_input("🖼️ Image Path (optional):")

# Generation Controls
submit = st.form_submit_button("🎥 Generate Video")
```

## ⚙️ Configuration Options

### Video Configuration
```python
class VideoConfig:
    width: int = 640          # Video width in pixels
    height: int = 480         # Video height in pixels
    fps: int = 24            # Frames per second
    duration: int = 5        # Duration in seconds
    quality: int = 8         # Compression quality (1-10)
```

### Style Settings
```python
style_settings = {
    'character_style': 'Cartoon',     # Cartoon, Realistic, Minimalist
    'background_style': 'Scene-based', # Gradient, Scene-based, Solid
    'animation_speed': 1.0,           # 0.5-2.0 multiplier
    'color_palette': 'vibrant',       # vibrant, muted, monochrome
    'lighting': 'natural'             # natural, dramatic, soft
}
```

### Advanced Options
```python
advanced_config = {
    'lip_sync_enabled': True,
    'scene_transitions': True,
    'background_animation': False,
    'character_shadows': True,
    'emotion_visualization': True
}
```

## 🐛 Troubleshooting

### Common Issues

#### 1. spaCy Model Not Found
```bash
# Error: Can't find model 'en_core_web_sm'
# Solution:
python -m spacy download en_core_web_sm
```

#### 2. Coreferee Import Errors
```python
# The system has multiple fallback strategies
# Check console output for which strategy is being used
```

#### 3. Video Generation Fails
```python
# Check available memory
# Reduce video resolution or duration
# Verify output directory permissions
```

#### 4. Streamlit Port Issues
```bash
# Use different port
streamlit run streamlit_app.py --server.port 8504
```

### Performance Issues

#### Memory Usage
- **High Memory**: Reduce video resolution or duration
- **Memory Leaks**: Restart the application periodically
- **GPU Issues**: Set device to CPU in main.py

#### Generation Speed
- **Slow Processing**: Use smaller models or reduced quality
- **Network Issues**: Ensure stable internet for model downloads
- **CPU Intensive**: Close other applications during processing

## 🚀 Performance Optimization

### Memory Optimization
```python
# Use smaller video dimensions for testing
config = VideoConfig(width=320, height=240, duration=3)

# Enable garbage collection
import gc
gc.collect()
```

### Processing Speed
```python
# Use CPU-optimized settings
device = "cpu"  # Force CPU usage

# Reduce frame count
fps = 15  # Lower frame rate for faster processing
```

### Quality vs Speed Trade-offs
- **Fast Generation**: 320x240, 15fps, 3 seconds
- **Balanced**: 640x480, 24fps, 5 seconds  
- **High Quality**: 1280x720, 30fps, 10 seconds

## 🛠️ Extension & Customization

### Adding New Character Styles
```python
class AdvancedVideoGenerator:
    def generate_character_avatar(self, character_info, style="custom"):
        if style == "custom":
            # Implement your custom character generation
            pass
```

### Custom Backgrounds
```python
def create_custom_background(self, scene_info, width, height):
    """Create custom scene backgrounds."""
    # Implement your background generation logic
    pass
```

### Additional Emotions
```python
emotion_colors = {
    'excitement': (255, 215, 0),    # Gold
    'confusion': (128, 128, 128),   # Gray
    'determination': (220, 20, 60)  # Crimson
}
```

### New Animation Types
```python
def animate_character_movement(self, character, frame_idx):
    """Add walking, gesturing, or other movements."""
    # Implement character animation logic
    pass
```

## 📊 Technical Specifications

### System Requirements
- **Minimum**: 2GB RAM, 1GB storage, Python 3.8
- **Recommended**: 4GB RAM, 2GB storage, Python 3.10+
- **Optimal**: 8GB RAM, 5GB storage, GPU support

### File Formats
- **Input**: TXT, PDF, DOCX (stories), JPG, PNG (images)
- **Output**: MP4 (H.264), WebM (optional), GIF (optional)

### Processing Limits
- **Text Length**: Up to 10,000 characters
- **Video Duration**: 1-30 seconds (configurable)
- **Characters**: Up to 10 per story
- **Scenes**: Up to 50 per story

## 🔮 Future Enhancements

### Planned Features
- [ ] Real-time audio synchronization
- [ ] Advanced facial expressions
- [ ] Background music integration
- [ ] Multi-language support
- [ ] Cloud deployment options
- [ ] API endpoints for integration
- [ ] Batch processing capabilities
- [ ] Template-based generation

### Technical Improvements
- [ ] GPU acceleration for video generation
- [ ] WebRTC for real-time streaming
- [ ] Advanced caching mechanisms
- [ ] Distributed processing support
- [ ] Machine learning model fine-tuning

## 📝 License & Credits

This project uses various open-source libraries and models:
- **spaCy**: Industrial-strength NLP
- **Transformers**: State-of-the-art ML models
- **Streamlit**: Web app framework
- **PIL/Pillow**: Image processing
- **imageio**: Video I/O operations

## 🤝 Contributing

See CONTRIBUTING.md for guidelines on:
- Code style and standards
- Testing requirements
- Documentation updates
- Feature proposals
- Bug reporting

---

For more information, see the individual component documentation files:
- [NLP_GUIDE.md](NLP_GUIDE.md) - Detailed NLP processing
- [VIDEO_GUIDE.md](VIDEO_GUIDE.md) - Video generation specifics
- [API_REFERENCE.md](API_REFERENCE.md) - Complete API documentation
- [EXAMPLES.md](EXAMPLES.md) - Usage examples and tutorials
