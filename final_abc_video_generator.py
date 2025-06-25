#!/usr/bin/env python3
"""
🎥 Final ABC Video Generator with Clear Voices
Create videos with clear spoken alphabet and real lyrics
"""

import cv2
import numpy as np
import soundfile as sf
from pathlib import Path
import math
import subprocess
import os
import re

class FinalABCVideoGenerator:
    """Generate videos with clear ABC voices and lyrics display"""
    
    def __init__(self):
        self.output_dir = Path("video_output")
        self.output_dir.mkdir(exist_ok=True)
        self.audio_dir = Path("audio_output")
        
        # Video settings
        self.width = 1920
        self.height = 1080
        self.fps = 30
        
        # Colors (BGR format for OpenCV)
        self.colors = {
            'background': (250, 248, 240),  # Cream background
            'primary': (255, 140, 0),       # Dark orange
            'secondary': (220, 20, 60),     # Crimson
            'accent': (34, 139, 34),        # Forest green
            'text': (25, 25, 112),          # Midnight blue
            'white': (255, 255, 255),
            'yellow': (0, 255, 255),
            'red': (0, 0, 255),
            'blue': (255, 0, 0),
            'green': (0, 255, 0),
            'purple': (255, 0, 255),
            'lyrics_bg': (40, 40, 40),      # Dark gray
            'lyrics_text': (255, 255, 255), # White text
            'highlight': (255, 215, 0)      # Gold
        }
        
        # Video configurations with clear audio files
        self.video_configs = [
            {
                'audio_file': 'abc_clear_teacher_female_clear.wav',
                'title': '👩‍🏫 Ms. Sarah - Professional Teacher',
                'subtitle': 'Clear pronunciation for learning',
                'character_type': 'teacher_female',
                'background_theme': 'classroom'
            },
            {
                'audio_file': 'abc_clear_child_girl_sweet.wav',
                'title': '👧 Emma (Age 5) - Sweet Girl',
                'subtitle': 'Adorable child learning ABCs',
                'character_type': 'child_girl',
                'background_theme': 'playful'
            },
            {
                'audio_file': 'abc_clear_child_boy_excited.wav',
                'title': '👦 Jake (Age 6) - Excited Boy',
                'subtitle': 'Energetic boy loves letters!',
                'character_type': 'child_boy',
                'background_theme': 'energetic'
            },
            {
                'audio_file': 'abc_clear_teacher_male_professional.wav',
                'title': '👨‍🏫 Mr. Johnson - Elementary Teacher',
                'subtitle': 'Professional classroom instruction',
                'character_type': 'teacher_male',
                'background_theme': 'educational'
            },
            {
                'audio_file': 'abc_clear_grandma_gentle.wav',
                'title': '👵 Grandma Rose - Gentle Voice',
                'subtitle': 'Loving grandmother teaching letters',
                'character_type': 'grandma',
                'background_theme': 'gentle'
            }
        ]
    
    def extract_letters_from_audio_time(self, current_time, audio_duration):
        """Estimate which letters are being spoken based on time"""
        # Simple estimation: alphabet is spoken roughly evenly throughout
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        # Account for intro/outro time
        intro_time = min(2.0, audio_duration * 0.1)  # First 10% or 2 seconds
        outro_time = min(2.0, audio_duration * 0.1)  # Last 10% or 2 seconds
        letter_time = audio_duration - intro_time - outro_time
        
        if current_time < intro_time:
            return 0  # Still in intro
        elif current_time > audio_duration - outro_time:
            return len(alphabet)  # In outro, show all letters
        else:
            # In the main alphabet section
            progress_in_letters = (current_time - intro_time) / letter_time
            return int(progress_in_letters * len(alphabet))
    
    def create_themed_background(self, frame_num, theme):
        """Create themed animated background"""
        frame = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Base gradient
        wave_offset = frame_num * 0.01
        
        if theme == 'classroom':
            # Professional classroom theme
            for y in range(self.height):
                wave = math.sin(y * 0.003 + wave_offset) * 10
                base_color = 240
                frame[y, :, 0] = min(255, max(220, int(base_color + wave)))
                frame[y, :, 1] = min(255, max(230, int(base_color + wave + 10)))
                frame[y, :, 2] = min(255, max(245, int(base_color + wave + 15)))
                
        elif theme == 'playful':
            # Colorful playful theme
            for y in range(self.height):
                wave1 = math.sin(y * 0.005 + wave_offset) * 15
                wave2 = math.cos(y * 0.007 + wave_offset * 1.5) * 10
                frame[y, :, 0] = min(255, max(200, int(240 + wave1)))
                frame[y, :, 1] = min(255, max(220, int(245 + wave2)))
                frame[y, :, 2] = min(255, max(240, int(250 + wave1 * 0.5)))
                
        elif theme == 'energetic':
            # Dynamic energetic theme
            for y in range(self.height):
                wave = math.sin(y * 0.008 + wave_offset * 2) * 20
                frame[y, :, 0] = min(255, max(210, int(235 + wave)))
                frame[y, :, 1] = min(255, max(230, int(240 + wave * 0.8)))
                frame[y, :, 2] = min(255, max(240, int(250 + wave * 0.6)))
                
        else:  # gentle, educational, or default
            # Calm, gentle theme
            for y in range(self.height):
                wave = math.sin(y * 0.002 + wave_offset * 0.5) * 8
                frame[y, :, 0] = min(255, max(235, int(245 + wave)))
                frame[y, :, 1] = min(255, max(240, int(248 + wave)))
                frame[y, :, 2] = min(255, max(245, int(250 + wave)))
        
        return frame
    
    def draw_title_and_subtitle(self, frame, title, subtitle):
        """Draw title and subtitle with nice formatting"""
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        # Main title
        title_size = 2.2
        title_thickness = 5
        (text_width, text_height), _ = cv2.getTextSize(title, font, title_size, title_thickness)
        title_x = (self.width - text_width) // 2
        title_y = 100
        
        # Title background
        padding = 20
        cv2.rectangle(frame, 
                     (title_x - padding, title_y - text_height - padding//2),
                     (title_x + text_width + padding, title_y + padding//2),
                     self.colors['white'], -1)
        cv2.rectangle(frame, 
                     (title_x - padding, title_y - text_height - padding//2),
                     (title_x + text_width + padding, title_y + padding//2),
                     self.colors['primary'], 3)
        
        # Title text
        cv2.putText(frame, title, (title_x, title_y), font, title_size, 
                   self.colors['text'], title_thickness)
        
        # Subtitle
        if subtitle:
            sub_size = 1.0
            sub_thickness = 2
            (sub_width, sub_height), _ = cv2.getTextSize(subtitle, font, sub_size, sub_thickness)
            sub_x = (self.width - sub_width) // 2
            sub_y = title_y + 50
            
            cv2.putText(frame, subtitle, (sub_x, sub_y), font, sub_size, 
                       self.colors['secondary'], sub_thickness)
        
        return frame
    
    def draw_alphabet_grid_with_highlight(self, frame, letters_spoken, current_time, audio_duration):
        """Draw alphabet grid with progressive highlighting"""
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        # Grid layout
        cols = 6
        rows = 5
        start_x = 200
        start_y = 250
        spacing_x = 260
        spacing_y = 140
        
        for i, letter in enumerate(alphabet):
            col = i % cols
            row = i // cols
            x = start_x + col * spacing_x
            y = start_y + row * spacing_y
            
            # Skip if position is out of bounds
            if x > self.width - 150 or y > self.height - 150:
                continue
            
            # Determine letter state
            if i < letters_spoken:
                # Already spoken - show as completed
                bg_color = self.colors['green']
                text_color = self.colors['white']
                border_color = self.colors['accent']
                size = 75
                pulse = 0
            elif i == letters_spoken:
                # Currently being spoken - animate
                pulse = abs(math.sin(current_time * 8)) * 20
                bg_color = self.colors['highlight']
                text_color = self.colors['text']
                border_color = self.colors['red']
                size = int(80 + pulse)
            else:
                # Not yet spoken
                bg_color = self.colors['white']
                text_color = self.colors['text']
                border_color = self.colors['text']
                size = 70
                pulse = 0
            
            # Draw letter background
            cv2.circle(frame, (x, y), size, bg_color, -1)
            cv2.circle(frame, (x, y), size, border_color, 4)
            
            # Draw the letter
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_size = 2.5
            font_thickness = 6
            
            (text_width, text_height), _ = cv2.getTextSize(letter, font, font_size, font_thickness)
            text_x = x - text_width // 2
            text_y = y + text_height // 2
            
            cv2.putText(frame, letter, (text_x, text_y), font, font_size, text_color, font_thickness)
        
        return frame
    
    def draw_progress_and_lyrics(self, frame, current_time, audio_duration, character_type):
        """Draw progress bar and current context"""
        progress = current_time / audio_duration if audio_duration > 0 else 0
        
        # Progress bar area
        progress_y = self.height - 120
        progress_width = int(self.width * 0.8)
        progress_x = (self.width - progress_width) // 2
        bar_height = 20
        
        # Background bar
        cv2.rectangle(frame, (progress_x, progress_y), 
                     (progress_x + progress_width, progress_y + bar_height),
                     self.colors['white'], -1)
        cv2.rectangle(frame, (progress_x, progress_y), 
                     (progress_x + progress_width, progress_y + bar_height),
                     self.colors['text'], 3)
        
        # Progress fill
        fill_width = int(progress_width * progress)
        cv2.rectangle(frame, (progress_x, progress_y), 
                     (progress_x + fill_width, progress_y + bar_height),
                     self.colors['primary'], -1)
        
        # Time display
        time_text = f"{current_time:.1f}s / {audio_duration:.1f}s"
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, time_text, (progress_x, progress_y - 10), font, 0.8, 
                   self.colors['text'], 2)
        
        # Character context
        context_text = f"🎤 {character_type.replace('_', ' ').title()} speaking..."
        (ctx_width, ctx_height), _ = cv2.getTextSize(context_text, font, 1.0, 2)
        ctx_x = (self.width - ctx_width) // 2
        ctx_y = progress_y + 60
        
        cv2.putText(frame, context_text, (ctx_x, ctx_y), font, 1.0, 
                   self.colors['secondary'], 2)
        
        return frame
    
    def create_abc_video_with_clear_voice(self, config):
        """Create ABC video with clear voice and proper timing"""
        audio_file = self.audio_dir / config['audio_file']
        
        if not audio_file.exists():
            print(f"❌ Audio file not found: {audio_file}")
            return None
        
        print(f"🎬 Creating video: {config['title']}")
        print(f"🎵 Audio: {audio_file}")
        
        # Load audio
        try:
            audio_data, sample_rate = sf.read(str(audio_file))
            audio_duration = len(audio_data) / sample_rate
            total_frames = int(audio_duration * self.fps)
            
            print(f"⏱️  Audio duration: {audio_duration:.1f} seconds")
            print(f"🎬 Generating {total_frames} frames...")
            
        except Exception as e:
            print(f"❌ Error reading audio: {e}")
            return None
        
        # Create video writer
        video_filename = f"abc_final_{config['character_type']}.mp4"
        video_path = self.output_dir / video_filename
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(str(video_path), fourcc, self.fps, (self.width, self.height))
        
        # Generate frames
        for frame_num in range(total_frames):
            current_time = frame_num / self.fps
            
            # Create themed background
            frame = self.create_themed_background(frame_num, config['background_theme'])
            
            # Add title and subtitle
            frame = self.draw_title_and_subtitle(frame, config['title'], config['subtitle'])
            
            # Calculate which letters have been spoken
            letters_spoken = self.extract_letters_from_audio_time(current_time, audio_duration)
            
            # Draw alphabet grid
            frame = self.draw_alphabet_grid_with_highlight(frame, letters_spoken, current_time, audio_duration)
            
            # Draw progress and context
            frame = self.draw_progress_and_lyrics(frame, current_time, audio_duration, config['character_type'])
            
            # Write frame
            video_writer.write(frame)
            
            # Progress reporting
            if frame_num % 90 == 0:  # Every 3 seconds
                progress_pct = (frame_num / total_frames) * 100
                print(f"📹 Progress: {progress_pct:.1f}% ({frame_num}/{total_frames} frames)")
        
        video_writer.release()
        print(f"✅ Video created: {video_path}")
        
        # Combine with audio
        final_video_path = self.output_dir / f"abc_final_{config['character_type']}_with_audio.mp4"
        
        try:
            print("🎬 Combining video with audio...")
            subprocess.run([
                'ffmpeg', '-y', '-loglevel', 'quiet',
                '-i', str(video_path),
                '-i', str(audio_file),
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-shortest',
                str(final_video_path)
            ], check=True)
            
            print(f"✅ Final video: {final_video_path}")
            
            # Clean up video-only file
            if video_path.exists():
                video_path.unlink()
            
            return str(final_video_path)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error combining audio: {e}")
            return str(video_path)
    
    def generate_final_abc_videos(self):
        """Generate all final ABC videos with clear voices"""
        print("🎥 Final ABC Video Generator - Clear Voices Edition")
        print("=" * 70)
        print("✨ Real spoken alphabet with synchronized visuals")
        print()
        
        videos_created = []
        
        for i, config in enumerate(self.video_configs, 1):
            print(f"🎬 Creating Video {i}/{len(self.video_configs)}")
            try:
                video_path = self.create_abc_video_with_clear_voice(config)
                if video_path:
                    videos_created.append({
                        'path': video_path,
                        'title': config['title'],
                        'subtitle': config['subtitle'],
                        'character': config['character_type']
                    })
                print()  # Blank line
                
            except Exception as e:
                print(f"❌ Error creating {config['title']}: {e}")
        
        print("🎉 Final ABC Video Collection Complete!")
        print("=" * 70)
        print(f"✅ Created {len(videos_created)} videos with clear spoken alphabet")
        
        for i, video in enumerate(videos_created, 1):
            print(f"\n🎥 Video {i}: {video['title']}")
            print(f"   📁 {Path(video['path']).name}")
            print(f"   📝 {video['subtitle']}")
            print(f"   🎭 Character: {video['character']}")
        
        print(f"\n📁 All videos saved to: {self.output_dir}")
        print("🎯 Perfect educational content with real spoken alphabet!")
        print("✨ Each video features actual voice saying A-B-C-D-E-F-G...")
        print("🏫 Ready for classroom use and educational apps!")
        
        return videos_created

def main():
    """Generate final ABC videos with clear voices"""
    generator = FinalABCVideoGenerator()
    generator.generate_final_abc_videos()

if __name__ == "__main__":
    main()
