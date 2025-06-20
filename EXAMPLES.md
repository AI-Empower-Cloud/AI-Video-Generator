# AI Video Generator - Examples and Tutorials

## 📚 Overview

This document provides practical examples and step-by-step tutorials for using the AI Video Generator effectively. Each example includes code snippets, expected outputs, and best practices.

## 🎯 Quick Start Examples

### Example 1: Basic Story Video Generation

```python
from main import process_video_generation
from engine.core.video_engine import VideoConfig
import asyncio

# Simple story input
story = """
Alice walked through the enchanted forest. She felt curious about the mysterious sounds.
Bob appeared from behind a large oak tree. He looked surprised to see Alice.
"Hello there!" Alice said cheerfully. Bob smiled back warmly.
"""

# Basic configuration
config = VideoConfig(width=640, height=480, fps=24, duration=5)

# Generate video
async def generate_basic_video():
    video_path, title, tags = await process_video_generation(
        script=story,
        config=config
    )
    print(f"Video generated: {video_path}")
    return video_path

# Run the example
asyncio.run(generate_basic_video())
```

### Example 2: Enhanced Video with Custom Characters

```python
from enhanced_video_generator import AdvancedVideoGenerator

# Initialize generator
generator = AdvancedVideoGenerator()

# Define custom characters
characters = [
    {
        'name': 'Alice',
        'gender': 'female',
        'age': 'young',
        'appearance': 'blonde hair, blue eyes',
        'personality': 'curious, friendly'
    },
    {
        'name': 'Bob',
        'gender': 'male',
        'age': 'adult',
        'appearance': 'brown hair, green eyes',
        'personality': 'mysterious, kind'
    }
]

# Define scenes with emotions
scenes = [
    {
        'description': 'Alice walking through enchanted forest',
        'emotion': 'curiosity',
        'characters': ['Alice'],
        'setting': 'forest'
    },
    {
        'description': 'Bob appears from behind tree',
        'emotion': 'surprise',
        'characters': ['Bob'],
        'setting': 'forest'
    },
    {
        'description': 'Alice and Bob meet and greet',
        'emotion': 'joy',
        'characters': ['Alice', 'Bob'],
        'setting': 'forest'
    }
]

# Generate enhanced video
generator.generate_story_video(
    script=story,
    characters=characters,
    scenes=scenes,
    output_path="enhanced_forest_story.mp4",
    width=1280,
    height=720,
    fps=30,
    duration=10
)
```

### Example 3: Streamlit Web Interface Usage

```python
# Run the web interface
# streamlit run streamlit_app.py --server.port 8503

# Example story for web interface
web_story = """
In a bustling city, Maria runs a small bakery. Every morning, she bakes fresh bread with passion.
Today, a young customer named David enters her shop. He looks nervous but excited.
"I'd like to propose to my girlfriend," David whispers. "Can you help me make this special?"
Maria's eyes light up with joy. "Of course! Let's create something magical together."
"""

# Web interface features to use:
# 1. Paste the story in the text area
# 2. Set video dimensions to 640x480
# 3. Choose "Cartoon" style for a warm, friendly look
# 4. Set duration to 8 seconds
# 5. Enable scene transitions
# 6. Click "Generate Video"
```

## 🎨 Style-Specific Examples

### Cartoon Style Video

```python
# Perfect for children's stories or lighthearted content
cartoon_story = """
Tommy the brave little mouse lived in a cozy hole. He dreamed of becoming a superhero.
One day, he found a magical cape in the garden. Suddenly, he could fly!
"I'm Super Mouse!" he declared proudly, soaring above the flowers.
"""

style_settings = {
    'character_style': 'Cartoon',
    'background_style': 'Scene-based',
    'animation_speed': 1.2,
    'color_palette': 'vibrant',
    'lighting': 'soft'
}

generator.generate_story_video(
    script=cartoon_story,
    output_path="super_mouse_cartoon.mp4",
    style_settings=style_settings,
    width=640, height=480, fps=24, duration=6
)
```

### Realistic Style Video

```python
# Ideal for drama, romance, or serious narratives
realistic_story = """
Dr. Sarah Thompson reviewed the medical charts late into the night. 
The mysterious illness was spreading, and time was running out.
Her colleague, Dr. James Wilson, entered the lab with new test results.
"I think we've found the breakthrough we needed," he announced hopefully.
"""

style_settings = {
    'character_style': 'Realistic',
    'background_style': 'Scene-based',
    'animation_speed': 0.8,
    'color_palette': 'muted',
    'lighting': 'dramatic'
}

generator.generate_story_video(
    script=realistic_story,
    output_path="medical_drama_realistic.mp4",
    style_settings=style_settings,
    width=1280, height=720, fps=30, duration=8
)
```

