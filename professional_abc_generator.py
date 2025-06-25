#!/usr/bin/env python3
"""
🎤 Professional ABC Song Generator with Clear Voices
Generate full ABC songs with clear pronunciation for YouTube-style videos
"""

import subprocess
import os
from pathlib import Path
import time

class ProfessionalABCGenerator:
    """Generate professional ABC songs with clear voices"""
    
    def __init__(self):
        self.output_dir = Path("audio_output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Full ABC song scripts with proper timing
        self.abc_scripts = {
            'teacher_clear': {
                'text': "Hello children! Let's learn the alphabet together. A for Apple, B for Ball, C for Cat, D for Dog, E for Elephant, F for Fish, G for Goat, H for Hat, I for Ice cream, J for Jump, K for Kite, L for Lion, M for Mouse, N for Nose, O for Orange, P for Penguin, Q for Queen, R for Robot, S for Sun, T for Tree, U for Umbrella, V for Van, W for Water, X for X-ray, Y for Yellow, Z for Zebra. Now let's sing the alphabet song! A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, and Z! Great job learning your ABCs!",
                'voice': 'en+f3',  # Female voice
                'speed': 160,
                'pitch': 50
            },
            'child_girl_happy': {
                'text': "Hi! I'm going to sing the ABC song! A, B, C, D, E, F, G! H, I, J, K, L, M, N, O, P! Q, R, S, T, U, V! W, X, Y, and Z! Now I know my A, B, Cs! Next time won't you sing with me! A is for Apple! B is for Ball! C is for Cat! I love them all! A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, and Z!",
                'voice': 'en+f5',  # Higher female voice for child
                'speed': 180,
                'pitch': 80
            },
            'child_boy_excited': {
                'text': "Hey everyone! Let's do the alphabet! A, B, C, D, E, F, G! H, I, J, K, L, M, N, O, P! Q, R, S, T, U, V! W, X, Y, and Z! Awesome! Let's do it again! A is for Airplane! B is for Batman! C is for Cool! A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, and Z! Yeah!",
                'voice': 'en+m3',  # Male voice for boy
                'speed': 190,
                'pitch': 60
            },
            'teacher_professional': {
                'text': "Welcome to our alphabet learning session. Today we will practice each letter clearly. A sounds like Ah in Apple. B sounds like Buh in Ball. Let's recite the complete alphabet. A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, and Z. Excellent work! Remember, practice makes perfect. Let's sing it together now. A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, and Z. Well done everyone!",
                'voice': 'en+f2',  # Professional female voice
                'speed': 150,
                'pitch': 45
            },
            'grandma_gentle': {
                'text': "Come here sweetie, let Grandma teach you the alphabet. A is for the Apple pie I bake. B is for the Beautiful flowers. C is for the Cozy hugs I give you. Now let's say them all together slowly. A... B... C... D... E... F... G... H... I... J... K... L... M... N... O... P... Q... R... S... T... U... V... W... X... Y... and Z. That's wonderful dear! Now let's sing the ABC song. A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, and Z. Good job my little one!",
                'voice': 'en+f1',  # Gentle female voice
                'speed': 140,
                'pitch': 40
            },
            'fun_energetic': {
                'text': "ARE YOU READY FOR THE ALPHABET? Let's GO! A, B, C, D, E, F, G! H, I, J, K, L, M, N, O, P! Q, R, S, T, U, V! W, X, Y, and Z! That was AWESOME! Let's make it even MORE fun! A for AWESOME! B for BRILLIANT! C for COOL! D for DANCE! E for EXCITING! F for FUN! G for GREAT! Now the whole alphabet! A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, and Z! FANTASTIC JOB EVERYONE!",
                'voice': 'en+m4',  # Energetic male voice
                'speed': 200,
                'pitch': 70
            }
        }
    
    def create_professional_abc_audio(self, script_name, filename):
        """Create professional ABC audio using espeak"""
        print(f"🎤 Creating: {filename}")
        
        script = self.abc_scripts[script_name]
        output_file = self.output_dir / f"{filename}.wav"
        
        # Build espeak command
        cmd = [
            'espeak',
            '-v', script['voice'],
            '-s', str(script['speed']),
            '-p', str(script['pitch']),
            '-a', '200',  # Amplitude (volume)
            '-g', '10',   # Gap between words
            '-w', str(output_file),  # Write to WAV file
            script['text']
        ]
        
        try:
            # Run espeak
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and output_file.exists():
                print(f"  ✅ Created: {output_file}")
                return str(output_file)
            else:
                print(f"  ❌ Error: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"  ❌ Exception: {e}")
            return None
    
    def generate_all_professional_abc(self):
        """Generate all professional ABC audio files"""
        print("🎵 Creating Professional ABC Audio for YouTube Videos")
        print("=" * 60)
        
        # Define all combinations
        audio_configs = [
            ('teacher_clear', 'professional_teacher_female'),
            ('child_girl_happy', 'sweet_girl_lily'),
            ('child_boy_excited', 'energetic_boy_tommy'),
            ('teacher_professional', 'classroom_teacher'),
            ('grandma_gentle', 'gentle_grandma_mary'),
            ('fun_energetic', 'super_fun_abc'),
        ]
        
        created_files = []
        
        for script_name, filename in audio_configs:
            audio_file = self.create_professional_abc_audio(script_name, filename)
            if audio_file:
                created_files.append(audio_file)
            
            time.sleep(0.5)  # Brief pause
        
        print(f"\n🎉 Professional ABC Audio Generation Complete!")
        print(f"✅ Created {len(created_files)} high-quality ABC audio files")
        print("\n📁 Generated Files:")
        for file in created_files:
            print(f"  🎵 {file}")
        
        return created_files

def main():
    """Generate professional ABC audio"""
    generator = ProfessionalABCGenerator()
    
    # Check if espeak is available
    try:
        subprocess.run(['espeak', '--version'], capture_output=True, check=True)
        print("✅ espeak is available")
    except:
        print("❌ espeak not found. Installing...")
        os.system("sudo apt-get update && sudo apt-get install -y espeak espeak-data")
    
    # Generate all audio
    files = generator.generate_all_professional_abc()
    
    print(f"\n🎯 Ready for YouTube-style video generation!")
    print(f"📊 {len(files)} professional ABC audio files created")
    print("🎤 Full-length ABC songs with clear pronunciation!")

if __name__ == "__main__":
    main()
