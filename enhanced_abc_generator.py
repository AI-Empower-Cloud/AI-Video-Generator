#!/usr/bin/env python3
"""
🌟 Enhanced ABC Video Generator with Advanced Features
Add multiple themes, languages, and interactive elements
"""

import cv2
import numpy as np
import soundfile as sf
from pathlib import Path
import random
import math
import subprocess
import os
import time
import json

class AdvancedABCVideoGenerator:
    """Enhanced ABC video generator with multiple themes and features"""
    
    def __init__(self):
        self.output_dir = Path("video_output")
        self.output_dir.mkdir(exist_ok=True)
        self.audio_dir = Path("audio_output")
        
        # Video settings
        self.width = 1920
        self.height = 1080
        self.fps = 30
        
        # Theme definitions
        self.themes = {
            'animals': {
                'name': 'Animal ABC Adventure',
                'words': {
                    'A': 'Alligator', 'B': 'Bear', 'C': 'Cat', 'D': 'Dog', 'E': 'Elephant',
                    'F': 'Frog', 'G': 'Giraffe', 'H': 'Horse', 'I': 'Iguana', 'J': 'Jaguar',
                    'K': 'Kangaroo', 'L': 'Lion', 'M': 'Monkey', 'N': 'Newt', 'O': 'Owl',
                    'P': 'Penguin', 'Q': 'Quail', 'R': 'Rabbit', 'S': 'Snake', 'T': 'Tiger',
                    'U': 'Unicorn', 'V': 'Vulture', 'W': 'Wolf', 'X': 'X-ray Fish', 'Y': 'Yak', 'Z': 'Zebra'
                },
                'colors': {
                    'background': (200, 255, 200),  # Light green
                    'primary': (0, 150, 0),         # Forest green
                    'secondary': (139, 69, 19),     # Brown
                    'accent': (255, 165, 0)         # Orange
                }
            },
            'space': {
                'name': 'Space ABC Exploration',
                'words': {
                    'A': 'Astronaut', 'B': 'Black Hole', 'C': 'Comet', 'D': 'Dragon Nebula', 'E': 'Earth',
                    'F': 'Flying Saucer', 'G': 'Galaxy', 'H': 'Hubble', 'I': 'International Space Station',
                    'J': 'Jupiter', 'K': 'Kuiper Belt', 'L': 'Lunar Module', 'M': 'Mars', 'N': 'Neptune',
                    'O': 'Observatory', 'P': 'Planet', 'Q': 'Quasar', 'R': 'Rocket', 'S': 'Satellite',
                    'T': 'Telescope', 'U': 'Universe', 'V': 'Venus', 'W': 'Wormhole', 'X': 'X-rays',
                    'Y': 'Year Light', 'Z': 'Zero Gravity'
                },
                'colors': {
                    'background': (0, 0, 50),       # Dark blue
                    'primary': (255, 255, 255),     # White
                    'secondary': (255, 215, 0),     # Gold
                    'accent': (0, 255, 255)        # Cyan
                }
            },
            'food': {
                'name': 'Delicious ABC Kitchen',
                'words': {
                    'A': 'Apple', 'B': 'Banana', 'C': 'Carrot', 'D': 'Donut', 'E': 'Egg',
                    'F': 'Fish', 'G': 'Grapes', 'H': 'Hamburger', 'I': 'Ice Cream', 'J': 'Juice',
                    'K': 'Kiwi', 'L': 'Lemon', 'M': 'Mango', 'N': 'Noodles', 'O': 'Orange',
                    'P': 'Pizza', 'Q': 'Quinoa', 'R': 'Rice', 'S': 'Strawberry', 'T': 'Tomato',
                    'U': 'Udon', 'V': 'Vanilla', 'W': 'Watermelon', 'X': 'Xigua', 'Y': 'Yogurt', 'Z': 'Zucchini'
                },
                'colors': {
                    'background': (255, 248, 220),  # Cornsilk
                    'primary': (255, 69, 0),        # Red-orange
                    'secondary': (34, 139, 34),     # Forest green
                    'accent': (255, 215, 0)         # Gold
                }
            }
        }
        
        # Language support
        self.languages = {
            'spanish': {
                'name': 'ABC en Español',
                'alphabet': 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ',
                'greeting': 'Hola niños! Vamos a aprender el abecedario!',
                'voice_settings': {'language': 'es', 'speed': 150}
            },
            'french': {
                'name': 'ABC en Français',
                'alphabet': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                'greeting': 'Bonjour les enfants! Apprenons l\'alphabet!',
                'voice_settings': {'language': 'fr', 'speed': 150}
            }
        }
        
        # Interactive elements
        self.interactive_modes = {
            'quiz': {
                'questions': [
                    "What letter comes after A?",
                    "What letter comes before C?",
                    "What letter is between M and O?",
                    "What is the first letter of the alphabet?",
                    "What is the last letter of the alphabet?"
                ],
                'answers': ['B', 'B', 'N', 'A', 'Z']
            },
            'repeat': {
                'prompts': [
                    "Now you say: A",
                    "Your turn: B", 
                    "Can you say: C?",
                    "Try this one: D"
                ]
            }
        }
    
    def create_themed_background(self, theme_name, frame_num, total_frames):
        """Create themed background based on selected theme"""
        theme = self.themes[theme_name]
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        if theme_name == 'animals':
            return self.create_jungle_background(frame, frame_num, theme['colors'])
        elif theme_name == 'space':
            return self.create_space_background(frame, frame_num, theme['colors'])
        elif theme_name == 'food':
            return self.create_kitchen_background(frame, frame_num, theme['colors'])
        
        return frame
    
    def create_jungle_background(self, frame, frame_num, colors):
        """Create animated jungle background"""
        # Sky gradient
        for y in range(self.height // 2):
            ratio = y / (self.height // 2)
            color = colors['background']
            b = int(color[0] * (1 - ratio * 0.3))
            g = int(color[1] * (1 - ratio * 0.2))
            r = int(color[2] * (1 - ratio * 0.1))
            frame[y, :] = [b, g, r]
        
        # Ground
        ground_color = colors['primary']
        frame[self.height // 2:, :] = ground_color
        
        # Animated trees
        tree_positions = [200, 500, 800, 1200, 1500]
        for i, x in enumerate(tree_positions):
            sway = int(10 * math.sin(frame_num * 0.02 + i))
            tree_x = x + sway
            
            # Tree trunk
            cv2.rectangle(frame, (tree_x - 20, self.height // 2), 
                         (tree_x + 20, self.height - 100), colors['secondary'], -1)
            
            # Tree leaves (animated)
            leaf_size = 80 + int(20 * math.sin(frame_num * 0.03 + i))
            cv2.circle(frame, (tree_x, self.height // 2 - 50), leaf_size, colors['accent'], -1)
        
        # Animated butterflies
        butterfly_positions = [
            (300 + int(100 * math.sin(frame_num * 0.05)), 200 + int(50 * math.cos(frame_num * 0.07))),
            (800 + int(80 * math.cos(frame_num * 0.04)), 150 + int(40 * math.sin(frame_num * 0.06)))
        ]
        
        for x, y in butterfly_positions:
            # Simple butterfly shape
            cv2.circle(frame, (x, y), 15, (255, 0, 255), -1)
            cv2.circle(frame, (x + 10, y), 10, (255, 0, 255), -1)
            cv2.circle(frame, (x, y + 10), 10, (255, 0, 255), -1)
            cv2.circle(frame, (x + 10, y + 10), 8, (255, 0, 255), -1)
        
        return frame
    
    def create_space_background(self, frame, frame_num, colors):
        """Create animated space background"""
        # Space background
        frame[:, :] = colors['background']
        
        # Animated stars
        num_stars = 100
        for i in range(num_stars):
            x = (i * 137 + frame_num) % self.width
            y = (i * 211) % self.height
            
            # Twinkling effect
            brightness = int(255 * (0.5 + 0.5 * math.sin(frame_num * 0.1 + i)))
            star_color = (brightness, brightness, brightness)
            
            cv2.circle(frame, (x, y), 2, star_color, -1)
        
        # Animated planets
        planet_positions = [
            (200 + int(50 * math.sin(frame_num * 0.01)), 300),
            (600 + int(30 * math.cos(frame_num * 0.015)), 500),
            (1000 + int(40 * math.sin(frame_num * 0.008)), 200)
        ]
        
        planet_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        
        for i, (x, y) in enumerate(planet_positions):
            size = 40 + int(10 * math.sin(frame_num * 0.02 + i))
            cv2.circle(frame, (x, y), size, planet_colors[i], -1)
            
            # Planet rings
            if i == 1:  # Saturn-like rings
                cv2.ellipse(frame, (x, y), (size + 20, size // 2), 0, 0, 360, colors['accent'], 3)
        
        # Shooting stars
        if frame_num % 180 < 60:  # Appear every 6 seconds for 2 seconds
            progress = (frame_num % 180) / 60.0
            start_x = int(-100 + progress * (self.width + 200))
            start_y = int(100 + progress * 200)
            end_x = start_x + 100
            end_y = start_y + 50
            
            cv2.line(frame, (start_x, start_y), (end_x, end_y), colors['primary'], 5)
        
        return frame
    
    def create_kitchen_background(self, frame, frame_num, colors):
        """Create animated kitchen background"""
        # Kitchen background
        frame[:, :] = colors['background']
        
        # Kitchen counter
        counter_height = self.height // 3
        cv2.rectangle(frame, (0, self.height - counter_height), 
                     (self.width, self.height), colors['secondary'], -1)
        
        # Animated cooking elements
        # Steam from pot
        steam_x = 300
        for i in range(5):
            steam_y = self.height - counter_height - 50 - (i * 30) - int(20 * math.sin(frame_num * 0.1 + i))
            cv2.circle(frame, (steam_x + int(10 * math.sin(frame_num * 0.05 + i)), steam_y), 
                      8 - i, (255, 255, 255), -1)
        
        # Spinning fruits
        fruit_positions = [500, 700, 900]
        fruit_colors = [(255, 0, 0), (255, 255, 0), (0, 255, 0)]  # Red, Yellow, Green
        
        for i, x in enumerate(fruit_positions):
            angle = frame_num * 0.05 + i
            y = self.height - counter_height - 50 + int(20 * math.sin(angle))
            cv2.circle(frame, (x, y), 25, fruit_colors[i], -1)
            
            # Add shine effect
            shine_x = x - 8 + int(5 * math.cos(angle))
            shine_y = y - 8 + int(5 * math.sin(angle))
            cv2.circle(frame, (shine_x, shine_y), 5, (255, 255, 255), -1)
        
        return frame
    
    def draw_themed_letter_display(self, frame, letter, theme_name, current_time, frame_num):
        """Draw letter with theme-specific decorations"""
        theme = self.themes[theme_name]
        
        # Get themed word for this letter
        themed_word = theme['words'].get(letter, letter)
        
        # Letter position
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        letter_index = letters.index(letter)
        
        col = letter_index % 6
        row = letter_index // 6
        
        x = 600 + col * 180
        y = 200 + row * 120
        
        # Draw themed background for letter
        theme_color = theme['colors']['accent']
        cv2.circle(frame, (x + 30, y - 30), 60, theme_color, -1)
        cv2.circle(frame, (x + 30, y - 30), 60, (255, 255, 255), 3)
        
        # Draw letter
        cv2.putText(frame, letter, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 
                   3, (255, 255, 255), 8)
        cv2.putText(frame, letter, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 
                   3, (0, 0, 0), 6)
        
        # Draw themed word below
        word_y = y + 50
        cv2.putText(frame, themed_word, (x - 20, word_y), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.8, theme['colors']['primary'], 3)
        cv2.putText(frame, themed_word, (x - 20, word_y), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.8, (255, 255, 255), 2)
    
    def create_interactive_element(self, frame, mode, frame_num):
        """Add interactive elements like quiz questions or prompts"""
        if mode == 'quiz':
            # Quiz question display
            question_area = (50, 50, self.width - 100, 150)
            cv2.rectangle(frame, (question_area[0], question_area[1]), 
                         (question_area[2], question_area[3]), (0, 0, 255), -1)
            cv2.rectangle(frame, (question_area[0], question_area[1]), 
                         (question_area[2], question_area[3]), (255, 255, 255), 3)
            
            # Pulsing effect for attention
            pulse = int(255 * (0.7 + 0.3 * math.sin(frame_num * 0.2)))
            
            cv2.putText(frame, "QUIZ TIME!", (70, 100), cv2.FONT_HERSHEY_SIMPLEX, 
                       2, (pulse, pulse, 0), 6)
            
            # Sample question
            question = "What letter comes after A?"
            cv2.putText(frame, question, (70, 140), cv2.FONT_HERSHEY_SIMPLEX, 
                       1, (255, 255, 255), 3)
        
        elif mode == 'repeat':
            # "Repeat after me" prompt
            prompt_y = self.height - 100
            cv2.rectangle(frame, (50, prompt_y - 50), (self.width - 50, prompt_y + 20), 
                         (0, 255, 0), -1)
            cv2.rectangle(frame, (50, prompt_y - 50), (self.width - 50, prompt_y + 20), 
                         (255, 255, 255), 3)
            
            cv2.putText(frame, "Now you say: A!", (70, prompt_y), cv2.FONT_HERSHEY_SIMPLEX, 
                       1.5, (255, 255, 255), 4)
    
    def generate_enhanced_abc_scripts(self):
        """Generate enhanced ABC scripts with themes and interactivity"""
        print("🌟 Generating Enhanced ABC Content...")
        
        scripts = []
        
        # Animal theme script
        animal_script = "Welcome to the Animal ABC Adventure! "
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            animal = self.themes['animals']['words'][letter]
            animal_script += f"{letter} is for {animal}! "
        animal_script += "Great job learning animals and letters!"
        
        scripts.append(('animals', animal_script))
        
        # Space theme script
        space_script = "Blast off to Space ABC Exploration! "
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            space_word = self.themes['space']['words'][letter]
            space_script += f"{letter} is for {space_word}! "
        space_script += "Amazing space alphabet adventure complete!"
        
        scripts.append(('space', space_script))
        
        # Food theme script
        food_script = "Welcome to the Delicious ABC Kitchen! "
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            food_word = self.themes['food']['words'][letter]
            food_script += f"{letter} is for {food_word}! "
        food_script += "Yummy alphabet cooking is complete!"
        
        scripts.append(('food', food_script))
        
        return scripts
    
    def create_enhanced_video(self, theme_name, audio_text, title):
        """Create enhanced themed ABC video"""
        print(f"🎬 Creating Enhanced Video: {title}")
        
        # Create audio first
        audio_file = self.audio_dir / f"enhanced_{theme_name}_abc.wav"
        self.create_enhanced_audio(audio_text, str(audio_file))
        
        if not audio_file.exists():
            print(f"❌ Audio creation failed for {theme_name}")
            return None
        
        # Load audio to get duration
        audio_data, sample_rate = sf.read(str(audio_file))
        duration = len(audio_data) / sample_rate
        total_frames = int(duration * self.fps)
        
        print(f"  📊 Duration: {duration:.1f}s, Frames: {total_frames}")
        
        # Video files
        video_name = f"enhanced_{theme_name}_abc.mp4"
        temp_video = self.output_dir / f"temp_{video_name}"
        final_video = self.output_dir / video_name
        
        # Create video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(temp_video), fourcc, self.fps, (self.width, self.height))
        
        print("  🎨 Creating enhanced themed animation...")
        
        for frame_num in range(total_frames):
            current_time = frame_num / self.fps
            
            if frame_num % 90 == 0:
                progress = int((frame_num / total_frames) * 100)
                print(f"    📹 Progress: {progress}%")
            
            # Create themed background
            frame = self.create_themed_background(theme_name, frame_num, total_frames)
            
            # Draw title
            cv2.putText(frame, title, (50, 80), cv2.FONT_HERSHEY_DUPLEX, 
                       2, (255, 255, 255), 6)
            cv2.putText(frame, title, (50, 80), cv2.FONT_HERSHEY_DUPLEX, 
                       2, (0, 0, 0), 4)
            
            # Draw themed letters
            letters_per_second = 26 / duration
            current_letter_index = int(current_time * letters_per_second)
            
            if current_letter_index < 26:
                letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[current_letter_index]
                self.draw_themed_letter_display(frame, letter, theme_name, current_time, frame_num)
            
            # Add interactive elements occasionally
            if frame_num % 300 < 60:  # Every 10 seconds for 2 seconds
                self.create_interactive_element(frame, 'quiz', frame_num)
            elif frame_num % 300 >= 240:  # Later in the cycle
                self.create_interactive_element(frame, 'repeat', frame_num)
            
            out.write(frame)
        
        out.release()
        
        # Combine with audio
        print("  🎵 Adding themed audio...")
        ffmpeg_cmd = [
            'ffmpeg', '-y',
            '-i', str(temp_video),
            '-i', str(audio_file),
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-shortest',
            str(final_video)
        ]
        
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            temp_video.unlink()
            print(f"  🎊 Enhanced video created: {final_video}")
            return str(final_video)
        else:
            print(f"  ❌ Error: {result.stderr}")
            return str(temp_video)
    
    def create_enhanced_audio(self, text, output_file):
        """Create enhanced audio with espeak"""
        cmd = [
            'espeak',
            '-v', 'en+f3',
            '-s', '160',
            '-p', '50',
            '-a', '200',
            '-g', '8',
            '-w', output_file,
            text
        ]
        
        try:
            subprocess.run(cmd, check=True)
            return True
        except:
            return False
    
    def generate_all_enhanced_videos(self):
        """Generate all enhanced ABC videos"""
        print("🌟 Creating Enhanced ABC Video Collection!")
        print("=" * 60)
        
        # Generate enhanced scripts
        scripts = self.generate_enhanced_abc_scripts()
        
        created_videos = []
        
        for theme_name, script_text in scripts:
            theme_title = self.themes[theme_name]['name']
            
            try:
                video_path = self.create_enhanced_video(theme_name, script_text, theme_title)
                if video_path:
                    created_videos.append(video_path)
                    
            except Exception as e:
                print(f"❌ Error creating {theme_name}: {e}")
        
        print(f"\n🎊 Enhanced Video Collection Complete!")
        print(f"✅ Created {len(created_videos)} themed educational videos")
        print("\n📁 Enhanced Videos:")
        for video in created_videos:
            print(f"  🎬 {video}")
        
        return created_videos

def main():
    """Generate enhanced ABC videos"""
    generator = AdvancedABCVideoGenerator()
    videos = generator.generate_all_enhanced_videos()
    
    print(f"\n🌟 Enhanced ABC Video Collection Ready!")
    print(f"📊 {len(videos)} themed educational videos created")
    print("🎯 Features: Animal themes, Space exploration, Food kitchen!")

if __name__ == "__main__":
    main()
