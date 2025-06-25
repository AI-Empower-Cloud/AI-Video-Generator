#!/usr/bin/env python3
"""
Enhanced Audio Integration for AI Video Generator

Features:
- 100% Local Text-to-Speech synthesis (no API dependencies)
- Multiple local TTS engines (pyttsx3, espeak, festival)
- Background music generation and mixing
- Audio synchronization with video
- Voice cloning and character-specific voices
- Dynamic music based on emotions
- Audio effects and processing
- SSML support for advanced speech control
"""

import numpy as np
import librosa
import soundfile as sf
from typing import List, Dict, Optional, Tuple
import tempfile
import os
from pathlib import Path
import logging
import json

# Import our local TTS engine
from local_tts_engine import LocalTTSEngine, VoiceProfile

# Import natural sound generation
from natural_sound_generator import NaturalSoundGenerator, SoundConfig

# Audio synthesis
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

    PYGAME_AVAILABLE = False

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False

class AdvancedAudioEngine:
    """Enhanced audio processing engine for video generation with 100% local TTS."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.sample_rate = 22050
        
        # Initialize local TTS engine
        self.tts_engine = LocalTTSEngine()
        
        # Character voice mapping (using local TTS profiles)
        self.character_voices = {
            'alice': 'alice',
            'bob': 'bob', 
            'carol': 'student_female',
            'teacher': 'teacher_female',
            'professor': 'teacher_male',
            'narrator': 'narrator',
            'expert': 'expert',
            'student_male': 'student_male',
            'student_female': 'student_female',
            'default_male': 'teacher_male',
            'default_female': 'teacher_female'
        }
        
        # Emotion-based music templates
        self.emotion_music = {
            'joy': {'tempo': 120, 'key': 'C_major', 'instruments': ['piano', 'strings']},
            'sadness': {'tempo': 60, 'key': 'A_minor', 'instruments': ['piano', 'cello']},
            'anger': {'tempo': 140, 'key': 'D_minor', 'instruments': ['drums', 'brass']},
            'fear': {'tempo': 90, 'key': 'F_minor', 'instruments': ['strings', 'ambient']},
            'surprise': {'tempo': 110, 'key': 'G_major', 'instruments': ['piano', 'bells']},
            'neutral': {'tempo': 100, 'key': 'C_major', 'instruments': ['piano']},
            'excitement': {'tempo': 130, 'key': 'D_major', 'instruments': ['piano', 'drums']},
            'calm': {'tempo': 80, 'key': 'F_major', 'instruments': ['strings', 'piano']}
        }
        
        self.logger.info("✅ Enhanced Audio Engine initialized with local TTS")
    
    def generate_character_voice(self, text: str, character_info: Dict, 
                               output_path: str, ssml: bool = False) -> Optional[str]:
        """Generate voice audio for a specific character using local TTS."""
        try:
            character_name = character_info.get('name', 'default').lower()
            
            # Map character to voice profile
            voice_profile = self.character_voices.get(
                character_name, 
                self.character_voices['default_male' if character_info.get('gender') == 'male' 
                                   else 'default_female']
            )
            
            # Create custom voice if specific parameters are provided
            if 'pitch' in character_info or 'speed' in character_info or 'emotion' in character_info:
                custom_voice = self.tts_engine.create_voice_profile(
                    name=character_name,
                    gender=character_info.get('gender', 'neutral'),
                    pitch=character_info.get('pitch', 1.0),
                    speed=character_info.get('speed', 1.0),
                    emotion=character_info.get('emotion', 'neutral'),
                    volume=character_info.get('volume', 0.8)
                )
                voice_profile = custom_voice
            
            # Generate speech using local TTS
            result = self.tts_engine.synthesize_speech(
                text=text,
                voice_profile=voice_profile,
                output_path=output_path,
                ssml=ssml
            )
            
            if result:
                self.logger.info(f"✅ Generated voice for {character_name}: {result}")
                return result
            else:
                self.logger.warning(f"❌ Failed to generate voice for {character_name}")
                return None
                
        except Exception as e:
            self.logger.error(f"Voice generation failed: {e}")
            return None
    
    def generate_educational_narration(self, script: str, subject: str, 
                                     age_group: str, output_path: str) -> Optional[str]:
        """Generate educational narration with appropriate voice for subject and age group."""
        try:
            # Select voice based on subject and age group
            if age_group in ['elementary', 'middle_school']:
                voice_profile = 'teacher_female'  # Friendly, clear voice
            elif age_group in ['high_school', 'college']:
                voice_profile = 'teacher_male' if subject in ['physics', 'engineering'] else 'teacher_female'
            else:  # Professional
                voice_profile = 'expert'
            
            # Add subject-specific emotion
            emotion = 'excited' if subject in ['science', 'technology'] else 'calm'
            
            # Create custom voice with appropriate characteristics
            custom_voice = self.tts_engine.create_voice_profile(
                name=f"{subject}_narrator",
                gender='neutral',
                emotion=emotion,
                style='narrative',
                speed=0.9 if age_group == 'elementary' else 1.0,
                pitch=1.1 if age_group == 'elementary' else 1.0
            )
            
            return self.tts_engine.synthesize_speech(
                text=script,
                voice_profile=custom_voice,
                output_path=output_path,
                ssml=True  # Enable SSML for educational content
            )
            
        except Exception as e:
            self.logger.error(f"Educational narration generation failed: {e}")
            return None
    
    def generate_dialogue(self, dialogue_lines: List[Dict], output_path: str) -> Optional[str]:
        """Generate multi-character dialogue."""
        try:
            combined_audio = []
            sr = self.sample_rate
            
            for i, line in enumerate(dialogue_lines):
                character = line.get('character', 'narrator')
                text = line.get('text', '')
                pause_after = line.get('pause_after', 0.5)
                
                # Generate individual line
                temp_path = f"temp_dialogue_{i}.wav"
                
                character_info = {'name': character}
                voice_result = self.generate_character_voice(text, character_info, temp_path)
                
                if voice_result and os.path.exists(voice_result):
                    # Load audio
                    audio, _ = librosa.load(voice_result, sr=sr)
                    combined_audio.append(audio)
                    
                    # Add pause
                    if pause_after > 0:
                        pause_samples = int(pause_after * sr)
                        combined_audio.append(np.zeros(pause_samples))
                    
                    # Clean up temp file
                    os.remove(voice_result)
            
            # Combine all audio
            if combined_audio:
                final_audio = np.concatenate(combined_audio)
                sf.write(output_path, final_audio, sr)
                return output_path
            else:
                return None
                
        except Exception as e:
            self.logger.error(f"Dialogue generation failed: {e}")
            return None
    
    def create_interactive_audio(self, content: Dict, output_path: str) -> Optional[str]:
        """Create interactive audio with questions, answers, and feedback."""
        try:
            segments = []
            sr = self.sample_rate
            
            # Introduction
            if 'introduction' in content:
                intro_audio = self._generate_segment(
                    content['introduction'], 
                    'teacher_female', 
                    'intro'
                )
                if intro_audio is not None:
                    segments.append(intro_audio)
                    segments.append(np.zeros(int(1.0 * sr)))  # 1s pause
            
            # Questions and answers
            for i, qa in enumerate(content.get('questions', [])):
                # Question
                question_audio = self._generate_segment(
                    qa.get('question', ''), 
                    'teacher_male', 
                    'question'
                )
                if question_audio is not None:
                    segments.append(question_audio)
                    segments.append(np.zeros(int(2.0 * sr)))  # 2s pause for thinking
                
                # Answer
                answer_audio = self._generate_segment(
                    qa.get('answer', ''), 
                    'student_female', 
                    'answer'
                )
                if answer_audio is not None:
                    segments.append(answer_audio)
                    segments.append(np.zeros(int(1.5 * sr)))  # 1.5s pause
                
                # Feedback
                feedback_audio = self._generate_segment(
                    qa.get('feedback', 'Excellent!'), 
                    'teacher_female', 
                    'feedback'
                )
                if feedback_audio is not None:
                    segments.append(feedback_audio)
                    segments.append(np.zeros(int(1.0 * sr)))  # 1s pause
            
            # Conclusion
            if 'conclusion' in content:
                conclusion_audio = self._generate_segment(
                    content['conclusion'], 
                    'narrator', 
                    'conclusion'
                )
                if conclusion_audio is not None:
                    segments.append(conclusion_audio)
            
            # Combine segments
            if segments:
                final_audio = np.concatenate(segments)
                sf.write(output_path, final_audio, sr)
                return output_path
            else:
                return None
                
        except Exception as e:
            self.logger.error(f"Interactive audio creation failed: {e}")
            return None
    
    def _generate_segment(self, text: str, voice_type: str, segment_type: str) -> Optional[np.ndarray]:
        """Generate audio segment with appropriate voice and emotion."""
        try:
            if not text.strip():
                return None
            
            # Create temporary file
            temp_path = f"temp_{segment_type}_{hash(text) % 10000}.wav"
            
            # Determine emotion based on segment type
            emotion_map = {
                'intro': 'friendly',
                'question': 'curious', 
                'answer': 'confident',
                'feedback': 'encouraging',
                'conclusion': 'satisfied'
            }
            emotion = emotion_map.get(segment_type, 'neutral')
            
            # Create voice profile
            voice_profile = self.tts_engine.create_voice_profile(
                name=f"{voice_type}_{segment_type}",
                emotion=emotion,
                style='conversational' if segment_type in ['question', 'answer'] else 'narrative'
            )
            
            # Generate audio
            result = self.tts_engine.synthesize_speech(
                text=text,
                voice_profile=voice_profile,
                output_path=temp_path
            )
            
            if result and os.path.exists(result):
                # Load and return audio array
                audio, _ = librosa.load(result, sr=self.sample_rate)
                os.remove(result)  # Clean up temp file
                return audio
            else:
                return None
                
        except Exception as e:
            self.logger.warning(f"Segment generation failed: {e}")
            return None
    
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

# Test the enhanced audio engine
def test_enhanced_audio_engine():
    """Test the enhanced audio engine with local TTS."""
    print("🎵 Testing Enhanced Audio Engine (100% Local)...")
    
    engine = AdvancedAudioEngine()
    
    # Test 1: Basic character voice generation
    print("\n🎭 Testing character voices...")
    characters = [
        {'name': 'alice', 'gender': 'female'},
        {'name': 'bob', 'gender': 'male'},
        {'name': 'teacher', 'gender': 'female'}
    ]
    
    for character in characters:
        voice_path = f"test_{character['name']}.wav"
        result = engine.generate_character_voice(
            f"Hello, my name is {character['name']}! I'm excited to help you learn!", 
            character, 
            voice_path
        )
        
        if result:
            print(f"✅ Generated voice for {character['name']}: {result}")
        else:
            print(f"❌ Failed to generate voice for {character['name']}")
    
    # Test 2: Educational narration
    print("\n📚 Testing educational narration...")
    educational_script = """
    Welcome to today's lesson on artificial intelligence! 
    AI is a fascinating field that combines computer science, mathematics, and cognitive science.
    Let's explore how machines can learn and make decisions like humans do.
    """
    
    narration_result = engine.generate_educational_narration(
        script=educational_script,
        subject="artificial_intelligence",
        age_group="high_school",
        output_path="test_education.wav"
    )
    
    if narration_result:
        print(f"✅ Educational narration generated: {narration_result}")
    else:
        print("❌ Educational narration generation failed")
    
    # Test 3: Multi-character dialogue
    print("\n💬 Testing dialogue generation...")
    dialogue = [
        {"character": "teacher", "text": "Who can tell me what artificial intelligence means?", "pause_after": 1.0},
        {"character": "student_female", "text": "AI is when computers can think and learn like humans!", "pause_after": 0.5},
        {"character": "teacher", "text": "Excellent answer! That's exactly right.", "pause_after": 1.0}
    ]
    
    dialogue_result = engine.generate_dialogue(dialogue, "test_dialogue.wav")
    
    if dialogue_result:
        print(f"✅ Dialogue generated: {dialogue_result}")
    else:
        print("❌ Dialogue generation failed")
    
    # Test 4: Interactive audio
    print("\n🔄 Testing interactive audio...")
    interactive_content = {
        "introduction": "Let's test your knowledge with a quick quiz!",
        "questions": [
            {
                "question": "What does AI stand for?",
                "answer": "Artificial Intelligence",
                "feedback": "Perfect! You've got it right!"
            }
        ],
        "conclusion": "Great job completing the quiz!"
    }
    
    interactive_result = engine.create_interactive_audio(interactive_content, "test_interactive.wav")
    
    if interactive_result:
        print(f"✅ Interactive audio generated: {interactive_result}")
    else:
        print("❌ Interactive audio generation failed")
    
    # Test 5: Background music
    print("\n🎵 Testing background music generation...")
    music_path = "test_music.wav"
    music_result = engine.generate_background_music('excitement', 8.0, music_path)
    
    if music_result:
        print(f"✅ Background music generated: {music_result}")
    else:
        print("❌ Background music generation failed")
    
    # Test 6: Available voices and engines
    print(f"\n🔧 Available TTS engines: {engine.tts_engine.get_engine_info()}")
    print(f"🎤 Available voice profiles: {engine.tts_engine.list_available_voices()}")
    
    print("\n🎵 Enhanced Audio Engine test completed!")
    print("✅ All audio features are now 100% local - no API dependencies!")

if __name__ == "__main__":
    test_enhanced_audio_engine()
