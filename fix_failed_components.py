#!/usr/bin/env python3
"""
Failed Components Diagnostic & Fix
=================================
Identifies and fixes the 3 failed files in the audio pipeline
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

def check_and_fix_failed_components():
    """Check and fix the 3 failed components"""
    
    print("🔧 FAILED COMPONENTS DIAGNOSTIC")
    print("=" * 40)
    
    failed_components = []
    working_components = []
    
    # Component 1: XTTS-v2 Voice Cloning
    print("\n1️⃣ XTTS-v2 VOICE CLONING:")
    try:
        from modules.xtts_v2_cloner import XTTSv2VoiceCloner
        xtts = XTTSv2VoiceCloner()
        print("   ✅ XTTS-v2 module: Working")
        working_components.append("XTTS-v2")
    except Exception as e:
        print(f"   ❌ XTTS-v2 module: Failed - {e}")
        failed_components.append("XTTS-v2")
    
    # Check TTS library
    try:
        import TTS
        print("   ✅ Coqui TTS library: Working")
    except ImportError:
        print("   ❌ Coqui TTS library: Missing")
        print("   🔧 Fix: pip install TTS")
        failed_components.append("TTS-Library")
    
    # Component 2: BBC Sound FX
    print("\n2️⃣ BBC SOUND FX LIBRARY:")
    try:
        from modules.bbc_sound_fx import BBCSoundFXLibrary
        bbc = BBCSoundFXLibrary()
        print("   ✅ BBC Sound FX module: Working")
        working_components.append("BBC-SoundFX")
    except Exception as e:
        print(f"   ❌ BBC Sound FX module: Failed - {e}")
        failed_components.append("BBC-SoundFX")
    
    # Check web scraping dependencies
    try:
        import requests
        import beautifulsoup4
        print("   ✅ Web scraping libraries: Working")
    except ImportError as e:
        print(f"   ❌ Web scraping libraries: Missing - {e}")
        print("   🔧 Fix: pip install requests beautifulsoup4")
        failed_components.append("Web-Scraping")
    
    # Component 3: Advanced Audio Processing
    print("\n3️⃣ ADVANCED AUDIO PROCESSING:")
    audio_libs = {
        'librosa': 'Audio analysis',
        'noisereduce': 'Noise reduction', 
        'scipy': 'Signal processing',
        'soundfile': 'Audio I/O',
        'pedalboard': 'Audio effects'
    }
    
    audio_working = []
    audio_failed = []
    
    for lib, description in audio_libs.items():
        try:
            __import__(lib)
            print(f"   ✅ {lib}: {description}")
            audio_working.append(lib)
        except ImportError:
            print(f"   ❌ {lib}: Missing - {description}")
            audio_failed.append(lib)
    
    if audio_failed:
        failed_components.append("Audio-Processing")
        print(f"   🔧 Fix: pip install {' '.join(audio_failed)}")
    else:
        working_components.append("Audio-Processing")
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 DIAGNOSTIC SUMMARY:")
    print(f"✅ Working components: {len(working_components)}")
    for comp in working_components:
        print(f"   - {comp}")
    
    print(f"\n❌ Failed components: {len(failed_components)}")
    for comp in failed_components:
        print(f"   - {comp}")
    
    # Generate fix commands
    if failed_components:
        print(f"\n🔧 RECOMMENDED FIXES:")
        
        if "TTS-Library" in failed_components:
            print("   pip install TTS coqui-ai-tts")
        
        if "Web-Scraping" in failed_components:
            print("   pip install requests beautifulsoup4 requests-html")
        
        if "Audio-Processing" in failed_components:
            print("   pip install librosa noisereduce scipy soundfile pedalboard")
        
        print(f"\n🚀 Or install all at once:")
        print("   pip install TTS librosa noisereduce scipy soundfile pedalboard requests beautifulsoup4")
    
    else:
        print(f"\n🎉 ALL COMPONENTS WORKING!")
        print("   Your audio pipeline is fully operational!")
    
    return len(failed_components)

def install_missing_packages():
    """Install missing packages automatically"""
    
    print("\n🔧 AUTO-INSTALLING MISSING PACKAGES...")
    print("=" * 40)
    
    packages_to_install = [
        "librosa",
        "noisereduce", 
        "scipy",
        "soundfile",
        "requests",
        "beautifulsoup4",
        "requests-html"
    ]
    
    for package in packages_to_install:
        try:
            print(f"Installing {package}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"   ✅ {package}: Installed successfully")
            else:
                print(f"   ❌ {package}: Installation failed")
                print(f"       Error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"   ⏰ {package}: Installation timeout")
        except Exception as e:
            print(f"   ❌ {package}: Exception - {e}")
    
    print(f"\n✅ Auto-installation complete!")

def create_test_script():
    """Create a test script for the new components"""
    
    test_script = '''#!/usr/bin/env python3
"""
Test Script for New Audio Components
===================================
"""

def test_xtts_v2():
    """Test XTTS-v2 voice cloning"""
    try:
        from modules.xtts_v2_cloner import XTTSv2VoiceCloner
        xtts = XTTSv2VoiceCloner()
        print("✅ XTTS-v2: Working")
        return True
    except Exception as e:
        print(f"❌ XTTS-v2: {e}")
        return False

def test_bbc_sound_fx():
    """Test BBC Sound FX library"""
    try:
        from modules.bbc_sound_fx import BBCSoundFXLibrary
        bbc = BBCSoundFXLibrary()
        effects = bbc.search_effects("rain", limit=1)
        print("✅ BBC Sound FX: Working")
        return True
    except Exception as e:
        print(f"❌ BBC Sound FX: {e}")
        return False

def test_audio_processing():
    """Test advanced audio processing"""
    try:
        import librosa
        import noisereduce
        import scipy
        print("✅ Audio Processing: Working")
        return True
    except Exception as e:
        print(f"❌ Audio Processing: {e}")
        return False

if __name__ == "__main__":
    print("🧪 TESTING NEW AUDIO COMPONENTS")
    print("=" * 35)
    
    tests = [
        ("XTTS-v2 Voice Cloning", test_xtts_v2),
        ("BBC Sound FX", test_bbc_sound_fx), 
        ("Audio Processing", test_audio_processing)
    ]
    
    passed = 0
    for name, test_func in tests:
        print(f"\\n{name}:")
        if test_func():
            passed += 1
    
    print(f"\\n📊 Results: {passed}/{len(tests)} tests passed")
'''
    
    with open("test_new_components.py", "w") as f:
        f.write(test_script)
    
    print("📝 Test script created: test_new_components.py")

def main():
    """Main diagnostic function"""
    
    print("🎵 AI VIDEO GENERATOR - COMPONENT DIAGNOSTIC")
    print("=" * 50)
    
    # Run diagnostic
    failed_count = check_and_fix_failed_components()
    
    # Create test script
    create_test_script()
    
    # Offer to auto-fix
    if failed_count > 0:
        print(f"\n❓ Would you like to auto-install missing packages?")
        print("   This will run: pip install [missing packages]")
        
        # For automated environments, we'll skip the input
        print("   Running auto-installation...")
        install_missing_packages()
        
        # Re-run diagnostic
        print(f"\n🔄 RE-RUNNING DIAGNOSTIC...")
        failed_count = check_and_fix_failed_components()
    
    if failed_count == 0:
        print(f"\n🎉 SUCCESS! All components are now working!")
        print(f"🎬 Your AI Video Generator is fully operational!")
    else:
        print(f"\n⚠️  {failed_count} components still need attention.")
        print(f"💡 Check the recommended fixes above.")

if __name__ == "__main__":
    main()
