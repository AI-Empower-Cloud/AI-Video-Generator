# API Reference - AI Video Generator

## 📚 Complete API Documentation

This document provides detailed API reference for all classes, methods, and functions in the AI Video Generator system.

## 🔧 Core Classes

### `AdvancedVideoGenerator`

Main class for enhanced video generation with character avatars and scene backgrounds.

#### Constructor
```python
generator = AdvancedVideoGenerator()
```

#### Methods

##### `generate_story_video(script, characters, scenes, output_path, **kwargs)`

Generates a complete story video with characters and scenes.

**Parameters:**
- `script` (str): The story text to convert to video
- `characters` (list): List of character dictionaries
- `scenes` (list): List of scene dictionaries  
- `output_path` (str): Path where the MP4 file will be saved
- `width` (int, optional): Video width in pixels. Default: 640
- `height` (int, optional): Video height in pixels. Default: 480
- `fps` (int, optional): Frames per second. Default: 24
- `duration` (int, optional): Video duration in seconds. Default: 5
- `style_settings` (dict, optional): Visual style configuration

**Returns:**
- `str`: Path to the generated video file

**Example:**
```python
from enhanced_video_generator import AdvancedVideoGenerator

generator = AdvancedVideoGenerator()
video_path = generator.generate_story_video(
    script="Alice met Bob in the enchanted forest...",
    characters=[
        {'name': 'Alice', 'gender': 'female'},
        {'name': 'Bob', 'gender': 'male'}
    ],
    scenes=[
        {'description': 'Meeting in forest', 'emotion': 'surprise'},
        {'description': 'Walking together', 'emotion': 'joy'}
    ],
    output_path="story_video.mp4",
    width=1280,
    height=720,
    fps=30,
    duration=8
)
```

##### `generate_character_avatar(character_info, width=400, height=400)`

Creates a unique avatar for a character based on their attributes.

**Parameters:**
- `character_info` (dict): Character data with name, gender, etc.
- `width` (int): Avatar width in pixels
- `height` (int): Avatar height in pixels

**Returns:**
- `PIL.Image`: Generated character avatar

**Character Info Structure:**
```python
character_info = {
    'name': 'Alice',           # Character name
    'gender': 'female',        # male, female, neutral
    'style': 'realistic',      # cartoon, realistic, minimalist
    'age_group': 'adult'       # child, teen, adult, elderly
}
```

##### `create_scene_background(scene_info, width, height)`

Generates appropriate background for a scene based on description and emotion.

**Parameters:**
- `scene_info` (dict): Scene data with description and emotion
- `width` (int): Background width in pixels
- `height` (int): Background height in pixels

**Returns:**
- `PIL.Image`: Generated background image

**Scene Info Structure:**
```python
scene_info = {
    'description': 'Alice walks through enchanted forest',
    'emotion': 'joy',          # joy, sadness, anger, fear, surprise, neutral
    'setting': 'outdoor',      # indoor, outdoor, fantasy
    'time': 'day'             # day, night, sunset, dawn
}
```

## 🧠 NLP Functions

### `parse_characters_and_scenes(text)`

Extracts characters and scenes from story text using advanced NLP.

**Parameters:**
- `text` (str): Input story text

**Returns:**
- `tuple`: (characters_list, scenes_list)

**Example:**
```python
from main import parse_characters_and_scenes

story = "Alice met Bob at the park. She was happy to see him."
characters, scenes = parse_characters_and_scenes(story)

print(characters)
# [{'name': 'Alice', 'gender': 'female'}, {'name': 'Bob', 'gender': 'male'}]

print(scenes)
# [{'description': 'Alice met Bob at the park', 'emotion': 'neutral'}, ...]
```

### `detect_emotion(text)`

Analyzes text to detect the dominant emotion using transformer models.

**Parameters:**
- `text` (str): Text to analyze for emotion

**Returns:**
- `str`: Detected emotion (joy, sadness, anger, fear, surprise, neutral)

**Example:**
```python
from main import detect_emotion

emotion = detect_emotion("I am so excited about this!")
print(emotion)  # "joy"

emotion = detect_emotion("This is terrible news.")
print(emotion)  # "sadness"
```

### `extract_text_from_pdf(pdf_path)`

Extracts text content from PDF files for story processing.

**Parameters:**
- `pdf_path` (str): Path to PDF file

