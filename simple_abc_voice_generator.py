#!/usr/bin/env python3
"""
🎤 Simple ABC Voice Generator with espeak
Generate clear spoken ABC songs using espeak
"""

import subprocess
import os
from pathlib import Path
import soundfile as sf
import numpy as np

class SimpleABCVoiceGenerator:
    """Generate clear ABC voices using espeak"""
    
    def __init__(self):
        self.output_dir = Path("audio_output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Voice configurations for espeak
        self.voice_configs = [
            {
                'name': 'teacher_female_clear',
                'espeak_voice': 'en+f3',  # Female voice
                'speed': 150,
                'pitch': 50,
                'text': 'A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, and Z. Now I know my A B C s, next time wont you sing with me?',
                'description': 'Clear female teacher voice'
            },
            {
                'name': 'child_girl_sweet',
                'espeak_voice': 'en+f5',  # Higher female voice for child
                'speed': 160,
                'pitch': 80,
                'text': 'A B C D E F G! H I J K L M N O P! Q R S! T U V! W X Y and Z! Now I know my A B C s! Lets sing it again!',
                'description': 'Sweet little girl voice'
            },
            {
                'name': 'child_boy_excited',
                'espeak_voice': 'en+m3',  # Male voice for boy
                'speed': 170,
                'pitch': 70,
                'text': 'A B C D E F G! H I J K L M N O P! Q R S T U V! W X Y and Z! Yay! I know my A B C s!',
                'description': 'Excited little boy voice'
            },
            {
                'name': 'teacher_male_professional',
                'espeak_voice': 'en+m2',  # Professional male voice
                'speed': 140,
                'pitch': 30,
                'text': 'Welcome class. Lets learn the alphabet together. A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, and Z. Excellent work everyone!',
                'description': 'Professional male teacher'
            },
            {
                'name': 'grandma_gentle',
                'espeak_voice': 'en+f1',  # Gentle female voice
                'speed': 120,
                'pitch': 40,
                'text': 'Hello dear. A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, and Z. Now you know your letters sweetie.',
                'description': 'Gentle grandmother voice'
            }
        ]
    
    def create_voice_file(self, config):
        """Create a single voice file using espeak"""
        print(f"🎤 Creating: {config['name']}")
        print(f"   📝 Text: {config['text'][:50]}...")
        
        output_file = self.output_dir / f"abc_clear_{config['name']}.wav"
        
        try:
            # Use espeak to generate speech
            cmd = [
                'espeak',
                '-v', config['espeak_voice'],
                '-s', str(config['speed']),
                '-p', str(config['pitch']),
                '-w', str(output_file),
                config['text']
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            if output_file.exists():
                # Check file size
                file_size = output_file.stat().st_size
                print(f"   ✅ Created: {output_file} ({file_size} bytes)")
                
                # Load and check audio duration
                try:
                    audio_data, sample_rate = sf.read(str(output_file))
                    duration = len(audio_data) / sample_rate
                    print(f"   ⏱️  Duration: {duration:.1f} seconds")
                    
                    if duration < 2:
                        print(f"   ⚠️  Warning: Audio seems too short")
                    
                except Exception as e:
                    print(f"   ⚠️  Could not verify audio: {e}")
                
                return str(output_file)
            else:
                print(f"   ❌ Failed to create file")
                return None
                
        except subprocess.CalledProcessError as e:
            print(f"   ❌ espeak error: {e}")
            return None
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def generate_all_voices(self):
        """Generate all ABC voice files"""
        print("🎵 Simple ABC Voice Generator")
        print("=" * 50)
        print("Using espeak for clear, consistent voices")
        print()
        
        voices_created = []
        
        for config in self.voice_configs:
            try:
                voice_file = self.create_voice_file(config)
                if voice_file:
                    voices_created.append({
                        'file': voice_file,
                        'name': config['name'],
                        'description': config['description']
                    })
                print()  # Blank line between voices
                
            except Exception as e:
                print(f"❌ Error creating {config['name']}: {e}")
        
        print("🎉 ABC Voice Generation Complete!")
        print("=" * 50)
        print(f"✅ Created {len(voices_created)} clear ABC voices")
        
        for voice in voices_created:
            print(f"🎵 {voice['name']}: {voice['description']}")
            print(f"   📁 {voice['file']}")
        
        print(f"\n📁 All voices saved to: {self.output_dir}")
        print("🎯 Ready for video generation with real spoken alphabet!")
        
        return voices_created

def main():
    """Generate all clear ABC voices"""
    generator = SimpleABCVoiceGenerator()
    generator.generate_all_voices()

if __name__ == "__main__":
    main()
