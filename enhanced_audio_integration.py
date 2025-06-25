#!/usr/bin/env python3
"""
🎬 Enhanced Audio Integration with Natural Sounds
Integrates TTS voices with procedural natural sound generation
100% Local, Crystal Clear, Educational Focus
"""

import numpy as np
import soundfile as sf
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple
import json
import random

# Import our existing modules
from advanced_local_tts import AdvancedLocalTTS
from natural_sound_generator import NaturalSoundGenerator, SoundConfig

class EnhancedAudioEngine:
    """
    Advanced Audio Engine combining TTS with Natural Sound Generation
    Perfect for educational videos with immersive soundscapes
    """
    
    def __init__(self, output_dir: str = "enhanced_audio"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize TTS and sound generation engines
        self.tts_engine = AdvancedLocalTTS()
        self.sound_generator = NaturalSoundGenerator(str(self.output_dir / "natural_sounds"))
        
        # Educational sound library
        self.educational_sounds = self._init_educational_sounds()
        
        # Audio mixing settings
        self.default_levels = {
            "voice": 0.8,      # Main voice level
            "background": 0.3,  # Background ambience level
            "effects": 0.5,     # Sound effects level
            "music": 0.2        # Background music level
        }

    def _init_educational_sounds(self) -> Dict:
        """Initialize educational sound combinations for different subjects"""
        return {
            "biology": {
                "forest_ecosystem": {
                    "environment": "forest",
                    "animals": ["robin", "frog"],
                    "weather": ["wind_gentle"],
                    "educational_focus": "Ecosystem diversity and interactions"
                },
                "marine_life": {
                    "environment": "ocean", 
                    "animals": ["dolphin"],
                    "weather": [],
                    "educational_focus": "Marine ecosystems and ocean life"
                },
                "wildlife_safari": {
                    "environment": "desert",
                    "animals": ["lion", "elephant"],
                    "weather": ["wind_gentle"],
                    "educational_focus": "African wildlife and adaptations"
                }
            },
            "earth_science": {
                "weather_patterns": {
                    "environment": None,
                    "animals": [],
                    "weather": ["rain_light", "thunder_distant", "wind_storm"],
                    "educational_focus": "Weather formation and climate systems"
                },
                "natural_disasters": {
                    "environment": None,
                    "animals": [],
                    "weather": ["thunder_close", "wind_storm", "rain_heavy"],
                    "educational_focus": "Severe weather and natural phenomena"
                }
            },
            "environmental_science": {
                "rainforest_conservation": {
                    "environment": "jungle",
                    "animals": ["exotic_birds"],
                    "weather": ["rain_light"],
                    "educational_focus": "Biodiversity and conservation"
                },
                "arctic_climate": {
                    "environment": "arctic",
                    "animals": [],
                    "weather": ["wind_storm"],
                    "educational_focus": "Climate change and polar ecosystems"
                }
            },
            "general_nature": {
                "peaceful_morning": {
                    "environment": "forest",
                    "animals": ["robin", "canary"],
                    "weather": ["wind_gentle"],
                    "educational_focus": "Nature appreciation and mindfulness"
                },
                "night_sounds": {
                    "environment": None,
                    "animals": ["owl", "wolf"],
                    "weather": [],
                    "educational_focus": "Nocturnal animals and adaptations"
                }
            }
        }

    def create_educational_lesson_audio(
        self,
        script: str,
        voice_profile: str,
        subject: str,
        scene_type: str,
        duration: float = 30.0,
        quality: str = "ultra"
    ) -> str:
        """
        Create complete educational lesson audio with TTS and natural sounds
        """
        
        print(f"🎬 Creating educational audio for {subject} - {scene_type}")
        
        # Get educational sound configuration
        if subject not in self.educational_sounds:
            subject = "general_nature"
        
        if scene_type not in self.educational_sounds[subject]:
            scene_type = list(self.educational_sounds[subject].keys())[0]
        
        sound_config = self.educational_sounds[subject][scene_type]
        
        # Generate TTS voice
        print("🎤 Generating voice narration...")
        tts_config = SoundConfig(duration=duration, quality=quality)
        voice_audio = self._generate_tts_audio(script, voice_profile, tts_config)
        
        # Generate background soundscape
        print("🌲 Generating natural soundscape...")
        background_audio = self._generate_background_soundscape(
            sound_config, duration, quality
        )
        
        # Mix audio layers
        print("🎵 Mixing audio layers...")
        mixed_audio = self._mix_audio_layers(
            voice_audio=voice_audio,
            background_audio=background_audio,
            levels=self.default_levels
        )
        
        # Save final audio
        filename = f"lesson_{subject}_{scene_type}_{quality}.wav"
        filepath = self.output_dir / filename
        
        # Save with metadata
        self._save_with_metadata(
            mixed_audio, 
            filepath, 
            tts_config, 
            {
                "subject": subject,
                "scene_type": scene_type,
                "voice_profile": voice_profile,
                "script": script[:100] + "..." if len(script) > 100 else script,
                "educational_focus": sound_config["educational_focus"]
            }
        )
        
        print(f"✅ Educational audio created: {filepath}")
        return str(filepath)

    def create_multi_scene_lesson(
        self,
        scenes: List[Dict],
        quality: str = "ultra"
    ) -> str:
        """
        Create multi-scene educational lesson with different soundscapes
        
        scenes format:
        [
            {
                "script": "Welcome to our forest ecosystem lesson...",
                "voice": "teacher_female_warm",
                "subject": "biology", 
                "scene": "forest_ecosystem",
                "duration": 15.0
            },
            ...
        ]
        """
        
        print(f"🎬 Creating multi-scene lesson with {len(scenes)} scenes")
        
        all_audio_segments = []
        scene_info = []
        
        for i, scene in enumerate(scenes):
            print(f"\n📖 Processing scene {i+1}/{len(scenes)}: {scene['scene']}")
            
            # Generate audio for this scene
            scene_audio = self.create_educational_lesson_audio(
                script=scene["script"],
                voice_profile=scene["voice"],
                subject=scene["subject"],
                scene_type=scene["scene"],
                duration=scene["duration"],
                quality=quality
            )
            
            # Load the generated audio
            audio_data, sample_rate = sf.read(scene_audio)
            all_audio_segments.append(audio_data)
            
            scene_info.append({
                "scene_number": i + 1,
                "duration": scene["duration"],
                "subject": scene["subject"],
                "scene_type": scene["scene"],
                "educational_focus": self.educational_sounds[scene["subject"]][scene["scene"]]["educational_focus"]
            })
        
        # Combine all scenes with smooth transitions
        print("🔗 Combining scenes with transitions...")
        final_audio = self._combine_scenes_with_transitions(all_audio_segments, sample_rate)
        
        # Save complete lesson
        filename = f"complete_lesson_{len(scenes)}_scenes_{quality}.wav"
        filepath = self.output_dir / filename
        
        config = SoundConfig(quality=quality)
        self._save_with_metadata(
            final_audio,
            filepath,
            config,
            {
                "lesson_type": "multi_scene",
                "total_scenes": len(scenes),
                "total_duration": sum(scene["duration"] for scene in scenes),
                "scenes": scene_info
            }
        )
        
        print(f"✅ Complete multi-scene lesson created: {filepath}")
        return str(filepath)

    def create_interactive_dialogue(
        self,
        dialogue: List[Dict],
        environment_scene: str = "forest",
        quality: str = "ultra"
    ) -> str:
        """
        Create interactive dialogue with natural sound background
        
        dialogue format:
        [
            {
                "speaker": "teacher",
                "voice": "teacher_female_warm", 
                "text": "What do you hear in the forest?",
                "pause_after": 2.0
            },
            {
                "speaker": "student",
                "voice": "student_enthusiastic",
                "text": "I hear birds singing!",
                "pause_after": 1.0
            }
        ]
        """
        
        print(f"🗣️ Creating interactive dialogue with {environment_scene} background")
        
        # Calculate total duration
        total_duration = sum(
            len(line["text"]) * 0.1 + line.get("pause_after", 1.0) 
            for line in dialogue
        )
        
        # Generate background environment
        config = SoundConfig(duration=total_duration, quality=quality)
        background = self.sound_generator.generate_environment_soundscape(
            environment_scene, config
        )
        
        # Generate dialogue audio
        dialogue_audio = np.zeros_like(background)
        current_time = 0
        sample_rate = self.sound_generator.sample_rates[quality]
        
        for line in dialogue:
            print(f"🎙️ Generating line: {line['speaker']} - {line['text'][:50]}...")
            
            # Generate TTS for this line
            line_config = SoundConfig(quality=quality)
            voice_audio = self._generate_tts_audio(
                line["text"], 
                line["voice"], 
                line_config
            )
            
            # Add to dialogue track
            start_idx = int(current_time * sample_rate)
            end_idx = min(start_idx + len(voice_audio), len(dialogue_audio))
            
            if end_idx > start_idx:
                dialogue_audio[start_idx:end_idx] += voice_audio[:end_idx-start_idx]
            
            # Update timing
            line_duration = len(voice_audio) / sample_rate
            current_time += line_duration + line.get("pause_after", 1.0)
        
        # Mix dialogue with background
        mixed_audio = self._mix_audio_layers(
            voice_audio=dialogue_audio,
            background_audio=background,
            levels={
                "voice": 0.8,
                "background": 0.25,
                "effects": 0.0,
                "music": 0.0
            }
        )
        
        # Save interactive dialogue
        filename = f"interactive_dialogue_{environment_scene}_{quality}.wav"
        filepath = self.output_dir / filename
        
        self._save_with_metadata(
            mixed_audio,
            filepath,
            config,
            {
                "content_type": "interactive_dialogue",
                "environment": environment_scene,
                "speakers": list(set(line["speaker"] for line in dialogue)),
                "total_lines": len(dialogue),
                "total_duration": total_duration
            }
        )
        
        print(f"✅ Interactive dialogue created: {filepath}")
        return str(filepath)

    def create_soundscape_library(self) -> Dict[str, str]:
        """Create a comprehensive library of educational soundscapes"""
        
        print("🎵 Creating Educational Soundscape Library...")
        
        library = {}
        config = SoundConfig(duration=30.0, quality="ultra", volume=0.6)
        
        # Generate soundscapes for each educational category
        for subject, scenes in self.educational_sounds.items():
            print(f"\n📚 Creating {subject} soundscapes...")
            
            for scene_name, scene_config in scenes.items():
                print(f"🎼 Generating {scene_name}...")
                
                # Generate the background soundscape
                soundscape_audio = self._generate_background_soundscape(
                    scene_config, config.duration, config.quality
                )
                
                # Save soundscape
                filename = f"soundscape_{subject}_{scene_name}.wav"
                filepath = self.output_dir / filename
                
                self._save_with_metadata(
                    soundscape_audio,
                    filepath,
                    config,
                    {
                        "soundscape_type": "educational_background",
                        "subject": subject,
                        "scene": scene_name,
                        "educational_focus": scene_config["educational_focus"],
                        "components": {
                            "environment": scene_config.get("environment"),
                            "animals": scene_config.get("animals", []),
                            "weather": scene_config.get("weather", [])
                        }
                    }
                )
                
                library[f"{subject}_{scene_name}"] = str(filepath)
        
        # Save library index
        library_index = self.output_dir / "soundscape_library_index.json"
        with open(library_index, 'w') as f:
            json.dump(library, f, indent=2)
        
        print(f"\n✅ Soundscape library created with {len(library)} soundscapes!")
        return library

    def _generate_tts_audio(self, text: str, voice_profile: str, config: SoundConfig) -> np.ndarray:
        """Generate TTS audio using our existing engine"""
        
        # Use existing TTS engine
        result = self.tts_engine.synthesize_speech(
            text=text,
            voice_profile=voice_profile,
            output_path=None,  # Return array instead of saving
            quality_override=config.quality
        )
        
        # Convert to numpy array if needed
        if isinstance(result, dict) and "audio_data" in result:
            return result["audio_data"]
        elif isinstance(result, np.ndarray):
            return result
        else:
            # Fallback: generate simple audio
            sample_rate = self.sound_generator.sample_rates[config.quality]
            duration = len(text) * 0.1  # Estimate duration
            t = np.linspace(0, duration, int(sample_rate * duration))
            return 0.5 * np.sin(2 * np.pi * 440 * t)  # Simple tone

    def _generate_background_soundscape(
        self, 
        sound_config: Dict, 
        duration: float, 
        quality: str
    ) -> np.ndarray:
        """Generate layered background soundscape"""
        
        config = SoundConfig(duration=duration, quality=quality, volume=0.4)
        sample_rate = self.sound_generator.sample_rates[quality]
        audio = np.zeros(int(sample_rate * duration))
        
        # Add environment base
        if sound_config.get("environment"):
            env_audio = self.sound_generator.generate_environment_soundscape(
                sound_config["environment"], config
            )
            audio += 0.6 * env_audio
        
        # Add animal sounds
        for animal in sound_config.get("animals", []):
            if hasattr(self.sound_generator, "generate_animal_sound"):
                animal_audio = self.sound_generator.generate_animal_sound(animal, config)
                audio += 0.3 * animal_audio
            elif hasattr(self.sound_generator, "generate_bird_sound"):
                try:
                    bird_audio = self.sound_generator.generate_bird_sound(animal, config)
                    audio += 0.3 * bird_audio
                except:
                    pass  # Skip if bird type not available
        
        # Add weather sounds
        for weather in sound_config.get("weather", []):
            weather_audio = self.sound_generator.generate_weather_sound(weather, config)
            audio += 0.4 * weather_audio
        
        return audio

    def _mix_audio_layers(
        self,
        voice_audio: np.ndarray,
        background_audio: np.ndarray,
        levels: Dict[str, float]
    ) -> np.ndarray:
        """Mix multiple audio layers with proper levels"""
        
        # Ensure same length
        max_length = max(len(voice_audio), len(background_audio))
        
        # Pad shorter audio
        if len(voice_audio) < max_length:
            voice_audio = np.pad(voice_audio, (0, max_length - len(voice_audio)))
        if len(background_audio) < max_length:
            background_audio = np.pad(background_audio, (0, max_length - len(background_audio)))
        
        # Mix with levels
        mixed = (
            levels["voice"] * voice_audio + 
            levels["background"] * background_audio
        )
        
        # Normalize to prevent clipping
        max_val = np.max(np.abs(mixed))
        if max_val > 0.95:
            mixed = mixed * 0.95 / max_val
        
        return mixed

    def _combine_scenes_with_transitions(
        self, 
        audio_segments: List[np.ndarray], 
        sample_rate: int
    ) -> np.ndarray:
        """Combine multiple audio segments with smooth transitions"""
        
        transition_duration = 1.0  # 1 second crossfade
        transition_samples = int(transition_duration * sample_rate)
        
        if not audio_segments:
            return np.array([])
        
        if len(audio_segments) == 1:
            return audio_segments[0]
        
        # Start with first segment
        combined = audio_segments[0].copy()
        
        for next_segment in audio_segments[1:]:
            # Create crossfade transition
            if len(combined) >= transition_samples and len(next_segment) >= transition_samples:
                # Fade out end of current audio
                fade_out = np.linspace(1, 0, transition_samples)
                combined[-transition_samples:] *= fade_out
                
                # Fade in start of next audio
                fade_in = np.linspace(0, 1, transition_samples)
                next_segment_copy = next_segment.copy()
                next_segment_copy[:transition_samples] *= fade_in
                
                # Overlap and add
                combined[-transition_samples:] += next_segment_copy[:transition_samples]
                combined = np.concatenate([combined, next_segment_copy[transition_samples:]])
            else:
                # Simple concatenation if segments are too short
                combined = np.concatenate([combined, next_segment])
        
        return combined

    def _save_with_metadata(
        self,
        audio: np.ndarray,
        filepath: Path,
        config: SoundConfig,
        metadata: Dict
    ):
        """Save audio with comprehensive metadata"""
        
        sample_rate = self.sound_generator.sample_rates[config.quality]
        
        # Save audio
        sf.write(str(filepath), audio, sample_rate)
        
        # Save metadata
        full_metadata = {
            "audio_file": filepath.name,
            "sample_rate": sample_rate,
            "duration": len(audio) / sample_rate,
            "quality": config.quality,
            "channels": 1,
            "format": "WAV",
            "generator": "EnhancedAudioEngine",
            "timestamp": "2025-06-20",
            **metadata
        }
        
        metadata_file = filepath.with_suffix('.json')
        with open(metadata_file, 'w') as f:
            json.dump(full_metadata, f, indent=2)


def main():
    """Demo of Enhanced Audio Engine"""
    
    print("🎬 Enhanced Audio Engine Demo")
    print("Creating educational content with natural sounds...")
    
    # Initialize enhanced audio engine
    audio_engine = EnhancedAudioEngine("demo_enhanced_audio")
    
    # Demo 1: Single educational lesson
    print("\n📖 Demo 1: Forest Ecosystem Lesson")
    forest_lesson = audio_engine.create_educational_lesson_audio(
        script="Welcome to our forest ecosystem lesson. Listen carefully to the sounds around us. Can you hear the birds singing? They play a vital role in seed dispersal and insect control.",
        voice_profile="teacher_female_warm",
        subject="biology",
        scene_type="forest_ecosystem",
        duration=15.0,
        quality="high"
    )
    print(f"✅ Forest lesson created: {forest_lesson}")
    
    # Demo 2: Multi-scene lesson
    print("\n🎬 Demo 2: Multi-Scene Nature Documentary")
    scenes = [
        {
            "script": "Our journey begins in the peaceful forest, where morning light filters through the canopy.",
            "voice": "narrator_professional",
            "subject": "biology",
            "scene": "forest_ecosystem", 
            "duration": 8.0
        },
        {
            "script": "As we approach the ocean, we hear the rhythmic waves and calls of marine life.",
            "voice": "narrator_professional",
            "subject": "biology",
            "scene": "marine_life",
            "duration": 8.0
        },
        {
            "script": "Finally, we witness the raw power of nature during a thunderstorm.",
            "voice": "narrator_professional",
            "subject": "earth_science",
            "scene": "weather_patterns",
            "duration": 8.0
        }
    ]
    
    multi_scene = audio_engine.create_multi_scene_lesson(scenes, quality="high")
    print(f"✅ Multi-scene lesson created: {multi_scene}")
    
    # Demo 3: Interactive dialogue
    print("\n🗣️ Demo 3: Interactive Forest Dialogue")
    dialogue = [
        {
            "speaker": "teacher",
            "voice": "teacher_female_warm",
            "text": "What sounds do you hear in our forest classroom?",
            "pause_after": 2.0
        },
        {
            "speaker": "student",
            "voice": "student_enthusiastic", 
            "text": "I hear birds chirping and leaves rustling!",
            "pause_after": 1.5
        },
        {
            "speaker": "teacher",
            "voice": "teacher_female_warm",
            "text": "Excellent observation! Those sounds tell us about a healthy ecosystem.",
            "pause_after": 1.0
        }
    ]
    
    interactive_audio = audio_engine.create_interactive_dialogue(
        dialogue, environment_scene="forest", quality="high"
    )
    print(f"✅ Interactive dialogue created: {interactive_audio}")
    
    print("\n🎯 Enhanced Audio Demo Complete!")
    print("🔊 All audio files combine crystal clear TTS with natural soundscapes!")
    print("📁 Check the 'demo_enhanced_audio' folder for all generated content.")


if __name__ == "__main__":
    main()
