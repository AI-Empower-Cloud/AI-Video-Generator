#!/usr/bin/env python3
"""
🎥 Real ABC Video Generator with Actual Singing
Create videos with real spoken alphabet and synchronized lyrics
"""

import cv2
import numpy as np
import soundfile as sf
from pathlib import Path
import math
import subprocess
import os

class RealABCVideoGenerator:
    """Generate videos with real ABC singing and lyrics display"""
    
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
            'background': (240, 248, 255),  # Alice blue
            'primary': (255, 140, 0),       # Dark orange
            'secondary': (255, 20, 147),    # Deep pink
            'accent': (50, 205, 50),        # Lime green
            'text': (25, 25, 112),          # Midnight blue
            'white': (255, 255, 255),
            'yellow': (0, 255, 255),
            'red': (0, 0, 255),
            'blue': (255, 0, 0),
            'green': (0, 255, 0),
            'purple': (255, 0, 255),
            'lyrics_bg': (50, 50, 50),      # Dark gray
            'lyrics_text': (255, 255, 255)  # White text
        }
        
        # Video configurations with real audio files
        self.video_configs = [
            {
                'audio_file': 'abc_voice_teacher_ms_smith.wav',
                'title': 'Teacher Ms. Smith - Learning Together',
                'description': 'Professional teacher with slow, clear pronunciation',
                'lyrics_style': 'educational',
                'character_type': 'teacher_female'
            },
            {
                'audio_file': 'abc_voice_lily_age_5.wav',
                'title': 'Lily (Age 5) - Excited Learning',
                'description': 'Sweet little girl excited about learning ABCs',
                'lyrics_style': 'child_excited',
                'character_type': 'child_girl'
            },
            {
                'audio_file': 'abc_voice_tommy_age_6.wav',
                'title': 'Tommy (Age 6) - Energetic Boy',
                'description': 'Energetic boy having fun with alphabet',
                'lyrics_style': 'child_excited',
                'character_type': 'child_boy'
            },
            {
                'audio_file': 'abc_voice_grandma_mary.wav',
                'title': 'Grandma Mary - Gentle Bedtime',
                'description': 'Gentle grandmother voice for calm learning',
                'lyrics_style': 'gentle',
                'character_type': 'grandma'
            },
            {
                'audio_file': 'abc_voice_teacher_lesson.wav',
                'title': 'Complete ABC Lesson',
                'description': 'Full educational lesson with examples',
                'lyrics_style': 'educational',
                'character_type': 'teacher_lesson'
            }
        ]
        
        # Lyrics that match the audio (simplified for display)
        self.lyrics_display = {
            'educational': [
                "Let's learn the alphabet together!",
                "A... B... C... D... E... F... G...",
                "H... I... J... K... L... M... N... O... P...",
                "Q... R... S... T... U... V...",
                "W... X... Y... and Z!",
                "Great job! Now you know your ABCs!"
            ],
            'child_excited': [
                "A B C D E F G!",
                "H I J K L M N O P!",
                "Q R S! T U V!",
                "W X Y and Z!",
                "Yay! Now I know my ABCs!",
                "Let's sing it again!"
            ],
            'gentle': [
                "A, B, C, D, E, F, G,",
                "H, I, J, K, L, M, N, O, P,",
                "Q, R, S, T, U, V,",
                "W, X, Y, and Z.",
                "Now close your eyes",
                "and dream of ABCs."
            ]
        }
    
    def create_animated_background(self, frame_num):
        """Create animated background with floating elements"""
        frame = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Animated gradient
        wave_offset = frame_num * 0.02
        for y in range(self.height):
            wave = math.sin(y * 0.005 + wave_offset) * 20
            gradient_color = int(240 + wave)
            frame[y, :, 0] = min(255, max(200, gradient_color))
            frame[y, :, 1] = min(255, max(210, gradient_color + 8))
            frame[y, :, 2] = min(255, max(220, gradient_color + 15))
        
        # Floating alphabet letters
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i, letter in enumerate(letters[:8]):  # Show 8 floating letters
            angle = frame_num * 0.01 + i * 0.8
            x = int(100 + i * 200 + math.sin(angle) * 30)
            y = int(200 + math.cos(angle + i) * 50)
            
            if 0 < x < self.width - 100 and 0 < y < self.height - 100:
                # Draw floating letter
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_size = 1.5
                alpha = 0.3
                color = self.colors['accent']
                
                cv2.putText(frame, letter, (x, y), font, font_size, color, 3)
        
        return frame
    
    def draw_title_section(self, frame, title, subtitle=""):
        """Draw title and subtitle"""
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        # Main title
        title_size = 2.5
        title_thickness = 6
        (text_width, text_height), _ = cv2.getTextSize(title, font, title_size, title_thickness)
        title_x = (self.width - text_width) // 2
        title_y = 120
        
        # Title shadow
        cv2.putText(frame, title, (title_x + 3, title_y + 3), font, title_size, 
                   (100, 100, 100), title_thickness)
        # Main title
        cv2.putText(frame, title, (title_x, title_y), font, title_size, 
                   self.colors['primary'], title_thickness)
        
        # Subtitle
        if subtitle:
            sub_size = 1.2
            sub_thickness = 3
            (sub_width, sub_height), _ = cv2.getTextSize(subtitle, font, sub_size, sub_thickness)
            sub_x = (self.width - sub_width) // 2
            sub_y = title_y + 60
            
            cv2.putText(frame, subtitle, (sub_x, sub_y), font, sub_size, 
                       self.colors['secondary'], sub_thickness)
        
        return frame
    
    def draw_alphabet_display(self, frame, current_time, audio_duration):
        """Draw alphabet letters with highlighting based on audio progress"""
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        # Calculate which letters to highlight based on time
        progress = current_time / audio_duration if audio_duration > 0 else 0
        letters_to_show = int(progress * len(letters))
        
        # Grid layout for alphabet
        cols = 6
        rows = 5
        start_x = 200
        start_y = 300
        spacing_x = 250
        spacing_y = 120
        
        for i, letter in enumerate(letters):
            col = i % cols
            row = i // cols
            x = start_x + col * spacing_x
            y = start_y + row * spacing_y
            
            # Check if we're within bounds
            if x > self.width - 100 or y > self.height - 100:
                continue
            
            # Determine if this letter should be highlighted
            is_current = i == letters_to_show
            is_past = i < letters_to_show
            
            # Choose colors
            if is_current:
                bg_color = self.colors['yellow']
                text_color = self.colors['red']
                size = 80
            elif is_past:
                bg_color = self.colors['green']
                text_color = self.colors['white']
                size = 70
            else:
                bg_color = self.colors['white']
                text_color = self.colors['text']
                size = 60
            
            # Draw letter background circle
            cv2.circle(frame, (x, y), size, bg_color, -1)
            cv2.circle(frame, (x, y), size, self.colors['text'], 3)
            
            # Draw the letter
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_size = 2.0
            font_thickness = 6
            
            (text_width, text_height), _ = cv2.getTextSize(letter, font, font_size, font_thickness)
            text_x = x - text_width // 2
            text_y = y + text_height // 2
            
            cv2.putText(frame, letter, (text_x, text_y), font, font_size, text_color, font_thickness)
        
        return frame
    
    def draw_lyrics_overlay(self, frame, lyrics, current_time, audio_duration):
        """Draw lyrics overlay with timing"""
        if not lyrics:
            return frame
        
        # Calculate which lyric line to show
        lines_count = len(lyrics)
        if lines_count == 0:
            return frame
        
        progress = current_time / audio_duration if audio_duration > 0 else 0
        current_line_index = int(progress * lines_count)
        current_line_index = min(current_line_index, lines_count - 1)
        
        # Create lyrics background
        lyrics_y_start = self.height - 200
        lyrics_height = 150
        
        # Semi-transparent background
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, lyrics_y_start), (self.width, self.height), 
                     self.colors['lyrics_bg'], -1)
        frame = cv2.addWeighted(frame, 0.7, overlay, 0.3, 0)
        
        # Draw current lyric line
        if current_line_index < len(lyrics):
            current_text = lyrics[current_line_index]
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_size = 1.8
            font_thickness = 4
            
            (text_width, text_height), _ = cv2.getTextSize(current_text, font, font_size, font_thickness)
            text_x = (self.width - text_width) // 2
            text_y = lyrics_y_start + 80
            
            # Draw text shadow
            cv2.putText(frame, current_text, (text_x + 2, text_y + 2), font, font_size, 
                       (0, 0, 0), font_thickness)
            # Draw main text
            cv2.putText(frame, current_text, (text_x, text_y), font, font_size, 
                       self.colors['lyrics_text'], font_thickness)
        
        # Show progress indicator
        progress_width = int(self.width * 0.8)
        progress_x = (self.width - progress_width) // 2
        progress_y = self.height - 50
        
        # Progress bar background
        cv2.rectangle(frame, (progress_x, progress_y - 10), 
                     (progress_x + progress_width, progress_y + 10), 
                     self.colors['white'], -1)
        
        # Progress bar fill
        fill_width = int(progress_width * progress)
        cv2.rectangle(frame, (progress_x, progress_y - 10), 
                     (progress_x + fill_width, progress_y + 10), 
                     self.colors['primary'], -1)
        
        return frame
    
    def create_abc_video(self, config):
        """Create a single ABC video with real singing"""
        audio_file = self.audio_dir / config['audio_file']
        
        if not audio_file.exists():
            print(f"❌ Audio file not found: {audio_file}")
            return None
        
        print(f"🎬 Creating video: {config['title']}")
        print(f"🎵 Audio: {audio_file}")
        
        # Load audio to get duration
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
        video_filename = f"abc_real_singing_{config['character_type']}.mp4"
        video_path = self.output_dir / video_filename
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(str(video_path), fourcc, self.fps, (self.width, self.height))
        
        # Get lyrics for this style
        lyrics = self.lyrics_display.get(config['lyrics_style'], self.lyrics_display['educational'])
        
        # Generate frames
        for frame_num in range(total_frames):
            current_time = frame_num / self.fps
            
            # Create base frame
            frame = self.create_animated_background(frame_num)
            
            # Add title
            frame = self.draw_title_section(frame, "🎵 ABC Song", config['description'])
            
            # Add alphabet display
            frame = self.draw_alphabet_display(frame, current_time, audio_duration)
            
            # Add lyrics overlay
            frame = self.draw_lyrics_overlay(frame, lyrics, current_time, audio_duration)
            
            # Write frame
            video_writer.write(frame)
            
            # Progress indicator
            if frame_num % 60 == 0:  # Every 2 seconds
                progress = (frame_num / total_frames) * 100
                print(f"📹 Progress: {progress:.1f}% ({frame_num}/{total_frames} frames)")
        
        # Release video writer
        video_writer.release()
        print(f"✅ Video created: {video_path}")
        
        # Combine video with audio using ffmpeg
        final_video_path = self.output_dir / f"abc_real_singing_{config['character_type']}_with_audio.mp4"
        
        try:
            print("🎬 Combining video with audio...")
            subprocess.run([
                'ffmpeg', '-y',
                '-i', str(video_path),
                '-i', str(audio_file),
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-shortest',
                str(final_video_path)
            ], check=True, capture_output=True)
            
            print(f"✅ Final video with audio: {final_video_path}")
            
            # Remove the video-only file
            if video_path.exists():
                video_path.unlink()
            
            return str(final_video_path)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error combining audio and video: {e}")
            return str(video_path)  # Return video without audio
    
    def generate_all_videos(self):
        """Generate all ABC videos with real singing"""
        print("🎥 Real ABC Video Generator - Actual Singing Edition")
        print("=" * 70)
        
        videos_created = []
        
        for config in self.video_configs:
            try:
                video_path = self.create_abc_video(config)
                if video_path:
                    videos_created.append({
                        'path': video_path,
                        'title': config['title'],
                        'description': config['description']
                    })
                    print()  # Blank line between videos
                    
            except Exception as e:
                print(f"❌ Error creating video {config['title']}: {e}")
        
        print("🎉 Real ABC Video Collection Complete!")
        print("=" * 70)
        print(f"✅ Created {len(videos_created)} videos with real singing")
        
        for i, video in enumerate(videos_created, 1):
            print(f"\n🎥 Video {i}: {video['title']}")
            print(f"   📁 {video['path']}")
            print(f"   📝 {video['description']}")
        
        print(f"\n📁 All videos saved to: {self.output_dir}")
        print("🎯 Perfect for educational content with real voices!")
        print("\n🎥 Your Real ABC Video Collection is Ready!")
        print("✨ Educational videos with actual spoken alphabet letters!")
        print("🏫 Perfect for classrooms, apps, and real learning!")
        
        return videos_created

def main():
    """Generate all real ABC videos"""
    generator = RealABCVideoGenerator()
    generator.generate_all_videos()

if __name__ == "__main__":
    main()
