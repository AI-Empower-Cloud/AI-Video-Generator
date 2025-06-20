#!/usr/bin/env python3
"""
Batch Educational Video Creator
Generate multiple educational videos automatically and upload to YouTube
"""

import json
import time
import sys
from pathlib import Path

sys.path.append('/workspaces/AI-Video-Generator')

from educational_video_generator import EducationalVideoGenerator, auto_upload_educational_video

class BatchEducationalVideoCreator:
    """Create multiple educational videos in batch."""
    
    def __init__(self):
        self.generator = EducationalVideoGenerator()
        self.created_videos = []
    
    def load_content_library(self):
        """Load predefined educational content library."""
        return {
            "slokas": [
                {
                    "title": "Gayatri Mantra - Complete Teaching",
                    "type": "mantra_teaching",
                    "duration": 20,
                    "data": {
                        "mantra_type": "gayatri",
                        "teacher_name": "Guruji",
                        "overview": "Complete guide to the most sacred Vedic mantra"
                    }
                },
                {
                    "title": "Maha Mantra Teaching",
                    "type": "mantra_teaching", 
                    "duration": 25,
                    "data": {
                        "text": "हरे कृष्ण हरे कृष्ण कृष्ण कृष्ण हरे हरे, हरे राम हरे राम राम राम हरे हरे",
                        "title": "Hare Krishna Maha Mantra",
                        "meaning": "The Great Mantra for liberation and divine consciousness",
                        "benefits": "Purifies the heart, brings peace, connects with divine love",
                        "teacher_name": "Spiritual Teacher"
                    }
                },
                {
                    "title": "Shanti Mantra Teaching",
                    "type": "sloka_teaching",
                    "duration": 15,
                    "data": {
                        "text": "ॐ सर्वे भवन्तु सुखिनः सर्वे सन्तु निरामयाः, सर्वे भद्राणि पश्यन्तु मा कश्चिद्दुःखभाग्भवेत्",
                        "title": "Universal Peace Mantra",
                        "meaning": "May all beings be happy, may all be free from illness, may all see what is auspicious, may no one suffer",
                        "benefits": "Promotes universal peace, compassion, and well-being for all",
                        "teacher_name": "Peace Teacher"
                    }
                },
                {
                    "title": "Ganesh Mantra Teaching",
                    "type": "mantra_teaching",
                    "duration": 18,
                    "data": {
                        "text": "ॐ गं गणपतये नमः",
                        "title": "Ganesh Mantra for Obstacle Removal",
                        "meaning": "Om Gam Ganapataye Namaha - Salutations to Lord Ganesha, remover of obstacles",
                        "benefits": "Removes obstacles, brings success, enhances wisdom and new beginnings",
                        "teacher_name": "Devotional Teacher"
                    }
                }
            ],
            "educational_topics": [
                {
                    "title": "Introduction to Sanskrit Language",
                    "type": "educational_lecture",
                    "duration": 30,
                    "data": {
                        "topic": "Sanskrit Language Basics",
                        "content": """Sanskrit is the ancient language of India and the liturgical language of Hinduism, Buddhism, and Jainism. 
                        In this comprehensive introduction, we will learn:
                        1. The origins and history of Sanskrit
                        2. The Devanagari script
                        3. Basic pronunciation rules
                        4. Simple words and phrases
                        5. Cultural significance""",
                        "category": "Language",
                        "teacher_name": "Sanskrit Scholar"
                    }
                },
                {
                    "title": "Vedic Mathematics Fundamentals",
                    "type": "educational_lecture", 
                    "duration": 35,
                    "data": {
                        "topic": "Vedic Mathematics",
                        "content": """Vedic Mathematics is an ancient system of calculation based on Sanskrit sutras.
                        This lesson covers:
                        1. History and origins
                        2. Basic multiplication techniques
                        3. Quick calculation methods
                        4. Practical applications
                        5. Mental math improvement""",
                        "category": "Mathematics",
                        "teacher_name": "Math Teacher"
                    }
                },
                {
                    "title": "Yoga Philosophy and Practice",
                    "type": "educational_lecture",
                    "duration": 40,
                    "data": {
                        "topic": "Yoga Philosophy",
                        "content": """Understanding the philosophical foundations of Yoga:
                        1. The Eight Limbs of Yoga (Ashtanga)
                        2. Ethical guidelines (Yamas and Niyamas)
                        3. Physical practices (Asanas)
                        4. Breathing techniques (Pranayama)
                        5. Meditation and spiritual growth""",
                        "category": "Spiritual",
                        "teacher_name": "Yoga Master"
                    }
                }
            ]
        }
    
    def create_video_series(self, series_name, video_list, output_dir="educational_series"):
        """Create a series of educational videos."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        print(f"🎬 Creating {series_name} video series...")
        print(f"📁 Output directory: {output_path}")
        print(f"🎥 Videos to create: {len(video_list)}")
        
        results = []
        
        for i, video_config in enumerate(video_list, 1):
            print(f"\n🎬 Creating video {i}/{len(video_list)}: {video_config['title']}")
            
            try:
                # Output settings
                output_settings = {
                    'duration': video_config['duration'] * 60,
                    'width': 1920,
                    'height': 1080,
                    'fps': 30
                }
                
                # Generate video
                video_filename = f"{series_name}_{i:02d}_{video_config['title'].replace(' ', '_')}.mp4"
                video_path = output_path / video_filename
                
                # Update output path in settings
                output_settings['output_path'] = str(video_path)
                
                video_path, metadata = self.generator.generate_educational_video(
                    video_config['type'],
                    video_config['data'],
                    output_settings
                )
                
                result = {
                    'title': video_config['title'],
                    'path': video_path,
                    'metadata': metadata,
                    'duration': video_config['duration'],
                    'status': 'success'
                }
                
                results.append(result)
                self.created_videos.append(result)
                
                print(f"✅ Video created: {video_path}")
                
                # Optional: Add delay between videos to avoid overwhelming the system
                time.sleep(5)
                
            except Exception as e:
                print(f"❌ Error creating video {i}: {e}")
                results.append({
                    'title': video_config['title'],
                    'status': 'failed',
                    'error': str(e)
                })
        
        return results
    
    def upload_series_to_youtube(self, results, playlist_name=None):
        """Upload all created videos to YouTube."""
        print(f"\n📤 Uploading {len(results)} videos to YouTube...")
        
        uploaded_videos = []
        
        for i, result in enumerate(results, 1):
            if result['status'] != 'success':
                print(f"⏭️ Skipping failed video: {result['title']}")
                continue
            
            print(f"📤 Uploading {i}: {result['title']}")
            
            try:
                video_url = auto_upload_educational_video(result['path'], result['metadata'])
                
                if video_url:
                    print(f"✅ Uploaded: {video_url}")
                    uploaded_videos.append({
                        'title': result['title'],
                        'url': video_url,
                        'status': 'uploaded'
                    })
                else:
                    print(f"❌ Failed to upload: {result['title']}")
                    uploaded_videos.append({
                        'title': result['title'],
                        'status': 'upload_failed'
                    })
                
                # Delay between uploads
                time.sleep(10)
                
            except Exception as e:
                print(f"❌ Upload error for {result['title']}: {e}")
                uploaded_videos.append({
                    'title': result['title'],
                    'status': 'upload_error',
                    'error': str(e)
                })
        
        return uploaded_videos
    
    def create_complete_series_report(self, series_name, results, uploads=None):
        """Create a comprehensive report of the video series."""
        report = {
            'series_name': series_name,
            'created_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_videos': len(results),
            'successful_creations': len([r for r in results if r['status'] == 'success']),
            'failed_creations': len([r for r in results if r['status'] == 'failed']),
            'results': results
        }
        
        if uploads:
            report['uploads'] = {
                'total_attempts': len(uploads),
                'successful_uploads': len([u for u in uploads if u['status'] == 'uploaded']),
                'failed_uploads': len([u for u in uploads if u['status'] != 'uploaded']),
                'upload_results': uploads
            }
        
        # Save report
        report_path = f"{series_name}_creation_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Series Creation Report:")
        print(f"📁 Report saved: {report_path}")
        print(f"🎥 Total videos: {report['total_videos']}")
        print(f"✅ Successful: {report['successful_creations']}")
        print(f"❌ Failed: {report['failed_creations']}")
        
        if uploads:
            print(f"📤 Upload attempts: {report['uploads']['total_attempts']}")
            print(f"✅ Successful uploads: {report['uploads']['successful_uploads']}")
            print(f"❌ Failed uploads: {report['uploads']['failed_uploads']}")
        
        return report

def create_sanskrit_learning_series():
    """Create a complete Sanskrit learning video series."""
    creator = BatchEducationalVideoCreator()
    content = creator.load_content_library()
    
    # Create Sanskrit/Mantra series
    sanskrit_series = content['slokas']
    results = creator.create_video_series("Sanskrit_Learning", sanskrit_series)
    
    # Optionally upload to YouTube (uncomment if you have API setup)
    # uploads = creator.upload_series_to_youtube(results, "Sanskrit Learning Series")
    # report = creator.create_complete_series_report("Sanskrit_Learning", results, uploads)
    
    report = creator.create_complete_series_report("Sanskrit_Learning", results)
    return report

def create_educational_content_series():
    """Create educational content video series."""
    creator = BatchEducationalVideoCreator()
    content = creator.load_content_library()
    
    # Create educational series
    edu_series = content['educational_topics']
    results = creator.create_video_series("Educational_Content", edu_series)
    
    report = creator.create_complete_series_report("Educational_Content", results)
    return report

def create_custom_series_from_config(config_file):
    """Create video series from a JSON configuration file."""
    creator = BatchEducationalVideoCreator()
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    series_name = config.get('series_name', 'Custom_Series')
    video_list = config.get('videos', [])
    
    results = creator.create_video_series(series_name, video_list)
    
    # Upload if specified in config
    if config.get('auto_upload', False):
        uploads = creator.upload_series_to_youtube(results)
        report = creator.create_complete_series_report(series_name, results, uploads)
    else:
        report = creator.create_complete_series_report(series_name, results)
    
    return report

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Batch Educational Video Creator")
    parser.add_argument('--series', choices=['sanskrit', 'educational', 'both'], 
                       default='both', help='Which series to create')
    parser.add_argument('--config', help='Path to custom configuration JSON file')
    parser.add_argument('--upload', action='store_true', help='Auto-upload to YouTube')
    
    args = parser.parse_args()
    
    if args.config:
        print(f"🎬 Creating custom series from: {args.config}")
        report = create_custom_series_from_config(args.config)
    else:
        if args.series in ['sanskrit', 'both']:
            print("🕉️ Creating Sanskrit Learning Series...")
            sanskrit_report = create_sanskrit_learning_series()
        
        if args.series in ['educational', 'both']:
            print("📚 Creating Educational Content Series...")
            edu_report = create_educational_content_series()
    
    print("🎉 Batch video creation complete!")
