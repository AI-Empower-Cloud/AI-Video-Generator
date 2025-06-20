#!/usr/bin/env python3
"""
Streamlit Web Interface for AI Video Generator
"""

import streamlit as st
import asyncio
from pathlib import Path
import sys
import random

# Add the project root to Python path
sys.path.append('/workspaces/AI-Video-Generator')

from main import (
    process_video_generation, 
    parse_characters_and_scenes, 
    detect_emotion,
    upload_to_youtube,
    extract_text_from_pdf
)
from engine.core.video_engine import VideoConfig
from enhanced_video_generator import AdvancedVideoGenerator

def main():
    """Streamlit web interface for AI Video Generator."""
    st.set_page_config(
        page_title="AI Video Generator",
        page_icon="🎬",
        layout="wide"
    )
    
    st.title("🎬 AI Video Generator")
    st.markdown("Transform your stories into engaging videos with AI-powered character detection and emotion analysis!")

    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Video Settings")
        width = st.selectbox("Width", [640, 1280, 1920], index=1)
        height = st.selectbox("Height", [480, 720, 1080], index=1)
        fps = st.slider("FPS", 24, 60, 30)
        duration = st.slider("Duration (seconds)", 3, 30, 5)
        
        st.header("🎨 Visual Settings")
        use_enhanced_generator = st.checkbox("Use Enhanced Video Generator", value=True)
        character_style = st.selectbox("Character Style", ["Cartoon", "Realistic", "Minimalist"], index=0)
        background_style = st.selectbox("Background Style", ["Gradient", "Scene-based", "Solid Color"], index=1)
        animation_speed = st.slider("Animation Speed", 0.5, 2.0, 1.0, 0.1)
        
        st.header("🎵 Audio Settings")
        enable_audio = st.checkbox("Enable Audio Generation", value=True)
        enable_background_music = st.checkbox("Enable Background Music", value=True)
        music_style = st.selectbox("Music Style", ["Orchestral", "Electronic", "Piano", "Ambient"], index=0)
        voice_rate = st.slider("Voice Speed", 100, 200, 150)
        voice_volume = st.slider("Voice Volume", 0.0, 1.0, 0.9, 0.1)
        
        st.header("🎭 Animation Settings")
        enable_advanced_animation = st.checkbox("Enable Advanced Animation", value=True)
        animation_style = st.selectbox("Animation Style", ["Realistic", "Cartoon", "Minimalist"], index=1)
        enable_particle_effects = st.checkbox("Enable Particle Effects", value=True)
        
        st.header("🎛️ Advanced Options")
        with st.expander("Voice Settings"):
            voice_id = st.selectbox("Voice Type", ["Default", "Male", "Female", "Child"], index=0)
            voice_pitch = st.slider("Voice Pitch", 0.5, 2.0, 1.0, 0.1)
        
        with st.expander("Music Settings"):
            music_tempo = st.selectbox("Music Tempo", ["Slow", "Medium", "Fast"], index=1)
            music_volume = st.slider("Music Volume", 0.0, 1.0, 0.5, 0.1)

    # Main input form
    with st.form("video_generation_form", clear_on_submit=False):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            headline = st.text_input("📰 Headline (optional):", placeholder="Enter a catchy headline...")
            script = st.text_area(
                "📝 Script or Story:", 
                placeholder="Enter your story here... e.g., 'Alice was walking through the enchanted forest. She felt curious about the magical creatures...'",
                height=150
            )
            
        with col2:
            image_path = st.text_input("🖼️ Image Path (optional):", placeholder="/path/to/image.jpg")
            youtube_link = st.text_input("🔗 YouTube Link (optional):", placeholder="https://youtube.com/...")
            pdf_file = st.file_uploader("📚 Upload Story PDF:", type=["pdf"])
        
        submit = st.form_submit_button("🎥 Generate Video", use_container_width=True)

    # Processing section
    if submit and script:
        config = VideoConfig(width=width, height=height, fps=fps, duration=duration)
        
        with st.spinner("🔄 Processing your story..."):
            # Show progress steps
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Parse story
            status_text.text("📖 Analyzing story and characters...")
            progress_bar.progress(20)
            
            # Save uploaded PDF if provided
            pdf_path = ""
            if pdf_file:
                pdf_path = "temp_story.pdf"
                with open(pdf_path, "wb") as f:
                    f.write(pdf_file.read())
            
            # Step 2: Character analysis
            status_text.text("👥 Detecting characters and emotions...")
            progress_bar.progress(40)
            
            if pdf_path:
                story_text = extract_text_from_pdf(pdf_path)
                characters, scenes = parse_characters_and_scenes(story_text)
            else:
                characters, scenes = parse_characters_and_scenes(script)
            
            # Step 3: Video generation
            status_text.text("🎬 Generating video content...")
            progress_bar.progress(60)
            
            # Use enhanced generator if selected
            if use_enhanced_generator:
                generator = AdvancedVideoGenerator()
                video_path = f"enhanced_video_{random.randint(1000000, 9999999)}.mp4"
                
                # Prepare audio settings
                audio_settings = {
                    'enable_audio': enable_audio,
                    'enable_background_music': enable_background_music,
                    'music_style': music_style.lower(),
                    'voice_settings': {
                        'rate': voice_rate,
                        'volume': voice_volume,
                        'voice_id': voice_id,
                        'pitch': voice_pitch
                    }
                }
                
                # Prepare animation settings
                animation_settings = {
                    'enable_advanced_animation': enable_advanced_animation,
                    'animation_style': animation_style.lower(),
                    'enable_particle_effects': enable_particle_effects
                }
                
                # Generate enhanced video with audio and animation
                generator.generate_story_video(
                    script=script,
                    characters=characters,
                    scenes=scenes,
                    output_path=video_path,
                    width=width,
                    height=height,
                    fps=fps,
                    duration=duration,
                    style_settings={
                        'character_style': character_style,
                        'background_style': background_style,
                        'animation_speed': animation_speed,
                        'music_tempo': music_tempo,
                        'music_volume': music_volume
                    },
                    audio_settings=audio_settings,
                    animation_settings=animation_settings
                )
                
                # Generate metadata
                title = f"AI Generated Story: {headline or 'Video Story'}"
                tags = ["AI", "story", "video", "generated", "characters"]
                if characters:
                    tags.extend([char['name'] for char in characters[:3]])
                if enable_audio:
                    tags.append("audio")
                if enable_background_music:
                    tags.append("music")
                if enable_advanced_animation:
                    tags.append("animation")
            else:
                # Process video generation with original method
                video_path, title, tags = asyncio.run(process_video_generation(
                    script=script,
                    headline=headline,
                    image_path=image_path,
                    youtube_link=youtube_link,
                    pdf_path=pdf_path,
                    config=config
                ))
            
            progress_bar.progress(100)
            status_text.text("✅ Video generation complete!")
            
        # Results section
        st.success("🎉 Video generated successfully!")
        
        # Video preview
        if video_path and Path(video_path).exists():
            st.subheader("🎬 Video Preview")
            video_file = open(video_path, 'rb')
            video_bytes = video_file.read()
            st.video(video_bytes)
            video_file.close()
        
        # Display results in columns
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📊 Analysis Results")
            
            # Characters found
            if characters:
                st.write("**👥 Characters Detected:**")
                for char in characters:
                    st.write(f"• {char['name']} ({char['gender']})")
            else:
                st.write("**👥 Characters:** None detected")
            
            # Scenes analysis
            if scenes:
                st.write("**🎭 Scene Analysis:**")
                for i, scene in enumerate(scenes[:3]):  # Show first 3 scenes
                    emotion_emoji = {"joy": "😊", "surprise": "😮", "sadness": "😢", "anger": "😠"}.get(scene['emotion'], "😐")
                    st.write(f"• Scene {i+1}: {scene['description'][:50]}... {emotion_emoji} *{scene['emotion']}*")
                if len(scenes) > 3:
                    st.write(f"... and {len(scenes)-3} more scenes")
        
        with col2:
            st.subheader("🎬 Video Details")
            st.write(f"**📁 File:** `{video_path}`")
            st.write(f"**📐 Resolution:** {width}x{height}")
            st.write(f"**🎞️ FPS:** {fps}")
            st.write(f"**⏱️ Duration:** {duration}s")
            
            # Audio and animation features info
            if use_enhanced_generator:
                st.write("**🎵 Audio Features:**")
                if enable_audio:
                    st.write(f"   • Voice: {voice_id} (Rate: {voice_rate})")
                    if enable_background_music:
                        st.write(f"   • Music: {music_style} ({music_tempo})")
                else:
                    st.write("   • Disabled")
                
                st.write("**🎭 Animation Features:**")
                if enable_advanced_animation:
                    st.write(f"   • Style: {animation_style}")
                    if enable_particle_effects:
                        st.write("   • Particle Effects: Enabled")
                else:
                    st.write("   • Basic Animation Only")
            
            # Download button
            if video_path and Path(video_path).exists():
                with open(video_path, 'rb') as f:
                    video_data = f.read()
                st.download_button(
                    label="📥 Download Video",
                    data=video_data,
                    file_name=f"{title.replace(':', '-').replace(' ', '_')}.mp4",
                    mime="video/mp4",
                    use_container_width=True
                )
            else:
                st.error("❌ Video file not found")
        
        # YouTube metadata
        st.subheader("📺 YouTube Metadata")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🏷️ Suggested Title:**")
            st.code(title)
        
        with col2:
            st.write("**🔖 Suggested Tags:**")
            st.code(", ".join(tags[:10]))  # Show first 10 tags
        
        # YouTube upload section
        st.subheader("📤 YouTube Upload")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if st.button("🚀 Upload to YouTube", use_container_width=True):
                with st.spinner("📤 Uploading to YouTube..."):
                    description = f"Generated by AI Video Generator\n\nHeadline: {headline}\n\nGenerated from: {script[:100]}..."
                    
                    # Note: This requires YouTube API setup
                    try:
                        video_url = asyncio.run(upload_to_youtube(
                            video_path, title, description, tags
                        ))
                        if video_url:
                            st.success(f"🎉 Video uploaded! [View on YouTube]({video_url})")
                        else:
                            st.error("❌ Upload failed. Please check your YouTube API credentials.")
                    except Exception as e:
                        st.error(f"❌ Upload error: {str(e)}")
        
        with col2:
            st.info("📝 **Note:** YouTube upload requires API credentials in `client_secrets.json`")

    elif submit:
        st.error("⚠️ Please enter a script or story to generate a video.")

    # Footer
    st.markdown("---")
    st.markdown("🤖 **AI Video Generator v2.0** - Enhanced with Audio & Animation")
    st.markdown("Powered by spaCy, Transformers, Audio Integration, Advanced Animation & Streamlit")

if __name__ == "__main__":
    main()
