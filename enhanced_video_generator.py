#!/usr/bin/env python3
"""
Enhanced Video Generation with Advanced Features
- Better character avatars
- Improved lip-sync
- Scene transitions
- Background effects
- Advanced audio integration
- Advanced character animations
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio
import random
import math
import os
import tempfile
from pathlib import Path

# Import the new audio and animation modules
try:
    from audio_integration import AdvancedAudioEngine
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("⚠️ Audio integration not available")

try:
    from advanced_animation import AdvancedAnimationEngine
    ANIMATION_AVAILABLE = True
except ImportError:
    ANIMATION_AVAILABLE = False
    print("⚠️ Advanced animation not available")

class AdvancedVideoGenerator:
    def __init__(self):
        self.colors = {
            'skin_tones': [(255, 220, 177), (240, 184, 160), (198, 134, 66), (161, 102, 94)],
            'hair_colors': [(139, 69, 19), (0, 0, 0), (255, 255, 0), (165, 42, 42)],
            'eye_colors': [(139, 69, 19), (0, 100, 0), (0, 0, 255), (128, 128, 128)],
            'backgrounds': [
                (135, 206, 235),  # Sky blue
                (34, 139, 34),    # Forest green
                (255, 192, 203),  # Pink
                (147, 112, 219),  # Purple
                (255, 165, 0)     # Orange
            ]
        }
        
        # Initialize audio and animation engines
        self.audio_engine = None
        self.animation_engine = None
        
        if AUDIO_AVAILABLE:
            try:
                self.audio_engine = AdvancedAudioEngine()
                print("✅ Audio engine initialized")
            except Exception as e:
                print(f"⚠️ Audio engine initialization failed: {e}")
        
        if ANIMATION_AVAILABLE:
            try:
                self.animation_engine = AdvancedAnimationEngine()
                print("✅ Animation engine initialized")
            except Exception as e:
                print(f"⚠️ Animation engine initialization failed: {e}")
    
    def generate_character_avatar(self, character_info, width=400, height=400):
        """Generate a unique avatar for each character."""
        # Create base image
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        center_x, center_y = width // 2, height // 2
        
        # Choose character attributes based on name
        name = character_info.get('name', 'Character')
        gender = character_info.get('gender', 'neutral')
        
        # Seed random based on character name for consistency
        random.seed(hash(name) % 1000)
        
        # Select colors
        skin_tone = random.choice(self.colors['skin_tones'])
        hair_color = random.choice(self.colors['hair_colors'])
        eye_color = random.choice(self.colors['eye_colors'])
        
        # Face size based on gender
        face_radius = 80 if gender == 'female' else 90
        
        # Draw face
        draw.ellipse([
            center_x - face_radius, center_y - face_radius,
            center_x + face_radius, center_y + face_radius
        ], fill=skin_tone, outline=(200, 150, 100), width=3)
        
        # Draw hair
        hair_radius = face_radius + 20
        if gender == 'female':
            # Longer hair for female characters
            draw.ellipse([
                center_x - hair_radius, center_y - hair_radius,
                center_x + hair_radius, center_y + hair_radius//2
            ], fill=hair_color)
        else:
            # Shorter hair for male characters
            draw.ellipse([
                center_x - hair_radius//2, center_y - hair_radius,
                center_x + hair_radius//2, center_y - hair_radius//4
            ], fill=hair_color)
        
        # Draw eyes
        eye_offset = face_radius // 2
        eye_radius = 12
        
        # Left eye
        draw.ellipse([
            center_x - eye_offset - eye_radius, center_y - eye_radius,
            center_x - eye_offset + eye_radius, center_y + eye_radius
        ], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
        draw.ellipse([
            center_x - eye_offset - eye_radius//2, center_y - eye_radius//2,
            center_x - eye_offset + eye_radius//2, center_y + eye_radius//2
        ], fill=eye_color)
        
        # Right eye
        draw.ellipse([
            center_x + eye_offset - eye_radius, center_y - eye_radius,
            center_x + eye_offset + eye_radius, center_y + eye_radius
        ], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
        draw.ellipse([
            center_x + eye_offset - eye_radius//2, center_y - eye_radius//2,
            center_x + eye_offset + eye_radius//2, center_y + eye_radius//2
        ], fill=eye_color)
        
        # Draw nose
        nose_y = center_y + 10
        draw.ellipse([
            center_x - 4, nose_y - 8,
            center_x + 4, nose_y + 8
        ], fill=tuple(max(0, c-20) for c in skin_tone))
        
        return img
    
    def generate_character_audio(self, character_name, text, voice_settings=None):
        """Generate audio for a character's dialogue."""
        if not self.audio_engine:
            return None
        
        try:
            # Create character info
            character_info = {
                'name': character_name,
                'gender': 'female' if 'alice' in character_name.lower() else 'male'
            }
            
            # Generate character voice
            audio_path = self.audio_engine.generate_character_voice(
                text=text,
                character_info=character_info,
                output_path=f"temp_voice_{character_name}_{hash(text) % 10000}.wav"
            )
            
            return audio_path
        except Exception as e:
            print(f"⚠️ Failed to generate audio for {character_name}: {e}")
            return None
    
    def generate_background_music(self, emotion, duration, style='orchestral'):
        """Generate background music based on emotion."""
        if not self.audio_engine:
            return None
        
        try:
            music_path = self.audio_engine.generate_background_music(
                emotion=emotion,
                duration=duration,
                output_path=f"temp_music_{emotion}_{hash(str(duration)) % 10000}.wav"
            )
            
            return music_path
        except Exception as e:
            print(f"⚠️ Failed to generate background music: {e}")
            return None
    
    def apply_advanced_animation(self, character_img, frame_idx, animation_type, emotion='neutral'):
        """Apply advanced animations to character."""
        if not self.animation_engine:
            return character_img
        
        try:
            # Create character rig for animation
            character_center = (100, 100)  # Center of the character image
            character_rig = self.animation_engine.generate_character_rig(
                character_center=character_center,
                character_size=(200, 200)
            )
            
            # Create animation sequence based on type
            if animation_type == 'walk_cycle':
                animation_frames = self.animation_engine.create_animation_sequence(
                    animation_type=self.animation_engine.AnimationType.WALK,
                    frame_count=8,
                    emotion=emotion
                )
            elif animation_type == 'gesture':
                animation_frames = self.animation_engine.create_animation_sequence(
                    animation_type=self.animation_engine.AnimationType.WAVE,
                    frame_count=8,
                    emotion=emotion
                )
            else:
                # Default idle animation
                animation_frames = self.animation_engine.create_animation_sequence(
                    animation_type=self.animation_engine.AnimationType.IDLE,
                    frame_count=8,
                    emotion=emotion
                )
            
            # Get the current frame from the animation sequence
            if animation_frames:
                current_frame_idx = frame_idx % len(animation_frames)
                keyframe = animation_frames[current_frame_idx]
                
                # Render the animated character
                animated_img = self.animation_engine.render_animated_character(
                    img=character_img,
                    character_rig=character_rig,
                    keyframe=keyframe
                )
                
                return animated_img
            else:
                return character_img
            
        except Exception as e:
            print(f"⚠️ Animation failed: {e}")
            return character_img
    
    def create_scene_background(self, scene_info, width, height):
        """Create background based on scene description."""
        description = scene_info.get('description', '').lower()
        emotion = scene_info.get('emotion', 'neutral')
        
        # Choose background based on scene content
        if any(word in description for word in ['forest', 'tree', 'nature']):
            bg_color = (34, 100, 34)  # Dark green
            # Add trees
            img = Image.new('RGB', (width, height), bg_color)
            draw = ImageDraw.Draw(img)
            for i in range(3):
                tree_x = (width // 4) * (i + 1)
                tree_y = height - 50
                draw.ellipse([tree_x-30, tree_y-80, tree_x+30, tree_y-20], fill=(0, 80, 0))
                draw.rectangle([tree_x-5, tree_y-20, tree_x+5, tree_y], fill=(101, 67, 33))
        
        elif any(word in description for word in ['sky', 'cloud', 'flying']):
            bg_color = (135, 206, 235)  # Sky blue
            img = Image.new('RGB', (width, height), bg_color)
            draw = ImageDraw.Draw(img)
            # Add clouds
            for i in range(2):
                cloud_x = (width // 3) * (i + 1)
                cloud_y = height // 4
                draw.ellipse([cloud_x-40, cloud_y-20, cloud_x+40, cloud_y+20], fill=(255, 255, 255))
        
        elif any(word in description for word in ['night', 'dark', 'moon']):
            bg_color = (25, 25, 112)  # Midnight blue
            img = Image.new('RGB', (width, height), bg_color)
            draw = ImageDraw.Draw(img)
            # Add moon
            draw.ellipse([width-80, 20, width-20, 80], fill=(255, 255, 224))
            # Add stars
            for _ in range(10):
                star_x = random.randint(20, width-20)
                star_y = random.randint(20, height//2)
                draw.ellipse([star_x-2, star_y-2, star_x+2, star_y+2], fill=(255, 255, 255))
        
        else:
            # Default background based on emotion
            emotion_colors = {
                'joy': (255, 248, 220),     # Light yellow
                'sadness': (176, 196, 222), # Light blue
                'anger': (255, 160, 122),   # Light red
                'surprise': (255, 182, 193), # Light pink
                'fear': (128, 128, 128),    # Gray
            }
            bg_color = emotion_colors.get(emotion, (240, 248, 255))  # Alice blue default
            img = Image.new('RGB', (width, height), bg_color)
        
        return img
    
    def draw_mouth_shape(self, draw, center_x, mouth_y, viseme, emotion):
        """Draw mouth shape based on viseme and emotion."""
        mouth_width = 25
        mouth_height = 15
        
        if viseme == 'open_mouth':
            # O shape for vowels
            draw.ellipse([
                center_x - mouth_width//3, mouth_y - mouth_height//2,
                center_x + mouth_width//3, mouth_y + mouth_height//2
            ], fill=(50, 50, 50), outline=(0, 0, 0), width=2)
        
        elif viseme == 'smile':
            # Smile shape
            if emotion in ['joy', 'happy']:
                # Big smile
                draw.arc([
                    center_x - mouth_width, mouth_y - mouth_height//2,
                    center_x + mouth_width, mouth_y + mouth_height
                ], 0, 180, fill=(200, 100, 100), width=4)
            else:
                # Small smile
                draw.arc([
                    center_x - mouth_width//2, mouth_y - mouth_height//4,
                    center_x + mouth_width//2, mouth_y + mouth_height//2
                ], 0, 180, fill=(150, 100, 100), width=3)
        
        elif viseme == 'round_mouth':
            # Round shape for consonants
            draw.ellipse([
                center_x - mouth_width//4, mouth_y - mouth_height//3,
                center_x + mouth_width//4, mouth_y + mouth_height//3
            ], fill=(100, 100, 100), outline=(0, 0, 0), width=2)
        
        else:
            # Neutral mouth
            draw.ellipse([
                center_x - mouth_width//3, mouth_y - mouth_height//4,
                center_x + mouth_width//3, mouth_y + mouth_height//4
            ], fill=(120, 120, 120), outline=(0, 0, 0), width=1)
    
    def generate_enhanced_video(self, story_data, config):
        """Generate enhanced video with multiple characters, scenes, audio, and animations."""
        frames = []
        total_frames = int(config['fps'] * config['duration'])
        width, height = config['width'], config['height']
        
        characters = story_data.get('characters', [])
        scenes = story_data.get('scenes', [])
        script = story_data.get('script', '')
        
        # Audio settings from config
        enable_audio = config.get('enable_audio', True)
        enable_music = config.get('enable_background_music', True)
        enable_advanced_animation = config.get('enable_advanced_animation', True)
        
        print(f"🎬 Generating enhanced video:")
        print(f"   Characters: {[c['name'] for c in characters]}")
        print(f"   Scenes: {len(scenes)}")
        print(f"   Frames: {total_frames}")
        print(f"   Audio: {'✅' if enable_audio and self.audio_engine else '❌'}")
        print(f"   Animation: {'✅' if enable_advanced_animation and self.animation_engine else '❌'}")
        
        # Pre-generate character avatars
        character_avatars = {}
        for char in characters:
            character_avatars[char['name']] = self.generate_character_avatar(char, 200, 200)
        
        # Generate audio for the first scene (if enabled)
        background_music_path = None
        character_audio_paths = {}
        
        if enable_audio and self.audio_engine and scenes:
            # Generate background music based on overall emotion
            main_emotion = scenes[0].get('emotion', 'neutral') if scenes else 'neutral'
            if enable_music:
                print("🎵 Generating background music...")
                background_music_path = self.generate_background_music(
                    emotion=main_emotion, 
                    duration=config['duration'],
                    style=config.get('music_style', 'orchestral')
                )
            
            # Generate character dialogue audio
            if script and characters:
                main_character = characters[0]['name']
                print(f"🗣️ Generating voice for {main_character}...")
                character_audio_paths[main_character] = self.generate_character_audio(
                    character_name=main_character,
                    text=script[:200],  # First part of script
                    voice_settings=config.get('voice_settings')
                )
        
        frames_per_scene = max(1, total_frames // len(scenes)) if scenes else total_frames
        
        for scene_idx, scene in enumerate(scenes):
            scene_start_frame = scene_idx * frames_per_scene
            scene_end_frame = min((scene_idx + 1) * frames_per_scene, total_frames)
            
            # Create scene background
            background = self.create_scene_background(scene, width, height)
            scene_emotion = scene.get('emotion', 'neutral')
            
            for frame_idx in range(scene_start_frame, scene_end_frame):
                # Start with background
                frame_img = background.copy()
                draw = ImageDraw.Draw(frame_img)
                
                # Add main character (if any)
                if characters:
                    main_char = characters[0]
                    char_avatar = character_avatars[main_char['name']].copy()
                    
                    # Apply advanced animation if enabled
                    if enable_advanced_animation and self.animation_engine:
                        # Determine animation type based on scene
                        if 'walk' in scene.get('description', '').lower():
                            animation_type = 'walk_cycle'
                        elif 'wave' in scene.get('description', '').lower():
                            animation_type = 'gesture'
                        else:
                            animation_type = 'facial_expression'
                        
                        char_avatar = self.apply_advanced_animation(
                            char_avatar, frame_idx, animation_type, scene_emotion
                        )
                    
                    # Position character
                    char_x = width // 2 - 100
                    char_y = height // 2 - 100
                    
                    # Paste character avatar
                    frame_img.paste(char_avatar, (char_x, char_y), char_avatar)
                    
                    # Animate mouth with improved lip-sync
                    mouth_center_x = char_x + 100
                    mouth_y = char_y + 140
                    
                    # More sophisticated viseme cycling
                    if character_audio_paths.get(main_char['name']):
                        # Audio-based mouth movement (simplified)
                        visemes = ['neutral', 'open_mouth', 'smile', 'round_mouth', 'neutral']
                        current_viseme = visemes[(frame_idx // 3) % len(visemes)]
                    else:
                        # Cycle through visemes
                        visemes = ['neutral', 'open_mouth', 'smile', 'round_mouth']
                        current_viseme = visemes[frame_idx % len(visemes)]
                    
                    self.draw_mouth_shape(draw, mouth_center_x, mouth_y, current_viseme, scene_emotion)
                
                # Add scene text
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
                except:
                    font = ImageFont.load_default()
                
                # Scene info with enhanced details
                scene_text = f"Scene {scene_idx + 1}: {scene.get('emotion', 'neutral')}"
                if enable_audio and self.audio_engine:
                    scene_text += " 🎵"
                if enable_advanced_animation and self.animation_engine:
                    scene_text += " 🎭"
                    
                draw.text((10, 10), scene_text, fill=(255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
                
                # Frame counter
                frame_text = f"Frame {frame_idx + 1}/{total_frames}"
                draw.text((10, height - 30), frame_text, fill=(255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
                
                # Character name
                if characters:
                    char_name = characters[0]['name']
                    draw.text((char_x, char_y - 25), char_name, fill=(255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
                
                # Add particle effects if animation engine is available
                if enable_advanced_animation and self.animation_engine and scene_emotion in ['joy', 'surprise']:
                    try:
                        # Add simple particle overlay
                        frame_img = self.animation_engine.create_particle_effect(
                            img=frame_img, 
                            effect_type='sparkles',
                            intensity=0.5,
                            center=(width//2, height//2)
                        )
                    except Exception as e:
                        print(f"⚠️ Particle effect failed: {e}")
                        pass  # Fail silently if particle effects don't work
                
                # Convert to numpy array
                frame_array = np.array(frame_img)
                frames.append(frame_array)
                
                if frame_idx % 10 == 0:
                    print(f"   Generated frame {frame_idx + 1}/{total_frames}")
        
        # Store audio paths for later use
        if background_music_path or character_audio_paths:
            # Store in config for later retrieval
            config['_generated_audio'] = {
                'background_music': background_music_path,
                'character_audio': character_audio_paths
            }
        
        return frames
    
    def generate_story_video(self, script, characters, scenes, output_path, 
                           width=640, height=480, fps=24, duration=5, style_settings=None,
                           audio_settings=None, animation_settings=None):
        """Generate a story video with the given parameters including audio and animation."""
        print(f"🎬 Generating story video: {output_path}")
        
        # Prepare story data in the expected format
        story_data = {
            'script': script,
            'characters': characters or [],
            'scenes': scenes or []
        }
        
        # Prepare config with new audio and animation settings
        config = {
            'width': width,
            'height': height,
            'fps': fps,
            'duration': duration,
            # Audio settings
            'enable_audio': audio_settings.get('enable_audio', True) if audio_settings else True,
            'enable_background_music': audio_settings.get('enable_background_music', True) if audio_settings else True,
            'music_style': audio_settings.get('music_style', 'orchestral') if audio_settings else 'orchestral',
            'voice_settings': audio_settings.get('voice_settings') if audio_settings else None,
            # Animation settings
            'enable_advanced_animation': animation_settings.get('enable_advanced_animation', True) if animation_settings else True,
        }
        
        if style_settings:
            config.update(style_settings)
        
        # Generate frames using enhanced method
        frames = self.generate_enhanced_video(story_data, config)
        
        # Save video with audio integration
        try:
            # Check if we have generated audio
            generated_audio = config.get('_generated_audio', {})
            background_music_path = generated_audio.get('background_music')
            
            if background_music_path and os.path.exists(background_music_path) and self.audio_engine:
                # Create video with audio
                temp_video_path = output_path.replace('.mp4', '_temp.mp4')
                
                # Save video without audio first
                imageio.mimsave(temp_video_path, frames, fps=fps, quality=8)
                
                # Combine video with audio using the audio engine
                final_path = self.audio_engine.mix_audio_with_video(
                    video_path=temp_video_path,
                    voice_audio_path=None,  # No character audio for now
                    background_audio_path=background_music_path,
                    output_path=output_path
                )
                
                # Clean up temporary files
                if os.path.exists(temp_video_path):
                    os.remove(temp_video_path)
                
                if final_path and os.path.exists(final_path):
                    print(f"✅ Story video with audio saved: {output_path}")
                else:
                    # Fallback to video without audio
                    imageio.mimsave(output_path, frames, fps=fps, quality=8)
                    print(f"✅ Story video saved (audio failed): {output_path}")
            else:
                # Save video without audio
                imageio.mimsave(output_path, frames, fps=fps, quality=8)
                print(f"✅ Story video saved: {output_path}")
            
            import os
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"📁 File size: {file_size:,} bytes")
                
                # Clean up temporary audio files
                for audio_path in generated_audio.get('character_audio', {}).values():
                    if audio_path and os.path.exists(audio_path) and 'temp_' in audio_path:
                        try:
                            os.remove(audio_path)
                        except:
                            pass
                
                if background_music_path and os.path.exists(background_music_path) and 'temp_' in background_music_path:
                    try:
                        os.remove(background_music_path)
                    except:
                        pass
                
                return output_path
                
        except Exception as e:
            print(f"❌ Error saving story video: {e}")
            raise e

# Test the enhanced generator
def test_enhanced_generation():
    generator = AdvancedVideoGenerator()
    
    # Sample story data
    story_data = {
        'characters': [
            {'name': 'Alice', 'gender': 'female', 'style': 'realistic'},
            {'name': 'Dragon', 'gender': 'neutral', 'style': 'fantasy'}
        ],
        'scenes': [
            {'description': 'Alice was walking through the enchanted forest', 'emotion': 'joy'},
            {'description': 'She felt curious about the magical creatures', 'emotion': 'surprise'},
            {'description': 'A friendly dragon appeared and smiled', 'emotion': 'joy'}
        ]
    }
    
    config = {
        'width': 640,
        'height': 480,
        'fps': 15,
        'duration': 3
    }
    
    print("🚀 Testing Enhanced Video Generation...")
    frames = generator.generate_enhanced_video(story_data, config)
    
    # Save video
    import time
    timestamp = int(time.time())
    output_path = f"enhanced_video_{timestamp}.mp4"
    
    try:
        imageio.mimsave(output_path, frames, fps=config['fps'], quality=8)
        print(f"✅ Enhanced video saved: {output_path}")
        
        import os
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"📁 File size: {file_size:,} bytes")
            return output_path
    except Exception as e:
        print(f"❌ Error saving video: {e}")
        return None

if __name__ == "__main__":
    test_enhanced_generation()
