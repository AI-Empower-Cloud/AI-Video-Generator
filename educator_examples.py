#!/usr/bin/env python3
"""
🎓 Educational Examples for ALL Subjects
Real examples of how educators across all fields use this platform
"""

# Example educational video configurations for different subjects

EDUCATOR_EXAMPLES = {
    "math_teacher": {
        "name": "Sarah Johnson - 5th Grade Math Teacher",
        "subject": "Mathematics",
        "topics": [
            "Understanding Fractions with Visual Models",
            "Introduction to Algebra for Young Learners", 
            "Geometry in Everyday Life",
            "Math Problem Solving Strategies"
        ],
        "typical_video": {
            "duration": 15,
            "level": "Elementary",
            "style": "Visual and interactive with lots of examples"
        },
        "testimonial": "My students love these videos! The visual explanations make complex math concepts so much easier to understand."
    },
    
    "physics_professor": {
        "name": "Dr. Michael Chen - University Physics Professor",
        "subject": "Physics", 
        "topics": [
            "Quantum Mechanics: Wave-Particle Duality",
            "Einstein's Theory of Relativity Explained",
            "Thermodynamics and Statistical Mechanics",
            "Advanced Electromagnetic Theory"
        ],
        "typical_video": {
            "duration": 35,
            "level": "College",
            "style": "Detailed mathematical derivations with clear explanations"
        },
        "testimonial": "Perfect for my advanced physics courses. Students can review complex topics at their own pace."
    },
    
    "spanish_instructor": {
        "name": "María García - Spanish Language Instructor",
        "subject": "Spanish Language",
        "topics": [
            "Spanish Grammar: Subjunctive Mood",
            "Latin American Literature Overview", 
            "Conversational Spanish for Travelers",
            "Spanish Culture and Traditions"
        ],
        "typical_video": {
            "duration": 25,
            "level": "Intermediate",
            "style": "Immersive with native pronunciation and cultural context"
        },
        "testimonial": "The multilingual support helps me create authentic Spanish content for my international students."
    },
    
    "sanskrit_teacher": {
        "name": "Acharya Pradeep Sharma - Sanskrit & Spiritual Studies",
        "subject": "Sanskrit/Spiritual",
        "topics": [
            "Gayatri Mantra: Meaning and Pronunciation",
            "Bhagavad Gita: Chapter 2 Analysis",
            "Vedic Mathematics Principles",
            "Yoga Philosophy: The Eight Limbs"
        ],
        "typical_video": {
            "duration": 30,
            "level": "Intermediate",
            "style": "Traditional approach with modern applications"
        },
        "testimonial": "Wonderful for sharing ancient wisdom with modern students worldwide. The pronunciation guides are excellent."
    },
    
    "history_teacher": {
        "name": "James Thompson - High School History Teacher",
        "subject": "History",
        "topics": [
            "World War II: Causes and Consequences",
            "Ancient Civilizations: Egypt and Mesopotamia",
            "The Renaissance: Art and Cultural Revolution", 
            "American Civil Rights Movement"
        ],
        "typical_video": {
            "duration": 30,
            "level": "High School",
            "style": "Narrative storytelling with historical evidence"
        },
        "testimonial": "My students are more engaged with history when they can watch these comprehensive video lessons."
    },
    
    "business_trainer": {
        "name": "Lisa Rodriguez - Corporate Training Manager",
        "subject": "Business",
        "topics": [
            "Leadership in the Digital Age",
            "Project Management Best Practices",
            "Marketing Strategy for Small Business",
            "Financial Planning for Entrepreneurs"
        ],
        "typical_video": {
            "duration": 20,
            "level": "Professional",
            "style": "Practical with real-world case studies"
        },
        "testimonial": "Essential for our employee development programs. Professional quality at a fraction of the cost."
    },
    
    "art_instructor": {
        "name": "Elena Petrov - Art History Professor",
        "subject": "Art & Music",
        "topics": [
            "Renaissance Art: Techniques and Masters",
            "Modern Art Movements: Cubism to Surrealism",
            "Digital Art: Traditional Meets Technology",
            "Music Theory: Harmony and Composition"
        ],
        "typical_video": {
            "duration": 25,
            "level": "College",
            "style": "Visual-rich with artwork analysis"
        },
        "testimonial": "The visual capabilities are perfect for art education. Students can see details they'd miss in textbooks."
    },
    
    "computer_science_teacher": {
        "name": "David Kim - CS Department Head",
        "subject": "Computer Science",
        "topics": [
            "Python Programming: Object-Oriented Design",
            "Machine Learning: Neural Networks Explained",
            "Cybersecurity: Ethical Hacking Basics",
            "Data Structures: Trees and Graphs"
        ],
        "typical_video": {
            "duration": 40,
            "level": "College",
            "style": "Code demonstrations with step-by-step examples"
        },
        "testimonial": "Great for coding bootcamps and CS courses. Students can follow along with the coding examples."
    },
    
    "elementary_teacher": {
        "name": "Amanda Foster - 2nd Grade Teacher",
        "subject": "Elementary Education",
        "topics": [
            "Reading Comprehension: Story Elements",
            "Basic Science: Plants and Animals",
            "Social Studies: Community Helpers",
            "Creative Writing: Tell Your Story"
        ],
        "typical_video": {
            "duration": 12,
            "level": "Elementary",
            "style": "Fun, colorful, and age-appropriate"
        },
        "testimonial": "Perfect for remote learning and homework help. Parents love having these resources too!"
    },
    
    "medical_educator": {
        "name": "Dr. Priya Patel - Medical School Instructor", 
        "subject": "Medical Education",
        "topics": [
            "Human Anatomy: Cardiovascular System",
            "Pharmacology: Drug Interactions",
            "Medical Ethics: Patient Care Principles",
            "Clinical Skills: Patient Assessment"
        ],
        "typical_video": {
            "duration": 35,
            "level": "Graduate",
            "style": "Detailed medical diagrams with clinical applications"
        },
        "testimonial": "Invaluable for medical education. Students can review complex procedures multiple times."
    }
}

