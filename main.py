import argparse
from typing import List, Dict, Optional, Tuple, Any
import asyncio
from pathlib import Path
import streamlit as st
import spacy
import sys
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import PyPDF2

from engine.core.video_engine import VideoGenerationEngine, VideoConfig
from engine.core import ConversationMemory, VoiceIntegration, ConversationalResponder, Avatar

try:
    from transformers import pipeline
except ImportError:
    print("transformers library is not installed. Please install it with 'pip install transformers'.")
    pipeline = None

# Initialize NLP with fallback options
print("Initializing AI Video Generator...")

# Fast mode: Use small model by default
try:
    print("Loading spaCy small model (faster initialization)...")
    nlp = spacy.load("en_core_web_sm")
    model_name = "small"
    print(f"✅ Loaded {model_name} model successfully")
except OSError:
    print("Error: No spaCy models found. Please install one with:")
    print("python -m spacy download en_core_web_sm")
    sys.exit(1)

# Try to add coreferee with multiple fallback strategies
use_coreferee = False
coreferee_nlp = None

try:
    import coreferee
    print(f"Successfully imported coreferee, trying different setup approaches...")
    
    # Strategy 1: Try with current small model
    try:
        nlp_test = spacy.load("en_core_web_sm")
        nlp_test.add_pipe('coreferee')
        # Test with simple text
        test_doc = nlp_test("John went home. He was tired.")
        use_coreferee = True
        coreferee_nlp = nlp_test
        print("✅ Strategy 1 success: Using en_core_web_sm with coreferee")
    except Exception as e1:
        print(f"Strategy 1 failed: {e1}")
        
        # Strategy 2: Try with blank pipeline + basic components
        try:
            nlp_blank = spacy.blank("en")
            nlp_blank.add_pipe("sentencizer")
            
            # Add basic NER manually for PERSON detection
            if "ner" not in nlp_blank.pipe_names:
                # Load just the NER component from the full model
                nlp_full = spacy.load("en_core_web_sm")
                ner = nlp_full.get_pipe("ner")
                nlp_blank.add_pipe("ner", source=nlp_full)
            
            nlp_blank.add_pipe('coreferee')
            test_doc = nlp_blank("John went home. He was tired.")
            use_coreferee = True
            coreferee_nlp = nlp_blank
            print("✅ Strategy 2 success: Using blank pipeline with coreferee")
        except Exception as e2:
            print(f"Strategy 2 failed: {e2}")
            
            # Strategy 3: Use coreferee in post-processing mode
            try:
                import coreferee
                # Keep original nlp, use coreferee separately
                use_coreferee = "manual"  # Flag for manual processing
                print("✅ Strategy 3: Will use coreferee in manual post-processing mode")
            except Exception as e3:
                print(f"Strategy 3 failed: {e3}")
                print("Continuing without coreference resolution")

except ImportError:
    print("coreferee not available, continuing without coreference resolution")

# Use the working coreferee pipeline if available, otherwise use original nlp
if coreferee_nlp is not None:
    nlp_coref = coreferee_nlp
    print(f"Using dedicated coreferee pipeline")
else:
    nlp_coref = nlp
    print(f"Using standard nlp pipeline")

emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)

def detect_emotion(text: str) -> str:
    """Detect emotion in text using distilroberta model."""
    if not emotion_classifier:
        return "neutral"
    try:
        result = emotion_classifier(text)
        # Handle different return formats
        if isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], list):
                # Format: [[{'label': 'emotion', 'score': 0.x}]]
                return result[0][0]['label'] if result[0] else "neutral"
            elif isinstance(result[0], dict):
                # Format: [{'label': 'emotion', 'score': 0.x}]
                return result[0]['label']
        return "neutral"
    except Exception as e:
        print(f"Error in emotion detection: {e}")
        return "neutral"

