# 🎤 Advanced Local Text-to-Speech (TTS) Engine

## Overview

The AI Video Generator now includes a comprehensive, **100% local** text-to-speech system with multiple high-quality engines. No API dependencies, no internet required, complete privacy protection.

## 🚀 TTS Engines Available

### 1. **Tortoise TTS** - Ultra High Quality
- **Quality**: ★★★★★ (Best available)
- **Speed**: ★★☆☆☆ (Slow but worth it)
- **Languages**: English only
- **Requirements**: GPU recommended for practical use
- **Best for**: Audiobooks, professional narration, premium content
- **Sample**: Natural, human-like voices with excellent prosody

### 2. **Coqui TTS** - Balanced Quality & Speed
- **Quality**: ★★★★☆ (Excellent)
- **Speed**: ★★★★☆ (Fast)
- **Languages**: 15+ languages (English, Spanish, French, German, etc.)
- **Requirements**: CPU or GPU
- **Best for**: Educational content, multi-language support, general use
- **Sample**: Clear, natural voices with good expressiveness

### 3. **ESPnet TTS** - Research Grade
- **Quality**: ★★★★☆ (High)
- **Speed**: ★★★☆☆ (Medium)
- **Languages**: English, Japanese, Chinese, Spanish
- **Requirements**: CPU or GPU
- **Best for**: Research applications, specific language needs
- **Sample**: Academic-quality synthesis with precise control

### 4. **espeak** - Lightweight & Fast
- **Quality**: ★★★☆☆ (Good)
- **Speed**: ★★★★★ (Very fast)
- **Languages**: 40+ languages
- **Requirements**: Minimal (always available)
- **Best for**: Prototyping, low-resource environments, accessibility
- **Sample**: Clear, robotic but intelligible

### 5. **pyttsx3** - System Integration
- **Quality**: ★★★☆☆ (System dependent)
- **Speed**: ★★★★☆ (Fast)
- **Languages**: System dependent
- **Requirements**: Operating system TTS
- **Best for**: System integration, fallback option
- **Sample**: Uses your system's built-in voices

## 🎭 Voice Profiles

### Educational Voices
```python
# Elementary education - friendly, clear, slightly slower
voice = "teacher_female_ultra"      # Ms. Anderson - warm, encouraging
voice = "student_enthusiastic"      # Alex - excited, curious teen

# Professional training - authoritative, clear
voice = "expert_authoritative"      # Dr. Roberts - confident, knowledgeable
voice = "narrator_professional"     # Professional narrator - neutral, engaging
```

### Character Voices
```python
# Conversational characters
voice = "alice_friendly"            # Alice - warm, approachable female
voice = "bob_confident"             # Bob - confident, reliable male
```

### Multi-Language Voices
```python
# International education
voice = "spanish_teacher"           # Profesora García - Spanish education
voice = "french_narrator"           # French narrator - native pronunciation
```

## 🔧 Quick Start

### Basic Usage
```python
from advanced_local_tts import AdvancedLocalTTS

# Initialize TTS engine
tts = AdvancedLocalTTS()

# Generate speech
result = tts.synthesize_speech(
    text="Welcome to our AI education lesson!",
    voice_profile="teacher_female_ultra",
    output_path="lesson_intro.wav"
)
```

### Quality Control
```python
# Ultra quality (slow, best quality)
tts.synthesize_speech(text, voice, "output.wav", quality_override="ultra")

# Fast generation (quick, good quality)
tts.synthesize_speech(text, voice, "output.wav", quality_override="fast")
```

### Custom Voice Creation
```python
# Create custom voice profile
custom_voice = tts.create_voice_profile(
    name="robot_teacher",
    gender="neutral",
    pitch=0.8,
    speed=0.9,
    emotion="calm",
    style="formal",
    quality="high"
)

result = tts.synthesize_speech(text, custom_voice, "robot_voice.wav")
```

## 📚 Educational Integration

### Lesson Narration
```python
from enhanced_ai_education_app import LocalTTSEducationApp

app = LocalTTSEducationApp()

# Generate complete educational lesson with voice
lesson = app.create_interactive_lesson(
    subject="artificial_intelligence",
    age_group="high_school",
    output_path="ai_lesson_complete.wav"
)
```

### Multi-Character Dialogue
```python
dialogue = [
    {"character": "teacher", "text": "What is machine learning?", "pause_after": 1.0},
    {"character": "student_female", "text": "It's when computers learn from data!", "pause_after": 0.5},
    {"character": "teacher", "text": "Excellent answer!", "pause_after": 0.5}
]

result = audio_engine.generate_dialogue(dialogue, "lesson_dialogue.wav")
```

## ⚙️ Installation & Setup

### Quick Setup (Recommended)
```bash
# Run automated setup
python setup_local_tts.py

# This will install:
# - Basic TTS engines (espeak, pyttsx3)
# - Coqui TTS (recommended for most use cases)
# - Optional: Tortoise TTS (if you have GPU)
# - Optional: ESPnet TTS (for research use)
```

