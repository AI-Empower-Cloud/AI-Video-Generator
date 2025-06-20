#!/usr/bin/env python3
"""
Educational Video Creator - Streamlit Interface
For creating 10-40 minute teaching videos with auto YouTube upload
"""

import streamlit as st
import sys
import time
from pathlib import Path
import asyncio

# Add project root to path
sys.path.append('/workspaces/AI-Video-Generator')

from educational_video_generator import EducationalVideoGenerator, auto_upload_educational_video

def main():
    """Educational Video Creator Interface."""
    st.set_page_config(
        page_title="Educational Video Creator",
        page_icon="🎓",
        layout="wide"
    )
    
    st.title("🎓 Educational Video Creator")
    st.markdown("Create 10-40 minute teaching videos for slokas, mantras, and educational content with automatic YouTube upload!")

    # Sidebar for settings
    with st.sidebar:
        st.header("🎬 Video Settings")
        duration_minutes = st.slider("Video Duration (minutes)", 10, 40, 20)
        resolution = st.selectbox("Resolution", ["720p (1280x720)", "1080p (1920x1080)", "4K (3840x2160)"], index=1)
        fps = st.selectbox("Frame Rate", [24, 30, 60], index=1)
        
        # Parse resolution
        width, height = {
            "720p (1280x720)": (1280, 720),
            "1080p (1920x1080)": (1920, 1080),
            "4K (3840x2160)": (3840, 2160)
        }[resolution]
        
        st.header("🎵 Audio Settings")
        voice_speed = st.slider("Teaching Voice Speed", 80, 150, 120)
        background_music = st.checkbox("Enable Background Music", value=True)
        music_style = st.selectbox("Music Style", ["Spiritual", "Classical", "Ambient", "Meditation"], index=0)
        
        st.header("📤 YouTube Settings")
        auto_upload = st.checkbox("Auto-upload to YouTube", value=False)
        if auto_upload:
            st.warning("⚠️ Make sure YouTube API credentials are configured!")

    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["🕉️ Sloka/Mantra", "📚 Educational Topic", "🎥 Video Library", "⚙️ Settings"])
    
    with tab1:
        st.header("🕉️ Sanskrit Sloka & Mantra Teaching")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            content_type = st.selectbox(
                "Content Type",
                ["Gayatri Mantra", "Custom Sloka", "Maha Mantra", "Shanti Mantra", "Other Mantra"]
            )
            
            if content_type == "Gayatri Mantra":
                st.info("📖 The most sacred mantra in Hinduism - complete teaching with pronunciation guide")
                title = "Gayatri Mantra - Complete Teaching"
                sloka_text = "ॐ भूर्भुवः स्वः तत्सवितुर्वरेण्यं भर्गो देवस्य धीमहि धियो यो नः प्रचोदयात्"
                meaning = st.text_area(
                    "Meaning (optional - will use default)",
                    placeholder="Leave empty to use comprehensive default meaning",
                    height=100
                )
                benefits = st.text_area(
                    "Benefits (optional - will use default)",
                    placeholder="Leave empty to use default spiritual benefits",
                    height=100
                )
            else:
                title = st.text_input("Title", placeholder="e.g., Shiva Mantra Teaching")
                sloka_text = st.text_area(
                    "Sanskrit Text",
                    placeholder="Enter the Sanskrit sloka or mantra in Devanagari or Roman script",
                    height=100
                )
                meaning = st.text_area(
                    "Meaning & Translation",
                    placeholder="Explain the meaning word by word and overall significance",
                    height=150
                )
                benefits = st.text_area(
                    "Spiritual Benefits",
                    placeholder="List the benefits of chanting this sloka/mantra",
                    height=100
                )
        
        with col2:
            st.subheader("👨‍🏫 Teacher Settings")
            teacher_name = st.text_input("Teacher Name", "Guruji")
            teacher_gender = st.selectbox("Teacher Voice", ["Male", "Female", "Neutral"], index=0)
            teaching_style = st.selectbox("Teaching Style", ["Traditional", "Modern", "Interactive"], index=0)
            
            st.subheader("🎯 Target Audience")
            audience_level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"], index=0)
            include_repetition = st.checkbox("Include Chanting Practice", value=True)
            repetition_count = st.slider("Repetition Count", 1, 10, 5) if include_repetition else 0
        
        if st.button("🎬 Generate Sloka/Mantra Video", use_container_width=True):
            if not sloka_text and content_type != "Gayatri Mantra":
                st.error("❌ Please enter the Sanskrit text")
            else:
                generate_educational_video(
                    'mantra_teaching' if 'Mantra' in content_type else 'sloka_teaching',
                    {
                        'text': sloka_text,
                        'meaning': meaning,
                        'benefits': benefits,
                        'title': title,
                        'teacher_name': teacher_name,
                        'teacher_gender': teacher_gender.lower(),
                        'mantra_type': 'gayatri' if content_type == "Gayatri Mantra" else 'custom',
                        'repetition_count': repetition_count
                    },
                    duration_minutes, width, height, fps, voice_speed, music_style, auto_upload
                )
    
    with tab2:
        st.header("📚 Educational Topic Video")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            topic_title = st.text_input("Topic Title", placeholder="e.g., Introduction to Vedic Mathematics")
            topic_category = st.selectbox(
                "Category",
                ["Spiritual Teachings", "Philosophy", "History", "Science", "Mathematics", "Language", "Arts", "Other"]
            )
            
            content_outline = st.text_area(
                "Content Outline",
                placeholder="""Structure your educational content:
1. Introduction to the topic
2. Key concepts and definitions
3. Examples and applications
4. Practice exercises
5. Summary and conclusion""",
                height=200
            )
            
            detailed_content = st.text_area(
                "Detailed Content",
                placeholder="Provide the detailed content that will be taught in the video...",
                height=300
            )
        
        with col2:
            st.subheader("📖 Learning Objectives")
            objectives = st.text_area(
                "What will students learn?",
                placeholder="""- Understand basic concepts
- Apply knowledge practically
- Gain deeper insights""",
                height=100
            )
            
            st.subheader("🎯 Course Settings")
            difficulty = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
            include_exercises = st.checkbox("Include Practice Exercises", value=True)
            interactive_elements = st.checkbox("Add Interactive Elements", value=True)
        
        if st.button("🎓 Generate Educational Video", use_container_width=True):
            if not topic_title or not detailed_content:
                st.error("❌ Please provide topic title and content")
            else:
                generate_educational_video(
                    'educational_lecture',
                    {
                        'topic': topic_title,
                        'content': detailed_content,
                        'outline': content_outline,
                        'objectives': objectives,
                        'category': topic_category,
                        'title': topic_title,
                        'teacher_name': teacher_name if 'teacher_name' in locals() else 'Teacher'
                    },
                    duration_minutes, width, height, fps, voice_speed, music_style, auto_upload
                )
    
    with tab3:
        st.header("🎥 Generated Video Library")
        
        # Display list of generated videos
        video_files = list(Path('.').glob('educational_*.mp4'))
        
        if video_files:
            st.write(f"📊 Found {len(video_files)} educational videos:")
            
            for video_file in sorted(video_files, key=lambda x: x.stat().st_mtime, reverse=True):
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.write(f"📹 **{video_file.name}**")
                    file_size = video_file.stat().st_size / (1024*1024)  # MB
                    st.write(f"📁 Size: {file_size:.1f} MB")
                
                with col2:
                    mod_time = time.ctime(video_file.stat().st_mtime)
                    st.write(f"🕒 Created: {mod_time}")
                
                with col3:
                    if st.button(f"▶️ Play", key=f"play_{video_file.name}"):
                        st.video(str(video_file))
        else:
            st.info("📝 No videos generated yet. Create your first educational video!")
    
    with tab4:
        st.header("⚙️ Advanced Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎨 Visual Settings")
            background_style = st.selectbox("Background Theme", [
                "Spiritual Temple", "Classical Library", "Modern Classroom", 
                "Nature Scene", "Minimalist", "Traditional Indian"
            ])
            text_overlay = st.checkbox("Show Sanskrit Text Overlay", value=True)
            pronunciation_guide = st.checkbox("Visual Pronunciation Guide", value=True)
            
        with col2:
            st.subheader("📤 YouTube Upload Settings")
            if auto_upload:
                channel_category = st.selectbox("YouTube Category", [
                    "Education", "Howto & Style", "People & Blogs", "Entertainment"
                ])
                video_privacy = st.selectbox("Privacy", ["Public", "Unlisted", "Private"])
                custom_thumbnail = st.checkbox("Generate Custom Thumbnail", value=True)
        
        st.subheader("🔧 Export Settings")
        export_subtitle = st.checkbox("Generate Subtitle File (.srt)", value=True)
        export_audio = st.checkbox("Export Audio Only (.mp3)", value=False)
        export_script = st.checkbox("Export Teaching Script (.txt)", value=True)

