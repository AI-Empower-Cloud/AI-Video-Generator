#!/usr/bin/env python3
"""
🎓 UNIVERSAL Educational Video Generator for ALL SUBJECTS
✨ Create 10-40 minute professional educational videos for ANY topic
🌍 Supports EVERY subject: STEM, Languages, Humanities, Arts, Spiritual Studies, Business, and more
📺 Automatic YouTube upload with SEO optimization
👨‍🏫 Perfect for educators, students, and content creators worldwide
"""

import streamlit as st
import random
import time
import os
import json
from datetime import datetime
from pathlib import Path
import sys

# Add project root to path
sys.path.append('/workspaces/AI-Video-Generator')

from enhanced_video_generator import AdvancedVideoGenerator
from main import upload_to_youtube

# Educational subjects configuration
EDUCATIONAL_SUBJECTS = {
    "Mathematics": {
        "topics": [
            "Algebra Fundamentals", "Geometry Basics", "Calculus Introduction",
            "Statistics and Probability", "Number Theory", "Trigonometry",
            "Linear Algebra", "Differential Equations", "Mathematical Logic"
        ],
        "levels": ["Elementary", "Middle School", "High School", "College"],
        "duration_range": (15, 35),
        "voice_style": "clear_teacher"
    },
    "Science": {
        "topics": [
            "Physics Laws", "Chemistry Reactions", "Biology Fundamentals",
            "Earth Science", "Astronomy", "Quantum Physics", "Organic Chemistry",
            "Human Anatomy", "Ecology", "Genetics", "Thermodynamics"
        ],
        "levels": ["Elementary", "Middle School", "High School", "College"],
        "duration_range": (20, 40),
        "voice_style": "scientific_narrator"
    },
    "History": {
        "topics": [
            "Ancient Civilizations", "World Wars", "Renaissance Period",
            "Industrial Revolution", "American History", "European History",
            "Asian History", "African History", "Modern History"
        ],
        "levels": ["Elementary", "Middle School", "High School", "College"],
        "duration_range": (25, 40),
        "voice_style": "storyteller"
    },
    "Language Arts": {
        "topics": [
            "Grammar Fundamentals", "Creative Writing", "Literature Analysis",
            "Poetry Appreciation", "Public Speaking", "Reading Comprehension",
            "Vocabulary Building", "Essay Writing", "Critical Thinking"
        ],
        "levels": ["Elementary", "Middle School", "High School", "College"],
        "duration_range": (15, 30),
        "voice_style": "articulate_teacher"
    },
    "Sanskrit/Spiritual": {
        "topics": [
            "Gayatri Mantra", "Sanskrit Slokas", "Vedic Teachings",
            "Bhagavad Gita", "Upanishads", "Yoga Philosophy",
            "Meditation Techniques", "Pranayama", "Spiritual Wisdom"
        ],
        "levels": ["Beginner", "Intermediate", "Advanced", "Scholar"],
        "duration_range": (20, 45),
        "voice_style": "spiritual_guide"
    },
    "Computer Science": {
        "topics": [
            "Programming Basics", "Data Structures", "Algorithms",
            "Web Development", "Machine Learning", "Database Systems",
            "Software Engineering", "Cybersecurity", "AI Fundamentals"
        ],
        "levels": ["Beginner", "Intermediate", "Advanced", "Expert"],
        "duration_range": (25, 40),
        "voice_style": "tech_instructor"
    },
    "Art & Music": {
        "topics": [
            "Drawing Fundamentals", "Color Theory", "Music Theory",
            "Art History", "Digital Art", "Classical Music", "Modern Art",
            "Sculpture", "Photography", "Musical Instruments"
        ],
        "levels": ["Beginner", "Intermediate", "Advanced", "Professional"],
        "duration_range": (20, 35),
        "voice_style": "creative_mentor"
    },
    "Economics": {
        "topics": [
            "Microeconomics", "Macroeconomics", "Market Structures",
            "International Trade", "Economic History", "Behavioral Economics",
            "Financial Markets", "Economic Policy", "Development Economics"
        ],
        "levels": ["High School", "College", "Graduate", "Professional"],
        "duration_range": (25, 40),
        "voice_style": "professional_analyst"
    },
    "Psychology": {
        "topics": [
            "Cognitive Psychology", "Behavioral Psychology", "Social Psychology",
            "Developmental Psychology", "Abnormal Psychology", "Learning Theory",
            "Memory and Cognition", "Personality Theory", "Research Methods"
        ],
        "levels": ["High School", "College", "Graduate", "Professional"],
        "duration_range": (20, 35),
        "voice_style": "calm_therapist"
    },
    "Geography": {
        "topics": [
            "Physical Geography", "Human Geography", "Climate Studies",
            "Cultural Geography", "Economic Geography", "Political Geography",
            "Environmental Geography", "Urban Planning", "GIS and Mapping"
        ],
        "levels": ["Elementary", "Middle School", "High School", "College"],
        "duration_range": (20, 35),
        "voice_style": "explorer_guide"
    },
    "AI for Middle School": {
        "topics": [
            "What is Artificial Intelligence?", "How Smart Phones Use AI",
            "AI in Video Games", "Virtual Assistants Like Siri and Alexa",
            "AI in Social Media Apps", "How AI Helps Doctors",
            "AI in Self-Driving Cars", "Machine Learning for Kids",
            "AI Art and Creativity", "The Future of AI Technology"
        ],
        "levels": ["6th Grade", "7th Grade", "8th Grade"],
        "duration_range": (12, 20),
        "voice_style": "friendly_teacher"
    },
    "AI for High School": {
        "topics": [
            "Introduction to Machine Learning", "Neural Networks Explained",
            "AI Ethics and Society", "Programming AI with Python",
            "Computer Vision Basics", "Natural Language Processing",
            "AI in Healthcare and Medicine", "Robotics and AI",
            "AI Career Paths", "Building Your First AI Project",
            "Deep Learning Fundamentals", "AI Research Methods"
        ],
        "levels": ["9th Grade", "10th Grade", "11th Grade", "12th Grade"],
        "duration_range": (20, 35),
        "voice_style": "tech_instructor"
    },
    "Professional AI Tools": {
        "topics": [
            "ChatGPT for Business Productivity", "AI Tools for Content Creation",
            "Machine Learning for Data Analysis", "AI in Digital Marketing",
            "Automation with AI Tools", "AI for Project Management",
            "AI in Customer Service", "AI Writing and Editing Tools",
            "AI for Financial Analysis", "AI in Human Resources",
            "Building AI Workflows", "AI Tool Integration Strategies"
        ],
        "levels": ["Professional", "Executive", "Specialist", "Expert"],
        "duration_range": (20, 35),
        "voice_style": "business_consultant"
    },
    "Computer Programming": {
        "topics": [
            "Python Programming Basics", "Web Development with HTML/CSS",
            "JavaScript for Beginners", "Database Design and SQL",
            "Mobile App Development", "Game Development Basics",
            "Software Engineering Principles", "Version Control with Git",
            "Data Structures and Algorithms", "Cybersecurity Fundamentals",
            "Cloud Computing Basics", "API Development and Integration"
        ],
        "levels": ["Beginner", "Intermediate", "Advanced", "Expert"],
        "duration_range": (25, 40),
        "voice_style": "coding_mentor"
    }
}