### Minimalist Style Video

```python
# Great for abstract concepts or modern presentations
minimalist_story = """
The concept emerged slowly in her mind. Innovation requires both courage and patience.
She sketched the idea on a clean white board. Simple lines formed complex solutions.
"Sometimes the best ideas are the simplest ones," she reflected quietly.
"""

style_settings = {
    'character_style': 'Minimalist',
    'background_style': 'Gradient',
    'animation_speed': 1.0,
    'color_palette': 'monochrome',
    'lighting': 'natural'
}

generator.generate_story_video(
    script=minimalist_story,
    output_path="innovation_minimalist.mp4",
    style_settings=style_settings,
    width=640, height=480, fps=24, duration=5
)
```

## 📊 Advanced Examples

### Example 4: Batch Processing Multiple Stories

```python
import os
from pathlib import Path

# Multiple stories for batch processing
stories = {
    "adventure": "Jack climbed the mountain peak. The view was breathtaking.",
    "romance": "Emma met her soulmate at the coffee shop. Love filled the air.",
    "mystery": "Detective Smith found the crucial clue. The case was almost solved.",
    "comedy": "The clumsy waiter spilled soup everywhere. Everyone laughed heartily."
}

# Batch generation function
async def batch_generate_videos():
    results = []
    
    for story_type, script in stories.items():
        config = VideoConfig(width=640, height=480, fps=24, duration=4)
        
        video_path, title, tags = await process_video_generation(
            script=script,
            config=config
        )
        
        # Rename with descriptive names
        new_path = f"batch_{story_type}_video.mp4"
        os.rename(video_path, new_path)
        
        results.append({
            'type': story_type,
            'path': new_path,
            'title': title,
            'tags': tags
        })
        
        print(f"Generated {story_type} video: {new_path}")
    
    return results

# Run batch processing
batch_results = asyncio.run(batch_generate_videos())
print(f"Generated {len(batch_results)} videos successfully!")
```

### Example 5: Custom Character Creation

```python
# Advanced character customization
def create_custom_character(name, attributes):
    """Create a highly customized character."""
    return {
        'name': name,
        'gender': attributes.get('gender', 'neutral'),
        'age': attributes.get('age', 'adult'),
        'height': attributes.get('height', 'average'),
        'build': attributes.get('build', 'average'),
        'hair_color': attributes.get('hair_color', 'brown'),
        'hair_style': attributes.get('hair_style', 'short'),
        'eye_color': attributes.get('eye_color', 'brown'),
        'skin_tone': attributes.get('skin_tone', 'medium'),
        'clothing': attributes.get('clothing', 'casual'),
        'accessories': attributes.get('accessories', []),
        'personality_traits': attributes.get('personality_traits', ['friendly']),
        'voice_type': attributes.get('voice_type', 'neutral')
    }

# Create diverse characters
characters = [
    create_custom_character('Luna', {
        'gender': 'female',
        'age': 'young',
        'hair_color': 'silver',
        'hair_style': 'long',
        'eye_color': 'violet',
        'clothing': 'magical_robes',
        'accessories': ['wand', 'crystal_necklace'],
        'personality_traits': ['wise', 'mysterious', 'powerful']
    }),
    create_custom_character('Marcus', {
        'gender': 'male',
        'age': 'middle_aged',
        'build': 'athletic',
        'hair_color': 'black',
        'hair_style': 'short',
        'eye_color': 'dark_brown',
        'clothing': 'armor',
        'accessories': ['sword', 'shield'],
        'personality_traits': ['brave', 'loyal', 'determined']
    })
]

# Fantasy story with custom characters
fantasy_story = """
Luna the sorceress studied ancient spells in her tower. Magic flowed through her fingers.
Marcus the knight approached the tower seeking help. His quest required magical assistance.
"I need your wisdom, Luna," Marcus said respectfully. Luna nodded with understanding.
"""

generator.generate_story_video(
    script=fantasy_story,
    characters=characters,
    output_path="fantasy_custom_characters.mp4",
    width=1280, height=720, fps=30, duration=12
)
```

### Example 6: PDF Story Processing

```python
import PyPDF2
from io import BytesIO

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    return text

# Process PDF story
pdf_story_text = extract_text_from_pdf("sample_story.pdf")

# Clean and prepare the text
cleaned_story = pdf_story_text.replace('\n', ' ').strip()

# Generate video from PDF content
config = VideoConfig(width=1920, height=1080, fps=30, duration=15)

async def process_pdf_story():
    video_path, title, tags = await process_video_generation(
        script=cleaned_story,
        config=config
    )
    print(f"PDF story video generated: {video_path}")
    return video_path

# Execute PDF processing
pdf_video = asyncio.run(process_pdf_story())
```

