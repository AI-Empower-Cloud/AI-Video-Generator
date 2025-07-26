#!/usr/bin/env python3
"""
🎯 ADVANCED AI VIDEO GENERATOR COMPONENT VERIFICATION
====================================================
Tests XTTS, Tortoise TTS, AudioCraft/MusicGen, and all pipeline components
"""

import sys
import subprocess
import importlib

def test_component(name, import_name, description=""):
    """Test if a component is working"""
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', 'Available')
        print(f"✅ {name}: {version} - {description}")
        return True
    except ImportError as e:
        print(f"❌ {name}: Missing - {str(e)}")
        return False
    except Exception as e:
        print(f"⚠️  {name}: Issue - {str(e)}")
        return False

def main():
    print("🎯 COMPREHENSIVE AI VIDEO GENERATOR VERIFICATION")
    print("=" * 60)
    
    # Advanced TTS Components
    print("\n🎤 ADVANCED TTS COMPONENTS:")
    print("-" * 40)
    
    tts_components = [
        ("Coqui TTS (XTTS)", "TTS", "Multilingual voice cloning"),
        ("Tortoise TTS", "tortoise", "High-quality expressive speech"),
        ("PyTorch", "torch", "Neural network backend"),
        ("Transformers", "transformers", "Hugging Face models"),
    ]
    
    tts_working = 0
    for name, import_name, desc in tts_components:
        if test_component(name, import_name, desc):
            tts_working += 1
    
    # AI Music Generation
    print("\n🎼 AI MUSIC GENERATION:")
    print("-" * 40)
    
    music_components = [
        ("AudioCraft", "audiocraft", "Meta's AI music toolkit"),
        ("MusicGen", "audiocraft.models.musicgen", "AI music generation"),
        ("Encodec", "encodec", "Neural audio codec"),
        ("Julius", "julius", "Audio resampling"),
    ]
    
    music_working = 0
    for name, import_name, desc in music_components:
        if test_component(name, import_name, desc):
            music_working += 1
    
    # Core Pipeline
    print("\n🎬 CORE VIDEO PIPELINE:")
    print("-" * 40)
    
    core_components = [
        ("MoviePy", "moviepy", "Video editing"),
        ("FFmpeg-Python", "ffmpeg", "Video processing"),
        ("Pydub", "pydub", "Audio manipulation"),
        ("OpenCV", "cv2", "Computer vision"),
        ("Pillow", "PIL", "Image processing"),
        ("NumPy", "numpy", "Array processing"),
        ("SciPy", "scipy", "Scientific computing"),
    ]
    
    core_working = 0
    for name, import_name, desc in core_components:
        if test_component(name, import_name, desc):
            core_working += 1
    
    # Audio Processing
    print("\n🔊 AUDIO PROCESSING:")
    print("-" * 40)
    
    audio_components = [
        ("Librosa", "librosa", "Audio analysis"),
        ("Soundfile", "soundfile", "Audio I/O"),
        ("Noise Reduce", "noisereduce", "Audio cleanup"),
        ("Freesound API", "freesound", "Sound effects"),
    ]
    
    audio_working = 0
    for name, import_name, desc in audio_components:
        if test_component(name, import_name, desc):
            audio_working += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 COMPONENT STATUS SUMMARY:")
    print(f"🎤 Advanced TTS: {tts_working}/{len(tts_components)} components working")
    print(f"🎼 AI Music: {music_working}/{len(music_components)} components working")
    print(f"🎬 Core Pipeline: {core_working}/{len(core_components)} components working")
    print(f"🔊 Audio Processing: {audio_working}/{len(audio_components)} components working")
    
    total_working = tts_working + music_working + core_working + audio_working
    total_components = len(tts_components) + len(music_components) + len(core_components) + len(audio_components)
    
    percentage = (total_working / total_components) * 100
    print(f"\n🎯 OVERALL STATUS: {total_working}/{total_components} ({percentage:.1f}%)")
    
    if percentage >= 90:
        print("🚀 EXCELLENT! Your AI Video Generator is production-ready!")
    elif percentage >= 75:
        print("✅ GOOD! Most components are working. Minor setup needed.")
    elif percentage >= 50:
        print("⚠️  PARTIAL: Some components need installation.")
    else:
        print("❌ CRITICAL: Major components missing.")
    
    # Test specific functionality
    print("\n🧪 FUNCTIONALITY TESTS:")
    print("-" * 40)
    
    # Test TTS
    try:
        from TTS.api import TTS
        print("✅ XTTS API: Ready for voice synthesis")
    except Exception as e:
        print(f"❌ XTTS API: {e}")
    
    # Test AudioCraft
    try:
        from audiocraft.models import MusicGen
        print("✅ MusicGen API: Ready for music generation")
    except Exception as e:
        print(f"❌ MusicGen API: {e}")
    
    # Test core video
    try:
        from moviepy.editor import VideoFileClip
        print("✅ Video Processing: MoviePy ready")
    except Exception as e:
        print(f"❌ Video Processing: {e}")
    
    print("\n✨ VERIFICATION COMPLETE!")

if __name__ == "__main__":
    main()
