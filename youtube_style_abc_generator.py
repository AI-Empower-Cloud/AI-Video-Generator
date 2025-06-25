#!/usr/bin/env python3
"""
📺 YouTube-Style ABC Video Generator
Create professional TV-quality educational videos with automatic animations
"""

import cv2
import numpy as np
import soundfile as sf
from pathlib import Path
import random
import math
import subprocess
import os
import json
import time

class YouTubeStyleABCGenerator:
    """Generate professional YouTube-style ABC educational videos"""
    
    def __init__(self):
        self.output_dir = Path("video_output")
        self.output_dir.mkdir(exist_ok=True)
        self.audio_dir = Path("audio_output")
        
        # Professional video settings (YouTube optimized)
        self.width = 1920  # Full HD
        self.height = 1080
        self.fps = 30
        
        # Professional color palette
        self.colors = {
            'sky_blue': (255, 200, 135),
            'grass_green': (100, 255, 100),
            'sun_yellow': (0, 255, 255),
            'rainbow_red': (0, 0, 255),
            'rainbow_orange': (0, 165, 255),
            'rainbow_purple': (255, 0, 255),
            'cloud_white': (255, 255, 255),
            'text_dark': (50, 50, 50),
            'letter_glow': (255, 255, 0),
            'character_skin': (220, 180, 140),
            'character_shirt': (0, 150, 255),
            'background_gradient_1': (255, 240, 200),
            'background_gradient_2': (200, 230, 255)
        }
        
        # Animation states
        self.animation_frame = 0
        self.letter_animations = {}
        self.character_position = {'x': 200, 'y': 600, 'bounce': 0}
        
        # Professional fonts and sizes
        self.fonts = {
            'title': cv2.FONT_HERSHEY_DUPLEX,
            'letter': cv2.FONT_HERSHEY_SIMPLEX,
            'subtitle': cv2.FONT_HERSHEY_COMPLEX
        }
        
        # Letter timing for synchronization
        self.letter_timings = {
            'A': (0.5, 1.0), 'B': (1.2, 1.7), 'C': (1.9, 2.4), 'D': (2.6, 3.1),
            'E': (3.3, 3.8), 'F': (4.0, 4.5), 'G': (4.7, 5.2), 'H': (5.4, 5.9),
            'I': (6.1, 6.6), 'J': (6.8, 7.3), 'K': (7.5, 8.0), 'L': (8.2, 8.7),
            'M': (8.9, 9.4), 'N': (9.6, 10.1), 'O': (10.3, 10.8), 'P': (11.0, 11.5),
            'Q': (11.7, 12.2), 'R': (12.4, 12.9), 'S': (13.1, 13.6), 'T': (13.8, 14.3),
            'U': (14.5, 15.0), 'V': (15.2, 15.7), 'W': (15.9, 16.4), 'X': (16.6, 17.1),
            'Y': (17.3, 17.8), 'Z': (18.0, 18.5)
        }
        
        # Character animations for different emotions
        self.character_expressions = {
            'happy': {'eye_y': -5, 'mouth_curve': 15, 'arm_angle': 20},
            'excited': {'eye_y': -8, 'mouth_curve': 20, 'arm_angle': 45},
            'teaching': {'eye_y': 0, 'mouth_curve': 5, 'arm_angle': 30},
            'celebrating': {'eye_y': -10, 'mouth_curve': 25, 'arm_angle': 60}
        }
    
    def create_animated_background(self, frame_num, total_frames):
        """Create animated background like TV shows"""
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Animated gradient background
        time_factor = frame_num / total_frames
        gradient_shift = int(50 * math.sin(time_factor * 4 * math.pi))
        
        for y in range(self.height):
            for x in range(self.width):
                # Create moving gradient
                r = int(200 + 55 * math.sin((x + y + gradient_shift) * 0.01))
                g = int(220 + 35 * math.cos((x - gradient_shift) * 0.008))
                b = int(255 - 30 * math.sin((y + gradient_shift) * 0.012))
                
                frame[y, x] = [max(0, min(255, b)), max(0, min(255, g)), max(0, min(255, r))]
        
        # Add animated clouds
        self.draw_animated_clouds(frame, frame_num)
        
        # Add animated sun
        self.draw_animated_sun(frame, frame_num)
        
        # Add rainbow
        self.draw_rainbow(frame, frame_num)
        
        return frame
    
    def draw_animated_clouds(self, frame, frame_num):
        """Draw moving clouds"""
        cloud_positions = [
            (100 + (frame_num * 2) % (self.width + 200), 100),
            (300 + (frame_num * 1.5) % (self.width + 200), 150),
            (500 + (frame_num * 2.5) % (self.width + 200), 80)
        ]
        
        for x, y in cloud_positions:
            if x > self.width + 100:
                x -= self.width + 300
            
            # Draw fluffy cloud
            cv2.circle(frame, (int(x), int(y)), 40, self.colors['cloud_white'], -1)
            cv2.circle(frame, (int(x-20), int(y+10)), 35, self.colors['cloud_white'], -1)
            cv2.circle(frame, (int(x+20), int(y+10)), 35, self.colors['cloud_white'], -1)
            cv2.circle(frame, (int(x+10), int(y-15)), 30, self.colors['cloud_white'], -1)
    
    def draw_animated_sun(self, frame, frame_num):
        """Draw animated sun with rays"""
        sun_x, sun_y = 1700, 200
        sun_radius = 80
        
        # Sun body
        cv2.circle(frame, (sun_x, sun_y), sun_radius, self.colors['sun_yellow'], -1)
        
        # Animated sun rays
        ray_length = 120
        num_rays = 12
        for i in range(num_rays):
            angle = (i * 2 * math.pi / num_rays) + (frame_num * 0.05)
            start_x = sun_x + int((sun_radius + 10) * math.cos(angle))
            start_y = sun_y + int((sun_radius + 10) * math.sin(angle))
            end_x = sun_x + int(ray_length * math.cos(angle))
            end_y = sun_y + int(ray_length * math.sin(angle))
            
            cv2.line(frame, (start_x, start_y), (end_x, end_y), self.colors['sun_yellow'], 8)
        
        # Sun face
        # Eyes
        cv2.circle(frame, (sun_x - 25, sun_y - 20), 8, (0, 0, 0), -1)
        cv2.circle(frame, (sun_x + 25, sun_y - 20), 8, (0, 0, 0), -1)
        
        # Smile
        cv2.ellipse(frame, (sun_x, sun_y + 10), (40, 25), 0, 0, 180, (0, 0, 0), 6)
    
    def draw_rainbow(self, frame, frame_num):
        """Draw animated rainbow"""
        center_x, center_y = self.width // 2, self.height - 100
        colors = [
            (0, 0, 255),    # Red
            (0, 165, 255),  # Orange
            (0, 255, 255),  # Yellow
            (0, 255, 0),    # Green
            (255, 0, 0),    # Blue
            (255, 0, 255),  # Purple
        ]
        
        # Animated rainbow appearance
        rainbow_progress = min(1.0, frame_num / 100.0)
        
        for i, color in enumerate(colors):
            radius = 300 - (i * 25)
            thickness = 20
            
            if rainbow_progress > i * 0.1:
                current_progress = min(1.0, (rainbow_progress - i * 0.1) * 10)
                end_angle = int(180 * current_progress)
                
                if end_angle > 0:
                    cv2.ellipse(frame, (center_x, center_y), (radius, radius), 
                              0, 0, end_angle, color, thickness)
    
    def draw_animated_character(self, frame, frame_num, expression='happy'):
        """Draw animated TV-style character"""
        char_x = self.character_position['x']
        char_y = self.character_position['y']
        
        # Bouncing animation
        bounce = int(15 * math.sin(frame_num * 0.2))
        char_y += bounce
        
        # Get expression
        expr = self.character_expressions.get(expression, self.character_expressions['happy'])
        
        # Character body
        body_center = (char_x, char_y)
        
        # Head
        cv2.circle(frame, (char_x, char_y - 100), 60, self.colors['character_skin'], -1)
        cv2.circle(frame, (char_x, char_y - 100), 60, (0, 0, 0), 3)
        
        # Eyes
        eye_y_offset = expr['eye_y']
        cv2.circle(frame, (char_x - 20, char_y - 110 + eye_y_offset), 8, (0, 0, 0), -1)
        cv2.circle(frame, (char_x + 20, char_y - 110 + eye_y_offset), 8, (0, 0, 0), -1)
        
        # Eye sparkles
        cv2.circle(frame, (char_x - 17, char_y - 113 + eye_y_offset), 2, (255, 255, 255), -1)
        cv2.circle(frame, (char_x + 23, char_y - 113 + eye_y_offset), 2, (255, 255, 255), -1)
        
        # Mouth
        mouth_curve = expr['mouth_curve']
        cv2.ellipse(frame, (char_x, char_y - 80), (25, mouth_curve), 0, 0, 180, (0, 0, 0), 3)
        
        # Hair
        cv2.ellipse(frame, (char_x, char_y - 130), (70, 40), 0, 0, 180, (139, 69, 19), -1)
        
        # Body
        cv2.rectangle(frame, (char_x - 40, char_y - 40), (char_x + 40, char_y + 60), 
                     self.colors['character_shirt'], -1)
        
        # Arms with animation
        arm_angle = expr['arm_angle']
        arm_length = 50
        
        # Left arm
        arm_end_x = char_x - 40 - int(arm_length * math.cos(math.radians(arm_angle + frame_num * 5)))
        arm_end_y = char_y - int(arm_length * math.sin(math.radians(arm_angle + frame_num * 5)))
        cv2.line(frame, (char_x - 40, char_y - 20), (arm_end_x, arm_end_y), 
                self.colors['character_skin'], 12)
        cv2.circle(frame, (arm_end_x, arm_end_y), 15, self.colors['character_skin'], -1)
        
        # Right arm
        arm_end_x = char_x + 40 + int(arm_length * math.cos(math.radians(arm_angle - frame_num * 5)))
        arm_end_y = char_y - int(arm_length * math.sin(math.radians(arm_angle - frame_num * 5)))
        cv2.line(frame, (char_x + 40, char_y - 20), (arm_end_x, arm_end_y), 
                self.colors['character_skin'], 12)
        cv2.circle(frame, (arm_end_x, arm_end_y), 15, self.colors['character_skin'], -1)
        
        # Legs
        cv2.line(frame, (char_x - 20, char_y + 60), (char_x - 20, char_y + 120), 
                self.colors['character_skin'], 15)
        cv2.line(frame, (char_x + 20, char_y + 60), (char_x + 20, char_y + 120), 
                self.colors['character_skin'], 15)
        
        # Shoes
        cv2.ellipse(frame, (char_x - 20, char_y + 130), (25, 10), 0, 0, 180, (0, 0, 0), -1)
        cv2.ellipse(frame, (char_x + 20, char_y + 130), (25, 10), 0, 0, 180, (0, 0, 0), -1)
    
    def draw_animated_letter(self, frame, letter, current_time, frame_num):
        """Draw animated letter with TV-style effects"""
        if letter not in self.letter_timings:
            return
        
        start_time, end_time = self.letter_timings[letter]
        
        # Check if letter should be visible
        if current_time < start_time:
            return
        
        # Letter position (grid layout)
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        letter_index = letters.index(letter)
        
        # 6 columns, multiple rows
        col = letter_index % 6
        row = letter_index // 6
        
        base_x = 600 + col * 200
        base_y = 200 + row * 150
        
        # Animation effects
        appear_progress = min(1.0, (current_time - start_time) * 4)
        
        if appear_progress <= 0:
            return
        
        # Scale animation
        scale = 0.3 + (appear_progress * 0.7)
        
        # Position animation (letter drops in)
        drop_offset = int(100 * (1 - appear_progress) ** 2)
        letter_y = base_y - drop_offset
        
        # Color animation
        glow_intensity = int(255 * appear_progress)
        letter_color = (min(255, glow_intensity), min(255, glow_intensity), 255)
        
        # Letter size
        font_size = int(4 * scale)
        thickness = max(2, int(8 * scale))
        
        # Draw letter shadow
        shadow_offset = max(2, int(5 * scale))
        cv2.putText(frame, letter, (base_x + shadow_offset, letter_y + shadow_offset), 
                   self.fonts['letter'], font_size, (50, 50, 50), thickness)
        
        # Draw main letter
        cv2.putText(frame, letter, (base_x, letter_y), 
                   self.fonts['letter'], font_size, letter_color, thickness)
        
        # Add sparkle effect when letter appears
        if current_time >= start_time and current_time <= start_time + 0.5:
            sparkle_progress = (current_time - start_time) * 2
            num_sparkles = int(5 * sparkle_progress)
            
            for i in range(num_sparkles):
                sparkle_x = base_x + random.randint(-50, 50)
                sparkle_y = letter_y + random.randint(-50, 50)
                sparkle_size = random.randint(3, 8)
                
                cv2.circle(frame, (sparkle_x, sparkle_y), sparkle_size, 
                          self.colors['letter_glow'], -1)
        
        # Highlight current letter being spoken
        if start_time <= current_time <= end_time:
            # Pulsing glow effect
            glow_radius = int(80 + 20 * math.sin(frame_num * 0.5))
            glow_color = (100, 255, 255)  # Bright yellow glow
            
            # Create glow effect
            overlay = frame.copy()
            cv2.circle(overlay, (base_x + 50, letter_y - 30), glow_radius, glow_color, -1)
            cv2.addWeighted(frame, 0.8, overlay, 0.2, 0, frame)
    
    def draw_progress_bar(self, frame, current_time, total_time):
        """Draw animated progress bar"""
        bar_x = 100
        bar_y = self.height - 80
        bar_width = self.width - 200
        bar_height = 20
        
        # Background bar
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), 
                     (100, 100, 100), -1)
        
        # Progress bar
        progress = min(1.0, current_time / total_time)
        progress_width = int(bar_width * progress)
        
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + progress_width, bar_y + bar_height), 
                     (0, 255, 0), -1)
        
        # Progress text
        progress_text = f"{int(progress * 100)}%"
        cv2.putText(frame, progress_text, (bar_x + bar_width + 20, bar_y + 15), 
                   self.fonts['subtitle'], 0.7, (255, 255, 255), 2)
    
    def create_youtube_style_video(self, audio_file, title, character_expression='happy'):
        """Create professional YouTube-style educational video"""
        print(f"🎬 Creating YouTube-style video: {title}")
        
        # Load audio to get duration
        audio_data, sample_rate = sf.read(audio_file)
        duration = len(audio_data) / sample_rate
        total_frames = int(duration * self.fps)
        
        print(f"  📊 Duration: {duration:.1f}s, Frames: {total_frames}")
        
        # Output video file
        video_filename = f"youtube_style_{Path(audio_file).stem}.mp4"
        temp_video = self.output_dir / f"temp_{video_filename}"
        final_video = self.output_dir / video_filename
        
        # Video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(temp_video), fourcc, self.fps, (self.width, self.height))
        
        print("  🎨 Generating frames...")
        
        for frame_num in range(total_frames):
            current_time = frame_num / self.fps
            progress = int((frame_num / total_frames) * 100)
            
            if frame_num % 60 == 0:  # Update every 2 seconds
                print(f"    📹 Progress: {progress}% ({frame_num}/{total_frames})")
            
            # Create base animated background
            frame = self.create_animated_background(frame_num, total_frames)
            
            # Draw animated character
            self.draw_animated_character(frame, frame_num, character_expression)
            
            # Draw title
            title_y = 60
            cv2.putText(frame, title, (50, title_y), self.fonts['title'], 2.0, 
                       (255, 255, 255), 6)
            cv2.putText(frame, title, (50, title_y), self.fonts['title'], 2.0, 
                       (0, 100, 255), 4)
            
            # Draw all letters with animation
            letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            for letter in letters:
                self.draw_animated_letter(frame, letter, current_time, frame_num)
            
            # Draw progress bar
            self.draw_progress_bar(frame, current_time, duration)
            
            # Add frame to video
            out.write(frame)
        
        out.release()
        print(f"  ✅ Video frames created: {temp_video}")
        
        # Combine with audio using ffmpeg
        print("  🎵 Adding audio...")
        try:
            # Use ffmpeg to combine video and audio
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
                # Cleanup temp file
                if temp_video.exists():
                    temp_video.unlink()
                
                print(f"  🎉 YouTube-style video created: {final_video}")
                return str(final_video)
            else:
                print(f"  ❌ FFmpeg error: {result.stderr}")
                return str(temp_video)
            
        except Exception as e:
            print(f"  ❌ Error combining audio: {e}")
            return str(temp_video)
    
    def generate_all_youtube_videos(self):
        """Generate all YouTube-style ABC videos"""
        print("📺 Creating Professional YouTube-Style ABC Videos!")
        print("=" * 70)
        
        # Find all voice files
        voice_files = list(self.audio_dir.glob("abc_voice_*.wav"))
        
        if not voice_files:
            print("❌ No voice files found! Run create_real_singing_abc.py first.")
            return []
        
        videos_created = []
        
        # Video configurations
        video_configs = [
            ("teacher_ms_smith", "🍎 Learn ABC with Ms. Smith", "teaching"),
            ("teacher_mr_johnson", "📚 ABC Adventure with Mr. Johnson", "happy"),
            ("lily_age_5", "🌸 Lily's ABC Song", "excited"),
            ("tommy_age_6", "⚽ Tommy's Alphabet Fun", "celebrating"),
            ("grandma_mary", "👵 Grandma Mary's Gentle ABCs", "happy"),
            ("teacher_lesson", "🏫 Professional ABC Lesson", "teaching"),
            ("emma_classic", "🎀 Emma's Classic ABC", "happy"),
            ("teacher_excited", "🎉 Exciting ABC Learning", "excited")
        ]
        
        for suffix, title, expression in video_configs:
            audio_file = self.audio_dir / f"abc_voice_{suffix}.wav"
            
            if audio_file.exists():
                try:
                    video_path = self.create_youtube_style_video(
                        str(audio_file), title, expression
                    )
                    videos_created.append(video_path)
                    
                except Exception as e:
                    print(f"❌ Error creating video for {suffix}: {e}")
            else:
                print(f"⚠️  Audio file not found: {audio_file}")
        
        print(f"\n🎊 YouTube-Style Video Generation Complete!")
        print(f"✅ Created {len(videos_created)} professional videos")
        print("\n📁 Generated Videos:")
        for video in videos_created:
            print(f"  🎬 {video}")
        
        print(f"\n🎯 Ready for YouTube upload!")
        print("📺 Professional TV-quality educational content created!")
        
        return videos_created

def main():
    """Generate YouTube-style ABC videos"""
    generator = YouTubeStyleABCGenerator()
    
    # Generate all professional videos
    videos = generator.generate_all_youtube_videos()
    
    print(f"\n🌟 Your YouTube-ready ABC videos are complete!")
    print(f"📊 {len(videos)} professional educational videos created")
    print("🎬 Perfect for YouTube, TV, and educational platforms!")

if __name__ == "__main__":
    main()