### Manual Installation
```bash
# Install basic dependencies
pip install pyttsx3 librosa soundfile scipy numpy torch torchaudio

# Install advanced engines
pip install TTS  # Coqui TTS
pip install tortoise-tts  # Tortoise TTS (GPU recommended)
pip install espnet espnet_model_zoo  # ESPnet TTS

# Install system dependencies (Linux)
sudo apt-get install espeak espeak-data ffmpeg libsndfile1
```

### System Requirements

#### Minimum (Basic TTS)
- Python 3.8+
- 2GB RAM
- 1GB disk space
- CPU only

#### Recommended (Advanced TTS)
- Python 3.9+
- 8GB RAM
- 10GB disk space
- GPU with 4GB+ VRAM (for Tortoise TTS)

#### Optimal (All Features)
- Python 3.10+
- 16GB RAM
- 20GB disk space
- Modern GPU with 8GB+ VRAM

## 🎯 Use Case Recommendations

### Elementary Education
```python
# Recommended setup
engine = "coqui"
voice = "teacher_female_ultra"
quality = "high"
speed = 0.8  # Slightly slower for young learners
```

### Professional Training
```python
# Recommended setup
engine = "tortoise"  # If GPU available
voice = "expert_authoritative" 
quality = "ultra"
speed = 1.0
```

### Quick Prototyping
```python
# Recommended setup
engine = "espeak"
voice = "narrator"
quality = "fast"
speed = 1.2  # Faster for testing
```

### Multi-Language Content
```python
# Recommended setup
engine = "coqui"
voice = "spanish_teacher"  # or other language
quality = "high"
language = "es"  # Spanish
```

### Audiobook Narration
```python
# Recommended setup
engine = "tortoise"
voice = "narrator_professional"
quality = "ultra"
speed = 0.95  # Slightly slower for listening comfort
```

## 🔍 Performance Benchmarks

### Speed Comparison (1000 words)
- **espeak**: ~2 seconds
- **pyttsx3**: ~5 seconds  
- **Coqui TTS**: ~15 seconds (CPU) / ~3 seconds (GPU)
- **Tortoise TTS**: ~5 minutes (CPU) / ~30 seconds (GPU)
- **ESPnet TTS**: ~30 seconds (CPU) / ~8 seconds (GPU)

### Quality Ranking
1. **Tortoise TTS** - Human-like, natural prosody
2. **Coqui TTS (VITS)** - Very natural, good expressiveness
3. **ESPnet TTS** - Clear, precise, academic quality
4. **Coqui TTS (Standard)** - Good clarity, some robotic qualities
5. **pyttsx3** - System dependent, generally acceptable
6. **espeak** - Robotic but clear and intelligible

### Resource Usage
- **espeak**: <100MB RAM, CPU minimal
- **pyttsx3**: ~200MB RAM, CPU light
- **Coqui TTS**: 1-2GB RAM, CPU/GPU moderate
- **Tortoise TTS**: 4-8GB RAM, GPU heavy
- **ESPnet TTS**: 2-4GB RAM, CPU/GPU moderate

## 🛠️ Advanced Features

### SSML Support
```python
# Use Speech Synthesis Markup Language for precise control
ssml_text = '''
<speak>
    Welcome to our lesson on <emphasis level="strong">artificial intelligence</emphasis>.
    <break time="1s"/>
    Today we'll learn about <prosody rate="slow">machine learning</prosody>.
</speak>
'''

result = tts.synthesize_speech(ssml_text, voice, "lesson.wav", ssml=True)
```

### Voice Cloning (Advanced)
```python
# Clone voice from reference audio (requires additional setup)
custom_voice = tts.create_voice_profile(
    name="teacher_clone",
    voice_clone_reference="reference_audio.wav",
    quality="ultra"
)
```

### Real-Time Synthesis
```python
# Stream audio for real-time applications
for text_chunk in text_chunks:
    tts.synthesize_speech(text_chunk, voice, f"chunk_{i}.wav", quality="fast")
```

## 🎙️ Advanced Voice Features

### Custom Voice Branding
Create unique institutional voices that represent your brand:

```python
# Create custom branded voice for school district
brand_voice = tts.create_voice_brand(
    institution="Springfield Elementary",
    voice_type="teacher_female",
    personality=["warm", "encouraging", "patient"],
    age_range="30s",
    accent="neutral_american",
    output_name="springfield_teacher"
)

# Use branded voice in lessons
lesson_audio = tts.synthesize_speech(
    text="Welcome to our math lesson today!",
    voice_profile=brand_voice,
    output_path="branded_lesson.wav"
)
```

### Voice Cloning from Audio Dataset
Train custom voices using 15-60 minutes of clear audio:

