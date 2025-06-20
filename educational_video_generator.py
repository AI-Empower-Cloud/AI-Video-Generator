#!/usr/bin/env python3
"""
Educational Video Generator for Long-form Content
Specialized for teaching videos like slokas, mantras, educational content
Supports 10-40 minute videos with automatic YouTube upload
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import List, Dict, Optional
import random

# Add project root to path
sys.path.append('/workspaces/AI-Video-Generator')

from enhanced_video_generator import AdvancedVideoGenerator
from main import upload_to_youtube

class EducationalVideoGenerator(AdvancedVideoGenerator):
    """Extended video generator for educational content."""
    
    def __init__(self):
        super().__init__()
        self.educational_templates = {
            'sloka_teaching': {
                'duration_range': (600, 1200),  # 10-20 minutes
                'segments': ['introduction', 'pronunciation', 'meaning', 'repetition', 'conclusion'],
                'repetitions': 3,
                'pause_duration': 2
            },
            'mantra_teaching': {
                'duration_range': (900, 1800),  # 15-30 minutes
                'segments': ['invocation', 'pronunciation', 'meditation', 'benefits', 'practice'],
                'repetitions': 5,
                'pause_duration': 3
            },
            'educational_lecture': {
                'duration_range': (1200, 2400),  # 20-40 minutes
                'segments': ['introduction', 'concept_explanation', 'examples', 'practice', 'summary'],
                'repetitions': 2,
                'pause_duration': 1
            }
        }
    
    def create_sloka_teaching_script(self, sloka_data):
        """Create a comprehensive script for teaching a sloka."""
        sloka_text = sloka_data.get('text', '')
        meaning = sloka_data.get('meaning', '')
        benefits = sloka_data.get('benefits', '')
        
        script_segments = []
        
        # Introduction segment
        intro = f"""
        Welcome to our Sanskrit learning series. Today we will learn the beautiful sloka:
        {sloka_text}
        
        This ancient verse carries deep wisdom and has been chanted for thousands of years.
        Let us begin by understanding its pronunciation and meaning.
        """
        
        # Pronunciation segment - break down syllables
        pronunciation = f"""
        Let us first learn the correct pronunciation. We will go word by word:
        {self.break_into_syllables(sloka_text)}
        
        Now let us chant it together slowly, focusing on each syllable.
        """
        
        # Meaning segment
        meaning_segment = f"""
        Now that we can pronounce it correctly, let us understand its beautiful meaning:
        {meaning}
        
        Each word in Sanskrit carries profound significance. Let us explore this deeper.
        """
        
        # Repetition for memorization
        repetition = f"""
        To help memorize this sloka, we will chant it together several times.
        Listen carefully and repeat after me:
        {sloka_text}
        
        Once more with devotion:
        {sloka_text}
        """
        
        # Benefits and conclusion
        conclusion = f"""
        Regular chanting of this sloka brings these benefits:
        {benefits}
        
        Practice chanting this sloka daily for spiritual growth and inner peace.
        Thank you for joining this learning session. Om Shanti Shanti Shanti.
        """
        
        return {
            'introduction': intro,
            'pronunciation': pronunciation,
            'meaning': meaning_segment,
            'repetition': repetition,
            'conclusion': conclusion
        }
    
    def create_gayatri_mantra_teaching(self):
        """Create comprehensive Gayatri Mantra teaching video script."""
        gayatri_mantra = "ॐ भूर्भुवः स्वः तत्सवितुर्वरेण्यं भर्गो देवस्य धीमहि धियो यो नः प्रचोदयात्"
        
        return self.create_sloka_teaching_script({
            'text': gayatri_mantra,
            'meaning': """
            Om - The primordial sound of the universe
            Bhur Bhuvah Svah - The three planes of existence
            Tat Savitur Varenyam - That divine light which is adorable
            Bhargo Devasya Dhimahi - We meditate upon that divine radiance
            Dhiyo Yo Nah Prachodayat - May that light illuminate our intellect
            """,
            'benefits': """
            - Purifies the mind and enhances concentration
            - Brings peace and spiritual awakening
            - Improves memory and intellectual capabilities
            - Connects us with divine consciousness
            - Provides protection and positive energy
            """
        })
    
    def break_into_syllables(self, text):
        """Break Sanskrit text into syllables for pronunciation guide."""
        # Simple syllable breaking for demonstration
        words = text.split()
        syllable_guide = []
        
        for word in words:
            # Basic syllable separation (can be enhanced with proper Sanskrit rules)
            syllables = []
            current = ""
            for char in word:
                current += char
                # Simple rule: after consonant+vowel combination
                if len(current) >= 2:
                    syllables.append(current)
                    current = ""
            if current:
                syllables.append(current)
            syllable_guide.append(" - ".join(syllables))
        
        return " | ".join(syllable_guide)
    
    def generate_educational_video(self, content_type, content_data, output_settings):
        """Generate long-form educational video."""
        template = self.educational_templates.get(content_type, self.educational_templates['educational_lecture'])
        
        # Create script based on content type
        if content_type == 'sloka_teaching':
            script_segments = self.create_sloka_teaching_script(content_data)
        elif content_type == 'mantra_teaching' and content_data.get('mantra_type') == 'gayatri':
            script_segments = self.create_gayatri_mantra_teaching()
        else:
            script_segments = self.create_generic_educational_script(content_data)
        
        # Calculate timing for each segment
        total_duration = output_settings.get('duration', 900)  # Default 15 minutes
        segment_durations = self.calculate_segment_durations(script_segments, total_duration, template)
        
        # Generate characters for educational video
        characters = [
            {
                'name': content_data.get('teacher_name', 'Teacher'),
                'gender': content_data.get('teacher_gender', 'neutral'),
                'style': 'educational',
                'voice_style': 'calm_teacher'
            }
        ]
        
        # Create scenes for each segment
        scenes = []
        for segment_name, script in script_segments.items():
            scene_duration = segment_durations.get(segment_name, total_duration // len(script_segments))
            
            scenes.append({
                'description': f'{segment_name.replace("_", " ").title()} segment',
                'emotion': self.get_segment_emotion(segment_name),
                'duration': scene_duration,
                'script': script,
                'background_style': self.get_educational_background(segment_name)
            })
        
        # Enhanced audio settings for educational content
        audio_settings = {
            'enable_audio': True,
            'enable_background_music': True,
            'music_style': 'spiritual',  # For slokas/mantras
            'voice_settings': {
                'rate': 120,  # Slower for learning
                'volume': 0.9,
                'voice_id': 'teacher',
                'clarity': 'high'
            }
        }
        
        # Animation settings for educational content
        animation_settings = {
            'enable_advanced_animation': True,
            'animation_style': 'educational',
            'enable_particle_effects': True,
            'text_animations': True
        }
        
        print(f"🎓 Generating educational video: {content_type}")
        print(f"📚 Total duration: {total_duration // 60} minutes {total_duration % 60} seconds")
        print(f"🎬 Segments: {len(scenes)}")
        
        # Generate the video
        video_path = f"educational_{content_type}_{int(time.time())}.mp4"
        
        result_path = self.generate_story_video(
            script=" ".join([scene['script'] for scene in scenes]),
            characters=characters,
            scenes=scenes,
            output_path=video_path,
            width=output_settings.get('width', 1920),
            height=output_settings.get('height', 1080),
            fps=output_settings.get('fps', 30),
            duration=total_duration,
            audio_settings=audio_settings,
            animation_settings=animation_settings
        )
        
        return result_path, self.create_youtube_metadata(content_type, content_data)
    
    def calculate_segment_durations(self, script_segments, total_duration, template):
        """Calculate duration for each segment."""
        segments = list(script_segments.keys())
        base_duration = total_duration // len(segments)
        
        # Adjust based on segment importance
        segment_weights = {
            'introduction': 0.8,
            'pronunciation': 1.5,
            'meaning': 1.2,
            'repetition': 2.0,
            'conclusion': 0.5,
            'invocation': 0.6,
            'meditation': 1.8,
            'benefits': 1.0,
            'practice': 2.2
        }
        
        durations = {}
        total_weight = sum(segment_weights.get(seg, 1.0) for seg in segments)
        
        for segment in segments:
            weight = segment_weights.get(segment, 1.0)
            durations[segment] = int((weight / total_weight) * total_duration)
        
        return durations
    
    def get_segment_emotion(self, segment_name):
        """Get appropriate emotion for each segment."""
        emotion_map = {
            'introduction': 'calm',
            'pronunciation': 'focused',
            'meaning': 'contemplative',
            'repetition': 'meditative',
            'conclusion': 'peaceful',
            'invocation': 'reverent',
            'meditation': 'serene',
            'benefits': 'inspiring',
            'practice': 'encouraging'
        }
        return emotion_map.get(segment_name, 'neutral')
    
    def get_educational_background(self, segment_name):
        """Get appropriate background for each segment."""
        background_map = {
            'introduction': 'temple',
            'pronunciation': 'classroom',
            'meaning': 'library',
            'repetition': 'meditation_hall',
            'conclusion': 'peaceful_garden',
            'invocation': 'altar',
            'meditation': 'lotus_pond',
            'benefits': 'sunrise',
            'practice': 'meditation_room'
        }
        return background_map.get(segment_name, 'spiritual')
    
    def create_youtube_metadata(self, content_type, content_data):
        """Create YouTube metadata for educational content."""
        title_templates = {
            'sloka_teaching': "Learn Sanskrit Sloka: {title} | Pronunciation, Meaning & Benefits",
            'mantra_teaching': "Sacred Mantra Teaching: {title} | Complete Guide with Pronunciation",
            'educational_lecture': "Educational Tutorial: {title} | Complete Learning Guide"
        }
        
        description_template = """
