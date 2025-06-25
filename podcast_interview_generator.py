#!/usr/bin/env python3
"""
🎙️ Podcast & Interview Generator
Creates educational podcasts and interviews with multiple voices and topics
"""

import soundfile as sf
from pathlib import Path
import subprocess
import random
import json
import time
from datetime import datetime

class PodcastInterviewGenerator:
    """Generate educational podcasts and interviews"""
    
    def __init__(self):
        self.output_dir = Path("podcast_output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Voice configurations for different characters
        self.voices = {
            'host': {'voice': 'en+f3', 'speed': 170, 'pitch': 45, 'amp': 200},
            'teacher': {'voice': 'en+f4', 'speed': 160, 'pitch': 50, 'amp': 190},
            'student': {'voice': 'en+f5', 'speed': 180, 'pitch': 55, 'amp': 185},
            'expert': {'voice': 'en+m3', 'speed': 150, 'pitch': 40, 'amp': 200},
            'child': {'voice': 'en+f6', 'speed': 190, 'pitch': 60, 'amp': 180},
            'narrator': {'voice': 'en+m4', 'speed': 155, 'pitch': 45, 'amp': 195}
        }
        
        # Podcast topics and content
        self.podcast_topics = {
            'abc_stories': {
                'title': 'ABC Story Time',
                'description': 'Interactive stories for each letter of the alphabet',
                'episodes': [
                    {'letter': 'A', 'story': 'The Amazing Adventure of Andy the Ant'},
                    {'letter': 'B', 'story': 'Bella the Butterfly\'s Big Day'},
                    {'letter': 'C', 'story': 'Charlie the Cat\'s Cooking Class'},
                    {'letter': 'D', 'story': 'Danny the Dog\'s Dance Party'},
                    {'letter': 'E', 'story': 'Emma the Elephant\'s Exciting Expedition'}
                ]
            },
            'science_fun': {
                'title': 'Science Fun for Kids',
                'description': 'Exploring science through fun experiments and stories',
                'episodes': [
                    {'topic': 'Colors', 'title': 'Why is the Sky Blue?'},
                    {'topic': 'Animals', 'title': 'How Do Birds Fly?'},
                    {'topic': 'Space', 'title': 'Journey to the Moon'},
                    {'topic': 'Water', 'title': 'The Amazing Water Cycle'},
                    {'topic': 'Plants', 'title': 'How Plants Make Their Food'}
                ]
            },
            'math_adventures': {
                'title': 'Math Adventures',
                'description': 'Making math fun with stories and games',
                'episodes': [
                    {'concept': 'Counting', 'title': 'Counting with the Number Pirates'},
                    {'concept': 'Shapes', 'title': 'The Shape Detective Mystery'},
                    {'concept': 'Addition', 'title': 'Adding Up the Fun at the Fair'},
                    {'concept': 'Subtraction', 'title': 'The Subtraction Superhero'},
                    {'concept': 'Patterns', 'title': 'Pattern Party in the Forest'}
                ]
            }
        }
        
        # Interview scenarios
        self.interview_scenarios = {
            'teacher_interview': {
                'participants': ['host', 'teacher'],
                'topic': 'Modern Education Techniques',
                'questions': [
                    "What makes learning fun for children today?",
                    "How do you adapt teaching for different learning styles?",
                    "What role does technology play in modern education?",
                    "How can parents support learning at home?",
                    "What's the future of education?"
                ]
            },
            'student_showcase': {
                'participants': ['host', 'student', 'child'],
                'topic': 'Student Success Stories',
                'questions': [
                    "What's your favorite subject and why?",
                    "How do you make learning fun?",
                    "What advice would you give other students?",
                    "What do you want to be when you grow up?",
                    "What's the coolest thing you've learned recently?"
                ]
            },
            'expert_discussion': {
                'participants': ['host', 'expert'],
                'topic': 'Child Development and Learning',
                'questions': [
                    "How do children learn best?",
                    "What are the key developmental milestones?",
                    "How can we support creative thinking?",
                    "What role does play have in learning?",
                    "How do we prepare kids for the future?"
                ]
            }
        }
    
    def create_voice_audio(self, text, voice_config, output_file):
        """Create audio with specific voice configuration"""
        cmd = [
            'espeak',
            '-v', voice_config['voice'],
            '-s', str(voice_config['speed']),
            '-p', str(voice_config['pitch']),
            '-a', str(voice_config['amp']),
            '-g', '10',
            '-w', str(output_file),
            text
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except Exception as e:
            print(f"Error creating voice: {e}")
            return False
    
    def add_audio_effects(self, input_file, output_file, effect_type='podcast'):
        """Add audio effects for professional sound"""
        if effect_type == 'podcast':
            # Add compression and normalization for podcast
            cmd = [
                'ffmpeg', '-y',
                '-i', input_file,
                '-af', 'dynaudnorm,highpass=f=80,lowpass=f=10000',
                '-ar', '44100',
                '-b:a', '128k',
                output_file
            ]
        elif effect_type == 'interview':
            # Add slight reverb for interview atmosphere
            cmd = [
                'ffmpeg', '-y',
                '-i', input_file,
                '-af', 'aecho=0.8:0.9:1000:0.3,dynaudnorm',
                '-ar', '44100',
                '-b:a', '128k',
                output_file
            ]
        else:
            # Default processing
            cmd = [
                'ffmpeg', '-y',
                '-i', input_file,
                '-af', 'dynaudnorm',
                '-ar', '44100',
                '-b:a', '128k',
                output_file
            ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except:
            return False
    
    def combine_audio_segments(self, segments, output_file, add_music=True):
        """Combine multiple audio segments with optional background music"""
        if not segments:
            return False
        
        # Create a temporary file list for ffmpeg
        temp_list = self.output_dir / "temp_segments.txt"
        
        with open(temp_list, 'w') as f:
            for segment in segments:
                f.write(f"file '{segment}'\n")
        
        if add_music:
            # Combine with background music
            cmd = [
                'ffmpeg', '-y',
                '-f', 'concat',
                '-safe', '0',
                '-i', str(temp_list),
                '-filter_complex', '[0:a]volume=1.0[a]',
                '-map', '[a]',
                '-c:a', 'mp3',
                '-b:a', '128k',
                str(output_file)
            ]
        else:
            # Simple concatenation
            cmd = [
                'ffmpeg', '-y',
                '-f', 'concat',
                '-safe', '0',
                '-i', str(temp_list),
                '-c', 'copy',
                str(output_file)
            ]
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True)
            temp_list.unlink()
            return True
        except Exception as e:
            print(f"Error combining audio: {e}")
            if temp_list.exists():
                temp_list.unlink()
            return False
    
    def create_podcast_episode(self, topic_key, episode_data):
        """Create a complete podcast episode"""
        topic = self.podcast_topics[topic_key]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if 'letter' in episode_data:
            episode_name = f"podcast_{topic_key}_{episode_data['letter']}_{timestamp}"
            story_title = episode_data['story']
        elif 'topic' in episode_data:
            episode_name = f"podcast_{topic_key}_{episode_data['topic'].lower()}_{timestamp}"
            story_title = episode_data['title']
        else:
            episode_name = f"podcast_{topic_key}_{episode_data['concept'].lower()}_{timestamp}"
            story_title = episode_data['title']
        
        print(f"🎙️ Creating Podcast Episode: {story_title}")
        
        segments = []
        
        # 1. Intro
        intro_text = f"Welcome to {topic['title']}! I'm your host, and today we're exploring {story_title}. Let's dive in!"
        intro_file = self.output_dir / f"{episode_name}_intro.wav"
        if self.create_voice_audio(intro_text, self.voices['host'], intro_file):
            segments.append(str(intro_file))
        
        # 2. Main content based on topic
        if topic_key == 'abc_stories':
            main_content = self.create_abc_story_content(episode_data)
        elif topic_key == 'science_fun':
            main_content = self.create_science_content(episode_data)
        else:
            main_content = self.create_math_content(episode_data)
        
        # Create main content segments
        for i, (speaker, text) in enumerate(main_content):
            segment_file = self.output_dir / f"{episode_name}_segment_{i}.wav"
            if self.create_voice_audio(text, self.voices[speaker], segment_file):
                segments.append(str(segment_file))
        
        # 3. Outro
        outro_text = f"That's all for today's episode of {topic['title']}! Thanks for listening, and remember - learning is always an adventure!"
        outro_file = self.output_dir / f"{episode_name}_outro.wav"
        if self.create_voice_audio(outro_text, self.voices['host'], outro_file):
            segments.append(str(outro_file))
        
        # Combine all segments
        final_file = self.output_dir / f"{episode_name}.mp3"
        if self.combine_audio_segments(segments, final_file):
            # Clean up temporary files
            for segment in segments:
                Path(segment).unlink()
            
            print(f"✅ Podcast episode created: {final_file}")
            return str(final_file)
        
        return None
    
    def create_abc_story_content(self, episode_data):
        """Create content for ABC story podcast"""
        letter = episode_data['letter']
        story = episode_data['story']
        
        content = [
            ('narrator', f"Today's letter is {letter}! Let's hear the story of {story}."),
            ('teacher', f"Once upon a time, there was a character whose name started with {letter}. Can you guess what it might be?"),
            ('child', f"Is it {letter.lower()}... {letter.lower()}... Oh! I know! It starts with {letter}!"),
            ('narrator', f"That's right! Our story is about {story}. Listen carefully as we tell this exciting tale!"),
            ('teacher', f"The {letter} character goes on an amazing adventure. They learn about friendship, courage, and the importance of being kind."),
            ('child', f"I love stories about {letter}! What happens next?"),
            ('narrator', f"And that's how our {letter} character saved the day! What a wonderful adventure!"),
            ('host', f"What did you learn from this story? Remember, every letter has its own special story to tell!")
        ]
        
        return content
    
    def create_science_content(self, episode_data):
        """Create content for science podcast"""
        topic = episode_data['topic']
        title = episode_data['title']
        
        content = [
            ('narrator', f"Today we're exploring the wonderful world of science! Our topic is: {title}"),
            ('expert', f"Hello everyone! I'm a scientist, and I'm excited to share some amazing facts about {topic.lower()}."),
            ('child', f"Wow! Science is so cool! Can you tell us something amazing?"),
            ('expert', f"Did you know that {topic.lower()} has some incredible properties? Let me explain in a fun way!"),
            ('teacher', f"This is fascinating! Can you help us understand this better?"),
            ('expert', f"Of course! Think of it like this - science is all around us, and {topic.lower()} is a perfect example!"),
            ('child', f"I want to be a scientist too! This is so interesting!"),
            ('narrator', f"Science helps us understand our amazing world. Keep asking questions and exploring!")
        ]
        
        return content
    
    def create_math_content(self, episode_data):
        """Create content for math podcast"""
        concept = episode_data['concept']
        title = episode_data['title']
        
        content = [
            ('narrator', f"Welcome to Math Adventures! Today's exciting story is: {title}"),
            ('teacher', f"Math is everywhere, and today we're going to discover {concept.lower()} in a fun way!"),
            ('child', f"I love math! It's like solving puzzles!"),
            ('teacher', f"That's exactly right! {concept} is like a puzzle that we can solve together."),
            ('child', f"Can you show us how {concept.lower()} works?"),
            ('teacher', f"Absolutely! Let's imagine we're going on an adventure where {concept.lower()} helps us solve problems."),
            ('narrator', f"Our math heroes use {concept.lower()} to save the day! Math really is magical!"),
            ('host', f"Remember, math is all around us. Look for {concept.lower()} in your daily life!")
        ]
        
        return content
    
    def create_interview(self, scenario_key):
        """Create an interview audio"""
        scenario = self.interview_scenarios[scenario_key]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        interview_name = f"interview_{scenario_key}_{timestamp}"
        
        print(f"🎤 Creating Interview: {scenario['topic']}")
        
        segments = []
        
        # Interview intro
        intro_text = f"Welcome to our special interview! Today we're discussing {scenario['topic']}. Let's meet our guests!"
        intro_file = self.output_dir / f"{interview_name}_intro.wav"
        if self.create_voice_audio(intro_text, self.voices['host'], intro_file):
            segments.append(str(intro_file))
        
        # Guest introductions
        for participant in scenario['participants'][1:]:  # Skip host
            intro_text = f"Hello everyone! I'm excited to be here to talk about {scenario['topic']}."
            guest_intro_file = self.output_dir / f"{interview_name}_{participant}_intro.wav"
            if self.create_voice_audio(intro_text, self.voices[participant], guest_intro_file):
                segments.append(str(guest_intro_file))
        
        # Interview questions and answers
        for i, question in enumerate(scenario['questions']):
            # Host asks question
            question_file = self.output_dir / f"{interview_name}_q{i}.wav"
            if self.create_voice_audio(question, self.voices['host'], question_file):
                segments.append(str(question_file))
            
            # Guest answers (rotate through guests)
            guest = scenario['participants'][1 + (i % len(scenario['participants'][1:]))]
            answer = self.generate_interview_answer(question, guest, scenario['topic'])
            answer_file = self.output_dir / f"{interview_name}_a{i}.wav"
            if self.create_voice_audio(answer, self.voices[guest], answer_file):
                segments.append(str(answer_file))
        
        # Interview outro
        outro_text = f"Thank you for joining us for this insightful discussion about {scenario['topic']}. Until next time!"
        outro_file = self.output_dir / f"{interview_name}_outro.wav"
        if self.create_voice_audio(outro_text, self.voices['host'], outro_file):
            segments.append(str(outro_file))
        
        # Combine all segments with interview effects
        final_file = self.output_dir / f"{interview_name}.mp3"
        if self.combine_audio_segments(segments, final_file):
            # Clean up temporary files
            for segment in segments:
                Path(segment).unlink()
            
            print(f"✅ Interview created: {final_file}")
            return str(final_file)
        
        return None
    
    def generate_interview_answer(self, question, guest_type, topic):
        """Generate contextual answers based on guest type"""
        if guest_type == 'teacher':
            if 'learning' in question.lower():
                return "In my experience, children learn best when they're engaged and having fun. Interactive activities and hands-on experiences make a huge difference."
            elif 'technology' in question.lower():
                return "Technology is a wonderful tool that can enhance learning, but it should complement, not replace, human interaction and creativity."
            elif 'parents' in question.lower():
                return "Parents play a crucial role by creating a supportive learning environment at home and showing genuine interest in their child's education."
            else:
                return "That's a great question! In education, we're always looking for new ways to inspire and motivate students to reach their full potential."
        
        elif guest_type == 'student' or guest_type == 'child':
            if 'favorite' in question.lower():
                return "I love science because we get to do cool experiments! It's like being a detective and solving mysteries about how things work."
            elif 'advice' in question.lower():
                return "I think the best advice is to never give up and always ask questions. Even if something seems hard, you can learn it if you keep trying!"
            elif 'future' in question.lower():
                return "I want to be a scientist or maybe an astronaut! I love learning about space and discovering new things."
            else:
                return "Learning is so much fun when you find something you're really interested in. I love asking questions and finding out new things!"
        
        elif guest_type == 'expert':
            if 'children' in question.lower():
                return "Research shows that children learn through play, exploration, and social interaction. They need safe environments to experiment and make mistakes."
            elif 'development' in question.lower():
                return "Key milestones include language development, social skills, and cognitive abilities. Each child develops at their own pace, which is perfectly normal."
            elif 'creative' in question.lower():
                return "Creativity flourishes when children have freedom to explore, access to diverse materials, and adults who value their unique ideas and expressions."
            else:
                return "The latest research in child development emphasizes the importance of emotional intelligence alongside academic skills for lifelong success."
        
        return "That's a wonderful question that really gets to the heart of what we're discussing today."
    
    def generate_all_podcasts(self):
        """Generate all podcast episodes"""
        print("🎙️ Creating Complete Podcast Collection!")
        print("=" * 60)
        
        created_files = []
        
        # Generate episodes for each topic
        for topic_key, topic_data in self.podcast_topics.items():
            print(f"\n📻 Creating {topic_data['title']} Series...")
            
            for episode_data in topic_data['episodes']:
                try:
                    podcast_file = self.create_podcast_episode(topic_key, episode_data)
                    if podcast_file:
                        created_files.append(podcast_file)
                except Exception as e:
                    print(f"❌ Error creating podcast: {e}")
        
        return created_files
    
    def generate_all_interviews(self):
        """Generate all interview episodes"""
        print("🎤 Creating Interview Collection!")
        print("=" * 60)
        
        created_files = []
        
        for scenario_key in self.interview_scenarios.keys():
            try:
                interview_file = self.create_interview(scenario_key)
                if interview_file:
                    created_files.append(interview_file)
            except Exception as e:
                print(f"❌ Error creating interview: {e}")
        
        return created_files
    
    def create_podcast_metadata(self, podcast_files, interview_files):
        """Create metadata file for all podcast content"""
        metadata = {
            'created': datetime.now().isoformat(),
            'total_episodes': len(podcast_files) + len(interview_files),
            'podcasts': {
                'episodes': len(podcast_files),
                'files': [Path(f).name for f in podcast_files]
            },
            'interviews': {
                'episodes': len(interview_files),
                'files': [Path(f).name for f in interview_files]
            },
            'topics': list(self.podcast_topics.keys()),
            'interview_scenarios': list(self.interview_scenarios.keys())
        }
        
        metadata_file = self.output_dir / "podcast_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"📊 Metadata saved: {metadata_file}")
        return str(metadata_file)

def main():
    """Generate all podcast and interview content"""
    generator = PodcastInterviewGenerator()
    
    print("🎙️ Educational Podcast & Interview Generator")
    print("=" * 60)
    
    # Generate all podcasts
    podcast_files = generator.generate_all_podcasts()
    
    # Generate all interviews
    interview_files = generator.generate_all_interviews()
    
    # Create metadata
    generator.create_podcast_metadata(podcast_files, interview_files)
    
    print(f"\n🎊 Podcast & Interview Collection Complete!")
    print(f"📻 Podcasts created: {len(podcast_files)}")
    print(f"🎤 Interviews created: {len(interview_files)}")
    print(f"📁 Total audio files: {len(podcast_files) + len(interview_files)}")
    
    print("\n📻 Podcast Episodes:")
    for file in podcast_files:
        print(f"  🎙️ {Path(file).name}")
    
    print("\n🎤 Interview Episodes:")
    for file in interview_files:
        print(f"  🎙️ {Path(file).name}")

if __name__ == "__main__":
    main()
