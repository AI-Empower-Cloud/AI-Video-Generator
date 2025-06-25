#!/usr/bin/env python3
"""
📺 YouTube-Style Professional ABC Video Generator
Create TV-quality educational videos with professional animations and voices
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

class YouTubeProfessionalABCGenerator:
    """Generate professional YouTube-style ABC educational videos"""
    
    def __init__(self):
        self.output_dir = Path("video_output")
        self.output_dir.mkdir(exist_ok=True)
        self.audio_dir = Path("audio_output")
        
        # Professional YouTube video settings
        self.width = 1920
        self.height = 1080
        self.fps = 30
        
        # Professional TV-style colors
        self.colors = {
            'sky_gradient_1': (255, 220, 180),
            'sky_gradient_2': (200, 240, 255),
            'grass_green': (100, 200, 100),
            'sun_yellow': (0, 255, 255),
            'cloud_white': (255, 255, 255),
            'rainbow_colors': [
                (0, 0, 255),    # Red
                (0, 165, 255),  # Orange  
                (0, 255, 255),  # Yellow
                (0, 255, 0),    # Green
                (255, 0, 0),    # Blue
                (255, 0, 255),  # Purple
            ],
            'character_skin': (220, 180, 140),
            'character_hair': (139, 69, 19),
            'character_shirt_blue': (255, 150, 0),
            'character_shirt_pink': (255, 192, 203),
            'letter_colors': [
                (0, 0, 255),     # Red
                (0, 255, 0),     # Green  
                (255, 0, 0),     # Blue
                (0, 255, 255),   # Yellow
                (255, 0, 255),   # Magenta
                (255, 165, 0),   # Orange
            ],
            'text_shadow': (50, 50, 50),
            'white': (255, 255, 255),
            'black': (0, 0, 0)
        }
        
        # Animation parameters
        self.animation_frame = 0
        self.floating_elements = []
        
        # Letter display timing (based on typical ABC song timing)
        self.letter_sequence = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
    def create_tv_background(self, frame_num, total_frames):
        """Create animated TV-style background"""
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Animated sky gradient
        for y in range(self.height // 2):
            ratio = y / (self.height // 2)
            color1 = self.colors['sky_gradient_1']
            color2 = self.colors['sky_gradient_2']
            
            # Animate gradient
            time_shift = math.sin(frame_num * 0.02) * 20
            b = int(color1[0] * (1 - ratio) + color2[0] * ratio + time_shift)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio + time_shift)
            r = int(color1[2] * (1 - ratio) + color2[2] * ratio + time_shift)
            
            frame[y, :] = [max(0, min(255, b)), max(0, min(255, g)), max(0, min(255, r))]
        
        # Ground
        ground_color = self.colors['grass_green']
        frame[self.height // 2:, :] = ground_color
        
        # Add animated elements
        self.add_animated_clouds(frame, frame_num)
        self.add_animated_sun(frame, frame_num)
        self.add_rainbow_arch(frame, frame_num, total_frames)
        self.add_floating_musical_notes(frame, frame_num)
        
        return frame
    
    def add_animated_clouds(self, frame, frame_num):
        """Add moving clouds"""
        cloud_positions = [
            (200 + (frame_num * 1) % (self.width + 300), 150),
            (400 + (frame_num * 1.5) % (self.width + 300), 100),
            (600 + (frame_num * 0.8) % (self.width + 300), 180),
        ]
        
        for x, y in cloud_positions:
            if x > self.width + 150:
                x -= self.width + 450
            
            # Draw fluffy cloud shape
            cv2.ellipse(frame, (int(x), int(y)), (60, 30), 0, 0, 360, self.colors['cloud_white'], -1)
            cv2.ellipse(frame, (int(x-30), int(y+10)), (40, 25), 0, 0, 360, self.colors['cloud_white'], -1)
            cv2.ellipse(frame, (int(x+30), int(y+10)), (40, 25), 0, 0, 360, self.colors['cloud_white'], -1)
            cv2.ellipse(frame, (int(x), int(y-15)), (35, 20), 0, 0, 360, self.colors['cloud_white'], -1)
    
    def add_animated_sun(self, frame, frame_num):
        """Add animated sun with face"""
        sun_x, sun_y = 1650, 200
        sun_size = 70
        
        # Pulsing effect
        pulse = int(10 * math.sin(frame_num * 0.1))
        current_size = sun_size + pulse
        
        # Sun body
        cv2.circle(frame, (sun_x, sun_y), current_size, self.colors['sun_yellow'], -1)
        
        # Sun rays
        num_rays = 16
        ray_length = 40
        for i in range(num_rays):
            angle = (i * 2 * math.pi / num_rays) + (frame_num * 0.03)
            start_x = sun_x + int((current_size + 10) * math.cos(angle))
            start_y = sun_y + int((current_size + 10) * math.sin(angle))
            end_x = sun_x + int((current_size + ray_length) * math.cos(angle))
            end_y = sun_y + int((current_size + ray_length) * math.sin(angle))
            
            cv2.line(frame, (start_x, start_y), (end_x, end_y), self.colors['sun_yellow'], 6)
        
        # Sun face
        # Eyes
        cv2.circle(frame, (sun_x - 20, sun_y - 15), 6, self.colors['black'], -1)
        cv2.circle(frame, (sun_x + 20, sun_y - 15), 6, self.colors['black'], -1)
        
        # Eye sparkles
        cv2.circle(frame, (sun_x - 17, sun_y - 18), 2, self.colors['white'], -1)
        cv2.circle(frame, (sun_x + 23, sun_y - 18), 2, self.colors['white'], -1)
        
        # Smile
        cv2.ellipse(frame, (sun_x, sun_y + 5), (30, 20), 0, 0, 180, self.colors['black'], 4)
    
    def add_rainbow_arch(self, frame, frame_num, total_frames):
        """Add animated rainbow arch"""
        center_x = self.width // 2
        center_y = self.height - 50
        
        # Rainbow appears progressively
        appear_progress = min(1.0, frame_num / (total_frames * 0.3))
        
        for i, color in enumerate(self.colors['rainbow_colors']):
            radius = 400 - (i * 30)
            thickness = 25
            
            if appear_progress > i * 0.15:
                arc_progress = min(1.0, (appear_progress - i * 0.15) * 6)
                end_angle = int(180 * arc_progress)
                
                if end_angle > 5:
                    cv2.ellipse(frame, (center_x, center_y), (radius, radius), 
                              0, 0, end_angle, color, thickness)
    
    def add_floating_musical_notes(self, frame, frame_num):
        """Add floating musical notes"""
        notes = ['♪', '♫', '♬', '♩']
        positions = [
            (300 + int(50 * math.sin(frame_num * 0.05)), 300 + int(30 * math.cos(frame_num * 0.07))),
            (1200 + int(40 * math.cos(frame_num * 0.06)), 250 + int(25 * math.sin(frame_num * 0.08))),
            (800 + int(35 * math.sin(frame_num * 0.04)), 400 + int(20 * math.cos(frame_num * 0.09))),
        ]
        
        for i, (x, y) in enumerate(positions):
            note = notes[i % len(notes)]
            # Note: OpenCV doesn't support Unicode characters well, so we'll use circles instead
            size = int(15 + 5 * math.sin(frame_num * 0.1 + i))
            cv2.circle(frame, (x, y), size, (255, 100, 255), -1)
            cv2.circle(frame, (x, y), size, (255, 255, 255), 2)
    
    def draw_tv_character(self, frame, frame_num, character_type='teacher'):
        """Draw animated TV-style character"""
        if character_type == 'teacher':
            char_x, char_y = 300, 700
            shirt_color = self.colors['character_shirt_blue']
        elif character_type == 'girl':
            char_x, char_y = 250, 720
            shirt_color = self.colors['character_shirt_pink']
        else:  # boy
            char_x, char_y = 280, 710
            shirt_color = self.colors['character_shirt_blue']
        
        # Bouncing animation
        bounce = int(8 * math.sin(frame_num * 0.15))
        char_y += bounce
        
        # Head
        cv2.circle(frame, (char_x, char_y - 120), 50, self.colors['character_skin'], -1)
        cv2.circle(frame, (char_x, char_y - 120), 50, self.colors['black'], 2)
        
        # Hair
        if character_type == 'girl':
            # Long hair
            cv2.ellipse(frame, (char_x, char_y - 150), (60, 35), 0, 0, 180, self.colors['character_hair'], -1)
            cv2.ellipse(frame, (char_x - 40, char_y - 120), (20, 60), 0, 0, 360, self.colors['character_hair'], -1)
            cv2.ellipse(frame, (char_x + 40, char_y - 120), (20, 60), 0, 0, 360, self.colors['character_hair'], -1)
        else:
            # Short hair
            cv2.ellipse(frame, (char_x, char_y - 145), (55, 30), 0, 0, 180, self.colors['character_hair'], -1)
        
        # Eyes with animation
        eye_blink = 0 if (frame_num % 120) < 5 else 8
        cv2.circle(frame, (char_x - 15, char_y - 130), eye_blink, self.colors['black'], -1)
        cv2.circle(frame, (char_x + 15, char_y - 130), eye_blink, self.colors['black'], -1)
        
        if eye_blink > 0:
            # Eye sparkles
            cv2.circle(frame, (char_x - 12, char_y - 133), 2, self.colors['white'], -1)
            cv2.circle(frame, (char_x + 18, char_y - 133), 2, self.colors['white'], -1)
        
        # Mouth
        cv2.ellipse(frame, (char_x, char_y - 105), (15, 8), 0, 0, 180, self.colors['black'], 2)
        
        # Body
        cv2.rectangle(frame, (char_x - 35, char_y - 70), (char_x + 35, char_y + 50), shirt_color, -1)
        
        # Arms with gesturing animation
        arm_angle = 20 * math.sin(frame_num * 0.1)
        
        # Left arm
        arm_x = char_x - 35 + int(25 * math.cos(math.radians(30 + arm_angle)))
        arm_y = char_y - 30 + int(25 * math.sin(math.radians(30 + arm_angle)))
        cv2.line(frame, (char_x - 35, char_y - 30), (arm_x, arm_y), self.colors['character_skin'], 10)
        cv2.circle(frame, (arm_x, arm_y), 8, self.colors['character_skin'], -1)
        
        # Right arm
        arm_x = char_x + 35 + int(25 * math.cos(math.radians(150 - arm_angle)))
        arm_y = char_y - 30 + int(25 * math.sin(math.radians(150 - arm_angle)))
        cv2.line(frame, (char_x + 35, char_y - 30), (arm_x, arm_y), self.colors['character_skin'], 10)
        cv2.circle(frame, (arm_x, arm_y), 8, self.colors['character_skin'], -1)
        
        # Legs
        cv2.line(frame, (char_x - 15, char_y + 50), (char_x - 15, char_y + 100), self.colors['character_skin'], 12)
        cv2.line(frame, (char_x + 15, char_y + 50), (char_x + 15, char_y + 100), self.colors['character_skin'], 12)
        
        # Shoes
        cv2.ellipse(frame, (char_x - 15, char_y + 110), (20, 8), 0, 0, 180, self.colors['black'], -1)
        cv2.ellipse(frame, (char_x + 15, char_y + 110), (20, 8), 0, 0, 180, self.colors['black'], -1)
    
    def draw_alphabet_display(self, frame, current_time, total_time):
        """Draw animated alphabet letters"""
        letters_per_second = 26 / total_time  # Distribute 26 letters across total time
        
        for i, letter in enumerate(self.letter_sequence):
            letter_time = i / letters_per_second
            
            # Calculate position in grid
            col = i % 6
            row = i // 6
            
            x = 700 + col * 180
            y = 200 + row * 120
            
            # Letter animation based on timing
            if current_time >= letter_time:
                # Letter has appeared
                appear_progress = min(1.0, (current_time - letter_time) * 3)
                
                # Scale and position animation
                scale = 0.3 + appear_progress * 0.7
                font_size = scale * 3
                thickness = max(2, int(scale * 6))
                
                # Color cycling
                color_index = i % len(self.colors['letter_colors'])
                letter_color = self.colors['letter_colors'][color_index]
                
                # Highlight current letter being pronounced
                current_letter_index = int(current_time * letters_per_second)
                if i == current_letter_index:
                    # Add glow effect
                    glow_size = int(60 + 20 * math.sin(frame_num * 0.3))
                    overlay = frame.copy()
                    cv2.circle(overlay, (x + 30, y - 20), glow_size, (100, 255, 255), -1)
                    cv2.addWeighted(frame, 0.7, overlay, 0.3, 0, frame)
                    
                    # Make letter bigger and brighter
                    font_size *= 1.3
                    thickness = int(thickness * 1.5)
                    letter_color = (255, 255, 255)  # White for current letter
                
                # Draw letter shadow
                cv2.putText(frame, letter, (x + 3, y + 3), cv2.FONT_HERSHEY_SIMPLEX, 
                           font_size, self.colors['text_shadow'], thickness)
                
                # Draw main letter
                cv2.putText(frame, letter, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 
                           font_size, letter_color, thickness)
    
    def draw_title_and_progress(self, frame, title, current_time, total_time):
        """Draw animated title and progress"""
        # Title
        title_scale = 1.5 + 0.2 * math.sin(frame_num * 0.08)
        cv2.putText(frame, title, (50, 80), cv2.FONT_HERSHEY_DUPLEX, 
                   title_scale, self.colors['text_shadow'], 6)
        cv2.putText(frame, title, (50, 80), cv2.FONT_HERSHEY_DUPLEX, 
                   title_scale, self.colors['white'], 4)
        
        # Progress bar
        bar_x, bar_y = 50, self.height - 60
        bar_width, bar_height = self.width - 100, 20
        
        # Background
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), 
                     (100, 100, 100), -1)
        
        # Progress
        progress = current_time / total_time
        progress_width = int(bar_width * progress)
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + progress_width, bar_y + bar_height), 
                     (0, 255, 0), -1)
        
        # Progress text
        progress_text = f"Learning Progress: {int(progress * 100)}%"
        cv2.putText(frame, progress_text, (bar_x, bar_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.6, self.colors['white'], 2)
    
    def create_professional_youtube_video(self, audio_file, title, character_type='teacher'):
        """Create professional YouTube-style video"""
        print(f"📺 Creating YouTube video: {title}")
        
        # Load audio
        audio_data, sample_rate = sf.read(audio_file)
        duration = len(audio_data) / sample_rate
        total_frames = int(duration * self.fps)
        
        print(f"  📊 Duration: {duration:.1f}s, Frames: {total_frames}")
        
        # Output files
        video_name = f"youtube_professional_{Path(audio_file).stem}.mp4"
        temp_video = self.output_dir / f"temp_{video_name}"
        final_video = self.output_dir / video_name
        
        # Video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(temp_video), fourcc, self.fps, (self.width, self.height))
        
        print("  🎨 Creating professional TV-style animation...")
        
        global frame_num
        for frame_num in range(total_frames):
            current_time = frame_num / self.fps
            
            if frame_num % 90 == 0:  # Update every 3 seconds
                progress = int((frame_num / total_frames) * 100)
                print(f"    📹 Progress: {progress}% - Frame {frame_num}/{total_frames}")
            
            # Create TV-style background
            frame = self.create_tv_background(frame_num, total_frames)
            
            # Draw animated character
            self.draw_tv_character(frame, frame_num, character_type)
            
            # Draw animated alphabet
            self.draw_alphabet_display(frame, current_time, duration)
            
            # Draw title and progress
            self.draw_title_and_progress(frame, title, current_time, duration)
            
            # Write frame
            out.write(frame)
        
        out.release()
        print(f"  ✅ Animation complete: {temp_video}")
        
        # Combine with audio
        print("  🎵 Adding professional audio...")
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
            print(f"  🎊 YouTube video created: {final_video}")
            return str(final_video)
        else:
            print(f"  ❌ Audio error: {result.stderr}")
            return str(temp_video)
    
    def generate_all_youtube_videos(self):
        """Generate all professional YouTube videos"""
        print("📺 Creating Professional YouTube-Style ABC Educational Videos!")
        print("=" * 80)
        
        # Video configurations
        video_configs = [
            ('professional_teacher_female.wav', '🍎 Professional ABC Learning', 'teacher'),
            ('sweet_girl_lily.wav', '🌸 Sweet Lily\'s ABC Adventure', 'girl'),
            ('energetic_boy_tommy.wav', '⚽ Tommy\'s Exciting ABC Fun', 'boy'),
            ('classroom_teacher.wav', '🏫 Classroom ABC Lesson', 'teacher'),
            ('gentle_grandma_mary.wav', '👵 Grandma\'s Gentle ABC Story', 'teacher'),
            ('super_fun_abc.wav', '🎉 Super Fun ABC Party', 'boy'),
        ]
        
        created_videos = []
        
        for audio_filename, title, character_type in video_configs:
            audio_file = self.audio_dir / audio_filename
            
            if audio_file.exists():
                try:
                    video_path = self.create_professional_youtube_video(
                        str(audio_file), title, character_type
                    )
                    created_videos.append(video_path)
                    print()  # Add spacing between videos
                    
                except Exception as e:
                    print(f"❌ Error creating {title}: {e}")
            else:
                print(f"⚠️  Audio file not found: {audio_file}")
        
        print("🎊 Professional YouTube Video Generation Complete!")
        print(f"✅ Created {len(created_videos)} TV-quality educational videos")
        print("\n📁 YouTube-Ready Videos:")
        for video in created_videos:
            print(f"  📺 {video}")
        
        print(f"\n🌟 Perfect for YouTube, Educational Apps, and TV!")
        print("🎬 Professional quality with full ABC songs and animations!")
        
        return created_videos

def main():
    """Generate professional YouTube-style ABC videos"""
    generator = YouTubeProfessionalABCGenerator()
    
    # Generate all videos
    videos = generator.generate_all_youtube_videos()
    
    print(f"\n🎯 Your professional ABC video collection is ready!")
    print(f"📊 {len(videos)} YouTube-quality educational videos")
    print("📺 TV-style animations with full ABC songs!")

if __name__ == "__main__":
    main()
