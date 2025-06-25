#!/usr/bin/env python3
"""
Simplified Local TTS Engine for AI Video Generator

A streamlined, working implementation focusing on:
- espeak for reliable TTS (available on the system)
- Basic voice profiles and customization
- 100% offline operation
- Educational content optimization
"""

import os
import subprocess
import tempfile
import logging
import numpy as np
import soundfile as sf
from typing import Dict, List, Optional, Union
from dataclasses import dataclass

@dataclass
class SimpleVoiceProfile:
    """Simplified voice profile."""
    name: str
    gender: str = "neutral"
    speed: float = 1.0  # 0.5-2.0
    pitch: float = 1.0  # 0.5-2.0
    volume: float = 0.8  # 0.0-1.0
    language: str = "en"

class SimplifiedLocalTTS:
    """Simplified local TTS engine that actually works."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.sample_rate = 22050
        
        # Check available engines
        self.engines = self._detect_engines()
        
        # Predefined voice profiles
        self.voice_profiles = {
            'narrator': SimpleVoiceProfile('narrator', 'neutral', 1.0, 1.0, 0.8),
            'teacher_female': SimpleVoiceProfile('teacher_female', 'female', 0.9, 1.1, 0.8),
            'teacher_male': SimpleVoiceProfile('teacher_male', 'male', 0.9, 0.9, 0.8),
            'student_female': SimpleVoiceProfile('student_female', 'female', 1.1, 1.3, 0.7),
            'student_male': SimpleVoiceProfile('student_male', 'male', 1.1, 1.1, 0.7),
            'alice': SimpleVoiceProfile('alice', 'female', 0.95, 1.2, 0.8),
            'bob': SimpleVoiceProfile('bob', 'male', 1.0, 0.8, 0.8),
            'expert': SimpleVoiceProfile('expert', 'neutral', 0.85, 0.95, 0.9)
        }
        
        self.logger.info(f"Simplified Local TTS initialized with {len(self.engines)} engines")
    
    def _detect_engines(self) -> Dict[str, bool]:
        """Detect available TTS engines."""
        engines = {}
        
        # Check espeak
        try:
            result = subprocess.run(['espeak', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                engines['espeak'] = True
                self.logger.info("✅ espeak engine detected")
        except:
            pass
        
        # Check pyttsx3
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engines['pyttsx3'] = True
            self.logger.info("✅ pyttsx3 engine detected")
        except:
            pass
        
        # Fallback to basic synthesis
        engines['fallback'] = True
        
        return engines
    
    def synthesize_speech(self, text: str, voice_profile: Union[str, SimpleVoiceProfile], 
                         output_path: str) -> Optional[str]:
        """Synthesize speech using available engines."""
        try:
            # Get voice profile
            if isinstance(voice_profile, str):
                profile = self.voice_profiles.get(voice_profile, self.voice_profiles['narrator'])
            else:
                profile = voice_profile
            
            # Clean text
            text = text.strip().replace('\n', ' ').replace('\t', ' ')
            if not text:
                return None
            
            # Try engines in order
            if 'espeak' in self.engines:
                return self._synthesize_espeak(text, profile, output_path)
            elif 'pyttsx3' in self.engines:
                return self._synthesize_pyttsx3(text, profile, output_path)
            else:
                return self._synthesize_fallback(text, profile, output_path)
                
        except Exception as e:
            self.logger.error(f"Speech synthesis failed: {e}")
            return None
    
    def _synthesize_espeak(self, text: str, profile: SimpleVoiceProfile, 
                          output_path: str) -> str:
        """Synthesize using espeak."""
        # Build espeak command
        cmd = [
            'espeak',
            '-w', output_path,  # Output to file
            '-s', str(int(150 * profile.speed)),  # Speed (words per minute)
            '-p', str(int(50 * profile.pitch)),   # Pitch (0-99)
            '-a', str(int(100 * profile.volume)), # Amplitude (0-200)
        ]
        
        # Select voice based on gender
        if profile.gender == 'female':
            cmd.extend(['-v', 'en+f3'])
        elif profile.gender == 'male':
            cmd.extend(['-v', 'en+m3'])
        else:
            cmd.extend(['-v', 'en'])
        
        cmd.append(text)
        
        # Execute command
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and os.path.exists(output_path):
            self.logger.info(f"✅ espeak synthesis successful: {output_path}")
            return output_path
        else:
            raise Exception(f"espeak failed: {result.stderr}")
    
    def _synthesize_pyttsx3(self, text: str, profile: SimpleVoiceProfile, 
                           output_path: str) -> str:
        """Synthesize using pyttsx3."""
        import pyttsx3
        
        engine = pyttsx3.init()
        
        # Configure voice
        voices = engine.getProperty('voices')
        if voices:
            for voice in voices:
                voice_name = voice.name.lower()
                if profile.gender == 'female' and 'female' in voice_name:
                    engine.setProperty('voice', voice.id)
                    break
                elif profile.gender == 'male' and 'male' in voice_name:
                    engine.setProperty('voice', voice.id)
                    break
        
        # Set properties
        rate = engine.getProperty('rate')
        engine.setProperty('rate', int(rate * profile.speed))
        engine.setProperty('volume', profile.volume)
        
        # Generate audio
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        
        if os.path.exists(output_path):
            self.logger.info(f"✅ pyttsx3 synthesis successful: {output_path}")
            return output_path
        else:
            raise Exception("pyttsx3 failed to create output file")
    
    def _synthesize_fallback(self, text: str, profile: SimpleVoiceProfile, 
                           output_path: str) -> str:
        """Fallback synthesis using tone generation."""
        # Generate simple beep pattern based on text
        duration = len(text) * 0.05 * (2.0 - profile.speed)
        sr = self.sample_rate
        t = np.linspace(0, duration, int(sr * duration), False)
        
        # Create tone sequence based on text
        base_freq = 440 * profile.pitch
        audio = np.zeros_like(t)
        
        # Simple pattern: different tones for different characters
        for i, char in enumerate(text[:20]):  # Limit to 20 characters
            if char.isalpha():
                freq = base_freq * (1 + 0.1 * (ord(char.lower()) - ord('a')) / 26)
                start_time = i * 0.1
                end_time = min((i + 1) * 0.1, duration)
                
                if start_time < duration:
                    mask = (t >= start_time) & (t < end_time)
                    tone = np.sin(2 * np.pi * freq * t[mask]) * profile.volume
                    audio[mask] = tone
        
        # Apply envelope
        envelope = np.exp(-t * 2)
        audio *= envelope
        
        # Save
        sf.write(output_path, audio, sr)
        self.logger.info(f"✅ Fallback synthesis successful: {output_path}")
        return output_path
    
    def create_voice_profile(self, name: str, **kwargs) -> SimpleVoiceProfile:
        """Create a custom voice profile."""
        return SimpleVoiceProfile(name=name, **kwargs)
    
    def list_available_voices(self) -> List[str]:
        """List available voice profiles."""
        return list(self.voice_profiles.keys())
    
    def get_engine_info(self) -> Dict[str, bool]:
        """Get engine information."""
        return self.engines.copy()

# Test the simplified TTS
def test_simplified_tts():
    """Test the simplified TTS engine."""
    print("🔊 Testing Simplified Local TTS Engine...")
    
    tts = SimplifiedLocalTTS()
    
    print(f"Available engines: {list(tts.engines.keys())}")
    print(f"Available voices: {tts.list_available_voices()}")
    
    # Test basic synthesis
    test_cases = [
        ("Hello! This is a test of the simplified local TTS engine.", "narrator"),
        ("Welcome to our AI education lesson!", "teacher_female"),
        ("I'm excited to learn about artificial intelligence!", "student_male"),
        ("Let me explain how machine learning works.", "expert")
    ]
    
    for i, (text, voice) in enumerate(test_cases):
        output_path = f"test_simple_{i+1}_{voice}.wav"
        print(f"\nTesting voice '{voice}': {text}")
        
        result = tts.synthesize_speech(text, voice, output_path)
        
        if result and os.path.exists(result):
            size = os.path.getsize(result)
            print(f"✅ Success: {result} ({size} bytes)")
            
            # Clean up test file
            try:
                os.remove(result)
                print(f"🧹 Cleaned up: {result}")
            except:
                pass
        else:
            print(f"❌ Failed: {voice}")
    
    print("\n🎉 Simplified Local TTS Engine test completed!")

if __name__ == "__main__":
    test_simplified_tts()
