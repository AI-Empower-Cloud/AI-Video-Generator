#!/usr/bin/env python3
"""
🎵 Universal Song Generator
Create real songs in different genres - pop, rock, classical, jazz, etc.
"""

import numpy as np
import soundfile as sf
from pathlib import Path
import random
import math

class UniversalSongGenerator:
    """Generate real songs in various genres"""
    
    def __init__(self):
        self.output_dir = Path("audio_output")
        self.output_dir.mkdir(exist_ok=True)
        self.sample_rate = 22050
        
    def generate_chord_progression(self, key='C', progression_type='pop'):
        """Generate chord progressions for different genres"""
        
        # Note frequencies (C4 = 261.63 Hz)
        notes = {
            'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13,
            'E': 329.63, 'F': 349.23, 'F#': 369.99, 'G': 392.00,
            'G#': 415.30, 'A': 440.00, 'A#': 466.16, 'B': 493.88
        }
        
        # Chord progressions by genre
        progressions = {
            'pop': ['C', 'G', 'Am', 'F'],  # I-V-vi-IV
            'rock': ['Am', 'F', 'C', 'G'],  # vi-IV-I-V
            'jazz': ['Cmaj7', 'Am7', 'Dm7', 'G7'],  # Jazz ii-V-I
            'classical': ['C', 'F', 'G', 'C'],  # I-IV-V-I
            'blues': ['C7', 'F7', 'C7', 'G7'],  # 12-bar blues
            'folk': ['C', 'F', 'Am', 'G'],  # Folk progression
            'ballad': ['C', 'Em', 'F', 'G']  # Romantic ballad
        }
        
        return progressions.get(progression_type, progressions['pop'])
    
    def create_melody(self, duration, genre='pop', tempo=120):
        """Create melody based on genre"""
        
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        melody = np.zeros_like(t)
        
        # Base frequencies for different genres
        if genre == 'pop':
            base_freq = 440  # A4
            pattern = [0, 2, 4, 5, 7, 9, 11, 12]  # Major scale
        elif genre == 'rock':
            base_freq = 220  # A3 (lower)
            pattern = [0, 2, 3, 5, 7, 8, 10, 12]  # Natural minor
        elif genre == 'jazz':
            base_freq = 330
            pattern = [0, 2, 4, 6, 7, 9, 11, 12]  # Jazz scale
        elif genre == 'classical':
            base_freq = 523  # C5 (higher)
            pattern = [0, 2, 4, 5, 7, 9, 11, 12]  # Major scale
        elif genre == 'blues':
            base_freq = 220
            pattern = [0, 3, 5, 6, 7, 10, 12]  # Blues scale
        else:
            base_freq = 440
            pattern = [0, 2, 4, 5, 7, 9, 11, 12]
        
        # Create melodic phrases
        note_duration = 60 / tempo  # Duration of each note
        notes_per_phrase = int(duration / note_duration)
        
        for i in range(notes_per_phrase):
            start_time = i * note_duration
            end_time = min((i + 1) * note_duration, duration)
            
            if start_time >= duration:
                break
                
            start_idx = int(start_time * self.sample_rate)
            end_idx = int(end_time * self.sample_rate)
            
            # Choose note from pattern
            note_idx = random.choice(pattern)
            freq = base_freq * (2 ** (note_idx / 12))
            
            # Generate note with envelope
            note_t = t[start_idx:end_idx] - start_time
            note_length = end_time - start_time
            
            # Create envelope (attack, decay, sustain, release)
            envelope = np.ones_like(note_t)
            attack_time = min(0.1, note_length * 0.1)
            release_time = min(0.1, note_length * 0.1)
            
            attack_samples = int(attack_time * self.sample_rate)
            release_samples = int(release_time * self.sample_rate)
            
            if len(envelope) > attack_samples:
                envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
            if len(envelope) > release_samples:
                envelope[-release_samples:] = np.linspace(1, 0, release_samples)
            
            # Generate note with harmonics
            note = np.sin(2 * np.pi * freq * note_t) * envelope
            # Add harmonics for richness
            note += 0.3 * np.sin(2 * np.pi * freq * 2 * note_t) * envelope
            note += 0.1 * np.sin(2 * np.pi * freq * 3 * note_t) * envelope
            
            melody[start_idx:end_idx] += note
        
        return melody * 0.7  # Normalize
    
    def create_bass_line(self, duration, genre='pop', tempo=120):
        """Create bass line"""
        
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        bass = np.zeros_like(t)
        
        # Bass frequencies (lower octave)
        base_freq = 110  # A2
        
        if genre == 'rock':
            pattern = [0, 0, 5, 5, 7, 7, 5, 3]  # Rock bass pattern
        elif genre == 'jazz':
            pattern = [0, 7, 5, 10, 0, 7, 5, 10]  # Walking bass
        elif genre == 'pop':
            pattern = [0, 5, 7, 5]  # Simple pop bass
        else:
            pattern = [0, 5, 7, 5]
        
        note_duration = 60 / tempo / 2  # Eighth notes
        beats = int(duration / note_duration)
        
        for i in range(beats):
            start_time = i * note_duration
            end_time = min((i + 1) * note_duration, duration)
            
            if start_time >= duration:
                break
                
            start_idx = int(start_time * self.sample_rate)
            end_idx = int(end_time * self.sample_rate)
            
            note_idx = pattern[i % len(pattern)]
            freq = base_freq * (2 ** (note_idx / 12))
            
            note_t = t[start_idx:end_idx] - start_time
            note = np.sin(2 * np.pi * freq * note_t) * 0.6
            
            bass[start_idx:end_idx] += note
        
        return bass
    
    def create_drums(self, duration, genre='pop', tempo=120):
        """Create drum track"""
        
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        drums = np.zeros_like(t)
        
        beat_duration = 60 / tempo
        beats = int(duration / beat_duration)
        
        for beat in range(beats):
            beat_time = beat * beat_duration
            beat_idx = int(beat_time * self.sample_rate)
            
            if beat_idx >= len(drums):
                break
            
            # Kick drum (every beat for pop/rock, different for jazz)
            if genre in ['pop', 'rock']:
                if beat % 4 == 0 or beat % 4 == 2:  # On 1 and 3
                    kick_duration = int(0.1 * self.sample_rate)
                    kick_end = min(beat_idx + kick_duration, len(drums))
                    kick_t = np.linspace(0, 0.1, kick_end - beat_idx)
                    kick = np.sin(2 * np.pi * 60 * kick_t) * np.exp(-kick_t * 10)
                    drums[beat_idx:kick_end] += kick * 0.8
            
            # Snare drum (on 2 and 4)
            if beat % 4 == 1 or beat % 4 == 3:
                snare_duration = int(0.05 * self.sample_rate)
                snare_end = min(beat_idx + snare_duration, len(drums))
                snare_t = np.linspace(0, 0.05, snare_end - beat_idx)
                # Snare is basically noise with envelope
                snare = np.random.normal(0, 1, len(snare_t)) * np.exp(-snare_t * 20)
                drums[beat_idx:snare_end] += snare * 0.4
            
            # Hi-hat (eighth notes)
            if beat % 2 == 0:  # On every other eighth note
                hihat_duration = int(0.02 * self.sample_rate)
                hihat_end = min(beat_idx + hihat_duration, len(drums))
                hihat_t = np.linspace(0, 0.02, hihat_end - beat_idx)
                hihat = np.random.normal(0, 1, len(hihat_t)) * np.exp(-hihat_t * 50)
                drums[beat_idx:hihat_end] += hihat * 0.2
        
        return drums
    
    def create_song(self, title, genre='pop', duration=30, tempo=120):
        """Create a complete song"""
        
        print(f"🎵 Creating {genre.upper()} song: {title}")
        print(f"⏱️  Duration: {duration}s | Tempo: {tempo} BPM")
        
        # Create different tracks
        melody = self.create_melody(duration, genre, tempo)
        bass = self.create_bass_line(duration, genre, tempo)
        drums = self.create_drums(duration, genre, tempo)
        
        # Mix tracks together
        song = melody + bass * 0.7 + drums * 0.8
        
        # Normalize
        song = song / np.max(np.abs(song)) * 0.9
        
        # Save song
        filename = f"song_{genre}_{title.lower().replace(' ', '_')}.wav"
        filepath = self.output_dir / filename
        sf.write(filepath, song, self.sample_rate)
        
        print(f"✅ Created: {filepath}")
        print(f"📊 Genre: {genre.title()} | Duration: {duration}s")
        print()
        
        return filepath
    
    def create_song_collection(self):
        """Create a collection of songs in different genres"""
        
        print("🎵 Universal Song Generator")
        print("=" * 50)
        print("Creating real songs in multiple genres!")
        print()
        
        songs = [
            # Pop Songs
            ("Summer Dreams", "pop", 45, 128),
            ("Dancing Tonight", "pop", 40, 124),
            ("Sunshine Love", "pop", 38, 120),
            
            # Rock Songs
            ("Thunder Road", "rock", 50, 140),
            ("Electric Nights", "rock", 45, 132),
            ("Wild Freedom", "rock", 42, 136),
            
            # Jazz Songs
            ("Midnight Blue", "jazz", 60, 90),
            ("Coffee House", "jazz", 55, 100),
            ("Smooth Sailing", "jazz", 48, 95),
            
            # Classical Songs
            ("Morning Serenade", "classical", 90, 80),
            ("Peaceful Garden", "classical", 75, 70),
            ("Royal Dance", "classical", 60, 110),
            
            # Blues Songs
            ("Lonely Highway", "blues", 50, 80),
            ("Rainy Day Blues", "blues", 45, 75),
            ("City Blues", "blues", 40, 85),
        ]
        
        created_songs = []
        
        for title, genre, duration, tempo in songs:
            filepath = self.create_song(title, genre, duration, tempo)
            created_songs.append({
                'title': title,
                'genre': genre,
                'duration': duration,
                'tempo': tempo,
                'file': filepath
            })
        
        print("🎉 Song Collection Complete!")
        print("=" * 50)
        print(f"✅ Created {len(created_songs)} original songs")
        
        # Group by genre
        genres = {}
        for song in created_songs:
            genre = song['genre']
            if genre not in genres:
                genres[genre] = []
            genres[genre].append(song)
        
        for genre, genre_songs in genres.items():
            print(f"\n🎵 {genre.upper()} SONGS:")
            for song in genre_songs:
                print(f"   • {song['title']}")
                print(f"     📁 {song['file'].name}")
                print(f"     ⏱️  {song['duration']}s | 🎵 {song['tempo']} BPM")
        
        print(f"\n🎯 Total songs: {len(created_songs)}")
        print("📁 Check 'audio_output' directory to listen!")
        
        return created_songs

def main():
    generator = UniversalSongGenerator()
    songs = generator.create_song_collection()
    
    print("\n🎵 Your Universal Song Collection is Ready!")
    print("Now you have REAL SONGS in multiple genres!")
    print("🎧 Pop, Rock, Jazz, Classical, and Blues!")

if __name__ == "__main__":
    main()
