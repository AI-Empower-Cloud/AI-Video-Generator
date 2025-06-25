#!/usr/bin/env python3
"""
🎵 Natural Sound Generator - Crystal Clear Environmental Audio
Advanced procedural audio synthesis for educational videos
100% Local, No API Dependencies, Professional Quality
"""

import numpy as np
import scipy.signal as signal
import scipy.io.wavfile as wavfile
import librosa
import soundfile as sf
import random
import os
from typing import Dict, List, Tuple, Optional, Union
import json
from dataclasses import dataclass
from pathlib import Path

@dataclass
class SoundConfig:
    """Configuration for natural sound generation"""
    sample_rate: int = 48000  # Professional quality
    duration: float = 10.0    # Default duration in seconds
    volume: float = 0.7       # Default volume level
    fade_in: float = 0.5      # Fade in duration
    fade_out: float = 0.5     # Fade out duration
    loop: bool = False        # Whether sound should loop
    quality: str = "ultra"    # ultra, high, standard, fast

class NaturalSoundGenerator:
    """
    Advanced Natural Sound Generator
    Creates crystal clear birds, animals, weather, and environmental sounds
    """
    
    def __init__(self, output_dir: str = "natural_sounds"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Professional audio specifications
        self.sample_rates = {
            "ultra": 48000,
            "high": 44100,
            "standard": 22050,
            "fast": 16000
        }
        
        # Sound libraries for educational content
        self.bird_sounds = self._init_bird_sounds()
        self.animal_sounds = self._init_animal_sounds()
        self.weather_sounds = self._init_weather_sounds()
        self.environment_sounds = self._init_environment_sounds()
        
    def _init_bird_sounds(self) -> Dict:
        """Initialize bird sound parameters for procedural generation"""
        return {
            "robin": {
                "base_freq": 2000,
                "freq_range": (1500, 3000),
                "chirp_pattern": "cheerful",
                "duration_range": (0.2, 0.8),
                "pause_range": (0.1, 0.5),
                "harmonics": [1, 2, 3],
                "educational_note": "Common backyard bird, territorial songs"
            },
            "eagle": {
                "base_freq": 800,
                "freq_range": (600, 1200),
                "chirp_pattern": "powerful",
                "duration_range": (1.0, 2.5),
                "pause_range": (0.5, 2.0),
                "harmonics": [1, 1.5, 2],
                "educational_note": "Birds of prey, hunting calls"
            },
            "canary": {
                "base_freq": 3000,
                "freq_range": (2500, 4000),
                "chirp_pattern": "melodic",
                "duration_range": (0.1, 0.4),
                "pause_range": (0.05, 0.2),
                "harmonics": [1, 2, 3, 4],
                "educational_note": "Domesticated songbird, complex melodies"
            },
            "owl": {
                "base_freq": 400,
                "freq_range": (200, 800),
                "chirp_pattern": "haunting",
                "duration_range": (0.5, 1.5),
                "pause_range": (1.0, 3.0),
                "harmonics": [1, 1.5],
                "educational_note": "Nocturnal hunter, silent flight adaptations"
            },
            "crow": {
                "base_freq": 1000,
                "freq_range": (600, 1500),
                "chirp_pattern": "harsh",
                "duration_range": (0.3, 0.8),
                "pause_range": (0.2, 1.0),
                "harmonics": [1, 2],
                "educational_note": "Highly intelligent, social communication"
            }
        }
    
    def _init_animal_sounds(self) -> Dict:
        """Initialize animal sound parameters"""
        return {
            "lion": {
                "base_freq": 150,
                "freq_range": (80, 300),
                "pattern": "roar",
                "duration_range": (2.0, 5.0),
                "intensity": "powerful",
                "educational_note": "Alpha predator, territorial roars audible for miles"
            },
            "elephant": {
                "base_freq": 20,
                "freq_range": (10, 100),
                "pattern": "trumpet",
                "duration_range": (1.5, 4.0),
                "intensity": "deep",
                "educational_note": "Infrasonic communication, long-distance social calls"
            },
            "wolf": {
                "base_freq": 300,
                "freq_range": (200, 800),
                "pattern": "howl",
                "duration_range": (3.0, 8.0),
                "intensity": "haunting",
                "educational_note": "Pack communication, territorial marking"
            },
            "dolphin": {
                "base_freq": 8000,
                "freq_range": (2000, 20000),
                "pattern": "clicks",
                "duration_range": (0.1, 0.3),
                "intensity": "rapid",
                "educational_note": "Echolocation, sophisticated marine intelligence"
            },
            "frog": {
                "base_freq": 1000,
                "freq_range": (500, 2000),
                "pattern": "ribbit",
                "duration_range": (0.3, 0.8),
                "intensity": "rhythmic",
                "educational_note": "Mating calls, amphibian life cycles"
            }
        }
    
    def _init_weather_sounds(self) -> Dict:
        """Initialize weather sound parameters"""
        return {
            "rain_light": {
                "droplet_freq": 200,
                "intensity": 0.3,
                "droplet_size": "small",
                "surface": "leaves",
                "educational_note": "Water cycle, precipitation formation"
            },
            "rain_heavy": {
                "droplet_freq": 800,
                "intensity": 0.8,
                "droplet_size": "large",
                "surface": "pavement",
                "educational_note": "Storm systems, weather patterns"
            },
            "thunder_distant": {
                "rumble_freq": 30,
                "intensity": 0.5,
                "duration": 3.0,
                "distance": "far",
                "educational_note": "Lightning formation, sound vs light speed"
            },
            "thunder_close": {
                "rumble_freq": 20,
                "intensity": 0.9,
                "duration": 2.0,
                "distance": "near",
                "educational_note": "Electrical discharge, storm safety"
            },
            "wind_gentle": {
                "base_freq": 100,
                "intensity": 0.4,
                "turbulence": "smooth",
                "environment": "trees",
                "educational_note": "Air pressure, atmospheric movement"
            },
            "wind_storm": {
                "base_freq": 50,
                "intensity": 0.9,
                "turbulence": "chaotic",
                "environment": "open",
                "educational_note": "Severe weather, wind power generation"
            }
        }
    
    def _init_environment_sounds(self) -> Dict:
        """Initialize environmental soundscape parameters"""
        return {
            "forest": {
                "base_sounds": ["birds", "wind", "leaves"],
                "density": "rich",
                "time_of_day": "day",
                "educational_note": "Ecosystem diversity, forest conservation"
            },
            "ocean": {
                "wave_freq": 0.1,
                "wave_intensity": 0.6,
                "foam": True,
                "depth": "deep",
                "educational_note": "Marine ecosystems, ocean currents"
            },
            "jungle": {
                "base_sounds": ["exotic_birds", "insects", "rain"],
                "density": "dense",
                "humidity": "high",
                "educational_note": "Biodiversity hotspots, rainforest climates"
            },
            "desert": {
                "base_sounds": ["wind", "sparse_insects"],
                "density": "sparse",
                "temperature": "hot",
                "educational_note": "Adaptation to extreme environments"
            },
            "arctic": {
                "base_sounds": ["wind", "ice_cracking"],
                "density": "minimal",
                "temperature": "cold",
                "educational_note": "Climate change effects, polar adaptations"
            }
        }

    def generate_bird_sound(self, bird_type: str, config: SoundConfig) -> np.ndarray:
        """Generate realistic bird sounds using procedural synthesis"""
        
        if bird_type not in self.bird_sounds:
            raise ValueError(f"Bird type '{bird_type}' not available")
        
        bird_config = self.bird_sounds[bird_type]
        sample_rate = self.sample_rates[config.quality]
        duration = config.duration
        
        # Generate time array
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = np.zeros_like(t)
        
        # Generate chirp patterns
        current_time = 0
        while current_time < duration:
            # Chirp duration and frequency
            chirp_duration = random.uniform(*bird_config["duration_range"])
            chirp_end_time = min(current_time + chirp_duration, duration)
            
            # Frequency modulation for natural variation
            base_freq = bird_config["base_freq"]
            freq_variation = random.uniform(*bird_config["freq_range"])
            
            # Generate chirp
            chirp_t = t[(t >= current_time) & (t <= chirp_end_time)]
            if len(chirp_t) > 0:
                # Primary frequency with harmonics
                chirp_audio = np.zeros_like(chirp_t)
                for harmonic in bird_config["harmonics"]:
                    freq = freq_variation * harmonic
                    amplitude = 1.0 / harmonic  # Natural harmonic decay
                    
                    # Add frequency modulation for realism
                    fm_freq = freq + 50 * np.sin(2 * np.pi * 5 * chirp_t)
                    chirp_audio += amplitude * np.sin(2 * np.pi * fm_freq * chirp_t)
                
                # Apply envelope for natural attack and decay
                envelope = self._create_chirp_envelope(len(chirp_t), bird_config["chirp_pattern"])
                chirp_audio *= envelope
                
                # Add to main audio
                start_idx = int(current_time * sample_rate)
                end_idx = start_idx + len(chirp_audio)
                if end_idx <= len(audio):
                    audio[start_idx:end_idx] += chirp_audio
            
            # Pause between chirps
            pause_duration = random.uniform(*bird_config["pause_range"])
            current_time = chirp_end_time + pause_duration
        
        # Apply final processing
        audio = self._apply_audio_processing(audio, config)
        
        return audio

    def generate_animal_sound(self, animal_type: str, config: SoundConfig) -> np.ndarray:
        """Generate realistic animal sounds"""
        
        if animal_type not in self.animal_sounds:
            raise ValueError(f"Animal type '{animal_type}' not available")
        
        animal_config = self.animal_sounds[animal_type]
        sample_rate = self.sample_rates[config.quality]
        duration = config.duration
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        if animal_config["pattern"] == "roar":
            audio = self._generate_roar(t, animal_config)
        elif animal_config["pattern"] == "howl":
            audio = self._generate_howl(t, animal_config)
        elif animal_config["pattern"] == "trumpet":
            audio = self._generate_trumpet(t, animal_config)
        elif animal_config["pattern"] == "clicks":
            audio = self._generate_clicks(t, animal_config, sample_rate)
        elif animal_config["pattern"] == "ribbit":
            audio = self._generate_ribbit(t, animal_config)
        else:
            # Generic animal sound
            audio = self._generate_generic_animal_sound(t, animal_config)
        
        audio = self._apply_audio_processing(audio, config)
        return audio

    def generate_weather_sound(self, weather_type: str, config: SoundConfig) -> np.ndarray:
        """Generate realistic weather sounds"""
        
        if weather_type not in self.weather_sounds:
            raise ValueError(f"Weather type '{weather_type}' not available")
        
        weather_config = self.weather_sounds[weather_type]
        sample_rate = self.sample_rates[config.quality]
        duration = config.duration
        
        if "rain" in weather_type:
            audio = self._generate_rain(duration, sample_rate, weather_config)
        elif "thunder" in weather_type:
            audio = self._generate_thunder(duration, sample_rate, weather_config)
        elif "wind" in weather_type:
            audio = self._generate_wind(duration, sample_rate, weather_config)
        else:
            raise ValueError(f"Weather pattern not implemented: {weather_type}")
        
        audio = self._apply_audio_processing(audio, config)
        return audio

    def generate_environment_soundscape(self, environment: str, config: SoundConfig) -> np.ndarray:
        """Generate layered environmental soundscapes"""
        
        if environment not in self.environment_sounds:
            raise ValueError(f"Environment '{environment}' not available")
        
        env_config = self.environment_sounds[environment]
        sample_rate = self.sample_rates[config.quality]
        duration = config.duration
        
        # Create base soundscape
        audio = np.zeros(int(sample_rate * duration))
        
        if environment == "forest":
            audio += 0.4 * self._generate_forest_ambience(duration, sample_rate)
            audio += 0.3 * self.generate_bird_sound("robin", config)
            audio += 0.2 * self.generate_weather_sound("wind_gentle", config)
            
        elif environment == "ocean":
            audio += 0.8 * self._generate_ocean_waves(duration, sample_rate, env_config)
            audio += 0.1 * self._generate_seagulls(duration, sample_rate)
            
        elif environment == "jungle":
            audio += 0.5 * self._generate_jungle_ambience(duration, sample_rate)
            audio += 0.3 * self.generate_weather_sound("rain_light", config)
            audio += 0.2 * self._generate_exotic_birds(duration, sample_rate)
            
        elif environment == "desert":
            audio += 0.7 * self.generate_weather_sound("wind_gentle", config)
            audio += 0.2 * self._generate_desert_insects(duration, sample_rate)
            
        elif environment == "arctic":
            audio += 0.8 * self.generate_weather_sound("wind_storm", config)
            audio += 0.1 * self._generate_ice_sounds(duration, sample_rate)
        
        audio = self._apply_audio_processing(audio, config)
        return audio

    def _generate_rain(self, duration: float, sample_rate: int, config: Dict) -> np.ndarray:
        """Generate realistic rain sounds"""
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = np.zeros_like(t)
        
        # Generate individual raindrops
        droplet_freq = config["droplet_freq"]
        intensity = config["intensity"]
        
        for _ in range(int(droplet_freq * duration)):
            # Random droplet timing
            drop_time = random.uniform(0, duration)
            drop_idx = int(drop_time * sample_rate)
            
            if drop_idx < len(audio) - 100:
                # Generate droplet impact
                droplet_duration = 0.01  # 10ms droplet
                droplet_samples = int(droplet_duration * sample_rate)
                
                # Droplet sound with natural frequency content
                drop_t = np.linspace(0, droplet_duration, droplet_samples)
                droplet = intensity * np.random.normal(0, 0.1, droplet_samples)
                
                # Apply droplet envelope
                envelope = np.exp(-drop_t * 50)  # Quick decay
                droplet *= envelope
                
                # Add to main audio
                end_idx = min(drop_idx + len(droplet), len(audio))
                audio[drop_idx:end_idx] += droplet[:end_idx-drop_idx]
        
        # Add continuous rain background
        background = intensity * 0.1 * np.random.normal(0, 0.05, len(audio))
        
        # Filter for rain-like frequency content
        sos = signal.butter(6, [500, 8000], btype='band', fs=sample_rate, output='sos')
        background = signal.sosfilt(sos, background)
        
        audio += background
        return audio

    def _generate_thunder(self, duration: float, sample_rate: int, config: Dict) -> np.ndarray:
        """Generate realistic thunder sounds"""
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # Thunder rumble - low frequency content
        rumble_freq = config["rumble_freq"]
        intensity = config["intensity"]
        
        # Generate rumble with multiple frequency components
        audio = np.zeros_like(t)
        
        # Multiple frequency layers for realistic thunder
        frequencies = [rumble_freq, rumble_freq * 1.5, rumble_freq * 2.3, rumble_freq * 3.1]
        amplitudes = [1.0, 0.7, 0.4, 0.2]
        
        for freq, amp in zip(frequencies, amplitudes):
            # Add frequency modulation for natural variation
            fm_signal = freq + 10 * np.sin(2 * np.pi * 0.5 * t)
            layer = amp * intensity * np.sin(2 * np.pi * fm_signal * t)
            
            # Add some noise for realism
            noise = 0.1 * np.random.normal(0, 0.1, len(t))
            layer += noise
            
            audio += layer
        
        # Apply thunder envelope (quick attack, slow decay)
        envelope = np.exp(-t * 0.5) * (1 + 0.5 * np.sin(2 * np.pi * 2 * t))
        audio *= envelope
        
        return audio

    def _generate_wind(self, duration: float, sample_rate: int, config: Dict) -> np.ndarray:
        """Generate realistic wind sounds"""
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # Generate wind as filtered noise
        base_noise = np.random.normal(0, config["intensity"], len(t))
        
        # Filter for wind-like characteristics
        if config["turbulence"] == "smooth":
            # Gentle wind - higher frequency content
            sos = signal.butter(4, [100, 2000], btype='band', fs=sample_rate, output='sos')
        else:
            # Storm wind - broader frequency range
            sos = signal.butter(4, [50, 5000], btype='band', fs=sample_rate, output='sos')
        
        wind = signal.sosfilt(sos, base_noise)
        
        # Add gusts and variations
        gust_envelope = 1 + 0.3 * np.sin(2 * np.pi * 0.2 * t) + 0.2 * np.sin(2 * np.pi * 0.7 * t)
        wind *= gust_envelope
        
        return wind

    def _create_chirp_envelope(self, length: int, pattern: str) -> np.ndarray:
        """Create natural chirp envelopes based on bird patterns"""
        
        t = np.linspace(0, 1, length)
        
        if pattern == "cheerful":
            # Quick attack, moderate decay
            envelope = np.exp(-t * 2) * (1 + 0.5 * np.sin(2 * np.pi * 10 * t))
        elif pattern == "powerful":
            # Strong attack, slow decay
            envelope = np.exp(-t * 1) * (t < 0.8)
        elif pattern == "melodic":
            # Smooth attack and decay
            envelope = np.sin(np.pi * t)
        elif pattern == "haunting":
            # Slow attack, very slow decay
            envelope = (1 - np.exp(-t * 5)) * np.exp(-t * 0.5)
        elif pattern == "harsh":
            # Sharp attack, quick decay
            envelope = np.exp(-t * 5) * (1 + 0.3 * np.random.normal(0, 0.1, length))
        else:
            # Default envelope
            envelope = np.exp(-t * 3)
        
        return envelope

    def _apply_audio_processing(self, audio: np.ndarray, config: SoundConfig) -> np.ndarray:
        """Apply professional audio processing"""
        
        # Normalize audio
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = audio / max_val
        
        # Apply volume
        audio *= config.volume
        
        # Apply fade in/out
        fade_in_samples = int(config.fade_in * len(audio))
        fade_out_samples = int(config.fade_out * len(audio))
        
        if fade_in_samples > 0:
            fade_in = np.linspace(0, 1, fade_in_samples)
            audio[:fade_in_samples] *= fade_in
        
        if fade_out_samples > 0:
            fade_out = np.linspace(1, 0, fade_out_samples)
            audio[-fade_out_samples:] *= fade_out
        
        # Apply gentle compression for consistent levels
        audio = np.tanh(audio * 1.5) / 1.5
        
        return audio

    def _generate_roar(self, t: np.ndarray, config: Dict) -> np.ndarray:
        """Generate lion/big cat roar"""
        base_freq = config["base_freq"]
        
        # Roar with frequency sweep and harmonics
        freq_sweep = base_freq + 50 * np.sin(2 * np.pi * 0.5 * t)
        roar = np.sin(2 * np.pi * freq_sweep * t)
        
        # Add harmonics for richness
        roar += 0.5 * np.sin(2 * np.pi * freq_sweep * 2 * t)
        roar += 0.3 * np.sin(2 * np.pi * freq_sweep * 3 * t)
        
        # Add growl texture
        growl = 0.2 * np.sin(2 * np.pi * 30 * t)
        roar *= (1 + growl)
        
        return roar

    def _generate_howl(self, t: np.ndarray, config: Dict) -> np.ndarray:
        """Generate wolf howl"""
        base_freq = config["base_freq"]
        
        # Howl with pitch variation
        pitch_curve = base_freq * (1 + 0.3 * np.sin(2 * np.pi * 0.2 * t))
        howl = np.sin(2 * np.pi * pitch_curve * t)
        
        # Add vibrato
        vibrato = 1 + 0.1 * np.sin(2 * np.pi * 5 * t)
        howl *= vibrato
        
        return howl

    def note_to_frequency(self, note, octave=4):
        """Convert note name to frequency"""
        notes = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 
                'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
        
        if note not in notes:
            return 440  # Default to A4
            
        # A4 = 440 Hz
        a4 = 440
        semitones = (octave - 4) * 12 + notes[note] - 9  # A is 9th semitone
        frequency = a4 * (2 ** (semitones / 12))
        
        return frequency
    
    def generate_tone(self, frequency, duration, amplitude=0.5, fade_in=0.1, fade_out=0.1):
        """Generate a pure tone with fade in/out"""
        sample_rate = self.sample_rates["high"]
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        
        # Generate sine wave
        wave = amplitude * np.sin(2 * np.pi * frequency * t)
        
        # Apply fade in/out
        fade_in_samples = int(fade_in * sample_rate)
        fade_out_samples = int(fade_out * sample_rate)
        
        if fade_in_samples > 0 and len(wave) > fade_in_samples:
            wave[:fade_in_samples] *= np.linspace(0, 1, fade_in_samples)
        if fade_out_samples > 0 and len(wave) > fade_out_samples:
            wave[-fade_out_samples:] *= np.linspace(1, 0, fade_out_samples)
            
        return wave
    
    def generate_chord(self, frequencies, duration, amplitude=0.3):
        """Generate a chord from multiple frequencies"""
        sample_rate = self.sample_rates["high"]
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        chord = np.zeros_like(t)
        
        for freq in frequencies:
            chord += amplitude * np.sin(2 * np.pi * freq * t)
            
        # Normalize to prevent clipping
        chord = chord / len(frequencies)
        return chord
    
    def create_abc_melody(self):
        """Create the classic ABC song melody"""
        # ABC song melody in C major
        melody_notes = [
            # "A B C D E F G"
            ('C', 4, 0.5), ('D', 4, 0.5), ('E', 4, 0.5), ('F', 4, 0.5), 
            ('G', 4, 0.5), ('A', 4, 0.5), ('G', 4, 1.0),
            
            # "H I J K L M N O P"  
            ('E', 4, 0.5), ('E', 4, 0.5), ('D', 4, 0.5), ('D', 4, 0.5),
            ('C', 4, 0.5), ('D', 4, 0.5), ('E', 4, 0.5), ('C', 4, 0.5), ('C', 4, 1.0),
            
            # "Q R S, T U V"
            ('G', 4, 0.5), ('G', 4, 0.5), ('F', 4, 1.0),
            ('F', 4, 0.5), ('F', 4, 0.5), ('E', 4, 1.0),
            
            # "W X Y and Z"
            ('E', 4, 0.5), ('D', 4, 0.5), ('E', 4, 0.5), ('F', 4, 0.5), ('G', 4, 1.5),
            
            # "Now I know my ABCs"
            ('C', 5, 0.5), ('C', 5, 0.5), ('G', 4, 0.5), ('G', 4, 0.5),
            ('A', 4, 0.5), ('A', 4, 0.5), ('G', 4, 1.0),
            
            # "Next time won't you sing with me"
            ('F', 4, 0.5), ('F', 4, 0.5), ('E', 4, 0.5), ('E', 4, 0.5),
            ('D', 4, 0.5), ('D', 4, 0.5), ('C', 4, 1.5)
        ]
        
        return melody_notes
    
    def create_simple_accompaniment(self, duration):
        """Create simple chord accompaniment"""
        sample_rate = self.sample_rates["high"]
        
        # Simple C major chord progression
        chord_progression = [
            # C major
            ([self.note_to_frequency('C', 3), self.note_to_frequency('E', 3), 
              self.note_to_frequency('G', 3)], 2.0),
            # F major  
            ([self.note_to_frequency('F', 3), self.note_to_frequency('A', 3), 
              self.note_to_frequency('C', 4)], 2.0),
            # G major
            ([self.note_to_frequency('G', 3), self.note_to_frequency('B', 3), 
              self.note_to_frequency('D', 4)], 2.0),
            # C major
            ([self.note_to_frequency('C', 3), self.note_to_frequency('E', 3), 
              self.note_to_frequency('G', 3)], 2.0),
        ]
        
        accompaniment = np.array([])
        current_time = 0
        
        while current_time < duration:
            for chord_freqs, chord_duration in chord_progression:
                if current_time >= duration:
                    break
                    
                chord = self.generate_chord(chord_freqs, chord_duration, amplitude=0.15)
                accompaniment = np.concatenate([accompaniment, chord])
                current_time += chord_duration
                
        # Trim to exact duration
        target_samples = int(duration * sample_rate)
        if len(accompaniment) > target_samples:
            accompaniment = accompaniment[:target_samples]
        elif len(accompaniment) < target_samples:
            # Pad with silence
            padding = np.zeros(target_samples - len(accompaniment))
            accompaniment = np.concatenate([accompaniment, padding])
            
        return accompaniment
    
    def create_drum_beat(self, duration, bpm=120):
        """Create simple drum beat"""
        sample_rate = self.sample_rates["high"]
        beat_interval = 60.0 / bpm  # Time between beats
        beats = int(duration / beat_interval)
        
        drum_track = np.array([])
        
        for i in range(beats):
            # Kick drum (low frequency click)
            if i % 4 == 0:  # On beat 1 and 3
                kick = self.generate_tone(60, 0.1, amplitude=0.3)
            else:
                kick = np.zeros(int(0.1 * sample_rate))
                
            # Hi-hat (high frequency noise)
            if i % 2 == 1:  # On beat 2 and 4
                t = np.linspace(0, 0.05, int(0.05 * sample_rate))
                hihat = 0.1 * np.random.normal(0, 1, len(t))
                hihat *= np.exp(-t * 50)  # Decay
            else:
                hihat = np.zeros(int(0.05 * sample_rate))
                
            # Silence to complete the beat
            silence_duration = beat_interval - 0.1
            silence = np.zeros(int(silence_duration * sample_rate))
            
            beat = kick + np.pad(hihat, (0, len(kick) - len(hihat)), 'constant')
            beat = np.concatenate([beat, silence])
            drum_track = np.concatenate([drum_track, beat])
            
        # Trim to exact duration
        target_samples = int(duration * sample_rate)
        if len(drum_track) > target_samples:
            drum_track = drum_track[:target_samples]
            
        return drum_track
    
    def generate_musical_abc_song(self, include_drums=True, include_accompaniment=True):
        """Generate complete ABC song with melody, chords, and rhythm"""
        print("🎵 Generating Musical ABC Song...")
        
        sample_rate = self.sample_rates["high"]
        
        # Create melody
        melody_notes = self.create_abc_melody()
        melody = np.array([])
        total_duration = 0
        
        print("🎼 Creating melody...")
        for note, octave, duration in melody_notes:
            freq = self.note_to_frequency(note, octave)
            tone = self.generate_tone(freq, duration, amplitude=0.4)
            melody = np.concatenate([melody, tone])
            total_duration += duration
            
        print(f"✅ Melody created: {total_duration:.1f} seconds")
        
        # Create accompaniment
        accompaniment = np.array([])
        if include_accompaniment:
            print("🎹 Creating chord accompaniment...")
            accompaniment = self.create_simple_accompaniment(total_duration)
            print("✅ Accompaniment created")
            
        # Create drum beat
        drums = np.array([])
        if include_drums:
            print("🥁 Creating drum beat...")
            drums = self.create_drum_beat(total_duration, bpm=120)
            print("✅ Drum beat created")
            
        # Mix all tracks
        print("🎚️ Mixing tracks...")
        final_mix = melody.copy()
        
        if len(accompaniment) > 0:
            # Ensure same length
            min_length = min(len(final_mix), len(accompaniment))
            final_mix = final_mix[:min_length] + accompaniment[:min_length]
            
        if len(drums) > 0:
            min_length = min(len(final_mix), len(drums))
            final_mix = final_mix[:min_length] + drums[:min_length]
            
        # Normalize to prevent clipping
        max_amplitude = np.max(np.abs(final_mix))
        if max_amplitude > 0.95:
            final_mix = final_mix * (0.95 / max_amplitude)
            
        return final_mix, total_duration, sample_rate

    def create_complete_musical_abc_library(self):
        """Create a complete musical ABC song library"""
        print("🎵 Creating Complete Musical ABC Song Library")
        print("=" * 60)
        
        # Create different musical versions
        versions = [
            {
                "name": "Musical ABC - Full Orchestra",
                "filename": "abc_song_full_orchestra",
                "drums": True,
                "accompaniment": True,
                "description": "Complete version with melody, chords, and drums"
            },
            {
                "name": "Musical ABC - Melody Only", 
                "filename": "abc_song_melody_only",
                "drums": False,
                "accompaniment": False,
                "description": "Pure melody version for singing along"
            },
            {
                "name": "Musical ABC - With Piano",
                "filename": "abc_song_with_piano", 
                "drums": False,
                "accompaniment": True,
                "description": "Melody with piano chord accompaniment"
            },
            {
                "name": "Musical ABC - With Rhythm",
                "filename": "abc_song_with_drums",
                "drums": True, 
                "accompaniment": False,
                "description": "Melody with drum beat for rhythm practice"
            }
        ]
        
        created_files = []
        
        for version in versions:
            print(f"\n🎼 Creating: {version['name']}")
            print("-" * 40)
            
            try:
                # Generate musical version
                audio_data, duration, sample_rate = self.generate_musical_abc_song(
                    include_drums=version["drums"],
                    include_accompaniment=version["accompaniment"]
                )
                
                # Save to audio_output directory (same as TTS files)
                output_dir = Path("audio_output")
                output_dir.mkdir(exist_ok=True)
                output_path = output_dir / f"{version['filename']}.wav"
                
                sf.write(output_path, audio_data, sample_rate)
                
                print(f"✅ Created: {output_path}")
                print(f"📊 Duration: {duration:.1f}s")
                print(f"📊 Description: {version['description']}")
                
                created_files.append({
                    "name": version["name"],
                    "path": output_path,
                    "duration": duration,
                    "description": version["description"]
                })
                
            except Exception as e:
                print(f"❌ Failed to create {version['name']}: {e}")
                import traceback
                traceback.print_exc()
        
        # Summary
        print(f"\n🎉 Musical ABC Library Complete!")
        print("=" * 60)
        print(f"✅ Created {len(created_files)} musical ABC versions")
        
        if created_files:
            total_duration = sum(f["duration"] for f in created_files)
            print(f"📊 Total music duration: {total_duration:.1f} seconds")
            
            print(f"\n🎵 Created Musical ABC Songs:")
            for file_info in created_files:
                print(f"   • {file_info['name']}")
                print(f"     📁 {file_info['path'].name} ({file_info['duration']:.1f}s)")
                print(f"     📝 {file_info['description']}")
        
        return created_files
def main():
    """Demo of the Natural Sound Generator"""
    
    print("🎵 Natural Sound Generator Demo")
    print("Creating crystal clear educational sounds...")
    
    # Initialize generator
    generator = NaturalSoundGenerator("demo_natural_sounds")
    
    # Configuration for demo sounds
    config = SoundConfig(
        duration=5.0,
        quality="ultra",
        volume=0.8,
        fade_in=0.2,
        fade_out=0.2
    )
    
    # Generate sample sounds
    demo_sounds = [
        ("robin", "bird"),
        ("rain_light", "weather"), 
        ("thunder_distant", "weather"),
        ("lion", "animal"),
        ("forest", "environment")
    ]
    
    for sound_name, sound_type in demo_sounds:
        print(f"\n🎼 Generating {sound_name} ({sound_type})...")
        
        try:
            if sound_type == "bird":
                audio = generator.generate_bird_sound(sound_name, config)
            elif sound_type == "weather":
                audio = generator.generate_weather_sound(sound_name, config)
            elif sound_type == "animal":
                audio = generator.generate_animal_sound(sound_name, config)
            elif sound_type == "environment":
                audio = generator.generate_environment_soundscape(sound_name, config)
            
            filename = f"demo_{sound_type}_{sound_name}.wav"
            filepath = generator.save_sound(audio, filename, config)
            print(f"✅ Saved: {filepath}")
            
        except Exception as e:
            print(f"❌ Error generating {sound_name}: {e}")
    
    print("\n🎯 Demo complete! Check the 'demo_natural_sounds' folder for generated audio files.")
    print("🔊 All sounds are crystal clear, professional quality for educational use!")


if __name__ == "__main__":
    main()
