#!/usr/bin/env python3
"""
Universal Educational Content Generator
Creates educational videos for ALL subjects: Math, Science, History, Languages, Arts, etc.
Supports 10-40 minute videos with automatic YouTube upload
"""

import json
import time
import os
import random
from datetime import datetime, timedelta
import sys

# Add project root to path
sys.path.append('/workspaces/AI-Video-Generator')

from universal_education_app import create_educational_video, EDUCATIONAL_SUBJECTS

# Extended subject configuration for all educational domains
COMPLETE_EDUCATION_SUBJECTS = {
    **EDUCATIONAL_SUBJECTS,  # Include all subjects from universal_education_app
    
    "Biology": {
        "topics": [
            "Cell Structure", "DNA and Genetics", "Evolution", "Ecology",
            "Human Body Systems", "Plant Biology", "Microbiology", 
            "Biotechnology", "Marine Biology", "Neuroscience"
        ],
        "levels": ["Middle School", "High School", "College", "Advanced"],
        "duration_range": (20, 35),
        "voice_style": "scientific_educator"
    },
    
    "Chemistry": {
        "topics": [
            "Atomic Structure", "Chemical Bonding", "Periodic Table",
            "Chemical Reactions", "Organic Chemistry", "Inorganic Chemistry",
            "Physical Chemistry", "Biochemistry", "Environmental Chemistry"
        ],
        "levels": ["High School", "College", "Advanced", "Research"],
        "duration_range": (25, 40),
        "voice_style": "chemistry_professor"
    },
    
    "Physics": {
        "topics": [
            "Mechanics", "Thermodynamics", "Electromagnetism", "Optics",
            "Quantum Physics", "Relativity", "Nuclear Physics", 
            "Astrophysics", "Particle Physics", "Condensed Matter"
        ],
        "levels": ["High School", "College", "Graduate", "Research"],
        "duration_range": (25, 45),
        "voice_style": "physics_teacher"
    },
    
    "Literature": {
        "topics": [
            "Poetry Analysis", "Novel Studies", "Drama and Theater",
            "World Literature", "Literary Criticism", "Creative Writing",
            "Comparative Literature", "Medieval Literature", "Modern Literature"
        ],
        "levels": ["Middle School", "High School", "College", "Graduate"],
        "duration_range": (20, 35),
        "voice_style": "literature_professor"
    },
    
    "Philosophy": {
        "topics": [
            "Ethics", "Logic", "Metaphysics", "Political Philosophy",
            "Philosophy of Mind", "Eastern Philosophy", "Western Philosophy",
            "Contemporary Philosophy", "Philosophy of Science"
        ],
        "levels": ["High School", "College", "Graduate", "Scholar"],
        "duration_range": (25, 40),
        "voice_style": "thoughtful_philosopher"
    },
    
    "Engineering": {
        "topics": [
            "Civil Engineering", "Mechanical Engineering", "Electrical Engineering",
            "Computer Engineering", "Chemical Engineering", "Aerospace Engineering",
            "Environmental Engineering", "Biomedical Engineering"
        ],
        "levels": ["College", "Graduate", "Professional", "Expert"],
        "duration_range": (30, 45),
        "voice_style": "engineering_instructor"
    },
    
    "Medicine": {
        "topics": [
            "Anatomy", "Physiology", "Pathology", "Pharmacology",
            "Medical Ethics", "Clinical Medicine", "Surgery",
            "Preventive Medicine", "Medical Research"
        ],
        "levels": ["Pre-med", "Medical School", "Residency", "Professional"],
        "duration_range": (25, 40),
        "voice_style": "medical_educator"
    },
    
    "Business": {
        "topics": [
            "Management", "Marketing", "Finance", "Entrepreneurship",
            "Business Strategy", "Operations", "Human Resources",
            "International Business", "Business Ethics"
        ],
        "levels": ["High School", "College", "MBA", "Executive"],
        "duration_range": (20, 35),
        "voice_style": "business_mentor"
    },
    
    "Law": {
        "topics": [
            "Constitutional Law", "Criminal Law", "Civil Law",
            "International Law", "Business Law", "Environmental Law",
            "Human Rights Law", "Legal Ethics", "Legal Research"
        ],
        "levels": ["Pre-law", "Law School", "Bar Prep", "Professional"],
        "duration_range": (25, 40),
        "voice_style": "legal_educator"
    },
    
    "Environmental Science": {
        "topics": [
            "Climate Change", "Ecology", "Conservation", "Pollution",
            "Renewable Energy", "Sustainability", "Environmental Policy",
            "Biodiversity", "Green Technology"
        ],
        "levels": ["High School", "College", "Graduate", "Professional"],
        "duration_range": (20, 35),
        "voice_style": "environmental_advocate"
    }
}