**Returns:**
- `str`: Extracted text content

**Example:**
```python
from main import extract_text_from_pdf

text = extract_text_from_pdf("story.pdf")
characters, scenes = parse_characters_and_scenes(text)
```

## ⚙️ Configuration Classes

### `VideoConfig`

Configuration object for video generation parameters.

**Attributes:**
- `width` (int): Video width in pixels
- `height` (int): Video height in pixels  
- `fps` (int): Frames per second
- `duration` (int): Duration in seconds
- `quality` (int): Compression quality (1-10)

**Example:**
```python
from engine.core.video_engine import VideoConfig

config = VideoConfig(
    width=1920,
    height=1080,
    fps=30,
    duration=10,
    quality=9
)
```

## 🎨 Style Configuration

### Style Settings Dictionary

Controls visual appearance and animation behavior.

```python
style_settings = {
    # Character appearance
    'character_style': 'cartoon',      # cartoon, realistic, minimalist
    'skin_tone_variety': True,         # Use diverse skin tones
    'facial_expressions': True,        # Enable expression changes
    
    # Background settings  
    'background_style': 'scene-based', # gradient, scene-based, solid
    'background_animation': False,     # Animate background elements
    'lighting_effects': True,          # Add lighting and shadows
    
    # Animation settings
    'animation_speed': 1.0,            # Speed multiplier (0.5-2.0)
    'lip_sync_enabled': True,          # Enable mouth movement
    'character_movement': True,        # Enable character animation
    
    # Color settings
    'color_palette': 'vibrant',        # vibrant, muted, monochrome
    'emotion_colors': True,            # Use emotion-based colors
    
    # Quality settings
    'anti_aliasing': True,             # Smooth edges
    'high_detail': False               # Extra detail (slower)
}
```

## 🚀 Async Functions

### `process_video_generation(script, headline, **kwargs)`

Main async function for complete video generation pipeline.

**Parameters:**
- `script` (str): Story text
- `headline` (str, optional): Video title
- `image_path` (str, optional): Reference image path
- `youtube_link` (str, optional): YouTube URL for context
- `pdf_path` (str, optional): PDF file path
- `config` (VideoConfig): Video configuration

**Returns:**
- `tuple`: (video_path, title, tags)

**Example:**
```python
import asyncio
from main import process_video_generation
from engine.core.video_engine import VideoConfig

async def generate_video():
    config = VideoConfig(width=640, height=480, fps=24, duration=5)
    
    video_path, title, tags = await process_video_generation(
        script="Your story here...",
        headline="Amazing Story",
        config=config
    )
    
    return video_path, title, tags

# Run the async function
video_path, title, tags = asyncio.run(generate_video())
```

### `upload_to_youtube(video_path, title, description, tags)`

Uploads generated video to YouTube (requires API credentials).

**Parameters:**
- `video_path` (str): Path to video file
- `title` (str): Video title
- `description` (str): Video description
- `tags` (list): List of tags

**Returns:**
- `str`: YouTube video URL if successful, None if failed

**Setup Requirements:**
1. Create `client_secrets.json` with YouTube API credentials
2. Enable YouTube Data API v3
3. Configure OAuth 2.0 credentials

## 🔨 Utility Functions

### Video Processing

```python
# Convert PIL images to video frames
def images_to_video(images, output_path, fps=24):
    """Convert list of PIL images to MP4 video."""
    frames = [np.array(img) for img in images]
    imageio.mimsave(output_path, frames, fps=fps, quality=8)

# Resize video maintaining aspect ratio
def resize_video(input_path, output_path, width, height):
    """Resize video to new dimensions."""
    # Implementation using imageio
    pass
```

### Character Processing

```python
# Gender detection from text context
def detect_gender(character_name, text_context):
    """Detect character gender from pronouns and context."""
    # Returns: 'male', 'female', 'neutral'
    pass

# Character relationship analysis
def analyze_relationships(characters, text):
    """Analyze relationships between characters."""
    # Returns: dict of character relationships
    pass
```

### Scene Analysis

```python
# Scene boundary detection
def segment_scenes(text):
    """Split text into logical scene segments."""
    # Returns: list of scene segments
    pass

# Setting detection (indoor/outdoor/fantasy)
def detect_setting(scene_description):
    """Detect scene setting from description."""
    # Returns: 'indoor', 'outdoor', 'fantasy', 'abstract'
    pass
```

