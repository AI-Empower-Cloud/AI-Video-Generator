#!/usr/bin/env python3
"""
🎙️ Simplified Podcast & Interview Generator
Creates educational podcasts and interviews with better audio handling
"""

import subprocess
from pathlib import Path
import random
import json
import time
from datetime import datetime

class SimplePodcastGenerator:
    """Generate educational podcasts and interviews with simplified audio processing"""
    
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
        
        # Podcast content
        self.podcast_content = {
            'abc_stories': [
                {
                    'title': 'The Amazing Adventure of Andy the Ant',
                    'content': "Welcome to ABC Story Time! Today's letter is A, and we're learning about Andy the Ant. Andy is an amazing ant who goes on exciting adventures. He teaches us that being active and ambitious leads to great achievements. Join Andy as he explores the world and makes new friends along the way!"
                },
                {
                    'title': "Bella the Butterfly's Big Day",
                    'content': "Today's letter is B! Meet Bella the Butterfly, who is having the biggest day of her life. Bella shows us how being brave and beautiful inside and out can help us overcome challenges. Watch as Bella spreads her wings and discovers the world around her!"
                },
                {
                    'title': "Charlie the Cat's Cooking Class",
                    'content': "Letter C brings us Charlie the Cat! Charlie is a creative cat who loves to cook. He teaches us that being curious and careful in the kitchen leads to delicious results. Come along as Charlie creates amazing dishes and shares his culinary secrets!"
                },
                {
                    'title': "Danny the Dog's Dance Party",
                    'content': "It's time for letter D with Danny the Dog! Danny is a delightful dog who loves to dance. He shows us that being determined and daring helps us learn new moves. Join Danny's dance party and discover the joy of movement and music!"
                },
                {
                    'title': "Emma the Elephant's Exciting Expedition",
                    'content': "Letter E introduces Emma the Elephant! Emma is going on an exciting expedition to explore new places. She teaches us that being enthusiastic and energetic helps us discover amazing things. Follow Emma on her journey of exploration and learning!"
                }
            ],
            'science_fun': [
                {
                    'title': 'Why is the Sky Blue?',
                    'content': "Welcome to Science Fun! Today we're exploring colors and light. The sky appears blue because of how sunlight interacts with tiny particles in our atmosphere. When white light from the sun hits these particles, blue light gets scattered more than other colors, making the sky look blue to our eyes!"
                },
                {
                    'title': 'How Do Birds Fly?',
                    'content': "Let's discover the amazing world of flight! Birds can fly because of their special wing shape and strong flight muscles. Their wings create lift by pushing air down, which pushes them up. Combined with their lightweight bones and powerful hearts, birds are perfectly designed for soaring through the sky!"
                },
                {
                    'title': 'Journey to the Moon',
                    'content': "Join us on an incredible space adventure! The moon is Earth's closest neighbor in space, about 240,000 miles away. Astronauts have visited the moon and discovered it has no air or water, and its gravity is much weaker than Earth's. That's why astronauts can jump so high on the moon!"
                },
                {
                    'title': 'The Amazing Water Cycle',
                    'content': "Discover how water travels around our planet! The water cycle is nature's way of recycling water. The sun heats water in oceans and lakes, turning it into invisible water vapor. This rises into the sky, forms clouds, and eventually falls back down as rain or snow to start the cycle again!"
                },
                {
                    'title': 'How Plants Make Their Food',
                    'content': "Learn about the amazing process of photosynthesis! Plants are like little food factories that make their own meals using sunlight, water, and carbon dioxide from the air. Their green leaves capture sunlight and use it to create sugar for food, while also producing the oxygen we breathe!"
                }
            ],
            'math_adventures': [
                {
                    'title': 'Counting with the Number Pirates',
                    'content': "Ahoy, mateys! Welcome to Math Adventures! Today we're sailing with the Number Pirates who love to count their treasure. Counting helps us understand how many things we have. Let's count gold coins, precious gems, and learn that numbers are everywhere, from 1 to 10 and beyond!"
                },
                {
                    'title': 'The Shape Detective Mystery',
                    'content': "Calling all junior detectives! We're solving the mystery of shapes all around us. Circles are round like wheels, squares have four equal sides like windows, triangles have three sides like pizza slices, and rectangles are longer squares like doors. Shapes are everywhere!"
                },
                {
                    'title': 'Adding Up the Fun at the Fair',
                    'content': "Welcome to the math fair! Addition is like putting things together to find out how many you have in total. If you have 2 balloons and someone gives you 3 more balloons, you add them together: 2 plus 3 equals 5 balloons! Addition makes numbers grow bigger!"
                },
                {
                    'title': 'The Subtraction Superhero',
                    'content': "Meet our Subtraction Superhero who helps solve problems by taking things away! Subtraction is the opposite of addition. If you have 5 cookies and eat 2 cookies, you subtract: 5 minus 2 equals 3 cookies left. Subtraction helps us find out how many remain!"
                },
                {
                    'title': 'Pattern Party in the Forest',
                    'content': "Join the pattern party with forest friends! Patterns are things that repeat in order, like red-blue-red-blue or big-small-big-small. Animals make patterns with their spots and stripes, flowers bloom in patterns, and even our days follow patterns. Patterns are everywhere in nature!"
                }
            ]
        }
        
        # Interview content
        self.interview_content = {
            'teacher_interview': {
                'title': 'Modern Education Techniques',
                'conversation': [
                    ('host', "Welcome to our educational interview series! Today we're talking with an experienced teacher about modern education techniques."),
                    ('teacher', "Thank you for having me! I'm excited to share insights about how education has evolved to meet today's learning needs."),
                    ('host', "What makes learning fun for children today?"),
                    ('teacher', "Interactive activities, hands-on experiences, and technology integration make learning engaging. Children learn best when they can explore, experiment, and connect lessons to their daily lives."),
                    ('host', "How do you adapt teaching for different learning styles?"),
                    ('teacher', "Every child is unique! Some are visual learners who need pictures and diagrams, others are auditory learners who benefit from discussions and music, and kinesthetic learners need movement and hands-on activities."),
                    ('host', "What advice do you have for parents supporting learning at home?"),
                    ('teacher', "Create a positive learning environment, read together daily, ask open-ended questions, and celebrate curiosity. Most importantly, show that learning is a lifelong adventure!"),
                    ('host', "Thank you for these valuable insights into modern education!")
                ]
            },
            'student_showcase': {
                'title': 'Student Success Stories',
                'conversation': [
                    ('host', "Today we're featuring amazing students and their learning journeys! Let's hear from some young learners."),
                    ('student', "Hi! I'm so excited to share my love of learning with everyone!"),
                    ('host', "What's your favorite subject and why?"),
                    ('student', "I love science because we get to do experiments and discover how things work! It's like being a detective solving mysteries about the world around us."),
                    ('host', "How do you make learning fun?"),
                    ('student', "I ask lots of questions, use colorful notes, and try to connect what I learn to things I already know. I also like to teach my little brother what I've learned!"),
                    ('host', "What advice would you give other students?"),
                    ('student', "Never give up, even when something seems hard! Ask for help when you need it, and remember that making mistakes is part of learning. Every expert was once a beginner!"),
                    ('host', "What inspiring words from our young learners! Keep up the great work!")
                ]
            },
            'expert_discussion': {
                'title': 'Child Development and Learning',
                'conversation': [
                    ('host', "Welcome to our expert discussion on child development and learning. Today we're speaking with a child development specialist."),
                    ('expert', "Thank you for having me. Child development is a fascinating field that helps us understand how children grow and learn."),
                    ('host', "How do children learn best?"),
                    ('expert', "Children learn through active engagement, play, and social interaction. They need safe environments to explore, make mistakes, and build on their natural curiosity about the world."),
                    ('host', "What role does play have in learning?"),
                    ('expert', "Play is children's work! Through play, they develop social skills, creativity, problem-solving abilities, and emotional regulation. It's not separate from learning—it IS learning."),
                    ('host', "How can we prepare children for the future?"),
                    ('expert', "Focus on developing critical thinking, creativity, emotional intelligence, and adaptability. These skills will serve them well regardless of how the world changes."),
                    ('host', "Thank you for sharing your expertise on child development and learning!")
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
    
    def convert_to_mp3(self, wav_file, mp3_file):
        """Convert WAV to MP3"""
        cmd = [
            'ffmpeg', '-y',
            '-i', str(wav_file),
            '-acodec', 'mp3',
            '-b:a', '128k',
            str(mp3_file)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except:
            return False
    
    def create_podcast_episode(self, category, episode_data):
        """Create a complete podcast episode"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        episode_name = f"podcast_{category}_{timestamp}"
        
        print(f"🎙️ Creating: {episode_data['title']}")
        
        # Create the complete podcast content
        if category == 'abc_stories':
            full_content = f"Welcome to ABC Story Time! {episode_data['content']} Thanks for listening to our alphabet adventure!"
        elif category == 'science_fun':
            full_content = f"Welcome to Science Fun for Kids! {episode_data['content']} Keep exploring and asking questions about our amazing world!"
        else:  # math_adventures
            full_content = f"Welcome to Math Adventures! {episode_data['content']} Remember, math is everywhere and can be lots of fun!"
        
        # Create audio file
        wav_file = self.output_dir / f"{episode_name}.wav"
        mp3_file = self.output_dir / f"{episode_name}.mp3"
        
        if self.create_voice_audio(full_content, self.voices['narrator'], wav_file):
            if self.convert_to_mp3(wav_file, mp3_file):
                wav_file.unlink()  # Remove WAV file
                print(f"✅ Created: {mp3_file.name}")
                return str(mp3_file)
        
        return None
    
    def create_interview_episode(self, interview_key, interview_data):
        """Create an interview episode"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        interview_name = f"interview_{interview_key}_{timestamp}"
        
        print(f"🎤 Creating Interview: {interview_data['title']}")
        
        # Combine all conversation parts
        full_conversation = ""
        for speaker, text in interview_data['conversation']:
            full_conversation += f"{text} "
        
        # Create audio file
        wav_file = self.output_dir / f"{interview_name}.wav"
        mp3_file = self.output_dir / f"{interview_name}.mp3"
        
        if self.create_voice_audio(full_conversation, self.voices['host'], wav_file):
            if self.convert_to_mp3(wav_file, mp3_file):
                wav_file.unlink()  # Remove WAV file
                print(f"✅ Created: {mp3_file.name}")
                return str(mp3_file)
        
        return None
    
    def generate_all_content(self):
        """Generate all podcast and interview content"""
        print("🎙️ Educational Podcast & Interview Generator")
        print("=" * 60)
        
        created_files = []
        
        # Generate podcasts
        for category, episodes in self.podcast_content.items():
            print(f"\n📻 Creating {category.replace('_', ' ').title()} Series...")
            for episode in episodes:
                try:
                    file_path = self.create_podcast_episode(category, episode)
                    if file_path:
                        created_files.append(file_path)
                except Exception as e:
                    print(f"❌ Error: {e}")
        
        # Generate interviews
        print(f"\n🎤 Creating Interview Series...")
        for interview_key, interview_data in self.interview_content.items():
            try:
                file_path = self.create_interview_episode(interview_key, interview_data)
                if file_path:
                    created_files.append(file_path)
            except Exception as e:
                print(f"❌ Error: {e}")
        
        # Create metadata
        metadata = {
            'created': datetime.now().isoformat(),
            'total_files': len(created_files),
            'files': [Path(f).name for f in created_files],
            'categories': list(self.podcast_content.keys()) + list(self.interview_content.keys())
        }
        
        metadata_file = self.output_dir / "podcast_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\n🎊 Content Generation Complete!")
        print(f"📁 Total files created: {len(created_files)}")
        print(f"📊 Metadata saved: {metadata_file}")
        
        return created_files

def main():
    """Generate all podcast and interview content"""
    generator = SimplePodcastGenerator()
    generator.generate_all_content()

if __name__ == "__main__":
    main()