class UniversalEducationCreator:
    """Create educational videos for any subject."""
    
    def __init__(self, config_file="universal_education_config.json"):
        self.config_file = config_file
        self.load_config()
        self.created_videos = []
        
    def load_config(self):
        """Load universal education configuration."""
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            # Create comprehensive default config
            self.config = {
                "daily_schedule": {
                    "mathematics_videos": 2,
                    "science_videos": 2,
                    "language_videos": 1,
                    "history_videos": 1,
                    "arts_videos": 1,
                    "total_daily_videos": 7
                },
                "quality_settings": {
                    "video_resolution": "1280x720",
                    "audio_quality": "high",
                    "voice_clarity": "educational",
                    "background_music": "subtle"
                },
                "youtube_automation": {
                    "auto_upload": True,
                    "schedule_uploads": True,
                    "upload_times": ["08:00", "12:00", "16:00", "20:00"],
                    "channel_branding": "Universal Education Hub"
                },
                "content_preferences": {
                    "include_examples": True,
                    "include_exercises": True,
                    "include_summaries": True,
                    "interactive_elements": True
                }
            }
            self.save_config()
    
    def save_config(self):
        """Save configuration."""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def create_curriculum_series(self, subject, weeks=4):
        """Create a complete curriculum series for any subject."""
        if subject not in COMPLETE_EDUCATION_SUBJECTS:
            print(f"❌ Subject '{subject}' not available")
            return []
        
        subject_config = COMPLETE_EDUCATION_SUBJECTS[subject]
        topics = subject_config["topics"]
        levels = subject_config["levels"]
        
        curriculum = []
        videos_per_week = min(len(topics), 3)  # Max 3 videos per week
        
        print(f"📚 Creating {weeks}-week curriculum for {subject}")
        print(f"   📖 Topics: {len(topics)}")
        print(f"   🎯 Levels: {levels}")
        print(f"   📅 Videos per week: {videos_per_week}")
        
        for week in range(weeks):
            week_videos = []
            
            for i in range(videos_per_week):
                topic_index = (week * videos_per_week + i) % len(topics)
                level_index = (week * videos_per_week + i) % len(levels)
                
                topic = topics[topic_index]
                level = levels[level_index]
                duration = random.randint(*subject_config["duration_range"])
                
                video_plan = {
                    "week": week + 1,
                    "subject": subject,
                    "topic": topic,
                    "level": level,
                    "duration": duration,
                    "voice_style": subject_config["voice_style"]
                }
                
                week_videos.append(video_plan)
            
            curriculum.append({
                "week": week + 1,
                "videos": week_videos
            })
        
        return curriculum
    
    def create_video_from_plan(self, video_plan):
        """Create educational video from curriculum plan."""
        print(f"🎬 Creating: {video_plan['subject']} - {video_plan['topic']}")
        print(f"   🎯 Level: {video_plan['level']}")
        print(f"   ⏱️ Duration: {video_plan['duration']} minutes")
        
        video_path, youtube_url = create_educational_video(
            subject=video_plan["subject"],
            topic=video_plan["topic"],
            level=video_plan["level"],
            duration=video_plan["duration"],
            auto_upload=self.config["youtube_automation"]["auto_upload"]
        )
        
        if video_path:
            video_plan["status"] = "completed"
            video_plan["video_path"] = video_path
            video_plan["youtube_url"] = youtube_url
            video_plan["created_at"] = datetime.now().isoformat()
            
            self.created_videos.append(video_plan)
            self.save_progress()
            
            print(f"✅ Video completed: {video_plan['topic']}")
            if youtube_url:
                print(f"📺 YouTube: {youtube_url}")
        else:
            video_plan["status"] = "failed"
            print(f"❌ Failed: {video_plan['topic']}")
        
        return video_plan
    
    def save_progress(self):
        """Save creation progress."""
        progress = {
            "total_videos": len(self.created_videos),
            "subjects_covered": list(set([v["subject"] for v in self.created_videos])),
            "last_updated": datetime.now().isoformat(),
            "videos": self.created_videos
        }
        
        with open("universal_education_progress.json", 'w') as f:
            json.dump(progress, f, indent=2)
    
    def create_daily_videos(self):
        """Create today's scheduled educational videos."""
        print("📅 Creating today's educational videos...")
        
        # Select subjects for today
        subjects_today = [
            "Mathematics", "Science", "History", "Computer Science", 
            "Language Arts", "Sanskrit/Spiritual"
        ]
        
        videos_created = 0
        target_videos = self.config["daily_schedule"]["total_daily_videos"]
        
        for subject in subjects_today:
            if videos_created >= target_videos:
                break
                
            if subject in COMPLETE_EDUCATION_SUBJECTS:
                subject_config = COMPLETE_EDUCATION_SUBJECTS[subject]
                
                # Random topic and level
                topic = random.choice(subject_config["topics"])
                level = random.choice(subject_config["levels"])
                duration = random.randint(*subject_config["duration_range"])
                
                video_plan = {
                    "subject": subject,
                    "topic": topic,
                    "level": level,
                    "duration": duration,
                    "voice_style": subject_config["voice_style"],
                    "scheduled_for": "today"
                }
                
                self.create_video_from_plan(video_plan)
                videos_created += 1
                
                # Delay between videos
                if videos_created < target_videos:
                    print("⏳ Waiting 3 minutes before next video...")
                    time.sleep(180)
        
        print(f"✅ Today's video creation complete! Created {videos_created} videos")
    
    def create_subject_focus(self, subject, num_videos=5):
        """Create multiple videos focused on one subject."""
        if subject not in COMPLETE_EDUCATION_SUBJECTS:
            print(f"❌ Subject '{subject}' not found")
            return
        
        print(f"🎓 Creating {num_videos} videos for {subject}")
        
        subject_config = COMPLETE_EDUCATION_SUBJECTS[subject]
        
        for i in range(num_videos):
            topic = random.choice(subject_config["topics"])
            level = random.choice(subject_config["levels"])
            duration = random.randint(*subject_config["duration_range"])
            
            video_plan = {
                "subject": subject,
                "topic": topic,
                "level": level,
                "duration": duration,
                "voice_style": subject_config["voice_style"],
                "series": f"{subject}_focus_series"
            }
            
            self.create_video_from_plan(video_plan)
            
            # Delay between videos
            if i < num_videos - 1:
                print("⏳ Waiting 2 minutes...")
                time.sleep(120)
    
    def generate_education_report(self):
        """Generate comprehensive education report."""
        if not self.created_videos:
            print("📊 No videos created yet")
            return
        
        # Analyze created videos
        subjects = {}
        total_duration = 0
        youtube_uploads = 0
        
        for video in self.created_videos:
            subject = video["subject"]
            subjects[subject] = subjects.get(subject, 0) + 1
            total_duration += video["duration"]
            if video.get("youtube_url"):
                youtube_uploads += 1
        
        report = {
            "summary": {
                "total_videos": len(self.created_videos),
                "total_duration_minutes": total_duration,
                "total_duration_hours": round(total_duration / 60, 2),
                "subjects_covered": len(subjects),
                "youtube_uploads": youtube_uploads
            },
            "by_subject": subjects,
            "recent_videos": self.created_videos[-10:] if len(self.created_videos) > 10 else self.created_videos
        }
        
        print("📊 Universal Education Report")
        print("=" * 40)
        print(f"📚 Total Videos: {report['summary']['total_videos']}")
        print(f"⏱️ Total Duration: {report['summary']['total_duration_hours']} hours")
        print(f"🎓 Subjects Covered: {report['summary']['subjects_covered']}")
        print(f"📺 YouTube Uploads: {report['summary']['youtube_uploads']}")
        print("\nVideos by Subject:")
        for subject, count in subjects.items():
            print(f"   {subject}: {count} videos")
        
        # Save report
        report_file = f"education_report_{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report

def main():
    """Main function for universal education creation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Universal Educational Video Creator")
    parser.add_argument("--mode", choices=["daily", "subject", "curriculum", "report"], 
                       default="daily", help="Creation mode")
    parser.add_argument("--subject", help="Subject for focused creation")
    parser.add_argument("--num-videos", type=int, default=5, help="Number of videos")
    parser.add_argument("--weeks", type=int, default=4, help="Curriculum duration in weeks")
    
    args = parser.parse_args()
    
    creator = UniversalEducationCreator()
    
    if args.mode == "daily":
        creator.create_daily_videos()
    elif args.mode == "subject":
        if not args.subject:
            print("❌ Please specify --subject")
            print("Available subjects:")
            for subject in COMPLETE_EDUCATION_SUBJECTS.keys():
                print(f"   - {subject}")
            return
        creator.create_subject_focus(args.subject, args.num_videos)
    elif args.mode == "curriculum":
        if not args.subject:
            print("❌ Please specify --subject for curriculum")
            return
        curriculum = creator.create_curriculum_series(args.subject, args.weeks)
        print(f"📚 Created curriculum plan for {args.subject}")
    elif args.mode == "report":
        creator.generate_education_report()

if __name__ == "__main__":
    main()
