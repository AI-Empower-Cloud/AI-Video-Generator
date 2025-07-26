#!/usr/bin/env python3
"""
Full Movie Audio Pipeline Verification
======================================
Tests all components for FREE movie audio generation pipeline
"""

import sys
import subprocess
import importlib.util

def check_package(package_name, import_name=None):
    """Check if a package is installed and importable"""
    if import_name is None:
        import_name = package_name
    
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', 'Unknown')
        print(f"✅ {package_name}: {version}")
        return True
    except ImportError:
        print(f"❌ {package_name}: Not installed")
        return False

def check_system_command(command):
    """Check if system command is available"""
    try:
        result = subprocess.run([command, '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ {command}: Available")
            return True
        else:
            print(f"❌ {command}: Not working")
            return False
    except Exception:
        print(f"❌ {command}: Not found")
        return False

def main():
    print("🎵 FULL MOVIE AUDIO PIPELINE VERIFICATION")
    print("=" * 50)
    
    # Component 1: TTS Voice Generation
    print("\n1️⃣ TTS VOICE GENERATION (Tortoise/XTTS):")
    print("-" * 40)
    tts_components = [
        ("Coqui TTS", "TTS"),
        ("PyTorch", "torch"),
        ("Torchaudio", "torchaudio"),
        ("Tortoise TTS", "tortoise"),
        ("gTTS", "gtts"),
    ]
    
    for name, import_name in tts_components:
        check_package(name, import_name)
    
    # Component 2: Cinematic Music Generation
    print("\n2️⃣ CINEMATIC MUSIC GENERATION (MusicGen):")
    print("-" * 40)
    music_components = [
        ("AudioCraft", "audiocraft"),
        ("MusicGen", "musicgen"),
        ("Encodec", "encodec"),
        ("Music21", "music21"),
    ]
    
    for name, import_name in music_components:
        check_package(name, import_name)
    
    # Component 3: Freesound.org SFX Download
    print("\n3️⃣ FREESOUND.ORG SFX DOWNLOAD:")
    print("-" * 40)
    sfx_components = [
        ("Freesound Python", "freesound"),
        ("Requests", "requests"),
        ("Soundfile", "soundfile"),
    ]
    
    for name, import_name in sfx_components:
        check_package(name, import_name)
    
    # Component 4: Audio Layer Combination
    print("\n4️⃣ AUDIO LAYER COMBINATION (pydub):")
    print("-" * 40)
    audio_components = [
        ("Pydub", "pydub"),
        ("Numpy", "numpy"),
        ("Scipy", "scipy"),
        ("Librosa", "librosa"),
    ]
    
    for name, import_name in audio_components:
        check_package(name, import_name)
    
    # Component 5: Audacity-style Processing
    print("\n5️⃣ AUDACITY-STYLE PROCESSING:")
    print("-" * 40)
    processing_components = [
        ("Audacity Python", "audacity"),
        ("Noise Reduce", "noisereduce"),
        ("Pedalboard", "pedalboard"),
        ("Audio Separator", "audio_separator"),
    ]
    
    for name, import_name in processing_components:
        check_package(name, import_name)
    
    # Component 6: FFmpeg Export & Muxing
    print("\n6️⃣ FFMPEG EXPORT & VIDEO MUXING:")
    print("-" * 40)
    ffmpeg_components = [
        ("FFmpeg Python", "ffmpeg"),
        ("MoviePy", "moviepy"),
        ("ImageIO FFmpeg", "imageio_ffmpeg"),
    ]
    
    for name, import_name in ffmpeg_components:
        check_package(name, import_name)
    
    # System Commands
    print("\n🖥️ SYSTEM COMMANDS:")
    print("-" * 40)
    system_commands = ["ffmpeg", "ffprobe"]
    
    for cmd in system_commands:
        check_system_command(cmd)
    
    print("\n" + "=" * 50)
    print("✅ VERIFICATION COMPLETE!")
    print("📝 Install missing packages with:")
    print("   pip install -r requirements_comprehensive_ai_video.txt")

if __name__ == "__main__":
    main()