def select_music(emotion: str) -> str:
    """Select background music based on emotion/situation."""
    music_map = {
        "happy": "upbeat_theme.mp3",
        "sad": "sad_piano.mp3",
        "angry": "intense_action.mp3"
    }
    return music_map.get(emotion, "neutral_background.mp3")

PHONEME_TO_VISEME: Dict[str, str] = {
    'AH': 'open_mouth',
    'EE': 'smile',
    'OH': 'round_mouth',
    # Add more mappings as needed
}

def text_to_phonemes(text: str) -> List[str]:
    """Convert text to phoneme sequence."""
    # TODO: Implement real phoneme extraction
    return ['AH', 'EE', 'OH']

def phonemes_to_visemes(phonemes: List[str]) -> List[str]:
    """Convert phoneme sequence to viseme sequence."""
    return [PHONEME_TO_VISEME.get(p, 'neutral') for p in phonemes]

EMOTION_TO_EXPRESSION: Dict[str, str] = {
    'happy': 'smile_face',
    'sad': 'frown_face',
    'angry': 'angry_eyebrows',
    'neutral': 'neutral_face'
}

def emotion_to_expression(emotion: str) -> str:
    """Convert emotion to facial expression name."""
    return EMOTION_TO_EXPRESSION.get(emotion, 'neutral_face')

def synthesize_frames(visemes: List[str], expression: str, config: VideoConfig) -> List[np.ndarray]:
    """Synthesize video frames based on visemes and expression using PIL."""
    frames = []
    total_frames = int(config.fps * config.duration)
    width, height = config.width, config.height
    
    print(f"Creating {total_frames} frames ({config.fps}fps × {config.duration}s)")
    
    for i in range(total_frames):
        # Create frame using PIL
        img = Image.new('RGB', (width, height), color=(50, 50, 50))
        draw = ImageDraw.Draw(img)
        
        # Draw simple avatar
        center_x, center_y = width // 2, height // 2
        avatar_radius = min(width, height) // 6
        
        # Draw face circle (skin tone)
        draw.ellipse([
            center_x - avatar_radius, center_y - avatar_radius,
            center_x + avatar_radius, center_y + avatar_radius
        ], fill=(220, 190, 170), outline=(180, 150, 130), width=2)
        
        # Draw eyes
        eye_offset = avatar_radius // 2
        eye_radius = avatar_radius // 6
        # Left eye
        draw.ellipse([
            center_x - eye_offset - eye_radius, center_y - eye_radius,
            center_x - eye_offset + eye_radius, center_y + eye_radius
        ], fill=(255, 255, 255), outline=(0, 0, 0))
        draw.ellipse([
            center_x - eye_offset - eye_radius//2, center_y - eye_radius//2,
            center_x - eye_offset + eye_radius//2, center_y + eye_radius//2
        ], fill=(0, 0, 0))
        
        # Right eye
        draw.ellipse([
            center_x + eye_offset - eye_radius, center_y - eye_radius,
            center_x + eye_offset + eye_radius, center_y + eye_radius
        ], fill=(255, 255, 255), outline=(0, 0, 0))
        draw.ellipse([
            center_x + eye_offset - eye_radius//2, center_y - eye_radius//2,
            center_x + eye_offset + eye_radius//2, center_y + eye_radius//2
        ], fill=(0, 0, 0))
        
        # Draw mouth based on viseme
        viseme_index = i % len(visemes) if visemes else 0
        current_viseme = visemes[viseme_index] if visemes else 'neutral'
        mouth_y = center_y + avatar_radius // 2
        mouth_width = avatar_radius // 2
        
        if current_viseme == 'open_mouth':
            # Open mouth (O shape)
            draw.ellipse([
                center_x - mouth_width//2, mouth_y - mouth_width//3,
                center_x + mouth_width//2, mouth_y + mouth_width//3
            ], fill=(50, 50, 50), outline=(0, 0, 0), width=2)
        elif current_viseme == 'smile':
            # Smile (curved line)
            draw.arc([
                center_x - mouth_width, mouth_y - mouth_width//2,
                center_x + mouth_width, mouth_y + mouth_width//2
            ], 0, 180, fill=(0, 0, 0), width=3)
        else:  # neutral or round_mouth
            # Neutral mouth (small line)
            draw.ellipse([
                center_x - mouth_width//3, mouth_y - mouth_width//4,
                center_x + mouth_width//3, mouth_y + mouth_width//4
            ], fill=(100, 100, 100), outline=(0, 0, 0))
        
        # Add emotion-based expression changes
        if expression == 'smile_face':
            # Add rosy cheeks for happiness
            cheek_radius = avatar_radius // 4
            draw.ellipse([
                center_x - avatar_radius + cheek_radius//2, center_y,
                center_x - avatar_radius + cheek_radius*2, center_y + cheek_radius
            ], fill=(255, 200, 200))
            draw.ellipse([
                center_x + avatar_radius - cheek_radius*2, center_y,
                center_x + avatar_radius - cheek_radius//2, center_y + cheek_radius
            ], fill=(255, 200, 200))
        
        # Add text overlay with frame info
        try:
            # Use default font or try to load a better one
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
            except:
                font = ImageFont.load_default()
            
            frame_text = f"Frame {i+1}/{total_frames}"
            emotion_text = f"{current_viseme} | {expression}"
            
            draw.text((10, 10), frame_text, fill=(255, 255, 255), font=font)
            draw.text((10, 25), emotion_text, fill=(200, 200, 200), font=font)
        except Exception as e:
            # Fallback without font
            draw.text((10, 10), f"F{i+1}/{total_frames}", fill=(255, 255, 255))
            draw.text((10, 25), f"{current_viseme}", fill=(200, 200, 200))
        
        # Convert PIL to numpy array
        frame = np.array(img)
        frames.append(frame)
        
        if i % 10 == 0 or i == total_frames - 1:  # Progress every 10 frames
            print(f"  Generated frame {i+1}/{total_frames}: {current_viseme} | {expression}")
    
    return frames