def generate_educational_script(subject, topic, level, duration):
    """Generate educational script based on subject, topic, level, and duration."""
    
    # Base script templates for different subjects
    script_templates = {
        "Mathematics": f"""
Welcome to today's {level} lesson on {topic}.

Mathematics is the language of the universe, and today we'll explore {topic} in a way that makes it clear and engaging.

Let's start with the fundamentals. {topic} is essential because it helps us understand patterns and solve real-world problems.

First, let's understand what {topic} means and why it's important...

[The script continues with detailed explanations, examples, and practice problems]

Key concepts we'll cover:
1. Basic definitions and terminology
2. Step-by-step problem-solving methods
3. Real-world applications
4. Common mistakes to avoid
5. Practice exercises

Remember, mathematics is about logical thinking and pattern recognition. Take your time to understand each concept before moving to the next.

Let's work through some examples together...

[Detailed examples and explanations follow]

In conclusion, {topic} is a powerful tool that helps us solve problems and understand the world around us. Keep practicing, and you'll master these concepts!
""",
        
        "Science": f"""
Welcome to our {level} exploration of {topic}.

Science is about understanding how our world works, and {topic} reveals fascinating secrets about nature.

Today's journey will take us through the wonderful world of {topic}, where we'll discover amazing facts and principles.

Let's begin with observation - the foundation of all scientific learning...

[The script continues with scientific explanations, experiments, and discoveries]

What we'll explore today:
1. Key scientific principles
2. Historical discoveries
3. Modern applications
4. Hands-on experiments you can try
5. Future possibilities

Science is all around us, and {topic} shows us how incredible our universe really is.

Let's dive into the fascinating details...

[Detailed scientific content follows]

Remember, science is about curiosity and discovery. Keep asking questions and exploring!
""",

        "Sanskrit/Spiritual": f"""
नमस्ते and welcome to our spiritual journey exploring {topic}.

Today we embark on a sacred learning path that has guided humanity for thousands of years.

{topic} carries profound wisdom that can transform our understanding of life and consciousness.

Let us begin with reverence and an open heart...

[The script continues with spiritual teachings, Sanskrit pronunciation, and meanings]

Our spiritual exploration includes:
1. Sacred pronunciation and meaning
2. Historical and cultural context
3. Practical applications in daily life
4. Meditation and contemplation practices
5. Connection to higher consciousness

The ancient sages gifted us these teachings to help us find peace, wisdom, and spiritual growth.

Let us chant together and feel the vibrations of these sacred sounds...

[Detailed spiritual content and practices follow]

May this knowledge bring you peace, wisdom, and spiritual awakening.
""",

        "AI for Middle School": f"""
🤖 Welcome to AI Adventures! Today we're exploring: {topic}

Hi everyone! I'm excited to share with you the amazing world of Artificial Intelligence!

Have you ever wondered how your phone knows what you're saying when you talk to Siri? Or how Netflix knows what movies you might like? That's AI at work!

Today we're going to learn about {topic} in a fun and easy way.

🌟 What we'll discover today:
• What {topic} really means in simple terms
• How it affects your daily life
• Cool examples you can see right now
• Why this technology is so exciting
• How you might use it in the future

Let's start with a question: Have you ever noticed how your phone can recognize your face to unlock? That's a type of AI called computer vision!

AI isn't just for scientists and engineers - it's all around us, helping make our lives easier and more fun!

Remember: AI is a tool that helps humans do amazing things. The most important part is always the human creativity and ideas!

🚀 What's next? Keep exploring, stay curious, and maybe you'll help create the next amazing AI technology!
""",

        "AI for High School": f"""
🧠 Advanced AI Learning: {topic}

Welcome to today's exploration of {topic} - one of the most exciting areas in modern technology.

As high school students, you're at the perfect age to understand both the technical aspects and real-world implications of AI.

Today's Learning Objectives:
• Understand the technical foundations of {topic}
• Explore real-world applications and case studies
• Discuss ethical considerations and social impact
• Hands-on coding examples (when applicable)
• Career pathways in AI and technology

The algorithms behind {topic} involve complex mathematical concepts including statistics, linear algebra, and calculus. Don't worry if you haven't mastered these yet - we'll explain the core ideas clearly.

💡 Real-World Applications:
Companies like Google, Tesla, and medical institutions use these exact techniques to solve real problems.

🤔 Critical Thinking Questions:
• How might this technology impact society?
• What are the potential benefits and risks?
• How can we ensure AI development is ethical?

Your generation will shape the future of AI. Understanding these concepts now gives you the power to be creators, not just consumers, of AI technology.

🎯 Next Steps: Consider exploring programming languages like Python, taking statistics courses, and staying curious about emerging technologies.
""",

        "Professional AI Tools": f"""
🚀 Professional AI Mastery: {topic}

Welcome to advanced AI tools for business professionals. Today we're exploring {topic} and how it can transform your workflow.

In today's competitive business environment, AI literacy isn't optional - it's essential for professional success.

📊 Business Impact Overview:
• Productivity improvements: 25-40% efficiency gains
• Cost reduction: Significant operational savings
• Competitive advantage: Stay ahead of the curve
• Career advancement: AI skills are highly valued

🛠️ Practical Implementation:
Let's walk through real business scenarios where {topic} delivers measurable results.

💼 Business Case Studies:
• Fortune 500 companies using this approach
• SMB success stories and implementations
• Measurable outcomes and KPIs
• Implementation timelines and costs

📈 Measuring Success:
Key metrics to track ROI and effectiveness of AI tool implementation.

Your competitive advantage comes from not just knowing about AI tools, but mastering their strategic implementation.

🎯 Action Items: Start with one tool, master it completely, then expand your AI toolkit strategically.
""",

        "default": f"""
Welcome to today's comprehensive lesson on {topic} for {level} learners.

Today we'll explore {topic} in depth, providing you with clear understanding and practical knowledge.

This subject is fascinating because it connects to so many aspects of our lives and learning.

Let's begin our educational journey...

[The script continues with subject-specific content]

What you'll learn today:
1. Core concepts and principles
2. Historical background
3. Practical applications
4. Critical thinking exercises
5. Future developments

Learning is a lifelong adventure, and {topic} opens doors to new understanding.

Let's explore this topic step by step...

[Detailed educational content follows]

Remember, every expert was once a beginner. Keep learning and growing!
"""
    }
    
    # Get appropriate template
    template = script_templates.get(subject, script_templates["default"])
    
    # Expand script based on duration (roughly 150 words per minute)
    target_words = duration * 150
    
    # Add more content based on duration
    if duration > 20:
        template += f"""

EXTENDED SECTION: Advanced {topic} Concepts

Now that we've covered the basics, let's dive deeper into advanced aspects of {topic}.

This extended section will provide you with comprehensive understanding and expert-level insights.

[Additional 10-15 minutes of detailed content]

Advanced topics include:
- Cutting-edge research and developments
- Expert techniques and methodologies
- Real-world case studies and applications
- Connections to other fields of study
- Future trends and possibilities

Let's explore these advanced concepts that will take your understanding to the next level...
"""
    
    if duration > 30:
        template += f"""

MASTERY SECTION: Becoming an Expert in {topic}

For those seeking mastery, this section provides expert-level knowledge and insights.

We'll explore the most sophisticated aspects of {topic} and how experts think about these concepts.

[Additional 10+ minutes of expert-level content]

Mastery elements include:
- Expert problem-solving strategies
- Advanced theoretical frameworks
- Research methodologies
- Professional applications
- Teaching and mentoring others

True mastery comes from deep understanding and the ability to apply knowledge creatively...
"""
    
    return template