def generate_educational_video(content_type, content_data, duration_minutes, width, height, fps, voice_speed, music_style, auto_upload):
    """Generate educational video with progress tracking."""
    
    with st.spinner("🎬 Generating your educational video..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Initialize generator
        status_text.text("🔧 Initializing video generator...")
        progress_bar.progress(10)
        
        generator = EducationalVideoGenerator()
        
        # Prepare settings
        output_settings = {
            'duration': duration_minutes * 60,
            'width': width,
            'height': height,
            'fps': fps
        }
        
        # Add voice settings to content data
        content_data['voice_speed'] = voice_speed
        content_data['music_style'] = music_style.lower()
        
        status_text.text("📝 Creating educational script...")
        progress_bar.progress(30)
        
        # Generate video
        status_text.text("🎬 Generating video content...")
        progress_bar.progress(50)
        
        try:
            video_path, metadata = generator.generate_educational_video(
                content_type, content_data, output_settings
            )
            
            progress_bar.progress(80)
            status_text.text("✅ Video generation complete!")
            
            # Display results
            st.success("🎉 Educational video generated successfully!")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if video_path and Path(video_path).exists():
                    st.subheader("🎬 Video Preview")
                    st.video(video_path)
                else:
                    st.error("❌ Video file not found")
            
            with col2:
                st.subheader("📊 Video Details")
                st.write(f"**📁 File:** `{video_path}`")
                st.write(f"**⏱️ Duration:** {duration_minutes} minutes")
                st.write(f"**📐 Resolution:** {width}x{height}")
                st.write(f"**🎞️ FPS:** {fps}")
                
                if video_path and Path(video_path).exists():
                    file_size = Path(video_path).stat().st_size / (1024*1024)
                    st.write(f"**📁 Size:** {file_size:.1f} MB")
                    
                    # Download button
                    with open(video_path, 'rb') as f:
                        video_data = f.read()
                    st.download_button(
                        label="📥 Download Video",
                        data=video_data,
                        file_name=f"{metadata['title'].replace(' ', '_')}.mp4",
                        mime="video/mp4",
                        use_container_width=True
                    )
            
            # YouTube metadata
            st.subheader("📺 YouTube Information")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**🏷️ Title:**")
                st.code(metadata['title'])
                st.write("**🔖 Tags:**")
                st.code(", ".join(metadata['tags'][:10]))
            
            with col2:
                st.write("**📝 Description Preview:**")
                st.text_area("", metadata['description'][:300] + "...", height=100, disabled=True)
            
            # Auto-upload to YouTube
            if auto_upload:
                progress_bar.progress(90)
                status_text.text("📤 Uploading to YouTube...")
                
                upload_result = auto_upload_educational_video(video_path, metadata)
                if upload_result:
                    st.success(f"🎉 Successfully uploaded to YouTube: {upload_result}")
                else:
                    st.error("❌ Failed to upload to YouTube. Check your API credentials.")
            
            progress_bar.progress(100)
            status_text.text("✅ All done!")
            
        except Exception as e:
            st.error(f"❌ Error generating video: {str(e)}")
            progress_bar.progress(0)

if __name__ == "__main__":
    main()