```python
# Voice cloning workflow
voice_cloner = VoiceCloner()

# Prepare training dataset
training_data = voice_cloner.prepare_dataset(
    audio_files=["principal_speech_01.wav", "principal_speech_02.wav"],
    transcript_files=["transcript_01.txt", "transcript_02.txt"],
    min_duration_minutes=20,
    quality_threshold=0.85
)

# Train custom voice model
custom_voice = voice_cloner.train_voice(
    dataset=training_data,
    voice_name="principal_anderson",
    training_epochs=150,
    output_dir="voices/custom/"
)

# Generate speech with cloned voice
result = tts.synthesize_speech(
    text="Good morning, students and faculty!",
    voice_profile=custom_voice,
    output_path="principal_announcement.wav"
)
```

### Expressive Prosody & Emotion Control
Fine-tune emotional expression and speaking patterns:

```python
# Advanced emotional expression
emotion_config = {
    "emotion": "enthusiastic",
    "emphasis_strength": 0.8,
    "pause_duration": 0.4,
    "pitch_variation": 0.6,
    "speed_variation": 0.3,
    "stress_patterns": "educational"
}

# Generate expressive speech
expressive_audio = tts.synthesize_with_emotion(
    text="Today we're going to discover something AMAZING about artificial intelligence!",
    voice="teacher_enthusiastic",
    emotion_config=emotion_config,
    output_path="excited_lesson_intro.wav"
)
```

### Multilingual Voice Cloning
Clone voices across different languages while maintaining personality:

```python
# Create multilingual teacher voices
base_voice = "ms_garcia_english"

# Clone to Spanish
spanish_voice = tts.clone_voice_to_language(
    base_voice=base_voice,
    target_language="es",
    adaptation_samples=["spanish_phrases.wav"],
    output_name="ms_garcia_spanish"
)

# Clone to French  
french_voice = tts.clone_voice_to_language(
    base_voice=base_voice,
    target_language="fr",
    adaptation_samples=["french_phrases.wav"],
    output_name="ms_garcia_french"
)

# Generate lesson in multiple languages
languages = {
    "en": ("Welcome to science class!", "ms_garcia_english"),
    "es": ("¡Bienvenidos a la clase de ciencias!", "ms_garcia_spanish"),
    "fr": ("Bienvenue au cours de sciences!", "ms_garcia_french")
}

for lang_code, (text, voice) in languages.items():
    audio = tts.synthesize_speech(
        text=text,
        voice_profile=voice,
        language=lang_code,
        output_path=f"lesson_intro_{lang_code}.wav"
    )
```

### High-Quality Professional Audio Output
Studio-grade audio specifications:

```python
# Professional audio settings
professional_config = {
    "sample_rate": 48000,        # Professional quality
    "bit_depth": 24,             # 24-bit precision
    "format": "wav",             # Uncompressed
    "noise_reduction": True,     # Clean output
    "normalization": True,       # Consistent levels
    "enhancement": {
        "eq_enabled": True,      # Audio equalization
        "clarity_boost": 0.3,    # Speech clarity
        "spatial_audio": "classroom"  # Room simulation
    }
}

# Generate professional-quality audio
pro_audio = tts.synthesize_professional(
    text=lesson_script,
    voice=brand_voice,
    audio_config=professional_config,
    output_path="professional_lesson.wav"
)
```

## 🎓 Educational Use Cases

### School District Voice Branding
```python
# Consistent voices across all district content
district_brand = {
    "elementary": {
        "voice_type": "teacher_female_warm",
        "age": "30s",
        "pace": "slow",
        "personality": ["patient", "encouraging"]
    },
    "middle_school": {
        "voice_type": "teacher_male_confident", 
        "age": "40s",
        "pace": "medium",
        "personality": ["engaging", "authoritative"]
    },
    "high_school": {
        "voice_type": "teacher_female_inspiring",
        "age": "35s", 
        "pace": "medium-fast",
        "personality": ["knowledgeable", "motivating"]
    }
}

# Create branded voices for each level
for level, specs in district_brand.items():
    voice_model = tts.create_district_voice(
        level=level,
        specifications=specs,
        training_duration_hours=2,
        output_path=f"district_voices/{level}_teacher.model"
    )
```

### Voice Dataset Requirements

#### **Training Data Specifications**

- **Minimum (15 minutes)**: Basic voice clone, recognizable
- **Recommended (30-45 minutes)**: High-quality clone with good expressiveness  
- **Optimal (60+ minutes)**: Exceptional quality, nearly indistinguishable

#### **Audio Quality Requirements**
- **Sample Rate**: 44.1kHz minimum, 48kHz preferred
- **Bit Depth**: 16-bit minimum, 24-bit preferred
- **Format**: WAV (uncompressed)
- **Background Noise**: Minimal (<-50dB)
- **Recording Environment**: Quiet room with minimal echo

```python
# Validate training dataset quality
quality_checker = AudioQualityValidator()

quality_report = quality_checker.validate_dataset(
    audio_files=training_files,
    requirements={
        "min_snr": 25,              # Signal-to-noise ratio
        "max_noise_floor": -60,     # Background noise limit
        "min_duration": 900,        # 15 minutes minimum
        "sample_rate": 48000,       # Professional quality
        "dynamic_range": 30         # Audio dynamic range
    },
    auto_enhance=True,              # Fix issues automatically
    output_report="quality_report.json"
)
```
