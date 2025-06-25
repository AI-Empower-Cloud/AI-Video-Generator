#!/usr/bin/env python3
"""
🎥 ABC Video Generator - Kids & Teacher Edition
Create engaging educational videos with kids and teacher voices
"""

import cv2
import numpy as np
import soundfile as sf
from pathlib import Path
import random
import math
import subprocess
import os

class ABCVideoGenerator:
    """Generate educational ABC videos with kids and teacher voices"""
    
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
            'primary': (255, 165, 0),       # Orange
            'secondary': (255, 20, 147),    # Deep pink
            'accent': (50, 205, 50),        # Lime green
            'text': (25, 25, 112),          # Midnight blue
            'white': (255, 255, 255),
            'yellow': (0, 255, 255),
            'red': (0, 0, 255),
            'blue': (255, 0, 0),
            'green': (0, 255, 0),
            'purple': (255, 0, 255)
        }
        
        # Letter positions for alphabet display
        self.letter_positions = self._generate_letter_positions()
        
        # ABC song lyrics for different styles
        self.lyrics_database = {
            'abc_real_girl_singing.wav': [
                "A, B, C, D, E, F, G,",
                "H, I, J, K, L, M, N, O, P,",
                "Q, R, S, T, U, V,",
                "W, X, Y, and Z!",
                "",
                "Now I know my A, B, Cs,",
                "Next time won't you sing with me?"
            ],
            'abc_real_boy_excited.wav': [
                "ABCDEFG! HIJKLMNOP!",
                "QRS! TUV! WXY and Z!",
                "Now I know my ABCs!",
                "Next time won't you sing with me!"
            ],
            'abc_real_teacher_lesson.wav': [
                "Let's learn the alphabet together!",
                "A is for Apple, B is for Ball,",
                "C is for Cat, D is for Dog,",
                "But let's sing them all!",
                "",
                "A, B, C, D, E, F, G,",
                "H, I, J, K, L, M, N, O, P,",
                "Q, R, S, T, U, V,",
                "W, X, Y, and Z!",
                "",
                "Great job learning your ABCs!"
            ],
            'abc_real_grandma_gentle.wav': [
                "A... B... C... D... E... F... G...",
                "H... I... J... K... L... M... N... O... P...",
                "Q... R... S... T... U... V...",
                "W... X... Y... and Z!",
                "",
                "Now I know my A B Cs!",
                "Next time won't you sing with me?"
            ],
            'abc_real_male_teacher.wav': [
                "A B C D E F G",
                "H I J K L M N O P",
                "Q R S T U V",
                "W X Y and Z",
                "",
                "ABC song is fun for me!",
                "Let's sing it again, one two three!"
            ],
            'abc_real_kids_chorus_clear.wav': [
                "A B C D E F G",
                "H I J K L M N O P",
                "Q R S T U V",
                "W X Y and Z",
                "",
                "ABC song is fun for me!",
                "Let's sing it again, one two three!"
            ]
        }
        
    def _generate_letter_positions(self):
        """Generate positions for alphabet letters in a grid"""
        positions = {}
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        # 6 rows x 5 columns (26 letters + 4 extras)
        cols = 6
        rows = 5
        start_x = 200
        start_y = 200
        spacing_x = 250
        spacing_y = 150
        
        for i, letter in enumerate(letters):
            col = i % cols
            row = i // cols
            x = start_x + col * spacing_x
            y = start_y + row * spacing_y
            positions[letter] = (x, y)
            
        return positions
    
    def create_background_frame(self):
        """Create animated background frame"""
        frame = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Add gradient
        for y in range(self.height):
            gradient_color = int(240 + 15 * math.sin(y * 0.01))
            frame[y, :, 0] = min(255, gradient_color)
            frame[y, :, 1] = min(255, gradient_color + 8)
            frame[y, :, 2] = min(255, gradient_color + 15)
        
        return frame
    
    def draw_title(self, frame, title, subtitle=""):
        """Draw animated title"""
        # Main title
        font = cv2.FONT_HERSHEY_SIMPLEX
        title_size = 3.0
        title_thickness = 8
        
        # Get text size for centering
        (text_width, text_height), _ = cv2.getTextSize(title, font, title_size, title_thickness)
        title_x = (self.width - text_width) // 2
        title_y = 100
        
        # Draw title shadow
        cv2.putText(frame, title, (title_x + 5, title_y + 5), font, title_size, 
                   (50, 50, 50), title_thickness)
        
        # Draw main title with gradient effect
        cv2.putText(frame, title, (title_x, title_y), font, title_size, 
                   self.colors['primary'], title_thickness)
        
        # Subtitle
        if subtitle:
            subtitle_size = 1.5
            subtitle_thickness = 3
            (sub_width, sub_height), _ = cv2.getTextSize(subtitle, font, subtitle_size, subtitle_thickness)
            sub_x = (self.width - sub_width) // 2
            sub_y = title_y + 80
            
            cv2.putText(frame, subtitle, (sub_x, sub_y), font, subtitle_size, 
                       self.colors['secondary'], subtitle_thickness)
        
        return frame
    
    def draw_letter(self, frame, letter, x, y, size=100, color=None, highlight=False):
        """Draw an animated letter"""
        if color is None:
            color = self.colors['text']
            
        if highlight:
            # Draw highlight circle
            cv2.circle(frame, (x, y), size + 20, self.colors['yellow'], -1)
            cv2.circle(frame, (x, y), size + 20, self.colors['accent'], 5)
            color = self.colors['red']
        
        # Draw letter background circle
        cv2.circle(frame, (x, y), size, self.colors['white'], -1)
        cv2.circle(frame, (x, y), size, color, 5)
        
        # Draw the letter
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 3.0
        font_thickness = 8
        
        (text_width, text_height), _ = cv2.getTextSize(letter, font, font_size, font_thickness)
        text_x = x - text_width // 2
        text_y = y + text_height // 2
        
        cv2.putText(frame, letter, (text_x, text_y), font, font_size, color, font_thickness)
        
        return frame
    
    def draw_alphabet_grid(self, frame, current_letter=None, progress=0):
        """Draw the full alphabet in a grid"""
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        for i, letter in enumerate(letters):
            if letter in self.letter_positions:
                x, y = self.letter_positions[letter]
                
                # Determine if this letter should be highlighted
                highlight = (letter == current_letter)
                
                # Add animation based on progress
                if progress > i / len(letters):
                    # Letter has been "learned"
                    color = self.colors['green']
                elif letter == current_letter:
                    # Current letter being taught
                    color = self.colors['red']
                else:
                    # Not yet learned
                    color = self.colors['text']
                
                self.draw_letter(frame, letter, x, y, size=60, color=color, highlight=highlight)
        
        return frame
    
    def draw_lyrics(self, frame, lyrics, progress):
        """Draw current lyrics on screen with karaoke-style highlighting"""
        if not lyrics:
            return frame
            
        # Handle both string and list formats
        if isinstance(lyrics, str):
            lines = lyrics.strip().split('\n')
        else:
            lines = lyrics  # Already a list
            
        if not lines:
            return frame
            
        # Calculate which line should be shown based on progress
        line_progress = progress * len(lines)
        current_line_index = int(line_progress)
        
        if current_line_index >= len(lines):
            current_line_index = len(lines) - 1
            
        current_line = lines[current_line_index].strip() if lines[current_line_index] else ""
        if not current_line:
            return frame
            
        # Draw lyrics background
        lyrics_y = self.height - 200
        cv2.rectangle(frame, (50, lyrics_y - 50), (self.width - 50, lyrics_y + 100), 
                     (0, 0, 0, 100), -1)  # Semi-transparent black background
        
        # Draw current line
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 1.5
        font_thickness = 3
        
        (text_width, text_height), _ = cv2.getTextSize(current_line, font, font_size, font_thickness)
        text_x = (self.width - text_width) // 2
        text_y = lyrics_y
        
        # Draw text shadow
        cv2.putText(frame, current_line, (text_x + 3, text_y + 3), font, font_size, 
                   (0, 0, 0), font_thickness)
        
        # Draw main text
        cv2.putText(frame, current_line, (text_x, text_y), font, font_size, 
                   self.colors['white'], font_thickness)
        
        # Show next line preview if available
        if current_line_index + 1 < len(lines):
            next_line = lines[current_line_index + 1].strip() if lines[current_line_index + 1] else ""
            if next_line:
                font_size_small = 1.0
                font_thickness_small = 2
                (next_width, next_height), _ = cv2.getTextSize(next_line, font, font_size_small, font_thickness_small)
                next_x = (self.width - next_width) // 2
                next_y = text_y + 50
                
                cv2.putText(frame, next_line, (next_x, next_y), font, font_size_small, 
                           self.colors['secondary'], font_thickness_small)
        
        return frame
    
    def draw_floating_elements(self, frame, frame_number):
        """Draw floating educational elements"""
        # Floating stars
        for i in range(10):
            x = int(100 + 300 * math.sin(frame_number * 0.02 + i))
            y = int(100 + 50 * math.cos(frame_number * 0.03 + i))
            
            if 0 <= x < self.width and 0 <= y < self.height:
                # Draw star
                star_points = []
                for j in range(5):
                    angle = j * 4 * math.pi / 5 + frame_number * 0.1
                    star_x = x + int(20 * math.cos(angle))
                    star_y = y + int(20 * math.sin(angle))
                    star_points.append([star_x, star_y])
                
                star_points = np.array(star_points, np.int32)
                cv2.fillPoly(frame, [star_points], self.colors['yellow'])
        
        return frame
    
    def create_abc_video(self, audio_file, title, output_name, duration=None):
        """Create ABC video with specified audio and lyrics"""
        
        print(f"🎥 Creating ABC Video: {title}")
        print(f"🎵 Audio: {audio_file}")
        
        # Load audio to get duration
        try:
            audio_data, sample_rate = sf.read(audio_file)
            if duration is None:
                duration = len(audio_data) / sample_rate
        except Exception as e:
            print(f"❌ Error loading audio: {e}")
            duration = 30  # Default duration
        
        print(f"⏱️  Video duration: {duration:.1f} seconds")
        
        # Get lyrics for this audio file
        audio_filename = Path(audio_file).name
        lyrics = self.lyrics_database.get(audio_filename, [])
        
        # Video setup
        video_path = self.output_dir / f"{output_name}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(str(video_path), fourcc, self.fps, (self.width, self.height))
        
        total_frames = int(duration * self.fps)
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        print(f"🎬 Generating {total_frames} frames...")
        
        for frame_num in range(total_frames):
            # Create base frame
            frame = self.create_background_frame()
            
            # Calculate progress
            progress = frame_num / total_frames
            
            # Determine current letter being highlighted
            letter_index = int(progress * len(letters)) % len(letters)
            current_letter = letters[letter_index]
            
            # Draw title (first 3 seconds)
            if frame_num < self.fps * 3:
                frame = self.draw_title(frame, "🎵 ABC Learning Song 🎵", title)
            else:
                # Draw smaller title at top
                font = cv2.FONT_HERSHEY_SIMPLEX
                title_text = f"🎵 {title}"
                title_size = 1.2
                title_thickness = 3
                (title_width, title_height), _ = cv2.getTextSize(title_text, font, title_size, title_thickness)
                title_x = (self.width - title_width) // 2
                title_y = 50
                
                cv2.putText(frame, title_text, (title_x, title_y), font, title_size, 
                           self.colors['primary'], title_thickness)
            
            # Draw alphabet grid
            frame = self.draw_alphabet_grid(frame, current_letter, progress)
            
            # Draw floating elements
            frame = self.draw_floating_elements(frame, frame_num)
            
            # Add current letter display (large) - after title phase
            if frame_num >= self.fps * 3:
                center_x, center_y = self.width // 2, 400
                self.draw_letter(frame, current_letter, center_x, center_y, size=120, 
                               color=self.colors['primary'], highlight=True)
                
                # Add "Current Letter" text
                font = cv2.FONT_HERSHEY_SIMPLEX
                text = f"Learning Letter: {current_letter}"
                text_size = 1.8
                text_thickness = 4
                (text_width, text_height), _ = cv2.getTextSize(text, font, text_size, text_thickness)
                text_x = (self.width - text_width) // 2
                text_y = center_y - 150
                
                cv2.putText(frame, text, (text_x, text_y), font, text_size, 
                           self.colors['secondary'], text_thickness)
            
            # Draw lyrics (after title phase)
            if frame_num >= self.fps * 3 and lyrics:
                # Adjust progress for lyrics (starts after title)
                lyrics_progress = (frame_num - self.fps * 3) / (total_frames - self.fps * 3)
                frame = self.draw_lyrics(frame, lyrics, lyrics_progress)
            
            # Add progress indicator
            progress_width = int(progress * (self.width - 100))
            cv2.rectangle(frame, (50, self.height - 30), (50 + progress_width, self.height - 10), 
                         self.colors['accent'], -1)
            cv2.rectangle(frame, (50, self.height - 30), (self.width - 50, self.height - 10), 
                         self.colors['text'], 2)
            
            # Write frame
            video_writer.write(frame)
            
            # Progress indicator
            if frame_num % (self.fps * 2) == 0:
                print(f"📹 Progress: {progress*100:.1f}% ({frame_num}/{total_frames} frames)")
        
        video_writer.release()
        print(f"✅ Video created: {video_path}")
        
        # Combine video with audio using ffmpeg
        final_video_path = self.output_dir / f"{output_name}_with_audio.mp4"
        
        try:
            cmd = [
                'ffmpeg', '-y',  # -y to overwrite output files
                '-i', str(video_path),  # Video input
                '-i', str(audio_file),  # Audio input
                '-c:v', 'libx264',      # Video codec
                '-c:a', 'aac',          # Audio codec
                '-shortest',            # Finish when shortest input ends
                str(final_video_path)
            ]
            
            print("🎬 Combining video with audio...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Final video with audio: {final_video_path}")
                # Remove temporary video without audio
                video_path.unlink()
                return final_video_path
            else:
                print(f"❌ FFmpeg error: {result.stderr}")
                print(f"📁 Video without audio saved as: {video_path}")
                return video_path
                
        except FileNotFoundError:
            print("⚠️  FFmpeg not found. Video created without audio.")
            print(f"📁 Video file: {video_path}")
            print(f"🎵 Audio file: {audio_file}")
            print("💡 You can combine them manually with video editing software.")
            return video_path
    
    def create_video_collection(self):
        """Create a collection of ABC videos with different voices"""
        
        print("🎥 ABC Video Generator - Kids & Teacher Edition")
        print("=" * 60)
        
        # Define videos to create with enhanced real singing voices
        videos = [
            {
                'audio': 'abc_real_girl_singing.wav',
                'title': '👧 Sweet Girl Singing ABC Song',
                'output': 'abc_video_real_girl_singing',
                'description': 'Sweet 5-year-old girl singing ABC song with real melody and lyrics'
            },
            {
                'audio': 'abc_real_boy_excited.wav',
                'title': '👦 Excited Boy ABC Adventure',
                'output': 'abc_video_real_boy_excited',
                'description': 'Excited 6-year-old boy singing ABC song energetically with clear pronunciation'
            },
            {
                'audio': 'abc_real_teacher_lesson.wav',
                'title': '👩‍🏫 Teacher ABC Learning Lesson',
                'output': 'abc_video_real_teacher_lesson',
                'description': 'Kind female teacher leading complete ABC learning lesson with examples'
            },
            {
                'audio': 'abc_real_grandma_gentle.wav',
                'title': '👵 Gentle Grandma ABC Story',
                'output': 'abc_video_real_grandma_gentle',
                'description': 'Gentle grandmother teaching ABCs slowly and clearly - perfect bedtime learning'
            },
            {
                'audio': 'abc_real_male_teacher.wav',
                'title': '👨‍🏫 Friendly Male Teacher',
                'output': 'abc_video_real_male_teacher',
                'description': 'Friendly male teacher singing traditional ABC song with children'
            },
            {
                'audio': 'abc_real_kids_chorus_clear.wav',
                'title': '🎭 Clear Kids Chorus',
                'output': 'abc_video_real_kids_chorus',
                'description': 'Crystal clear kids chorus singing the classic ABC song with perfect pronunciation'
            }
        ]
        
        created_videos = []
        
        for video_info in videos:
            audio_path = self.audio_dir / video_info['audio']
            
            if audio_path.exists():
                print(f"\n🎬 Creating video: {video_info['title']}")
                print(f"📝 {video_info['description']}")
                
                video_path = self.create_abc_video(
                    audio_path,
                    video_info['title'],
                    video_info['output']
                )
                
                created_videos.append({
                    'title': video_info['title'],
                    'description': video_info['description'],
                    'file': video_path,
                    'audio_source': video_info['audio']
                })
            else:
                print(f"❌ Audio file not found: {audio_path}")
        
        print("\n🎉 ABC Video Collection Complete!")
        print("=" * 60)
        print(f"✅ Created {len(created_videos)} educational videos")
        
        for video in created_videos:
            print(f"\n🎥 {video['title']}")
            print(f"   📁 {video['file'].name}")
            print(f"   📝 {video['description']}")
            print(f"   🎵 Audio: {video['audio_source']}")
        
        print(f"\n📁 All videos saved to: {self.output_dir}")
        print("🎯 Perfect for educational content and classroom use!")
        
        return created_videos

def main():
    generator = ABCVideoGenerator()
    videos = generator.create_video_collection()
    
    print("\n🎥 Your ABC Video Collection is Ready!")
    print("✨ Educational videos with kids and teacher voices!")
    print("🏫 Perfect for classrooms, apps, and learning!")

if __name__ == "__main__":
    main()