def demonstrate_educator_usage():
    """Show how different educators use the platform"""
    
    print("🎓 UNIVERSAL EDUCATIONAL VIDEO GENERATOR")
    print("=" * 50)
    print("Real Examples from Educators Across ALL Subjects")
    print()
    
    for educator_type, info in EDUCATOR_EXAMPLES.items():
        print(f"👤 {info['name']}")
        print(f"📚 Subject: {info['subject']}")
        print(f"🎯 Typical Video: {info['typical_video']['duration']} min, {info['typical_video']['level']} level")
        print(f"📝 Style: {info['typical_video']['style']}")
        print()
        print("📖 Example Topics:")
        for topic in info['topics']:
            print(f"   • {topic}")
        print()
        print(f"💬 Testimonial: \"{info['testimonial']}\"")
        print("-" * 50)
        print()

def get_subject_recommendations(educator_type):
    """Get video creation recommendations for different educator types"""
    
    recommendations = {
        "elementary": {
            "duration": "10-15 minutes",
            "style": "Visual, interactive, age-appropriate",
            "tips": "Use simple language, lots of examples, engaging visuals"
        },
        "middle_school": {
            "duration": "15-25 minutes", 
            "style": "Engaging with real-world connections",
            "tips": "Connect to student interests, use interactive elements"
        },
        "high_school": {
            "duration": "20-30 minutes",
            "style": "Comprehensive with exam preparation focus",
            "tips": "Include test-taking strategies, detailed explanations"
        },
        "college": {
            "duration": "25-40 minutes",
            "style": "In-depth analysis with critical thinking",
            "tips": "Encourage discussion, provide multiple perspectives"
        },
        "professional": {
            "duration": "20-35 minutes",
            "style": "Practical with immediate applications",
            "tips": "Focus on real-world scenarios, actionable insights"
        },
        "spiritual": {
            "duration": "20-45 minutes",
            "style": "Contemplative with traditional wisdom",
            "tips": "Include pronunciation guides, cultural context"
        }
    }
    
    return recommendations.get(educator_type, recommendations["college"])

if __name__ == "__main__":
    demonstrate_educator_usage()
