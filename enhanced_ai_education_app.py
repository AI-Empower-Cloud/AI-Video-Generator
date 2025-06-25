#!/usr/bin/env python3
"""
Enhanced AI Technology Education App with Local TTS

A comprehensive educational video generator featuring:
- 100% local Text-to-Speech (no API dependencies)
- Multi-character dialogues
- Interactive quizzes with audio
- Background music generation
- Advanced voice profiles for different educational contexts
"""

import os
import sys
import logging
from typing import Dict, List, Optional, Tuple
import json
from pathlib import Path

# Import our enhanced local audio system
try:
    from audio_integration import AdvancedAudioEngine
    from local_tts_engine import LocalTTSEngine
    from enhanced_video_generator import EnhancedVideoGenerator
    AUDIO_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Audio integration not available: {e}")
    AUDIO_AVAILABLE = False

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocalTTSEducationApp:
    """Enhanced educational app with complete local TTS capabilities."""
    
    def __init__(self):
        """Initialize the education app with local TTS."""
        self.logger = logging.getLogger(__name__)
        
        # Initialize audio engine
        if AUDIO_AVAILABLE:
            self.audio_engine = AdvancedAudioEngine()
            self.tts_engine = LocalTTSEngine()
            self.logger.info("✅ Local TTS education app initialized")
        else:
            self.audio_engine = None
            self.tts_engine = None
            self.logger.warning("⚠️  Audio features disabled")
        
        # Initialize video generator
        try:
            self.video_generator = EnhancedVideoGenerator()
        except:
            self.video_generator = None
            self.logger.warning("⚠️  Video generator not available")
        
        # Educational content templates
        self.subjects = self._load_subject_templates()
        
        # Audio profiles for different educational contexts
        self.educational_profiles = {
            'elementary': {
                'narrator': 'teacher_female',
                'student': 'student_female',
                'speed': 0.8,
                'enthusiasm': 'high'
            },
            'middle_school': {
                'narrator': 'teacher_male',
                'student': 'student_male',
                'speed': 0.9,
                'enthusiasm': 'medium'
            },
            'high_school': {
                'narrator': 'expert',
                'student': 'student_female',
                'speed': 1.0,
                'enthusiasm': 'medium'
            },
            'college': {
                'narrator': 'expert',
                'student': 'student_male',
                'speed': 1.0,
                'enthusiasm': 'low'
            },
            'professional': {
                'narrator': 'expert',
                'student': 'expert',
                'speed': 1.1,
                'enthusiasm': 'low'
            }
        }
    
    def _load_subject_templates(self) -> Dict:
        """Load educational subject templates."""
        return {
            'artificial_intelligence': {
                'title': 'Introduction to Artificial Intelligence',
                'description': 'Learn the fundamentals of AI and machine learning',
                'key_concepts': ['algorithms', 'data', 'learning', 'prediction', 'automation'],
                'difficulty_levels': ['elementary', 'middle_school', 'high_school', 'college', 'professional']
            },
            'machine_learning': {
                'title': 'Machine Learning Basics',
                'description': 'Understand how computers learn from data',
                'key_concepts': ['training', 'models', 'features', 'classification', 'regression'],
                'difficulty_levels': ['middle_school', 'high_school', 'college', 'professional']
            },
            'programming': {
                'title': 'Introduction to Programming',
                'description': 'Learn the basics of computer programming',
                'key_concepts': ['variables', 'functions', 'loops', 'conditions', 'debugging'],
                'difficulty_levels': ['elementary', 'middle_school', 'high_school', 'college']
            },
            'data_science': {
                'title': 'Data Science Fundamentals',
                'description': 'Explore the world of data analysis and visualization',
                'key_concepts': ['statistics', 'visualization', 'analysis', 'insights', 'patterns'],
                'difficulty_levels': ['high_school', 'college', 'professional']
            },
            'cybersecurity': {
                'title': 'Cybersecurity Basics',
                'description': 'Learn about digital security and privacy',
                'key_concepts': ['encryption', 'passwords', 'firewalls', 'threats', 'protection'],
                'difficulty_levels': ['middle_school', 'high_school', 'college', 'professional']
            },
            'robotics': {
                'title': 'Introduction to Robotics',
                'description': 'Discover how robots work and their applications',
                'key_concepts': ['sensors', 'actuators', 'programming', 'automation', 'interaction'],
                'difficulty_levels': ['elementary', 'middle_school', 'high_school', 'college']
            }
        }
    
    def create_interactive_lesson(self, subject: str, age_group: str, 
                                output_path: str = None) -> Optional[str]:
        """Create an interactive lesson with local TTS narration and dialogue."""
        if not AUDIO_AVAILABLE:
            self.logger.error("Audio features not available")
            return None
        
        try:
            subject_info = self.subjects.get(subject)
            if not subject_info:
                self.logger.error(f"Subject '{subject}' not found")
                return None
            
            if age_group not in subject_info['difficulty_levels']:
                self.logger.error(f"Age group '{age_group}' not available for {subject}")
                return None
            
            # Generate lesson content
            lesson_content = self._generate_lesson_content(subject, age_group)
            
            # Create audio components
            audio_files = self._create_lesson_audio(lesson_content, age_group)
            
            # Generate video if available
            if self.video_generator and output_path:
                video_result = self._create_lesson_video(lesson_content, audio_files, output_path)
                return video_result
            else:
                return audio_files.get('main_narration')
            
        except Exception as e:
            self.logger.error(f"Interactive lesson creation failed: {e}")
            return None
    
    def _generate_lesson_content(self, subject: str, age_group: str) -> Dict:
        """Generate lesson content adapted for age group."""
        subject_info = self.subjects[subject]
        
        # Adapt content based on age group
        if age_group == 'elementary':
            intro = f"Hi kids! Today we're going to learn about {subject_info['title']}. It's going to be fun and exciting!"
            explanation = self._create_simple_explanation(subject, subject_info)
            activities = self._create_elementary_activities(subject, subject_info)
        elif age_group == 'middle_school':
            intro = f"Welcome students! Let's explore {subject_info['title']} and discover how it works."
            explanation = self._create_detailed_explanation(subject, subject_info)
            activities = self._create_middle_school_activities(subject, subject_info)
        elif age_group == 'high_school':
            intro = f"Today we'll dive into {subject_info['title']} and understand its real-world applications."
            explanation = self._create_comprehensive_explanation(subject, subject_info)
            activities = self._create_high_school_activities(subject, subject_info)
        elif age_group in ['college', 'professional']:
            intro = f"In this session, we'll examine {subject_info['title']} from both theoretical and practical perspectives."
            explanation = self._create_advanced_explanation(subject, subject_info)
            activities = self._create_advanced_activities(subject, subject_info)
        
        return {
            'subject': subject,
            'age_group': age_group,
            'title': subject_info['title'],
            'introduction': intro,
            'main_explanation': explanation,
            'interactive_activities': activities,
            'conclusion': f"Great job learning about {subject_info['title']}! Keep exploring and asking questions."
        }
    
    def _create_simple_explanation(self, subject: str, subject_info: Dict) -> str:
        """Create simple explanation for elementary students."""
        explanations = {
            'artificial_intelligence': """
            Artificial Intelligence, or AI, is like giving computers a brain! 
            Just like you can learn new things, computers can learn too.
            They can recognize pictures, understand what you say, and even play games.
            AI helps us in many ways, like when you ask your phone a question!
            """,
            'programming': """
            Programming is like giving instructions to a computer.
            It's like teaching your pet a new trick, but instead we teach computers!
            We use special words called code to tell computers what to do.
            Programmers are like teachers for computers!
            """,
            'robotics': """
            Robots are machines that can move and do things by themselves.
            They have sensors to see and feel the world around them.
            Some robots can walk, others can fly, and some help us clean our houses!
            Robots are like helpful friends made of metal and computers.
            """
        }
        return explanations.get(subject, f"Let's learn about {subject_info['title']}!")
    
    def _create_detailed_explanation(self, subject: str, subject_info: Dict) -> str:
        """Create detailed explanation for middle school students."""
        explanations = {
            'artificial_intelligence': """
            Artificial Intelligence is a field of computer science that creates systems 
            capable of performing tasks that typically require human intelligence.
            AI systems can learn from data, recognize patterns, and make decisions.
            Examples include voice assistants, recommendation systems, and game-playing programs.
            AI is transforming many industries including healthcare, transportation, and education.
            """,
            'machine_learning': """
            Machine Learning is a subset of AI that enables computers to learn automatically 
            from experience without being explicitly programmed for every task.
            Instead of following pre-written instructions, ML systems improve their performance 
            by finding patterns in data and making predictions based on those patterns.
            """,
            'cybersecurity': """
            Cybersecurity is the practice of protecting digital systems, networks, and data 
            from digital attacks, unauthorized access, and damage.
            It involves using various techniques like encryption, firewalls, and secure passwords
            to keep our digital information safe from hackers and malicious software.
            """
        }
        return explanations.get(subject, f"Today we'll explore {subject_info['description']}")
    
    def _create_comprehensive_explanation(self, subject: str, subject_info: Dict) -> str:
        """Create comprehensive explanation for high school students."""
        explanations = {
            'data_science': """
            Data Science is an interdisciplinary field that combines statistics, 
            computer science, and domain expertise to extract insights from data.
            Data scientists collect, clean, analyze, and visualize data to discover patterns,
            make predictions, and inform decision-making across various industries.
            The field involves programming languages like Python and R, statistical methods,
            and machine learning algorithms to solve real-world problems.
            """
        }
        return explanations.get(subject, f"We'll examine {subject_info['description']} in detail.")
    
    def _create_advanced_explanation(self, subject: str, subject_info: Dict) -> str:
        """Create advanced explanation for college/professional level."""
        explanations = {
            'artificial_intelligence': """
            Artificial Intelligence encompasses multiple paradigms including symbolic AI,
            connectionist approaches through neural networks, and evolutionary computation.
            Modern AI systems leverage deep learning architectures, reinforcement learning,
            and transfer learning to achieve human-level performance in specific domains.
            Current research focuses on explainable AI, ethical considerations,
            and developing artificial general intelligence.
            """
        }
        return explanations.get(subject, f"Advanced exploration of {subject_info['description']}")
    
    def _create_elementary_activities(self, subject: str, subject_info: Dict) -> List[Dict]:
        """Create elementary-level activities."""
        return [
            {
                "type": "question",
                "question": f"Can you name one way {subject} helps us in daily life?",
                "expected_answer": "Various answers accepted",
                "feedback": "Great thinking! You're absolutely right!"
            },
            {
                "type": "drawing",
                "instruction": f"Draw a picture of how you imagine {subject} working!",
                "feedback": "What a creative drawing! You have great ideas!"
            }
        ]
    
    def _create_middle_school_activities(self, subject: str, subject_info: Dict) -> List[Dict]:
        """Create middle school-level activities."""
        activities = {
            'artificial_intelligence': [
                {
                    "type": "quiz",
                    "question": "What are the three main components that AI systems need to work?",
                    "options": ["Data, Algorithms, Computing Power", "Robots, Games, Apps", "Internet, Phones, Computers"],
                    "correct": 0,
                    "feedback": "Excellent! AI indeed needs data to learn from, algorithms to process information, and computing power to run."
                }
            ],
            'programming': [
                {
                    "type": "coding",
                    "instruction": "Let's think about the steps to make a sandwich. This is like programming!",
                    "steps": ["Get bread", "Add filling", "Close sandwich"],
                    "feedback": "Perfect! You understand how to break down tasks into steps, just like programming!"
                }
            ]
        }
        return activities.get(subject, [])
    
    def _create_high_school_activities(self, subject: str, subject_info: Dict) -> List[Dict]:
        """Create high school-level activities."""
        return [
            {
                "type": "analysis",
                "question": f"How might {subject} impact society in the next 10 years?",
                "guidance": "Consider both positive impacts and potential challenges",
                "feedback": "Thoughtful analysis! You're thinking critically about technology's role in society."
            }
        ]
    
    def _create_advanced_activities(self, subject: str, subject_info: Dict) -> List[Dict]:
        """Create college/professional-level activities."""
        return [
            {
                "type": "research",
                "question": f"Identify current research challenges in {subject}",
                "requirements": "Include at least 3 specific examples with citations",
                "feedback": "Excellent research! You're engaging with cutting-edge developments in the field."
            }
        ]
    
    def _create_lesson_audio(self, lesson_content: Dict, age_group: str) -> Dict[str, str]:
        """Create audio files for the lesson."""
        audio_files = {}
        profile = self.educational_profiles[age_group]
        
        try:
            # Main narration
            full_narration = f"""
            {lesson_content['introduction']}
            
            {lesson_content['main_explanation']}
            
            {lesson_content['conclusion']}
            """
            
            narration_result = self.audio_engine.generate_educational_narration(
                script=full_narration,
                subject=lesson_content['subject'],
                age_group=age_group,
                output_path=f"lesson_{lesson_content['subject']}_{age_group}_narration.wav"
            )
            
            if narration_result:
                audio_files['main_narration'] = narration_result
                self.logger.info(f"✅ Generated main narration: {narration_result}")
            
            # Interactive activities audio
            for i, activity in enumerate(lesson_content['interactive_activities']):
                if activity['type'] in ['question', 'quiz']:
                    dialogue = [
                        {"character": "teacher", "text": activity['question'], "pause_after": 2.0},
                        {"character": "student", "text": "Let me think about that...", "pause_after": 1.0},
                        {"character": "teacher", "text": activity['feedback'], "pause_after": 1.0}
                    ]
                    
                    activity_audio = self.audio_engine.generate_dialogue(
                        dialogue,
                        f"lesson_{lesson_content['subject']}_{age_group}_activity_{i}.wav"
                    )
                    
                    if activity_audio:
                        audio_files[f'activity_{i}'] = activity_audio
                        self.logger.info(f"✅ Generated activity audio {i}: {activity_audio}")
            
            # Background music
            emotion = 'excitement' if age_group in ['elementary', 'middle_school'] else 'calm'
            music_result = self.audio_engine.generate_background_music(
                emotion=emotion,
                duration=60.0,  # 1 minute of background music
                output_path=f"lesson_{lesson_content['subject']}_{age_group}_music.wav"
            )
            
            if music_result:
                audio_files['background_music'] = music_result
                self.logger.info(f"✅ Generated background music: {music_result}")
            
        except Exception as e:
            self.logger.error(f"Audio creation failed: {e}")
        
        return audio_files
    
    def _create_lesson_video(self, lesson_content: Dict, audio_files: Dict, 
                           output_path: str) -> Optional[str]:
        """Create video combining audio with visuals."""
        if not self.video_generator:
            self.logger.warning("Video generator not available")
            return None
        
        try:
            # Create video content structure
            video_content = {
                'title': lesson_content['title'],
                'scenes': [
                    {
                        'type': 'title',
                        'content': lesson_content['title'],
                        'duration': 3.0
                    },
                    {
                        'type': 'narration',
                        'content': lesson_content['main_explanation'],
                        'audio_file': audio_files.get('main_narration'),
                        'background_music': audio_files.get('background_music')
                    }
                ]
            }
            
            # Add activity scenes
            for i, activity in enumerate(lesson_content['interactive_activities']):
                if f'activity_{i}' in audio_files:
                    video_content['scenes'].append({
                        'type': 'interactive',
                        'content': activity,
                        'audio_file': audio_files[f'activity_{i}']
                    })
            
            # Generate video (this would integrate with the existing video generator)
            # For now, return the main narration file
            return audio_files.get('main_narration', output_path)
            
        except Exception as e:
            self.logger.error(f"Video creation failed: {e}")
            return None
    
    def create_subject_overview(self, age_group: str, output_dir: str = "educational_content") -> Dict[str, str]:
        """Create overview content for all available subjects."""
        if not AUDIO_AVAILABLE:
            return {}
        
        os.makedirs(output_dir, exist_ok=True)
        results = {}
        
        for subject, subject_info in self.subjects.items():
            if age_group in subject_info['difficulty_levels']:
                output_path = os.path.join(output_dir, f"{subject}_{age_group}_overview")
                
                result = self.create_interactive_lesson(
                    subject=subject,
                    age_group=age_group,
                    output_path=output_path
                )
                
                if result:
                    results[subject] = result
                    self.logger.info(f"✅ Created {subject} overview for {age_group}")
        
        return results
    
    def list_available_content(self) -> Dict:
        """List all available educational content."""
        return {
            'subjects': list(self.subjects.keys()),
            'age_groups': list(self.educational_profiles.keys()),
            'voice_profiles': self.tts_engine.list_available_voices() if self.tts_engine else [],
            'audio_available': AUDIO_AVAILABLE
        }
    
    def get_system_info(self) -> Dict:
        """Get information about the system capabilities."""
        info = {
            'audio_engine_available': AUDIO_AVAILABLE,
            'video_generator_available': self.video_generator is not None,
            'local_tts': True,
            'api_dependencies': False
        }
        
        if AUDIO_AVAILABLE:
            info['tts_engines'] = self.tts_engine.get_engine_info()
            info['available_voices'] = self.tts_engine.list_available_voices()
        
        return info

