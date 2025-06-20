"""
AI Video Generation Engine - Example Usage
Demonstrates how to use the custom AI video generation engine
"""

import asyncio
from engine.core import VideoGenerationEngine, VideoConfig, VideoFormat, AIModel

async def example_text_to_video():
    """Example: Generate video from text prompt"""
    
    # Initialize the engine
    engine = VideoGenerationEngine()
    success = await engine.initialize()
    
    if not success:
        print("Failed to initialize engine")
        return
    
    # Configure video generation
    config = VideoConfig(
        width=1920,
        height=1080,
        fps=30,
        duration=5.0,
        format=VideoFormat.MP4,
        quality="high",
        ai_model=AIModel.TEXT_TO_VIDEO
    )
    
    # Define progress callback
    async def progress_callback(progress):
        print(f"Progress: {progress.percentage:.1f}% - {progress.current_stage}")
        print(f"Frame {progress.current_frame}/{progress.total_frames}")
        print(f"ETA: {progress.estimated_time_remaining:.1f}s")
        print("-" * 40)
    
    # Generate video
    prompt = "A majestic dragon flying over a mystical forest at sunset"
    print(f"Generating video from prompt: '{prompt}'")
    print("=" * 60)
    
    result = await engine.generate_video_from_text(
        prompt=prompt,
        config=config,
        progress_callback=progress_callback
    )
    
    # Display results
    print("\n🎉 Video Generation Complete!")
    print(f"Job ID: {result['job_id']}")
    print(f"Status: {result['status']}")
    print(f"Output: {result['video_path']}")
    print(f"Generation Time: {result['metadata']['generation_time']:.2f}s")

async def example_performance_test():
    """Test engine performance with different configurations"""
    
    engine = VideoGenerationEngine()
    await engine.initialize()
    
    test_configs = [
        {"name": "HD", "width": 1280, "height": 720, "duration": 3.0},
        {"name": "Full HD", "width": 1920, "height": 1080, "duration": 3.0},
        {"name": "4K", "width": 3840, "height": 2160, "duration": 2.0},
    ]
    
    print("🚀 Performance Testing")
    print("=" * 50)
    
    for test in test_configs:
        config = VideoConfig(
            width=test["width"],
            height=test["height"],
            duration=test["duration"],
            fps=24
        )
        
        start_time = asyncio.get_event_loop().time()
        
        result = await engine.generate_video_from_text(
            prompt="Test video generation",
            config=config
        )
        
        end_time = asyncio.get_event_loop().time()
        generation_time = end_time - start_time
        
        print(f"{test['name']}: {generation_time:.2f}s")

if __name__ == "__main__":
    print("🎬 AI Video Generation Engine Demo")
    print("Custom engine - no external dependencies!")
    print("=" * 60)
    
    # Run the example
    asyncio.run(example_text_to_video())
    
    print("\n" + "=" * 60)
    
    # Run performance test
    asyncio.run(example_performance_test())