## 🛠️ Error Handling

### Custom Exceptions

```python
class VideoGenerationError(Exception):
    """Raised when video generation fails."""
    pass

class CharacterExtractionError(Exception):
    """Raised when character extraction fails."""
    pass

class SceneAnalysisError(Exception):
    """Raised when scene analysis fails."""
    pass
```

### Error Handling Patterns

```python
try:
    video_path = generator.generate_story_video(
        script=script,
        characters=characters,
        scenes=scenes,
        output_path="output.mp4"
    )
except VideoGenerationError as e:
    print(f"Video generation failed: {e}")
    # Fallback to simple video generation
except Exception as e:
    print(f"Unexpected error: {e}")
    # Log error and show user-friendly message
```

## 📊 Performance Monitoring

### Timing Functions

```python
import time
from functools import wraps

def timing_decorator(func):
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return wrapper

# Usage
@timing_decorator
def generate_character_avatar(character_info):
    # Character generation code
    pass
```

### Memory Monitoring

```python
import psutil
import gc

def monitor_memory():
    """Monitor current memory usage."""
    process = psutil.Process()
    memory_mb = process.memory_info().rss / 1024 / 1024
    print(f"Memory usage: {memory_mb:.1f} MB")

def cleanup_memory():
    """Force garbage collection to free memory."""
    gc.collect()
    monitor_memory()
```

## 🔧 Advanced Configuration

### Model Configuration

```python
# NLP model settings
nlp_config = {
    'spacy_model': 'en_core_web_sm',    # or en_core_web_lg for better accuracy
    'use_coreferee': True,              # Enable coreference resolution
    'emotion_model': 'j-hartmann/emotion-english-distilroberta-base',
    'device': 'cpu',                    # or 'cuda' for GPU acceleration
    'batch_size': 32                    # For batch processing
}

# Video generation settings
video_config = {
    'default_width': 640,
    'default_height': 480,
    'default_fps': 24,
    'default_duration': 5,
    'max_characters': 10,
    'max_scenes': 50,
    'compression_quality': 8
}
```

### Logging Configuration

```python
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('video_generator.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('VideoGenerator')

# Usage in functions
def generate_video():
    logger.info("Starting video generation")
    try:
        # Video generation code
        logger.info("Video generation completed successfully")
    except Exception as e:
        logger.error(f"Video generation failed: {e}")
```

## 📝 Testing

### Unit Test Examples

```python
import unittest
from main import detect_emotion, parse_characters_and_scenes

class TestNLPFunctions(unittest.TestCase):
    
    def test_emotion_detection(self):
        """Test emotion detection accuracy."""
        test_cases = [
            ("I am so happy!", "joy"),
            ("This is terrible.", "sadness"),
            ("What a surprise!", "surprise")
        ]
        
        for text, expected_emotion in test_cases:
            detected_emotion = detect_emotion(text)
            self.assertEqual(detected_emotion, expected_emotion)
    
    def test_character_extraction(self):
        """Test character extraction from text."""
        text = "Alice met Bob at the park. She smiled at him."
        characters, scenes = parse_characters_and_scenes(text)
        
        character_names = [char['name'] for char in characters]
        self.assertIn('Alice', character_names)
        self.assertIn('Bob', character_names)

if __name__ == '__main__':
    unittest.main()
```

### Integration Tests

```python
def test_full_video_generation():
    """Test complete video generation pipeline."""
    from enhanced_video_generator import AdvancedVideoGenerator
    
    generator = AdvancedVideoGenerator()
    
    # Test data
    script = "Alice walked through the forest and met a friendly dragon."
    characters = [{'name': 'Alice', 'gender': 'female'}]
    scenes = [{'description': 'Forest meeting', 'emotion': 'surprise'}]
    
    # Generate video
    output_path = "test_video.mp4"
    result_path = generator.generate_story_video(
        script=script,
        characters=characters,
        scenes=scenes,
        output_path=output_path,
        width=320,
        height=240,
        duration=2
    )
    
    # Verify output
    assert os.path.exists(result_path)
    assert os.path.getsize(result_path) > 0
    
    print("✅ Full video generation test passed")
```

---

For more examples and tutorials, see:
- [EXAMPLES.md](EXAMPLES.md) - Practical usage examples
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development guidelines