def main():
    """Main function to demonstrate the enhanced education app."""
    print("🎓 Enhanced AI Technology Education App with Local TTS")
    print("=" * 60)
    
    # Initialize app
    app = LocalTTSEducationApp()
    
    # Display system info
    system_info = app.get_system_info()
    print(f"🔧 System Info: {system_info}")
    print()
    
    # List available content
    content_info = app.list_available_content()
    print(f"📚 Available subjects: {content_info['subjects']}")
    print(f"👥 Age groups: {content_info['age_groups']}")
    print(f"🎤 Voice profiles: {len(content_info['voice_profiles'])} available")
    print()
    
    if AUDIO_AVAILABLE:
        # Create sample lessons
        print("🎬 Creating sample educational content...")
        
        # Elementary AI lesson
        print("Creating elementary AI lesson...")
        result1 = app.create_interactive_lesson(
            subject='artificial_intelligence',
            age_group='elementary',
            output_path='ai_elementary_lesson.wav'
        )
        
        if result1:
            print(f"✅ Elementary AI lesson created: {result1}")
        
        # High school programming lesson
        print("Creating high school programming lesson...")
        result2 = app.create_interactive_lesson(
            subject='programming',
            age_group='high_school',
            output_path='programming_highschool_lesson.wav'
        )
        
        if result2:
            print(f"✅ High school programming lesson created: {result2}")
        
        # Professional data science overview
        print("Creating professional data science overview...")
        result3 = app.create_interactive_lesson(
            subject='data_science',
            age_group='professional',
            output_path='datascience_professional_lesson.wav'
        )
        
        if result3:
            print(f"✅ Professional data science lesson created: {result3}")
        
        print()
        print("🎉 Sample educational content generation completed!")
        print("✅ All content generated using 100% local TTS - no API dependencies!")
        
    else:
        print("⚠️  Audio features not available. Please install required dependencies.")
    
    print("\n🚀 Enhanced AI Technology Education App ready for use!")

if __name__ == "__main__":
    main()
