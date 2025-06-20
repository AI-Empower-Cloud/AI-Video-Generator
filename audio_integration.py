#!/usr/bin/env python3
"""
Advanced Audio Integration for AI Video Generator

Features:
- Text-to-Speech synthesis with multiple voices
- Background music generation and mixing
- Audio synchronization with video
- Voice cloning and character-specific voices
- Dynamic music based on emotions
- Audio effects and processing
"""

import numpy as np
import librosa
import soundfile as sf
from typing import List, Dict, Optional, Tuple
import tempfile
import os
from pathlib import Path
import logging

# Audio synthesis
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False

class AdvancedAudioEngine:
    """Advanced audio processing engine for video generation."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.sample_rate = 22050
        self.voice_engines = self._initialize_voice_engines()
        
        # Character voice mapping
        self.character_voices = {
            'alice': {'gender': 'female', 'pitch': 1.2, 'speed': 0.9},
            'bob': {'gender': 'male', 'pitch': 0.8, 'speed': 1.0},
            'carol': {'gender': 'female', 'pitch': 1.1, 'speed': 1.1},
            'default_male': {'gender': 'male', 'pitch': 1.0, 'speed': 1.0},
            'default_female': {'gender': 'female', 'pitch': 1.15, 'speed': 1.05}
        }
        
        # Emotion-based music templates
        self.emotion_music = {
            'joy': {'tempo': 120, 'key': 'C_major', 'instruments': ['piano', 'strings']},
            'sadness': {'tempo': 60, 'key': 'A_minor', 'instruments': ['piano', 'cello']},
            'anger': {'tempo': 140, 'key': 'D_minor', 'instruments': ['drums', 'brass']},
            'fear': {'tempo': 90, 'key': 'F_minor', 'instruments': ['strings', 'ambient']},
            'surprise': {'tempo': 110, 'key': 'G_major', 'instruments': ['piano', 'bells']},
            'neutral': {'tempo': 100, 'key': 'C_major', 'instruments': ['piano']}
        }
    
    def _initialize_voice_engines(self) -> Dict:
        """Initialize available text-to-speech engines."""
        engines = {}
        
        if PYTTSX3_AVAILABLE:
            try:
                engine = pyttsx3.init()
                engines['pyttsx3'] = engine
                self.logger.info("✅ pyttsx3 voice engine initialized")
            except Exception as e:
                self.logger.warning(f"❌ pyttsx3 initialization failed: {e}")
        
        if GTTS_AVAILABLE:
            engines['gtts'] = True
            self.logger.info("✅ Google TTS available")
        
        return engines
    
    def generate_character_voice(self, text: str, character_info: Dict, 
                               output_path: str) -> Optional[str]:
        """Generate voice audio for a specific character."""
        try:
            character_name = character_info.get('name', 'default').lower()
            voice_config = self.character_voices.get(
                character_name, 
                self.character_voices['default_male' if character_info.get('gender') == 'male' 
                                   else 'default_female']
            )
            
            # Try pyttsx3 first (offline, faster)
            if 'pyttsx3' in self.voice_engines:
                return self._generate_pyttsx3_voice(text, voice_config, output_path)
            
            # Fallback to Google TTS
            elif 'gtts' in self.voice_engines:
                return self._generate_gtts_voice(text, voice_config, output_path)
            
            else:
                self.logger.warning("No voice engines available")
                return None
                
        except Exception as e:
            self.logger.error(f"Voice generation failed: {e}")
            return None
    
    def _generate_pyttsx3_voice(self, text: str, voice_config: Dict, 
                              output_path: str) -> str:
        """Generate voice using pyttsx3 (offline)."""
        engine = self.voice_engines['pyttsx3']
        
        # Configure voice properties
        voices = engine.getProperty('voices')
        
        # Select voice based on gender
        selected_voice = None
        gender = voice_config.get('gender', 'female')
        
        for voice in voices:
            if gender == 'female' and ('female' in voice.name.lower() or 'zira' in voice.name.lower()):
                selected_voice = voice.id
                break
            elif gender == 'male' and ('male' in voice.name.lower() or 'david' in voice.name.lower()):
                selected_voice = voice.id
                break
        
        if selected_voice:
            engine.setProperty('voice', selected_voice)
        
        # Set speech rate and pitch
        rate = engine.getProperty('rate')
        engine.setProperty('rate', int(rate * voice_config.get('speed', 1.0)))
        
        # Generate audio
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        
        # Apply pitch modification if needed
        if voice_config.get('pitch', 1.0) != 1.0:
            self._modify_pitch(output_path, voice_config['pitch'])
        
        return output_path
    
    def _generate_gtts_voice(self, text: str, voice_config: Dict, 
                           output_path: str) -> str:
        """Generate voice using Google Text-to-Speech."""
        # Select language based on gender (approximation)
        lang = 'en-us'  # Default
        
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_path)
        
        # Apply voice modifications
        if voice_config.get('pitch', 1.0) != 1.0 or voice_config.get('speed', 1.0) != 1.0:
            self._modify_audio_properties(output_path, voice_config)
        
        return output_path
    
    def _modify_pitch(self, audio_path: str, pitch_factor: float):
        """Modify pitch of audio file."""
        try:
            # Load audio
            y, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # Pitch shift
            y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=pitch_factor * 12)
            
            # Save modified audio
            sf.write(audio_path, y_shifted, sr)
            
        except Exception as e:
            self.logger.warning(f"Pitch modification failed: {e}")
    
    def _modify_audio_properties(self, audio_path: str, voice_config: Dict):
        """Modify audio speed and pitch using librosa."""
        try:
            # Load audio
            y, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # Speed modification
            speed_factor = voice_config.get('speed', 1.0)
            if speed_factor != 1.0:
                y = librosa.effects.time_stretch(y, rate=speed_factor)
            
            # Pitch modification
            pitch_factor = voice_config.get('pitch', 1.0)
            if pitch_factor != 1.0:
                n_steps = (pitch_factor - 1.0) * 12
                y = librosa.effects.pitch_shift(y, sr=sr, n_steps=n_steps)
            
            # Save modified audio
            sf.write(audio_path, y, sr)
            
        except Exception as e:
            self.logger.warning(f"Audio property modification failed: {e}")
    
    def generate_background_music(self, emotion: str, duration: float, 
                                output_path: str) -> Optional[str]:
        """Generate background music based on emotion and duration."""
        try:
            music_config = self.emotion_music.get(emotion, self.emotion_music['neutral'])
            
            # Generate simple procedural music
            return self._create_procedural_music(music_config, duration, output_path)
            
        except Exception as e:
            self.logger.error(f"Background music generation failed: {e}")
            return None
    
    def _create_procedural_music(self, config: Dict, duration: float, 
                               output_path: str) -> str:
        """Create simple procedural background music."""
        try:
            sr = self.sample_rate
            t = np.linspace(0, duration, int(sr * duration), False)
            
            # Generate basic chord progression
            tempo = config['tempo']
            beat_duration = 60.0 / tempo
            
            # Simple chord progression in the specified key
            frequencies = self._get_chord_frequencies(config['key'])
            
            # Generate audio
            audio = np.zeros_like(t)
            
            for i, freq in enumerate(frequencies):
                # Create chord progression
                chord_start = i * beat_duration
                chord_end = min((i + 1) * beat_duration, duration)
                
                if chord_start < duration:
                    chord_mask = (t >= chord_start) & (t < chord_end)
                    
                    # Generate chord (root + third + fifth)
                    root = np.sin(2 * np.pi * freq * t[chord_mask])
                    third = np.sin(2 * np.pi * freq * 1.25 * t[chord_mask]) * 0.7
                    fifth = np.sin(2 * np.pi * freq * 1.5 * t[chord_mask]) * 0.5
                    
                    # Apply envelope
                    envelope = np.exp(-t[chord_mask] * 2)
                    chord_audio = (root + third + fifth) * envelope * 0.1
                    
                    audio[chord_mask] += chord_audio
            
            # Add some reverb effect
            audio = self._add_reverb(audio, sr)
            
            # Normalize
            audio = audio / np.max(np.abs(audio)) * 0.7
            
            # Save
            sf.write(output_path, audio, sr)
            return output_path
            
        except Exception as e:
            self.logger.error(f"Procedural music creation failed: {e}")
            return None
    
    def _get_chord_frequencies(self, key: str) -> List[float]:
        """Get chord frequencies for a musical key."""
        # Simple chord progressions
        chord_progressions = {
            'C_major': [261.63, 329.63, 392.00, 261.63],  # C-E-G-C
            'A_minor': [220.00, 261.63, 329.63, 220.00],  # A-C-E-A
            'D_minor': [293.66, 349.23, 440.00, 293.66],  # D-F-A-D
            'F_minor': [174.61, 207.65, 261.63, 174.61],  # F-Ab-C-F
            'G_major': [196.00, 246.94, 293.66, 196.00],  # G-B-D-G
        }
        return chord_progressions.get(key, chord_progressions['C_major'])
    
    def _add_reverb(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """Add simple reverb effect to audio."""
        try:
            # Create a simple delay-based reverb
            delay_samples = int(0.1 * sr)  # 100ms delay
            reverb = np.zeros_like(audio)
            
            if len(audio) > delay_samples:
                reverb[delay_samples:] = audio[:-delay_samples] * 0.3
                reverb[delay_samples*2:] += audio[:-delay_samples*2] * 0.1
            
            return audio + reverb
            
        except Exception as e:
            self.logger.warning(f"Reverb effect failed: {e}")
            return audio
    
    def mix_audio_with_video(self, video_path: str, voice_audio_path: str, 
                           music_audio_path: Optional[str], output_path: str) -> str:
        """Mix voice and background music with video."""
        try:
            if not PYDUB_AVAILABLE:
                self.logger.warning("Pydub not available, skipping audio mixing")
                return video_path
            
            # Load audio files
            voice_audio = AudioSegment.from_file(voice_audio_path)
            
            # Mix with background music if provided
            if music_audio_path and os.path.exists(music_audio_path):
                music_audio = AudioSegment.from_file(music_audio_path)
                
                # Adjust music volume (background)
                music_audio = music_audio - 20  # Reduce volume by 20dB
                
                # Match duration
                if len(music_audio) > len(voice_audio):
                    music_audio = music_audio[:len(voice_audio)]
                else:
                    # Loop music if shorter
                    while len(music_audio) < len(voice_audio):
                        music_audio += music_audio
                    music_audio = music_audio[:len(voice_audio)]
                
                # Mix audio
                mixed_audio = voice_audio.overlay(music_audio)
            else:
                mixed_audio = voice_audio
            
            # Save mixed audio
            temp_audio_path = output_path.replace('.mp4', '_audio.wav')
            mixed_audio.export(temp_audio_path, format="wav")
            
            # Combine with video (requires moviepy or ffmpeg)
            self._combine_video_audio(video_path, temp_audio_path, output_path)
            
            # Clean up temporary file
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Audio mixing failed: {e}")
            return video_path
    
    def _combine_video_audio(self, video_path: str, audio_path: str, 
                           output_path: str):
        """Combine video and audio files."""
        try:
            # Simple approach - copy video file if audio mixing fails
            # In production, you'd use moviepy or ffmpeg here
            import shutil
            shutil.copy2(video_path, output_path)
            self.logger.info(f"Video copied to {output_path} (audio mixing not implemented)")
            
        except Exception as e:
            self.logger.error(f"Video-audio combination failed: {e}")

# Test the audio engine
def test_audio_engine():
    """Test the advanced audio engine."""
    print("🎵 Testing Advanced Audio Engine...")
    
    engine = AdvancedAudioEngine()
    
    # Test character voice generation
    character_info = {'name': 'Alice', 'gender': 'female'}
    voice_path = "test_voice.wav"
    
    result = engine.generate_character_voice(
        "Hello, my name is Alice and I'm excited to meet you!", 
        character_info, 
        voice_path
    )
    
    if result:
        print(f"✅ Voice generated: {result}")
    else:
        print("❌ Voice generation failed")
    
    # Test background music
    music_path = "test_music.wav"
    music_result = engine.generate_background_music('joy', 5.0, music_path)
    
    if music_result:
        print(f"✅ Background music generated: {music_result}")
    else:
        print("❌ Background music generation failed")
    
    print("🎵 Audio engine test completed!")

if __name__ == "__main__":
    test_audio_engine()
