#!/usr/bin/env python3
"""
Advanced Local TTS Engine with High-Quality Neural Models

Integrates multiple state-of-the-art local TTS engines:
- Tortoise TTS: High-quality English TTS (GPU-accelerated)
- Coqui TTS: Multi-language, fast inference
- ESPnet-TTS: Research-grade speech synthesis
- espeak: Lightweight fallback
- Custom neural synthesis

100% local operation - no API dependencies
"""

import os
import sys
import subprocess
import tempfile
import logging
import json
import time
from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import soundfile as sf

# Import simplified TTS as fallback
from simplified_local_tts import SimplifiedLocalTTS, SimpleVoiceProfile

@dataclass
class AdvancedVoiceProfile:
    """Advanced voice profile with neural TTS features."""
    name: str
    gender: str = "neutral"
    age: str = "adult"  # child, teen, adult, elderly
    language: str = "en"
    accent: str = "general"
    speed: float = 1.0
    pitch: float = 1.0
    volume: float = 0.8
    emotion: str = "neutral"
    style: str = "narrative"
    quality: str = "standard"  # fast, standard, high, ultra
    voice_clone_reference: Optional[str] = None

class AdvancedLocalTTS:
    """Advanced local TTS engine with multiple high-quality backends."""
    
    def __init__(self, enable_gpu: bool = True):
        self.logger = logging.getLogger(__name__)
        self.enable_gpu = enable_gpu
        self.sample_rate = 22050
        self.temp_dir = tempfile.mkdtemp()
        
        # Initialize engines
        self.engines = self._detect_advanced_engines()
        
        # Fallback to simplified TTS
        self.fallback_tts = SimplifiedLocalTTS()
        
        # Advanced voice profiles
        self.voice_profiles = self._create_advanced_voice_profiles()
        
        # Model cache
        self.model_cache = {}
        
        self.logger.info(f"Advanced Local TTS initialized with {len(self.engines)} engines")
        if self.enable_gpu and self._has_gpu():
            self.logger.info("🚀 GPU acceleration enabled")
        else:
            self.logger.info("💻 CPU-only mode")
    
    def _detect_advanced_engines(self) -> Dict[str, Dict]:
        """Detect available advanced TTS engines."""
        engines = {}
        
        # Check Coqui TTS
        try:
            import TTS
            from TTS.api import TTS as CoquiTTS
            engines['coqui'] = {
                'available': True,
                'models': self._get_coqui_models(),
                'quality': 'high',
                'speed': 'fast',
                'languages': ['en', 'es', 'fr', 'de', 'it', 'pt', 'pl', 'tr', 'ru', 'nl', 'cs', 'ar', 'zh', 'ja']
            }
            self.logger.info("✅ Coqui TTS detected")
        except ImportError:
            engines['coqui'] = {'available': False, 'reason': 'Not installed'}
        
        # Check Tortoise TTS
        try:
            import tortoise.api
            engines['tortoise'] = {
                'available': True,
                'quality': 'ultra',
                'speed': 'slow',
                'languages': ['en'],
                'gpu_recommended': True
            }
            self.logger.info("✅ Tortoise TTS detected")
        except ImportError:
            engines['tortoise'] = {'available': False, 'reason': 'Not installed'}
        
        # Check ESPnet TTS
        try:
            import espnet2
            from espnet2.bin.tts_inference import Text2Speech
            engines['espnet'] = {
                'available': True,
                'quality': 'high',
                'speed': 'medium',
                'languages': ['en', 'ja', 'zh', 'es'],
                'models': self._get_espnet_models()
            }
            self.logger.info("✅ ESPnet TTS detected")
        except ImportError:
            engines['espnet'] = {'available': False, 'reason': 'Not installed'}
        
        # Check VITS (Variational Inference TTS)
        try:
            import vits
            engines['vits'] = {
                'available': True,
                'quality': 'high',
                'speed': 'fast',
                'languages': ['en', 'ja', 'zh']
            }
            self.logger.info("✅ VITS TTS detected")
        except ImportError:
            engines['vits'] = {'available': False, 'reason': 'Not installed'}
        
        # Always include basic engines
        engines['espeak'] = {'available': True, 'quality': 'basic', 'speed': 'very_fast'}
        engines['fallback'] = {'available': True, 'quality': 'basic', 'speed': 'very_fast'}
        
        return engines
    
    def _get_coqui_models(self) -> List[str]:
        """Get available Coqui TTS models."""
        try:
            from TTS.api import TTS
            models = TTS.list_models()
            # Filter for best models
            recommended = [
                'tts_models/en/ljspeech/tacotron2-DDC',
                'tts_models/en/ljspeech/glow-tts',
                'tts_models/en/ljspeech/speedy-speech',
                'tts_models/en/vctk/vits',
                'tts_models/multilingual/multi-dataset/your_tts'
            ]
            return [m for m in models if any(rec in m for rec in recommended)]
        except:
            return []
    
    def _get_espnet_models(self) -> List[str]:
        """Get available ESPnet models."""
        return [
            'espnet/english_male_ryanspeech',
            'espnet/english_female_ljspeech', 
            'espnet/japanese_male_jsut',
            'espnet/mandarin_female_baker'
        ]
    
    def _has_gpu(self) -> bool:
        """Check if GPU is available."""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False
    
    def _create_advanced_voice_profiles(self) -> Dict[str, AdvancedVoiceProfile]:
        """Create advanced voice profiles."""
        profiles = {}
        
        # Educational voices with different quality levels
        profiles['teacher_female_ultra'] = AdvancedVoiceProfile(
            name="Ms. Anderson", gender="female", age="adult", 
            language="en", accent="general", speed=0.9, pitch=1.1, 
            volume=0.8, emotion="calm", style="formal", quality="ultra"
        )
        
        profiles['teacher_male_ultra'] = AdvancedVoiceProfile(
            name="Mr. Thompson", gender="male", age="adult", 
            language="en", accent="general", speed=0.9, pitch=0.9, 
            volume=0.8, emotion="calm", style="formal", quality="ultra"
        )
        
        profiles['narrator_professional'] = AdvancedVoiceProfile(
            name="Professional Narrator", gender="neutral", age="adult", 
            language="en", accent="general", speed=1.0, pitch=1.0, 
            volume=0.9, emotion="neutral", style="narrative", quality="high"
        )
        
        profiles['student_enthusiastic'] = AdvancedVoiceProfile(
            name="Alex", gender="neutral", age="teen", 
            language="en", accent="general", speed=1.1, pitch=1.2, 
            volume=0.8, emotion="excited", style="conversational", quality="high"
        )
        
        profiles['expert_authoritative'] = AdvancedVoiceProfile(
            name="Dr. Roberts", gender="neutral", age="adult", 
            language="en", accent="general", speed=0.85, pitch=0.95, 
            volume=0.9, emotion="confident", style="formal", quality="ultra"
        )
        
        # Character voices
        profiles['alice_friendly'] = AdvancedVoiceProfile(
            name="Alice", gender="female", age="adult", 
            language="en", accent="general", speed=0.95, pitch=1.2, 
            volume=0.8, emotion="friendly", style="conversational", quality="high"
        )
        
        profiles['bob_confident'] = AdvancedVoiceProfile(
            name="Bob", gender="male", age="adult", 
            language="en", accent="general", speed=1.0, pitch=0.8, 
            volume=0.8, emotion="confident", style="conversational", quality="high"
        )
        
        # Multi-language voices (if engines support)
        profiles['spanish_teacher'] = AdvancedVoiceProfile(
            name="Profesora García", gender="female", age="adult", 
            language="es", accent="general", speed=0.9, pitch=1.1, 
            volume=0.8, emotion="calm", style="formal", quality="high"
        )
        
        profiles['french_narrator'] = AdvancedVoiceProfile(
            name="Narrateur", gender="male", age="adult", 
            language="fr", accent="general", speed=1.0, pitch=1.0, 
            volume=0.8, emotion="neutral", style="narrative", quality="high"
        )
        
        return profiles
    
    def synthesize_speech(self, text: str, voice_profile: Union[str, AdvancedVoiceProfile], 
                         output_path: str, quality_override: Optional[str] = None) -> Optional[str]:
        """Synthesize speech using the best available engine for the requested quality."""
        try:
            # Get voice profile
            if isinstance(voice_profile, str):
                profile = self.voice_profiles.get(voice_profile)
                if not profile:
                    # Try fallback TTS
                    return self.fallback_tts.synthesize_speech(text, voice_profile, output_path)
            else:
                profile = voice_profile
            
            # Determine quality level
            quality = quality_override or profile.quality
            
            # Clean text
            text = self._clean_text(text)
            if not text:
                return None
            
            # Select engine based on quality and language
            engine_name = self._select_best_engine(profile, quality)
            
            self.logger.info(f"Using {engine_name} engine for {quality} quality synthesis")
            
            # Synthesize with selected engine
            if engine_name == 'tortoise' and self.engines['tortoise']['available']:
                return self._synthesize_tortoise(text, profile, output_path)
            elif engine_name == 'coqui' and self.engines['coqui']['available']:
                return self._synthesize_coqui(text, profile, output_path)
            elif engine_name == 'espnet' and self.engines['espnet']['available']:
                return self._synthesize_espnet(text, profile, output_path)
            elif engine_name == 'vits' and self.engines['vits']['available']:
                return self._synthesize_vits(text, profile, output_path)
            else:
                # Fallback to simplified TTS
                simple_profile = SimpleVoiceProfile(
                    name=profile.name,
                    gender=profile.gender,
                    speed=profile.speed,
                    pitch=profile.pitch,
                    volume=profile.volume
                )
                return self.fallback_tts.synthesize_speech(text, simple_profile, output_path)
                
        except Exception as e:
            self.logger.error(f"Advanced TTS synthesis failed: {e}")
            # Try fallback
            try:
                return self.fallback_tts.synthesize_speech(text, voice_profile, output_path)
            except:
                return None
    
    def _clean_text(self, text: str) -> str:
        """Clean and prepare text for synthesis."""
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Handle common abbreviations
        replacements = {
            'AI': 'artificial intelligence',
            'ML': 'machine learning',
            'TTS': 'text to speech',
            'API': 'A P I',
            'URL': 'U R L',
            'HTML': 'H T M L',
            'CSS': 'C S S',
            'JS': 'JavaScript'
        }
        
        for abbrev, full in replacements.items():
            text = text.replace(abbrev, full)
        
        return text.strip()
    
    def _select_best_engine(self, profile: AdvancedVoiceProfile, quality: str) -> str:
        """Select the best engine based on quality requirements and language."""
        if quality == 'ultra' and profile.language == 'en':
            if self.engines['tortoise']['available']:
                return 'tortoise'
        
        if quality in ['high', 'ultra']:
            if profile.language == 'en' and self.engines['coqui']['available']:
                return 'coqui'
            elif self.engines['espnet']['available']:
                return 'espnet'
            elif self.engines['vits']['available']:
                return 'vits'
        
        if quality in ['standard', 'fast']:
            if self.engines['coqui']['available']:
                return 'coqui'
        
        # Fallback to basic engines
        return 'espeak'
    
    def _synthesize_tortoise(self, text: str, profile: AdvancedVoiceProfile, 
                           output_path: str) -> str:
        """Synthesize using Tortoise TTS (highest quality, slowest)."""
        try:
            from tortoise.api import TextToSpeech
            from tortoise.utils.audio import load_voice
            
            # Initialize Tortoise
            if 'tortoise_model' not in self.model_cache:
                self.model_cache['tortoise_model'] = TextToSpeech()
            
            tts = self.model_cache['tortoise_model']
            
            # Select voice based on profile
            voice_samples, conditioning_latents = load_voice(self._map_voice_to_tortoise(profile))
            
            # Generate audio
            gen = tts.tts_with_preset(
                text, 
                voice_samples=voice_samples, 
                conditioning_latents=conditioning_latents,
                preset='standard'  # Options: ultra_fast, fast, standard, high_quality
            )
            
            # Save audio
            import torchaudio
            torchaudio.save(output_path, gen.squeeze(0).cpu(), 24000)
            
            self.logger.info(f"✅ Tortoise TTS synthesis completed: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Tortoise TTS failed: {e}")
            raise
    
    def _synthesize_coqui(self, text: str, profile: AdvancedVoiceProfile, 
                         output_path: str) -> str:
        """Synthesize using Coqui TTS (good quality, fast)."""
        try:
            from TTS.api import TTS
            
            # Select model based on language and quality
            model_name = self._select_coqui_model(profile)
            
            # Initialize or get cached model
            cache_key = f"coqui_{model_name}"
            if cache_key not in self.model_cache:
                self.model_cache[cache_key] = TTS(model_name, gpu=self.enable_gpu and self._has_gpu())
            
            tts = self.model_cache[cache_key]
            
            # Generate audio
            if 'vits' in model_name or 'your_tts' in model_name:
                # Multi-speaker model
                tts.tts_to_file(
                    text=text,
                    file_path=output_path,
                    speaker=self._map_voice_to_coqui_speaker(profile)
                )
            else:
                # Single speaker model
                tts.tts_to_file(text=text, file_path=output_path)
            
            # Apply voice modifications
            self._apply_voice_effects(output_path, profile)
            
            self.logger.info(f"✅ Coqui TTS synthesis completed: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Coqui TTS failed: {e}")
            raise
    
    def _synthesize_espnet(self, text: str, profile: AdvancedVoiceProfile, 
                          output_path: str) -> str:
        """Synthesize using ESPnet TTS (research-grade quality)."""
        try:
            from espnet2.bin.tts_inference import Text2Speech
            
            # Select model
            model_tag = self._select_espnet_model(profile)
            
            # Initialize or get cached model
            cache_key = f"espnet_{model_tag}"
            if cache_key not in self.model_cache:
                self.model_cache[cache_key] = Text2Speech.from_pretrained(
                    model_tag=model_tag,
                    device="cuda" if self.enable_gpu and self._has_gpu() else "cpu"
                )
            
            text2speech = self.model_cache[cache_key]
            
            # Generate audio
            wav = text2speech(text)["wav"]
            
            # Save audio
            sf.write(output_path, wav.cpu().numpy(), 22050)
            
            # Apply voice modifications
            self._apply_voice_effects(output_path, profile)
            
            self.logger.info(f"✅ ESPnet TTS synthesis completed: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"ESPnet TTS failed: {e}")
            raise
    
    def _synthesize_vits(self, text: str, profile: AdvancedVoiceProfile, 
                        output_path: str) -> str:
        """Synthesize using VITS (Variational Inference TTS)."""
        try:
            # This would be implemented with a specific VITS model
            # For now, fallback to Coqui which includes VITS models
            return self._synthesize_coqui(text, profile, output_path)
            
        except Exception as e:
            self.logger.error(f"VITS TTS failed: {e}")
            raise
    
    def _map_voice_to_tortoise(self, profile: AdvancedVoiceProfile) -> str:
        """Map voice profile to Tortoise voice."""
        voice_mapping = {
            'female': 'emma',
            'male': 'tom',
            'neutral': 'alex'
        }
        return voice_mapping.get(profile.gender, 'alex')
    
    def _select_coqui_model(self, profile: AdvancedVoiceProfile) -> str:
        """Select appropriate Coqui model."""
        if profile.language == 'en':
            if profile.quality == 'ultra':
                return 'tts_models/en/vctk/vits'
            elif profile.quality == 'high':
                return 'tts_models/en/ljspeech/glow-tts'
            else:
                return 'tts_models/en/ljspeech/speedy-speech'
        elif profile.language in ['es', 'fr', 'de']:
            return 'tts_models/multilingual/multi-dataset/your_tts'
        else:
            return 'tts_models/en/ljspeech/tacotron2-DDC'
    
    def _map_voice_to_coqui_speaker(self, profile: AdvancedVoiceProfile) -> str:
        """Map voice profile to Coqui speaker."""
        # This would map to actual speaker IDs in multi-speaker models
        if profile.gender == 'female':
            return 'p225'  # Example VCTK speaker ID
        elif profile.gender == 'male':
            return 'p226'
        else:
            return 'p225'
    
    def _select_espnet_model(self, profile: AdvancedVoiceProfile) -> str:
        """Select appropriate ESPnet model."""
        if profile.language == 'en':
            if profile.gender == 'female':
                return 'espnet/english_female_ljspeech'
            else:
                return 'espnet/english_male_ryanspeech'
        elif profile.language == 'ja':
            return 'espnet/japanese_male_jsut'
        elif profile.language == 'zh':
            return 'espnet/mandarin_female_baker'
        else:
            return 'espnet/english_female_ljspeech'
    
    def _apply_voice_effects(self, audio_path: str, profile: AdvancedVoiceProfile):
        """Apply voice effects and modifications."""
        try:
            import librosa
            
            # Load audio
            y, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # Apply speed modification
            if profile.speed != 1.0:
                y = librosa.effects.time_stretch(y, rate=profile.speed)
            
            # Apply pitch modification
            if profile.pitch != 1.0:
                n_steps = (profile.pitch - 1.0) * 12
                y = librosa.effects.pitch_shift(y, sr=sr, n_steps=n_steps)
            
            # Apply emotion effects
            y = self._apply_emotion_effects(y, profile.emotion, sr)
            
            # Apply volume
            y = y * profile.volume
            
            # Normalize
            if np.max(np.abs(y)) > 0:
                y = y / np.max(np.abs(y)) * 0.95
            
            # Save modified audio
            sf.write(audio_path, y, sr)
            
        except Exception as e:
            self.logger.warning(f"Voice effects application failed: {e}")
    
    def _apply_emotion_effects(self, audio: np.ndarray, emotion: str, sr: int) -> np.ndarray:
        """Apply emotion-based audio effects."""
        try:
            if emotion == 'excited':
                # Increase brightness and add slight tremolo
                audio = self._add_brightness(audio, 0.2)
                audio = self._add_tremolo(audio, sr, 4.0, 0.05)
            elif emotion == 'calm':
                # Smooth the audio and reduce brightness
                audio = self._add_brightness(audio, -0.1)
            elif emotion == 'confident':
                # Enhance lower frequencies
                audio = self._enhance_bass(audio, sr)
            elif emotion == 'friendly':
                # Slight upward pitch variation
                audio = self._add_pitch_variation(audio, sr, 0.03)
            
            return audio
            
        except Exception as e:
            self.logger.warning(f"Emotion effects failed: {e}")
            return audio
    
    def _add_brightness(self, audio: np.ndarray, amount: float) -> np.ndarray:
        """Add brightness to audio."""
        try:
            import librosa
            return librosa.effects.preemphasis(audio, coef=amount)
        except:
            return audio
    
    def _add_tremolo(self, audio: np.ndarray, sr: int, rate: float, depth: float) -> np.ndarray:
        """Add tremolo effect."""
        t = np.arange(len(audio)) / sr
        tremolo = 1 + depth * np.sin(2 * np.pi * rate * t)
        return audio * tremolo
    
    def _enhance_bass(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """Enhance bass frequencies."""
        try:
            import librosa
            # Simple bass boost using preemphasis with negative coefficient
            return librosa.effects.preemphasis(audio, coef=-0.05)
        except:
            return audio
    
    def _add_pitch_variation(self, audio: np.ndarray, sr: int, amount: float) -> np.ndarray:
        """Add subtle pitch variation."""
        try:
            import librosa
            # Add very subtle random pitch variations
            n_steps = amount * np.random.randn() * 2
            return librosa.effects.pitch_shift(audio, sr=sr, n_steps=n_steps)
        except:
            return audio
    
    def create_voice_profile(self, name: str, **kwargs) -> AdvancedVoiceProfile:
        """Create a custom advanced voice profile."""
        return AdvancedVoiceProfile(name=name, **kwargs)
    
    def list_available_voices(self) -> List[str]:
        """List all available voice profiles."""
        return list(self.voice_profiles.keys())
    
    def get_engine_info(self) -> Dict:
        """Get detailed engine information."""
        return self.engines.copy()
    
    def get_recommendations(self, use_case: str) -> Dict[str, str]:
        """Get recommendations for voice profiles and engines based on use case."""
        recommendations = {
            'elementary_education': {
                'voice': 'student_enthusiastic',
                'quality': 'high',
                'engine': 'coqui',
                'reason': 'Clear, friendly voice with good expressiveness'
            },
            'professional_training': {
                'voice': 'expert_authoritative',
                'quality': 'ultra',
                'engine': 'tortoise',
                'reason': 'Professional, authoritative voice with highest quality'
            },
            'language_learning': {
                'voice': 'spanish_teacher',
                'quality': 'high',
                'engine': 'coqui',
                'reason': 'Native-like pronunciation with multi-language support'
            },
            'audiobook_narration': {
                'voice': 'narrator_professional',
                'quality': 'ultra',
                'engine': 'tortoise',
                'reason': 'Natural, engaging narration with human-like quality'
            },
            'quick_prototyping': {
                'voice': 'alice_friendly',
                'quality': 'standard',
                'engine': 'coqui',
                'reason': 'Fast generation with good quality'
            }
        }
        
        return recommendations.get(use_case, {
            'voice': 'narrator_professional',
            'quality': 'standard',
            'engine': 'coqui',
            'reason': 'General-purpose recommendation'
        })
    
    def benchmark_engines(self, test_text: str = "This is a benchmark test.") -> Dict[str, Dict]:
        """Benchmark available engines for speed and quality."""
        results = {}
        
        for engine_name, engine_info in self.engines.items():
            if not engine_info['available']:
                continue
            
            try:
                start_time = time.time()
                temp_output = os.path.join(self.temp_dir, f"benchmark_{engine_name}.wav")
                
                profile = self.voice_profiles['narrator_professional']
                result = self.synthesize_speech(test_text, profile, temp_output)
                
                end_time = time.time()
                
                if result and os.path.exists(result):
                    file_size = os.path.getsize(result)
                    results[engine_name] = {
                        'success': True,
                        'time_seconds': end_time - start_time,
                        'file_size_bytes': file_size,
                        'quality': engine_info.get('quality', 'unknown'),
                        'speed_rating': engine_info.get('speed', 'unknown')
                    }
                    os.remove(result)
                else:
                    results[engine_name] = {'success': False}
                    
            except Exception as e:
                results[engine_name] = {'success': False, 'error': str(e)}
        
        return results
    
    def cleanup(self):
        """Clean up temporary files and cached models."""
        try:
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            self.model_cache.clear()
        except:
            pass

# Installation helper
def install_advanced_tts_engines():
    """Install advanced TTS engines."""
    print("🚀 Installing Advanced Local TTS Engines...")
    
    engines_to_install = [
        ("Coqui TTS", "TTS"),
        ("Tortoise TTS", "tortoise-tts"),
        ("ESPnet", "espnet espnet_model_zoo"),
    ]
    
    for name, package in engines_to_install:
        print(f"\n📦 Installing {name}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"✅ {name} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ {name} installation failed: {e}")
            print("💡 You can still use the basic TTS engines")

# Test function
def test_advanced_tts():
    """Test the advanced TTS engine."""
    print("🎤 Testing Advanced Local TTS Engine...")
    
    tts = AdvancedLocalTTS()
    
    print(f"\nAvailable engines: {list(tts.engines.keys())}")
    print(f"Available voices: {tts.list_available_voices()}")
    
    # Test different quality levels
    test_cases = [
        ("Welcome to advanced local text-to-speech!", "teacher_female_ultra", "ultra"),
        ("This is high-quality neural synthesis.", "narrator_professional", "high"),
        ("Fast generation for quick prototyping.", "alice_friendly", "standard"),
    ]
    
    for i, (text, voice, quality) in enumerate(test_cases):
        print(f"\n🎵 Test {i+1}: {quality} quality with {voice}")
        output_path = f"test_advanced_{i+1}_{quality}.wav"
        
        start_time = time.time()
        result = tts.synthesize_speech(text, voice, output_path, quality_override=quality)
        end_time = time.time()
        
        if result and os.path.exists(result):
            size = os.path.getsize(result)
            duration = end_time - start_time
            print(f"✅ Success: {result} ({size} bytes, {duration:.2f}s)")
            
            # Clean up
            try:
                os.remove(result)
            except:
                pass
        else:
            print(f"❌ Failed: {voice} with {quality} quality")
    
    # Benchmark engines
    print("\n⚡ Benchmarking engines...")
    benchmark_results = tts.benchmark_engines()
    
    for engine, results in benchmark_results.items():
        if results.get('success'):
            print(f"✅ {engine}: {results['time_seconds']:.2f}s, {results.get('quality', 'unknown')} quality")
        else:
            print(f"❌ {engine}: Failed")
    
    # Get recommendations
    print("\n💡 Use case recommendations:")
    use_cases = ['elementary_education', 'professional_training', 'quick_prototyping']
    for use_case in use_cases:
        rec = tts.get_recommendations(use_case)
        print(f"  {use_case}: {rec.get('voice', 'N/A')} ({rec.get('reason', 'N/A')})")
    
    tts.cleanup()
    print("\n🎉 Advanced Local TTS Engine test completed!")

if __name__ == "__main__":
    # Check if advanced engines should be installed
    if len(sys.argv) > 1 and sys.argv[1] == "--install":
        install_advanced_tts_engines()
    else:
        test_advanced_tts()