def create_educational_video(subject, topic, level, duration, auto_upload=False):
    """Create a complete educational video."""
    
    print(f"🎓 Creating {duration}-minute educational video:")
    print(f"   Subject: {subject}")
    print(f"   Topic: {topic}")
    print(f"   Level: {level}")
    
    # Generate educational script
    script = generate_educational_script(subject, topic, level, duration)
    
    # Create characters (educational presenters)
    characters = [
        {
            'name': 'Professor',
            'gender': 'neutral',
            'style': 'professional',
            'role': 'main_teacher'
        },
        {
            'name': 'Student',
            'gender': 'neutral', 
            'style': 'curious',
            'role': 'learner'
        }
    ]
    
    # Create educational scenes
    scenes = [
        {
            'description': f'Introduction to {topic}',
            'emotion': 'joy',
            'setting': 'classroom',
            'duration': duration * 0.1  # 10% for intro
        },
        {
            'description': f'Core concepts of {topic}',
            'emotion': 'neutral',
            'setting': 'educational',
            'duration': duration * 0.6  # 60% for main content
        },
        {
            'description': f'Summary and conclusion of {topic}',
            'emotion': 'satisfaction',
            'setting': 'classroom',
            'duration': duration * 0.3  # 30% for conclusion
        }
    ]
    
    # Generate video
    generator = AdvancedVideoGenerator()
    
    timestamp = int(time.time())
    video_filename = f"educational_{subject.lower().replace(' ', '_')}_{topic.lower().replace(' ', '_')}_{timestamp}.mp4"
    
    # Audio settings for educational content
    audio_settings = {
        'enable_audio': True,
        'enable_background_music': True,
        'music_style': 'ambient',
        'voice_settings': {
            'rate': 130,  # Slower for educational content
            'volume': 0.95,
            'voice_id': 'educational',
            'pitch': 1.0
        }
    }
    
    # Animation settings for educational content
    animation_settings = {
        'enable_advanced_animation': True,
        'animation_style': 'professional',
        'enable_particle_effects': False  # Clean look for education
    }
    
    video_path = generator.generate_story_video(
        script=script,
        characters=characters,
        scenes=scenes,
        output_path=video_filename,
        width=1280,
        height=720,
        fps=30,
        duration=duration * 60,  # Convert to seconds
        style_settings={
            'character_style': 'professional',
            'background_style': 'educational',
            'animation_speed': 0.8  # Slower for clarity
        },
        audio_settings=audio_settings,
        animation_settings=animation_settings
    )
    
    if video_path and os.path.exists(video_path):
        print(f"✅ Educational video created: {video_path}")
        
        # Auto-upload to YouTube if requested
        if auto_upload:
            print("📤 Uploading to YouTube...")
            
            title = f"{topic} - Complete {level} Guide | {subject} Education"
            description = f"""
Complete educational video on {topic} for {level} learners.

📚 Subject: {subject}
🎯 Level: {level}
⏱️ Duration: {duration} minutes

This comprehensive lesson covers all essential aspects of {topic}, designed specifically for {level} students.

🔔 Subscribe for more educational content!
👍 Like if this helped you learn!
💬 Comment with your questions!

Generated by AI Video Generator - Making education accessible to everyone.

#Education #{subject.replace(' ', '')} #{topic.replace(' ', '')} #Learning #Tutorial
"""
            
            tags = [
                "education", subject.lower(), topic.lower().replace(' ', ''),
                level.lower(), "tutorial", "learning", "teaching", "lesson"
            ]
            
            try:
                youtube_url = upload_to_youtube(video_path, title, description, tags)
                if youtube_url:
                    print(f"✅ Video uploaded to YouTube: {youtube_url}")
                    return video_path, youtube_url
                else:
                    print("⚠️ YouTube upload failed")
                    return video_path, None
            except Exception as e:
                print(f"❌ YouTube upload error: {e}")
                return video_path, None
        
        return video_path, None
    else:
        print("❌ Video creation failed")
        return None, None

