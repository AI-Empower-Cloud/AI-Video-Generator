#!/usr/bin/env python3
"""
Advanced Demo Script for AI Video Generator
Shows off all the enhanced features including:
- Character extraction and coreference resolution
- Enhanced video generation with avatars
- Scene transitions and emotions
- Multiple video styles
"""

import sys
sys.path.append('/workspaces/AI-Video-Generator')

from main import parse_characters_and_scenes, detect_emotion
from enhanced_video_generator import AdvancedVideoGenerator
import random

def demo_story_analysis():
    """Demonstrate NLP story analysis capabilities."""
    print("🔍 AI Video Generator - Advanced Demo")
    print("=" * 50)
    
    # Sample story with multiple characters
    story = """
    Alice was walking through the enchanted forest when she met Bob. 
    He was sitting by a crystal stream, looking worried. 
    "What's wrong?" Alice asked with concern. Bob explained that his sister Carol had gone missing.
    Alice felt determined to help. She knew the forest well and had a magical compass.
    Together, they searched through the misty valleys. Bob was grateful for her assistance.
    After hours of searching, they finally found Carol trapped in a cave. 
    She was scared but unharmed. Bob hugged his sister tightly while Alice smiled with relief.
    Carol thanked Alice for her bravery. All three friends walked back through the forest,
    feeling joyful about their adventure and the new friendship they had formed.
    """
    
    print("📖 Story:")
    print(story)
    print("\n" + "=" * 50)
    
    # Analyze characters and scenes
    print("👥 Analyzing Characters...")
    characters, scenes = parse_characters_and_scenes(story)
    
    print(f"\n✅ Found {len(characters)} characters:")
    for i, char in enumerate(characters, 1):
        print(f"  {i}. {char['name']} ({char['gender']})")
    
    print(f"\n🎭 Found {len(scenes)} scenes:")
    for i, scene in enumerate(scenes, 1):
        emotion_emoji = {
            "joy": "😊", 
            "surprise": "😮", 
            "sadness": "😢", 
            "anger": "😠", 
            "fear": "😨",
            "neutral": "😐"
        }.get(scene['emotion'], "😐")
        print(f"  {i}. {scene['description'][:60]}... {emotion_emoji} ({scene['emotion']})")
    
    return story, characters, scenes

def demo_video_generation(story, characters, scenes):
    """Demonstrate video generation with different styles."""
    print("\n" + "=" * 50)
    print("🎬 Generating Enhanced Videos...")
    
    generator = AdvancedVideoGenerator()
    
    # Generate videos with different styles
    styles = [
        {
            'name': 'Cartoon Style',
            'settings': {
                'character_style': 'Cartoon',
                'background_style': 'Gradient',
                'animation_speed': 1.2
            }
        },
        {
            'name': 'Realistic Style', 
            'settings': {
                'character_style': 'Realistic',
                'background_style': 'Scene-based',
                'animation_speed': 1.0
            }
        },
        {
            'name': 'Minimalist Style',
            'settings': {
                'character_style': 'Minimalist',
                'background_style': 'Solid Color',
                'animation_speed': 0.8
            }
        }
    ]
    
    generated_videos = []
    
    for style in styles:
        print(f"\n🎨 Generating {style['name']}...")
        
        video_path = f"demo_{style['name'].lower().replace(' ', '_')}_{random.randint(1000, 9999)}.mp4"
        
        try:
            generator.generate_story_video(
                script=story,
                characters=characters,
                scenes=scenes,
                output_path=video_path,
                width=640,
                height=480,
                fps=24,
                duration=8,
                style_settings=style['settings']
            )
            
            print(f"✅ Generated: {video_path}")
            generated_videos.append({
                'style': style['name'],
                'path': video_path,
                'settings': style['settings']
            })
            
        except Exception as e:
            print(f"❌ Error generating {style['name']}: {e}")
    
    return generated_videos

def demo_emotion_detection():
    """Demonstrate emotion detection on various text samples."""
    print("\n" + "=" * 50)
    print("😊 Emotion Detection Demo")
    
    text_samples = [
        "I am so happy and excited about this adventure!",
        "This is terrible news, I feel devastated.",
        "What a shocking surprise! I never expected this.",
        "I'm feeling quite angry about what happened.",
        "The weather is nice today.",
        "I'm scared of what might happen next."
    ]
    
    for text in text_samples:
        emotion = detect_emotion(text)
        emotion_emoji = {
            "joy": "😊", 
            "surprise": "😮", 
            "sadness": "😢", 
            "anger": "😠", 
            "fear": "😨",
            "neutral": "😐"
        }.get(emotion, "😐")
        
        print(f"{emotion_emoji} \"{text}\" → {emotion}")

def main():
    """Run the complete advanced demo."""
    try:
        # Demo 1: Story Analysis
        story, characters, scenes = demo_story_analysis()
        
        # Demo 2: Emotion Detection
        demo_emotion_detection()
        
        # Demo 3: Video Generation
        videos = demo_video_generation(story, characters, scenes)
        
        # Summary
        print("\n" + "=" * 50)
        print("🎉 Demo Complete!")
        print(f"✅ Analyzed story with {len(characters)} characters and {len(scenes)} scenes")
        print(f"✅ Generated {len(videos)} videos in different styles")
        
        if videos:
            print("\n📹 Generated Videos:")
            for video in videos:
                print(f"  • {video['style']}: {video['path']}")
        
        print("\n🌟 Features Demonstrated:")
        print("  • Natural Language Processing with spaCy")
        print("  • Coreference Resolution with coreferee")
        print("  • Character and Scene Extraction")
        print("  • Emotion Detection")
        print("  • Enhanced Video Generation")
        print("  • Multiple Visual Styles")
        print("  • Animated Characters and Scenes")
        
        print("\n🚀 Ready for production use!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
