#!/usr/bin/env python3
"""
🎵 Advanced Music System Generator
Creates enhanced music files with effects and professional audio processing
"""

import numpy as np
import soundfile as sf
from pathlib import Path
import json
from datetime import datetime
import sys

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

try:
    from natural_sound_generator import NaturalSoundGenerator
    from tts_core_interface import CoreTTSInterface
except ImportError as e:
    print(f"Warning: {e}")

class AdvancedMusicSystem:
    """Advanced music system with effects and processing"""
    
    def __init__(self):
        self.output_dir = Path("audio_output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize music generator
        try:
            self.music_gen = NaturalSoundGenerator()
            self.tts = CoreTTSInterface()
        except Exception as e:
            print(f"Warning: Could not initialize advanced systems: {e}")
            self.music_gen = None
            self.tts = None
    
    def apply_audio_effects(self, audio, sample_rate, effects=None):
        """Apply professional audio effects to enhance the sound"""
        if effects is None:
            effects = ['normalize', 'compression', 'eq']
        
        processed_audio = audio.copy()
        
        # Normalize audio
        if 'normalize' in effects:
            max_val = np.max(np.abs(processed_audio))
            if max_val > 0:
                processed_audio = processed_audio / max_val * 0.9
        
        # Simple compression
        if 'compression' in effects:
            threshold = 0.7
            ratio = 4.0
            over_threshold = np.abs(processed_audio) > threshold
            processed_audio[over_threshold] = np.sign(processed_audio[over_threshold]) * (
                threshold + (np.abs(processed_audio[over_threshold]) - threshold) / ratio
            )
        
        # Basic EQ (enhance certain frequencies)
        if 'eq' in effects:
            # Add slight high-frequency boost for clarity
            # This is a simple implementation - real EQ would use proper filters
            processed_audio = processed_audio * 1.05
        
        # Add subtle reverb effect
        if 'reverb' in effects:
            delay_samples = int(0.1 * sample_rate)  # 100ms delay
            reverb_audio = np.zeros_like(processed_audio)
            if len(processed_audio) > delay_samples:
                reverb_audio[delay_samples:] = processed_audio[:-delay_samples] * 0.3
                processed_audio = processed_audio + reverb_audio
        
        return processed_audio
    
    def create_enhanced_versions(self):
        """Create enhanced versions of existing ABC songs"""
        print("🎵 Creating Enhanced Music System")
        print("=" * 50)
        
        enhanced_songs = []
        
        # Check for existing files
        existing_files = [
            ("abc_kids_teacher_duet.wav", "Teacher + Kids Duet"),
            ("abc_kids_chorus_musical.wav", "Kids Chorus Musical"),
            ("abc_song_full_orchestra.wav", "Full Orchestra"),
            ("abc_teacher_educational_music.wav", "Teacher Educational")
        ]
        
        for filename, title in existing_files:
            file_path = self.output_dir / filename
            if file_path.exists():
                try:
                    # Load existing audio
                    audio, sample_rate = sf.read(file_path)
                    
                    # Create enhanced version with effects
                    enhanced_audio = self.apply_audio_effects(
                        audio, sample_rate, 
                        effects=['normalize', 'compression', 'eq', 'reverb']
                    )
                    
                    # Save enhanced version
                    enhanced_filename = filename.replace('.wav', '_enhanced.wav')
                    enhanced_path = self.output_dir / enhanced_filename
                    sf.write(enhanced_path, enhanced_audio, sample_rate)
                    
                    print(f"✅ Enhanced: {title}")
                    print(f"   📁 {enhanced_filename}")
                    
                    enhanced_songs.append({
                        "title": f"🌟 {title} (Enhanced)",
                        "file": enhanced_filename,
                        "original": filename,
                        "effects": "Professional audio processing"
                    })
                    
                except Exception as e:
                    print(f"❌ Failed to enhance {filename}: {e}")
        
        return enhanced_songs
    
    def create_ambient_versions(self):
        """Create ambient/relaxing versions"""
        print("\n🌙 Creating Ambient Versions")
        print("=" * 40)
        
        if not self.music_gen:
            print("❌ Music generator not available")
            return []
        
        ambient_songs = []
        
        try:
            # Create ambient ABC melody
            sample_rate = 22050
            duration = 30.0  # 30 seconds
            
            # Generate soft, ambient ABC melody
            print("🎼 Generating ambient ABC melody...")
            melody = self.music_gen.generate_abc_melody(
                tempo_bpm=60,  # Slower tempo
                duration=duration,
                sample_rate=sample_rate
            )
            
            # Add soft pad sounds
            print("🌌 Adding ambient pads...")
            t = np.linspace(0, duration, int(sample_rate * duration))
            
            # Soft sine wave pads
            pad1 = 0.2 * np.sin(2 * np.pi * 220 * t)  # A3
            pad2 = 0.15 * np.sin(2 * np.pi * 330 * t)  # E4
            pad3 = 0.1 * np.sin(2 * np.pi * 440 * t)   # A4
            
            # Apply envelope to pads
            envelope = np.exp(-t / 10)  # Slow decay
            pad1 *= envelope
            pad2 *= envelope
            pad3 *= envelope
            
            # Mix melody with pads
            ambient_mix = melody * 0.7 + (pad1 + pad2 + pad3) * 0.3
            
            # Apply effects
            ambient_mix = self.apply_audio_effects(
                ambient_mix, sample_rate,
                effects=['normalize', 'reverb']
            )
            
            # Save ambient version
            ambient_path = self.output_dir / "abc_ambient_lullaby.wav"
            sf.write(ambient_path, ambient_mix, sample_rate)
            
            print("✅ Created: ABC Ambient Lullaby")
            print(f"   📁 abc_ambient_lullaby.wav")
            print(f"   ⏱️  {duration}s")
            
            ambient_songs.append({
                "title": "🌙 ABC Ambient Lullaby",
                "file": "abc_ambient_lullaby.wav",
                "description": "Soft, relaxing version perfect for bedtime",
                "duration": f"{duration}s"
            })
            
        except Exception as e:
            print(f"❌ Failed to create ambient version: {e}")
        
        return ambient_songs
    
    def create_upbeat_versions(self):
        """Create upbeat/energetic versions"""
        print("\n🎉 Creating Upbeat Versions")
        print("=" * 40)
        
        if not self.music_gen:
            print("❌ Music generator not available")
            return []
        
        upbeat_songs = []
        
        try:
            # Create energetic ABC song
            sample_rate = 22050
            duration = 25.0
            
            print("🎵 Generating upbeat ABC melody...")
            melody = self.music_gen.generate_abc_melody(
                tempo_bpm=140,  # Fast tempo
                duration=duration,
                sample_rate=sample_rate
            )
            
            print("🥁 Adding energetic drum beat...")
            drums = self.music_gen.generate_drum_beat(
                tempo_bpm=140,
                duration=duration,
                sample_rate=sample_rate
            )
            
            print("🎹 Adding piano chords...")
            chords = self.music_gen.generate_chord_progression(
                duration=duration,
                sample_rate=sample_rate,
                tempo_bpm=140
            )
            
            # Mix all elements
            upbeat_mix = melody * 0.5 + drums * 0.3 + chords * 0.4
            
            # Apply effects for energy
            upbeat_mix = self.apply_audio_effects(
                upbeat_mix, sample_rate,
                effects=['normalize', 'compression', 'eq']
            )
            
            # Save upbeat version
            upbeat_path = self.output_dir / "abc_dance_party.wav"
            sf.write(upbeat_path, upbeat_mix, sample_rate)
            
            print("✅ Created: ABC Dance Party")
            print(f"   📁 abc_dance_party.wav")
            print(f"   ⏱️  {duration}s")
            
            upbeat_songs.append({
                "title": "🎉 ABC Dance Party",
                "file": "abc_dance_party.wav",
                "description": "High-energy version perfect for active learning",
                "duration": f"{duration}s"
            })
            
        except Exception as e:
            print(f"❌ Failed to create upbeat version: {e}")
        
        return upbeat_songs
    
    def generate_playlist_metadata(self, all_songs):
        """Generate metadata for the music player"""
        metadata = {
            "generated": datetime.now().isoformat(),
            "total_songs": len(all_songs),
            "categories": {
                "Enhanced": [s for s in all_songs if "Enhanced" in s.get("title", "")],
                "Ambient": [s for s in all_songs if "Ambient" in s.get("title", "")],
                "Upbeat": [s for s in all_songs if "Dance" in s.get("title", "")]
            },
            "songs": all_songs
        }
        
        # Save metadata
        metadata_path = self.output_dir / "playlist_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\n📋 Playlist metadata saved: {metadata_path}")
        return metadata
    
    def run_full_system(self):
        """Run the complete advanced music system"""
        print("🎵 Advanced Music System Generator")
        print("=" * 60)
        print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        all_songs = []
        
        # Create enhanced versions
        enhanced = self.create_enhanced_versions()
        all_songs.extend(enhanced)
        
        # Create ambient versions
        ambient = self.create_ambient_versions()
        all_songs.extend(ambient)
        
        # Create upbeat versions
        upbeat = self.create_upbeat_versions()
        all_songs.extend(upbeat)
        
        # Generate metadata
        metadata = self.generate_playlist_metadata(all_songs)
        
        print("\n🎉 Advanced Music System Complete!")
        print("=" * 50)
        print(f"✅ Total new songs created: {len(all_songs)}")
        print(f"📁 All files saved in: {self.output_dir}")
        print("\n🎯 New Features Added:")
        print("   • Professional audio effects")
        print("   • Enhanced versions with reverb & compression")
        print("   • Ambient lullaby versions")
        print("   • Upbeat dance party versions")
        print("   • Playlist metadata for web player")
        
        return all_songs

if __name__ == "__main__":
    system = AdvancedMusicSystem()
    system.run_full_system()
