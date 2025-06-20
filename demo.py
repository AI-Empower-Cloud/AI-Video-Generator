#!/usr/bin/env python3
"""
Demo script showing AI Video Generator capabilities
"""

import sys
import asyncio
sys.path.append('/workspaces/AI-Video-Generator')

from main import process_video_generation, parse_characters_and_scenes, detect_emotion
from engine.core.video_engine import VideoConfig

async def demo():
    print("🎬 AI Video Generator Demo\n")
    
    # Test 1: Simple story processing
    story = "Alice was walking through the enchanted forest. She felt curious about the magical creatures. Suddenly, a friendly dragon appeared and smiled at her."
    
    print("📝 Story:", story)
    print("\n🔍 Analysis:")
    
    # Parse characters and scenes
    characters, scenes = parse_characters_and_scenes(story)
    
    print(f"👥 Characters found: {[c['name'] for c in characters]}")
    print(f"🎭 Scenes detected: {len(scenes)}")
    
    for i, scene in enumerate(scenes):
        print(f"   Scene {i+1}: {scene['description'][:50]}... (Emotion: {scene['emotion']})")
    
    print("\n🎥 Generating video...")
    
    # Generate video
    config = VideoConfig(width=1280, height=720, fps=30, duration=5)
    video_path, title, tags = await process_video_generation(
        script=story,
        headline="Magical Adventure",
        config=config
    )
    
    print(f"✅ Video generated: {video_path}")
    print(f"🏷️ Title: {title}")
    print(f"🔖 Tags: {', '.join(tags[:5])}...")
    
    print("\n🎉 Demo completed successfully!")

if __name__ == "__main__":
    asyncio.run(demo())