🕉️ Welcome to our Sanskrit Learning Series!

In this video, you will learn:
✨ Correct pronunciation
📚 Deep meaning and significance  
🙏 Spiritual benefits
🎵 Proper chanting technique

📖 Content Overview:
{content_overview}

🎯 Who is this for:
- Sanskrit learning enthusiasts
- Spiritual seekers
- Students of ancient wisdom
- Anyone interested in mantras and slokas

🔔 Subscribe for more educational content!
💬 Share your experience in comments
🙏 Like if this helped your spiritual journey

#Sanskrit #Mantra #Sloka #Spirituality #Education #Meditation #Hinduism #AncientWisdom
        """
        
        title = title_templates.get(content_type, "Educational Video: {title}").format(
            title=content_data.get('title', 'Spiritual Learning')
        )
        
        description = description_template.format(
            content_overview=content_data.get('overview', 'Complete spiritual learning experience')
        )
        
        tags = [
            'Sanskrit', 'Education', 'Spiritual', 'Mantra', 'Sloka', 'Learning',
            'Pronunciation', 'Meditation', 'Hinduism', 'Ancient Wisdom',
            'Teaching', 'Spiritual Growth', 'Devotional', 'Sacred'
        ]
        
        # Add specific tags based on content
        if 'gayatri' in content_data.get('title', '').lower():
            tags.extend(['Gayatri Mantra', 'Gayatri', 'Sun God', 'Savitri'])
        
        return {
            'title': title,
            'description': description,
            'tags': tags,
            'category': 'Education',
            'privacy': 'public'
        }
    
    def create_generic_educational_script(self, content_data):
        """Create script for generic educational content."""
        topic = content_data.get('topic', 'Educational Topic')
        content = content_data.get('content', '')
        
        return {
            'introduction': f"Welcome to today's lesson on {topic}. Let us begin our learning journey.",
            'explanation': content,
            'examples': f"Let us explore some examples to understand {topic} better.",
            'practice': f"Now let us practice what we have learned about {topic}.",
            'conclusion': f"Thank you for learning about {topic}. Practice regularly for mastery."
        }

# Example usage and test functions
def create_gayatri_mantra_video():
    """Create a complete Gayatri Mantra teaching video."""
    generator = EducationalVideoGenerator()
    
    content_data = {
        'mantra_type': 'gayatri',
        'title': 'Gayatri Mantra - Complete Teaching',
        'teacher_name': 'Guruji',
        'teacher_gender': 'male',
        'overview': 'Complete guide to learning and chanting the sacred Gayatri Mantra'
    }
    
    output_settings = {
        'duration': 1200,  # 20 minutes
        'width': 1920,
        'height': 1080,
        'fps': 30
    }
    
    video_path, metadata = generator.generate_educational_video(
        'mantra_teaching', content_data, output_settings
    )
    
    return video_path, metadata

def create_custom_sloka_video(sloka_text, meaning, benefits, title):
    """Create a teaching video for any sloka."""
    generator = EducationalVideoGenerator()
    
    content_data = {
        'text': sloka_text,
        'meaning': meaning,
        'benefits': benefits,
        'title': title,
        'teacher_name': 'Teacher',
        'overview': f'Learn the beautiful {title} with proper pronunciation and meaning'
    }
    
    output_settings = {
        'duration': 900,  # 15 minutes
        'width': 1280,
        'height': 720,
        'fps': 24
    }
    
    video_path, metadata = generator.generate_educational_video(
        'sloka_teaching', content_data, output_settings
    )
    
    return video_path, metadata

def auto_upload_educational_video(video_path, metadata):
    """Automatically upload educational video to YouTube."""
    try:
        video_url = upload_to_youtube(
            video_path=video_path,
            title=metadata['title'],
            description=metadata['description'],
            tags=metadata['tags']
        )
        
        if video_url:
            print(f"✅ Successfully uploaded to YouTube: {video_url}")
            return video_url
        else:
            print("❌ Failed to upload to YouTube")
            return None
            
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return None

if __name__ == "__main__":
    # Test with Gayatri Mantra
    print("🕉️ Creating Gayatri Mantra teaching video...")
    video_path, metadata = create_gayatri_mantra_video()
    
    print(f"📹 Video created: {video_path}")
    print(f"📝 Title: {metadata['title']}")
    print(f"🏷️ Tags: {', '.join(metadata['tags'][:10])}")
    
    # Uncomment to auto-upload to YouTube
    # auto_upload_educational_video(video_path, metadata)