## 🎛️ Configuration Examples

### High-Quality Production Settings

```python
# Professional quality settings
production_config = VideoConfig(
    width=1920,      # Full HD width
    height=1080,     # Full HD height
    fps=60,          # Smooth motion
    duration=20,     # Longer duration
    quality=10       # Maximum quality
)

production_style = {
    'character_style': 'Realistic',
    'background_style': 'Scene-based',
    'animation_speed': 1.0,
    'color_palette': 'natural',
    'lighting': 'cinematic',
    'lip_sync_enabled': True,
    'scene_transitions': True,
    'background_animation': True,
    'character_shadows': True,
    'emotion_visualization': True
}
```

### Quick Draft Settings

```python
# Fast generation for testing
draft_config = VideoConfig(
    width=320,       # Low resolution
    height=240,      # Low resolution
    fps=15,          # Lower frame rate
    duration=3,      # Short duration
    quality=3        # Basic quality
)

draft_style = {
    'character_style': 'Minimalist',
    'background_style': 'Solid',
    'animation_speed': 1.5,
    'color_palette': 'simple',
    'lighting': 'flat'
}
```

## 🐛 Debugging Examples

### Error Handling and Logging

```python
import logging
import traceback

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def robust_video_generation(script, config):
    """Video generation with comprehensive error handling."""
    try:
        logger.info("Starting video generation...")
        
        # Validate input
        if not script or len(script.strip()) == 0:
            raise ValueError("Script cannot be empty")
        
        if len(script) > 10000:
            logger.warning("Script is very long, truncating...")
            script = script[:10000]
        
        # Generate video with error recovery
        video_path, title, tags = await process_video_generation(
            script=script,
            config=config
        )
        
        logger.info(f"Video generated successfully: {video_path}")
        return video_path, title, tags
        
    except Exception as e:
        logger.error(f"Video generation failed: {str(e)}")
        logger.error(traceback.format_exc())
        
        # Fallback to basic settings
        try:
            logger.info("Attempting fallback generation...")
            fallback_config = VideoConfig(width=320, height=240, fps=15, duration=3)
            return await process_video_generation(script[:1000], fallback_config)
        except Exception as fallback_error:
            logger.error(f"Fallback also failed: {str(fallback_error)}")
            raise
```

### Performance Monitoring

```python
import time
import psutil
import gc

def monitor_video_generation(func):
    """Decorator to monitor performance during video generation."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        print(f"Starting generation - Memory: {start_memory:.1f} MB")
        
        try:
            result = func(*args, **kwargs)
            
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            print(f"Generation completed in {end_time - start_time:.2f} seconds")
            print(f"Memory usage: {end_memory:.1f} MB (Delta: {end_memory - start_memory:.1f} MB)")
            
            # Cleanup
            gc.collect()
            
            return result
            
        except Exception as e:
            print(f"Generation failed after {time.time() - start_time:.2f} seconds: {e}")
            raise
    
    return wrapper

# Use the monitor
@monitor_video_generation
async def monitored_generation(script):
    config = VideoConfig(width=640, height=480, fps=24, duration=5)
    return await process_video_generation(script, config)
```

## 📈 Best Practices

### 1. Story Writing Tips

- Keep sentences clear and descriptive
- Include character emotions and actions
- Use present tense for better processing
- Limit to 2-5 main characters per story
- Describe settings and environments

### 2. Performance Optimization

- Start with smaller resolutions for testing
- Use appropriate duration for content length
- Monitor memory usage for longer videos
- Clean up temporary files regularly

### 3. Quality Guidelines

- Use higher FPS for action scenes
- Choose appropriate styles for content tone
- Test different animation speeds
- Validate character names and attributes

### 4. Error Prevention

- Validate input text length
- Check available disk space
- Ensure proper character encoding
- Handle network timeouts gracefully

## 🎯 Common Use Cases

See the `use_cases/` folder for detailed examples:

- Educational content creation
- Marketing and advertising
- Social media content
- Storytelling and entertainment
- Training and tutorials
- Presentations and demos

## 🚀 Next Steps

1. Experiment with different story types
2. Customize characters and scenes
3. Try various visual styles
4. Optimize for your specific use case
5. Share your creations with the community

For more detailed examples, check the `use_cases/` directory in this repository.
