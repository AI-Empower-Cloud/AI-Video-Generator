import streamlit as st
import asyncio
from main import (
    extract_text_from_pdf, parse_characters_and_scenes, parse_tags_and_title,
    VideoGenerationEngine, VideoConfig, ConversationMemory, VoiceIntegration, ConversationalResponder, Avatar,
    detect_emotion, select_music
)

st.title("AI Video Generator")

headline = st.text_input("Enter a headline (optional):")
script = st.text_area("Enter a script or lines for the video:")
image_path = st.text_input("Enter an image file path (optional):")
youtube_link = st.text_input("Enter a YouTube link (optional):")
pdf_file = st.file_uploader("Upload a story PDF (optional):", type=["pdf"])

if st.button("Generate Video"):
    if pdf_file:
        with open("temp_story.pdf", "wb") as f:
            f.write(pdf_file.read())
        story_text = extract_text_from_pdf("temp_story.pdf")
        characters, scenes = parse_characters_and_scenes(story_text)
    else:
        characters, scenes = parse_characters_and_scenes(script)
    avatar_info = characters[0] if characters else {"name": "AI", "gender": "neutral", "style": "realistic"}
    avatar = Avatar(**avatar_info)
    script_text = scenes[0]['description'] if scenes else script
    emotion = scenes[0]['emotion'] if scenes else detect_emotion(script)
    music = select_music(emotion)
    config = VideoConfig()
    engine = VideoGenerationEngine()
    video_path = asyncio.run(engine.generate_video_with_lipsync_and_emotion(
        text=script_text, emotion=emotion, config=config, music=music, avatar=avatar
    ))
    st.success(f"Video generated: {video_path}")
    with open(video_path, "rb") as f:
        st.download_button("Download Video", f, file_name=video_path)
    title, tags = parse_tags_and_title(scenes, characters)
    st.write(f"**YouTube Title Suggestion:** {title}")
    st.write(f"**YouTube Tags:** {', '.join(tags)}")