def main():
    """Streamlit interface for educational video generator."""
    st.set_page_config(
        page_title="Universal Educational Video Generator",
        page_icon="🎓",
        layout="wide"
    )
    
    st.title("🎓 Universal Educational Video Generator for ALL SUBJECTS")
    st.markdown("""
    ### 🌟 Create Professional Educational Videos for ANY Topic
    
    **✨ Supported Subjects Include:**
    - 🔬 **STEM**: Math, Physics, Chemistry, Biology, Computer Science, Engineering
    - 🌍 **Languages**: English, Spanish, French, German, Chinese, Arabic, and 50+ more  
    - 🏛️ **Humanities**: History, Geography, Philosophy, Psychology, Literature
    - 🎨 **Arts**: Visual Arts, Music, Theater, Creative Writing, Design
    - 🙏 **Spiritual**: Sanskrit, Meditation, World Religions, Philosophy
    - 💼 **Professional**: Business, Marketing, Finance, Healthcare, Law
    - 🌱 **Life Skills**: Cooking, Fitness, Personal Development, Career Skills
    
    **🎬 Features:** 10-40 minute videos • HD quality • Auto YouTube upload • Multiple languages
    """)
    st.markdown("Generate comprehensive educational videos for ANY subject with automatic YouTube upload!")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("🎯 Educational Settings")
        
        # Subject selection
        subject_option = st.radio(
            "📚 Choose Subject Type",
            ["Pre-defined Subjects", "Custom Subject (ANY topic)"]
        )
        
        if subject_option == "Pre-defined Subjects":
            subject = st.selectbox(
                "📚 Select Subject",
                list(EDUCATIONAL_SUBJECTS.keys()),
                help="Choose from our curated list of educational subjects"
            )
            subject_config = EDUCATIONAL_SUBJECTS[subject]
            
            # Topic selection based on subject
            topic = st.selectbox(
                "📖 Select Topic",
                subject_config["topics"]
            )
            
            # Level selection
            level = st.selectbox(
                "🎯 Academic Level",
                subject_config["levels"]
            )
            
            # Duration settings
            min_duration, max_duration = subject_config["duration_range"]
            duration = st.slider(
                "⏱️ Video Duration (minutes)",
                min_value=10,
                max_value=45,
                value=min_duration,
                help=f"Recommended: {min_duration}-{max_duration} minutes for {subject}"
            )
        else:
            st.markdown("### 🌟 Create Video for ANY Subject!")
            subject = st.text_input(
                "📚 Enter Subject Name",
                placeholder="e.g., Advanced Quantum Physics, Ancient Greek Literature, Ayurvedic Medicine",
                help="Enter ANY subject - we support all educational topics!"
            )
            
            topic = st.text_input(
                "📖 Enter Specific Topic",
                placeholder="e.g., Wave-Particle Duality, Homer's Odyssey, Herbal Remedies",
                help="Be specific about what you want to teach"
            )
            
            level = st.selectbox(
                "🎯 Academic Level",
                ["Elementary", "Middle School", "High School", "College", "Graduate", "Professional", "Beginner", "Intermediate", "Advanced", "Expert"]
            )
            
            duration = st.slider(
                "⏱️ Video Duration (minutes)",
                min_value=10,
                max_value=45,
                value=25,
                help="Choose any duration - we'll create comprehensive content"
            )
        
        st.header("🎬 Video Settings")
        
        # Video quality
        video_quality = st.selectbox(
            "📹 Video Quality",
            ["720p (Recommended)", "1080p (High Quality)", "480p (Fast)"]
        )
        
        # Audio settings
        voice_speed = st.slider("🗣️ Voice Speed", 100, 180, 130)
        background_music = st.checkbox("🎵 Background Music", value=True)
        
        st.header("📤 YouTube Settings")
        auto_upload = st.checkbox("🚀 Auto-upload to YouTube", value=False)
        
        if auto_upload:
            st.info("📝 Make sure you have set up YouTube API credentials in `client_secrets.json`")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"📚 {subject}: {topic}")
        st.write(f"**Level:** {level}")
        st.write(f"**Duration:** {duration} minutes")
        st.write(f"**Voice Style:** {subject_config['voice_style']}")
        
        # Custom script input
        st.subheader("📝 Custom Content (Optional)")
        custom_script = st.text_area(
            "Add custom content or let AI generate everything:",
            placeholder=f"Enter additional content for {topic}...",
            height=150
        )
        
        # Generate button
        if st.button("🎬 Generate Educational Video", use_container_width=True):
            with st.spinner(f"Creating {duration}-minute educational video..."):
                
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("📝 Generating educational script...")
                progress_bar.progress(20)
                
                status_text.text("🎭 Creating educational characters...")
                progress_bar.progress(40)
                
                status_text.text("🎬 Generating video content...")
                progress_bar.progress(60)
                
                # Create the educational video
                video_path, youtube_url = create_educational_video(
                    subject=subject,
                    topic=topic,
                    level=level,
                    duration=duration,
                    auto_upload=auto_upload
                )
                
                if auto_upload and youtube_url:
                    status_text.text("📤 Uploading to YouTube...")
                    progress_bar.progress(80)
                
                progress_bar.progress(100)
                status_text.text("✅ Educational video complete!")
                
                if video_path:
                    st.success("🎉 Educational video generated successfully!")
                    
                    # Video preview
                    if os.path.exists(video_path):
                        st.subheader("🎬 Video Preview")
                        video_file = open(video_path, 'rb')
                        video_bytes = video_file.read()
                        st.video(video_bytes)
                        video_file.close()
                        
                        # Download button
                        with open(video_path, 'rb') as f:
                            video_data = f.read()
                        st.download_button(
                            label="📥 Download Video",
                            data=video_data,
                            file_name=f"{subject}_{topic}_{level}.mp4",
                            mime="video/mp4",
                            use_container_width=True
                        )
                    
                    # YouTube link
                    if youtube_url:
                        st.success(f"📺 Video uploaded to YouTube!")
                        st.markdown(f"**🔗 YouTube Link:** [Watch on YouTube]({youtube_url})")
                
                else:
                    st.error("❌ Video generation failed. Please try again.")
    
    with col2:
        st.subheader("📊 Subject Statistics")
        
        # Subject info
        st.metric("📚 Available Topics", len(subject_config["topics"]))
        st.metric("🎯 Academic Levels", len(subject_config["levels"]))
        st.metric("⏱️ Duration Range", f"{subject_config['duration_range'][0]}-{subject_config['duration_range'][1]} min")
        
        # Recent videos
        st.subheader("🎬 Generated Videos")
        st.info("Video history will appear here after generation")
        
        # Tips
        st.subheader("💡 Tips for Better Videos")
        st.write("• Choose appropriate duration for your topic")
        st.write("• Select the right academic level")
        st.write("• Enable background music for engagement")
        st.write("• Use custom content for specific needs")
    
    # Footer
    st.markdown("---")
    st.markdown("🎓 **Universal Educational Video Generator** - Making quality education accessible to everyone!")

if __name__ == "__main__":
    main()