def create_video_file(frames: List[np.ndarray], output_path: str, fps: int = 30) -> str:
    """Create video file from frames using imageio."""
    try:
        print(f"Creating video file with {len(frames)} frames at {fps}fps...")
        
        # Frames are already in RGB format from PIL
        imageio.mimsave(output_path, frames, fps=fps, quality=8)
        print(f"✅ Video saved successfully: {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ Error creating video: {e}")
        # Fallback: create a simple image
        fallback_path = output_path.replace('.mp4', '_preview.png')
        if frames:
            # Save first frame as preview
            img = Image.fromarray(frames[0])
            img.save(fallback_path)
            print(f"✅ Fallback: Saved preview image: {fallback_path}")
            return fallback_path
        return output_path

def mix_music_with_video(video_path: str, music_path: str) -> None:
    """Mix background music with video."""
    # TODO: Implement real audio/video mixing with ffmpeg
    print(f"🎵 Mixing {music_path} with {video_path}")
    print("Note: Audio mixing not yet implemented - video contains visual only")

async def generate_video_with_lipsync_and_emotion(text: str, emotion: str, config: VideoConfig, 
                                                music: Optional[str] = None) -> str:
    """Generate video with lip sync and emotional expression."""
    print(f"🎬 Generating video: '{text[:50]}...' (Emotion: {emotion})")
    
    # Generate phonemes and visemes
    phonemes = text_to_phonemes(text)
    visemes = phonemes_to_visemes(phonemes)
    expression = emotion_to_expression(emotion)
    
    # Generate video frames
    frames = synthesize_frames(visemes, expression, config)
    
    # Create output filename with timestamp
    import time
    timestamp = int(time.time())
    video_filename = f"output_{emotion}_{timestamp}.mp4"
    video_path = os.path.join(os.getcwd(), video_filename)
    
    # Create video file
    final_path = create_video_file(frames, video_path, config.fps)
    
    # Mix music if provided
    if music:
        mix_music_with_video(final_path, music)
    
    return final_path

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file."""
    print(f"[PDF] Extracting story from: {pdf_path}")
    text = ""
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"[PDF extraction error]: {e}")
    return text

def parse_characters_and_scenes(story_text: str) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    """Parse story text to extract characters and scenes."""
    print("[Story] Parsing characters and scenes...")
    
    # Use appropriate nlp pipeline
    doc = nlp_coref(story_text) if 'nlp_coref' in globals() else nlp(story_text)
    character_map: Dict[str, str] = {}
    
    # Use global use_coreferee variable
    global use_coreferee
    
    # Try different coreferee approaches
    if use_coreferee == True:
        # Standard coreferee pipeline approach
        try:
            for chain in doc._.coref_chains:
                person_mentions = [m for m in chain if m.root.ent_type_ == "PERSON"]
                if person_mentions:
                    canonical = person_mentions[0].text
                    for mention in chain:
                        character_map[mention.text] = canonical
            print(f"✅ Used coreferee pipeline for coreference resolution")
        except Exception as e:
            print(f"Coreferee pipeline failed, falling back: {e}")
            use_coreferee = False
    
    elif use_coreferee == "manual":
        # Manual coreferee processing approach
        try:
            import coreferee
            # Process text separately with coreferee
            nlp_temp = spacy.blank("en")
            nlp_temp.add_pipe("sentencizer")
            nlp_temp.add_pipe('coreferee')
            coref_doc = nlp_temp(story_text)
            
            for chain in coref_doc._.coref_chains:
                for mention in chain:
                    # Map to first mention as canonical
                    if len(chain) > 0:
                        canonical = chain[0].text
                        character_map[mention.text] = canonical
            print(f"✅ Used manual coreferee processing")
        except Exception as e:
            print(f"Manual coreferee failed, using basic NLP: {e}")
    
    # Always collect PERSON entities (works with or without coreferee)
    for ent in doc.ents:
        if ent.label_ == "PERSON" and ent.text not in character_map:
            character_map[ent.text] = ent.text
    
    # Add pronoun resolution (basic fallback)
    if not character_map:
        # Simple pronoun detection as fallback
        pronouns = {"he", "him", "his", "she", "her", "hers", "they", "them", "their"}
        words = story_text.lower().split()
        for word in words:
            if word in pronouns:
                character_map[word] = "Character"  # Generic character
    
    characters = list(set(character_map.values()))
    
    def guess_gender(name: str) -> str:
        """Basic gender inference from name/pronouns."""
        if name.lower() in ["he", "him", "mr", "sir", "john"]: return "male"
        if name.lower() in ["she", "her", "ms", "mrs", "miss", "mary"]: return "female"
        return "neutral"
    
    character_objs = [
        {
            "name": name,
            "gender": guess_gender(name),
            "style": "realistic"
        }
        for name in characters
    ] if characters else [{"name": "Narrator", "gender": "neutral", "style": "realistic"}]
    
    scenes = [
        {
            "description": sent.text.strip(),
            "emotion": detect_emotion(sent.text)
        }
        for sent in doc.sents
        if sent.text.strip()
    ]
    
    if not scenes:
        # Fallback: create scene from entire text
        scenes = [{
            "description": story_text[:200] + "..." if len(story_text) > 200 else story_text,
            "emotion": detect_emotion(story_text)
        }]
    
    return character_objs, scenes

def parse_tags_and_title(scenes: List[Dict[str, str]], characters: List[Dict[str, str]]) -> Tuple[str, List[str]]:
    """Generate video title and tags based on content."""
    main_char = characters[0]['name'] if characters else "AI Movie"
    main_scene = scenes[0]['description'] if scenes else "A new adventure"
    
    extra_keywords = [
        "Nature", "Animals", "Birds", "Water", "Sky", 
        "Beach", "City", "World", "AI Video"
    ]
    
    # Build tags list
    tags = [f"#{k.replace(' ', '')}" for k in extra_keywords]
    tags += [c['name'].replace(' ', '') for c in characters]
    tags += [w for s in scenes for w in s['description'].split() 
            if w.istitle() and len(w) > 2]  # Add capitalized words as tags
    tags += ["#Viral", "#Trending", "#Shorts", "#Movie", "#Story"]
    
    # Remove duplicates and limit
    tags = list(dict.fromkeys(tags))[:15]
    title = f"{main_char}: {main_scene[:60]}"
    
    return title, tags

def get_user_inputs() -> Tuple[str, str, str, str]:
    """Get user inputs from command line interface."""
    print("\n--- AI Video Generator Input ---")
    headline = input("Enter a headline (optional): ")
    script = input("Enter a script or lines for the video: ")
    image_path = input("Enter an image file path (optional): ")
    youtube_link = input("Enter a YouTube link (optional): ")
    return headline, script, image_path, youtube_link

async def upload_to_youtube(video_path: str, title: str, description: str, tags: List[str]) -> str:
    """Upload video to YouTube and return video URL."""
    try:
        scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", scopes)
        credentials = flow.run_console()
        youtube = build("youtube", "v3", credentials=credentials)

        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "categoryId": "22"  # People & Blogs
                },
                "status": {
                    "privacyStatus": "private"  # Start as private
                }
            },
            media_body=MediaFileUpload(video_path)
        )
        response = request.execute()
        video_url = f"https://youtu.be/{response['id']}"
        print(f"Uploaded to YouTube: {video_url}")
        return video_url
    except Exception as e:
        print(f"YouTube upload failed: {str(e)}")
        return ""

async def process_video_generation(
    script: str,
    headline: str = "",
    image_path: str = "",
    youtube_link: str = "",
    pdf_path: str = "",
    config: Optional[VideoConfig] = None
) -> Tuple[str, str, List[str]]:
    """Process video generation with all inputs and return video path and metadata."""
    if config is None:
        config = VideoConfig(width=640, height=480, fps=24, duration=3)  # Smaller, faster config
    
    # Initialize core components
    engine = VideoGenerationEngine()
    memory = ConversationMemory()
    voice = VoiceIntegration()
    responder = ConversationalResponder(memory)
    
    # Process PDF if provided
    if pdf_path:
        story_text = extract_text_from_pdf(pdf_path)
        characters, scenes = parse_characters_and_scenes(story_text)
    else:
        characters, scenes = parse_characters_and_scenes(script)
    
    # Configure avatar and scene
    avatar_info = characters[0] if characters else {
        "name": "AI", "gender": "neutral", "style": "realistic"
    }
    avatar = Avatar(**avatar_info)
    script_text = scenes[0]['description'] if scenes else script
    emotion = scenes[0]['emotion'] if scenes else detect_emotion(script)
    
    # Generate response and select music
    ai_response = responder.generate_response(script_text)
    music = select_music(emotion)
    
    # Generate video
    video_path = await generate_video_with_lipsync_and_emotion(
        text=script_text,
        emotion=emotion,
        config=config,
        music=music
    )
    
    # Generate metadata
    title, tags = parse_tags_and_title(scenes, characters)
    
    return video_path, title, tags

def run_cli() -> None:
    """Run the command-line interface version."""
    parser = argparse.ArgumentParser(description="Run the AI Video Generation Engine.")
    parser.add_argument('--width', type=int, default=1280, help='Video width')
    parser.add_argument('--height', type=int, default=720, help='Video height')
    parser.add_argument('--fps', type=int, default=30, help='Frames per second')
    parser.add_argument('--duration', type=int, default=5, help='Duration in seconds')
    args = parser.parse_args()
    
    config = VideoConfig(
        width=args.width,
        height=args.height,
        fps=args.fps,
        duration=args.duration
    )
    
    print("AI Video Generator (type 'exit' to quit)")
    while True:
        # Get user inputs
        headline, script, image_path, youtube_link = get_user_inputs()
        if script.strip().lower() == 'exit':
            break
            
        pdf_path = input("Upload a story PDF (optional, press Enter to skip): ")
        
        # Process video generation
        video_path, title, tags = asyncio.run(process_video_generation(
            script=script,
            headline=headline,
            image_path=image_path,
            youtube_link=youtube_link,
            pdf_path=pdf_path,
            config=config
        ))
        
        print(f"\nVideo generated successfully!")
        print(f"Video path: {video_path}")
        print(f"Suggested title: {title}")
        print(f"Suggested tags: {', '.join(tags)}")
        
        # Optional YouTube upload
        if input("\nUpload to YouTube? (y/N): ").lower().strip() == 'y':
            description = f"Generated by AI Video Generator\nHeadline: {headline}"
            video_url = asyncio.run(upload_to_youtube(video_path, title, description, tags))
            if video_url:
                print(f"Video uploaded successfully: {video_url}")

def run_streamlit() -> None:
    """Run the Streamlit web interface version."""
    st.title("AI Video Generator")

    with st.form("video_generation_form"):
        headline = st.text_input("Enter a headline (optional):")
        script = st.text_area("Enter a script or lines for the video:")
        image_path = st.text_input("Enter an image file path (optional):")
        youtube_link = st.text_input("Enter a YouTube link (optional):")
        pdf_file = st.file_uploader("Upload a story PDF (optional):", type=["pdf"])
        
        submit = st.form_submit_button("Generate Video")
        
    if submit and script:
        with st.spinner("Generating video..."):
            # Save uploaded PDF if provided
            pdf_path = ""
            if pdf_file:
                pdf_path = "temp_story.pdf"
                with open(pdf_path, "wb") as f:
                    f.write(pdf_file.read())
            
            # Process video generation
            video_path, title, tags = asyncio.run(process_video_generation(
                script=script,
                headline=headline,
                image_path=image_path,
                youtube_link=youtube_link,
                pdf_path=pdf_path
            ))
            
            # Show results
            st.success("Video generated successfully!")
            
            # Show video info
            if os.path.exists(video_path):
                file_size = os.path.getsize(video_path)
                st.info(f"📁 File: {video_path} ({file_size:,} bytes)")
                
                # Video preview (only for small files to avoid loading issues)
                if file_size < 50_000_000:  # Less than 50MB
                    try:
                        with open(video_path, "rb") as video_file:
                            video_bytes = video_file.read()
                            st.video(video_bytes)
                    except Exception as e:
                        st.warning(f"Could not display video preview: {e}")
                        
                # Download button
                with open(video_path, "rb") as f:
                    st.download_button(
                        "📥 Download Video",
                        f,
                        file_name=Path(video_path).name,
                        mime="video/mp4"
                    )
            else:
                st.error(f"Video file not found: {video_path}")
            
            # Show metadata
            st.subheader("Video Metadata")
            st.write(f"**Title:** {title}")
            st.write(f"**Tags:** {', '.join(tags)}")
            
            # YouTube upload option
            if st.button("Upload to YouTube"):
                with st.spinner("Uploading to YouTube..."):
                    description = f"Generated by AI Video Generator\nHeadline: {headline}"
                    video_url = asyncio.run(upload_to_youtube(
                        video_path, title, description, tags
                    ))
                    if video_url:
                        st.success(f"Video uploaded successfully! View at {video_url}")
    elif submit:
        st.error("Please enter a script for the video.")

def main() -> None:
    """Main entry point that decides which interface to run."""
    # Check if running in Streamlit by checking sys.argv
    if any('streamlit' in str(arg).lower() for arg in sys.argv):
        run_streamlit()
        return
    
    # Check for streamlit environment variables
    if os.environ.get('STREAMLIT_SERVER_PORT') or os.environ.get('_STREAMLIT_INTERNAL_KEY_NAME'):
        run_streamlit()
        return
    
    # Default to CLI
    run_cli()

if __name__ == "__main__":
    main()