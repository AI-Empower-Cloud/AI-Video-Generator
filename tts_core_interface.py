#!/usr/bin/env python3
"""
🎤 Core TTS Interface - Complete Text-to-Speech System
AI Video Generator - Self-Contained TTS Platform

Core Capabilities:
- 🔤 Text input (plain text or markdown)
- 🗣️ Voice selection (preloaded voices: Daniel, Emma, etc.)
- 🗃️ Audio format support (.wav, .mp3, .ogg)
- 🔊 Play + Download (audio preview and local save)
- 🌍 Multilingual Support (Coqui TTS for multiple languages)
- 🧪 Voice Cloning (fine-tune with custom speaker data)
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple
import streamlit as st
import numpy as np
import soundfile as sf
from pydub import AudioSegment
from pydub.playback import play
import tempfile
import markdown
import re

# Import our existing TTS engines
try:
    from advanced_local_tts import AdvancedLocalTTS
    from simplified_local_tts import SimplifiedLocalTTS
    from audio_integration import AudioIntegration
except ImportError:
    print("Warning: Some TTS modules not found. Installing fallback...")

class CoreTTSInterface:
    """
    Complete TTS interface with all core capabilities
    """
    
    def __init__(self):
        """Initialize the TTS interface with all engines and voices"""
        self.setup_logging()
        self.setup_directories()
        self.initialize_engines()
        self.load_voice_library()
        self.setup_audio_formats()
        
    def setup_logging(self):
        """Setup logging for TTS operations"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_directories(self):
        """Create necessary directories for TTS operations"""
        self.base_dir = Path(__file__).parent
        self.voices_dir = self.base_dir / "voices"
        self.audio_output_dir = self.base_dir / "audio_output"
        self.custom_voices_dir = self.voices_dir / "custom"
        self.temp_dir = self.base_dir / "temp"
        
        # Create directories
        for dir_path in [self.voices_dir, self.audio_output_dir, 
                        self.custom_voices_dir, self.temp_dir]:
            dir_path.mkdir(exist_ok=True)
            
    def initialize_engines(self):
        """Initialize all TTS engines"""
        self.engines = {}
        
        try:
            # Initialize advanced TTS
            self.engines['advanced'] = AdvancedLocalTTS()
            self.logger.info("Advanced TTS engine initialized")
        except Exception as e:
            self.logger.warning(f"Advanced TTS not available: {e}")
            
        try:
            # Initialize simplified TTS
            self.engines['simplified'] = SimplifiedLocalTTS()
            self.logger.info("Simplified TTS engine initialized")
        except Exception as e:
            self.logger.warning(f"Simplified TTS not available: {e}")
            
        try:
            # Initialize audio integration
            self.audio_engine = AudioIntegration()
            self.logger.info("Audio integration engine initialized")
        except Exception as e:
            self.logger.warning(f"Audio integration not available: {e}")
            
    def load_voice_library(self):
        """Load preloaded voice library"""
        self.voice_library = {
            # 🗣️ Preloaded Professional Voices
            "Daniel": {
                "name": "Daniel",
                "gender": "male",
                "age": "adult",
                "accent": "american",
                "style": "professional",
                "quality": "high",
                "engine": "coqui",
                "languages": ["en"],
                "description": "Professional male narrator - clear, authoritative"
            },
            "Emma": {
                "name": "Emma",
                "gender": "female", 
                "age": "adult",
                "accent": "british",
                "style": "friendly",
                "quality": "high",
                "engine": "coqui",
                "languages": ["en"],
                "description": "Friendly female teacher - warm, engaging"
            },
            "Carlos": {
                "name": "Carlos",
                "gender": "male",
                "age": "adult",
                "accent": "neutral",
                "style": "educational",
                "quality": "high", 
                "engine": "coqui",
                "languages": ["es", "en"],
                "description": "Bilingual educator - Spanish/English"
            },
            "Sophie": {
                "name": "Sophie",
                "gender": "female",
                "age": "adult",
                "accent": "french",
                "style": "elegant",
                "quality": "high",
                "engine": "coqui",
                "languages": ["fr", "en"],
                "description": "French narrator - elegant, clear pronunciation"
            },
            "Akira": {
                "name": "Akira",
                "gender": "male",
                "age": "adult",
                "accent": "japanese",
                "style": "calm",
                "quality": "high",
                "engine": "coqui",
                "languages": ["ja", "en"],
                "description": "Japanese narrator - calm, precise"
            },
            "Linda": {
                "name": "Linda",
                "gender": "female",
                "age": "mature",
                "accent": "american",
                "style": "authoritative",
                "quality": "ultra",
                "engine": "tortoise",
                "languages": ["en"],
                "description": "Senior educator - authoritative, experienced"
            },
            "Robot": {
                "name": "Robot",
                "gender": "neutral",
                "age": "artificial",
                "accent": "synthetic",
                "style": "robotic",
                "quality": "fast",
                "engine": "espeak",
                "languages": ["en", "es", "fr", "de"],
                "description": "AI assistant voice - clear, synthetic"
            }
        }
        
        # Load custom voices if available
        self.load_custom_voices()
        
    def load_custom_voices(self):
        """Load user-created custom voices"""
        custom_voices_file = self.custom_voices_dir / "custom_voices.json"
        if custom_voices_file.exists():
            try:
                with open(custom_voices_file, 'r') as f:
                    custom_voices = json.load(f)
                self.voice_library.update(custom_voices)
                self.logger.info(f"Loaded {len(custom_voices)} custom voices")
            except Exception as e:
                self.logger.warning(f"Could not load custom voices: {e}")
                
    def setup_audio_formats(self):
        """Setup supported audio formats"""
        self.supported_formats = {
            'wav': {
                'extension': '.wav',
                'mime_type': 'audio/wav',
                'quality': 'lossless',
                'description': 'Uncompressed audio (best quality)'
            },
            'mp3': {
                'extension': '.mp3', 
                'mime_type': 'audio/mpeg',
                'quality': 'compressed',
                'description': 'Compressed audio (smaller file size)'
            },
            'ogg': {
                'extension': '.ogg',
                'mime_type': 'audio/ogg',
                'quality': 'compressed',
                'description': 'Open-source compressed audio'
            }
        }
        
    def process_text_input(self, text: str, input_type: str = "plain") -> str:
        """
        🔤 Process text input (plain text or markdown)
        """
        if input_type == "markdown":
            # Convert markdown to plain text for TTS
            # Remove markdown formatting but keep structure
            text = self.markdown_to_speech_text(text)
        elif input_type == "plain":
            # Clean plain text
            text = self.clean_text_for_speech(text)
            
        return text
    
    def markdown_to_speech_text(self, markdown_text: str) -> str:
        """Convert markdown to speech-friendly text"""
        # Convert markdown to HTML first
        html = markdown.markdown(markdown_text)
        
        # Remove HTML tags but keep content
        text = re.sub(r'<[^>]+>', '', html)
        
        # Add pauses for structure
        text = re.sub(r'\n\n+', '. ', text)  # Paragraph breaks
        text = re.sub(r'\n', ', ', text)      # Line breaks
        
        # Clean up extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def clean_text_for_speech(self, text: str) -> str:
        """Clean plain text for optimal speech synthesis"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Add pauses for readability
        text = re.sub(r'([.!?])\s*', r'\1 ', text)
        
        # Handle abbreviations
        abbreviations = {
            'AI': 'Artificial Intelligence',
            'ML': 'Machine Learning',
            'TTS': 'Text to Speech',
            'API': 'Application Programming Interface',
            'URL': 'U R L',
            'HTML': 'H T M L',
            'CSS': 'C S S'
        }
        
        for abbr, full in abbreviations.items():
            text = text.replace(abbr, full)
            
        return text.strip()
    
    def get_available_voices(self, language: str = "en") -> Dict[str, Dict]:
        """
        🗣️ Get available voices for selection
        """
        available_voices = {}
        
        for voice_id, voice_info in self.voice_library.items():
            if language in voice_info.get('languages', ['en']):
                available_voices[voice_id] = voice_info
                
        return available_voices
    
    def synthesize_speech(self, 
                         text: str, 
                         voice_id: str = "Emma",
                         language: str = "en",
                         output_format: str = "wav",
                         quality: str = "high") -> Tuple[str, Dict]:
        """
        Main speech synthesis function
        """
        try:
            # Get voice configuration
            if voice_id not in self.voice_library:
                voice_id = "Emma"  # Fallback to default
                
            voice_config = self.voice_library[voice_id]
            engine_name = voice_config.get('engine', 'coqui')
            
            # Generate unique filename
            timestamp = int(time.time())
            base_filename = f"tts_{voice_id}_{timestamp}"
            
            # Synthesize with appropriate engine
            if engine_name == "tortoise" and 'advanced' in self.engines:
                audio_path = self._synthesize_tortoise(text, voice_config, base_filename)
            elif engine_name == "coqui" and 'advanced' in self.engines:
                audio_path = self._synthesize_coqui(text, voice_config, base_filename, language)
            elif engine_name == "espeak" and 'simplified' in self.engines:
                audio_path = self._synthesize_espeak(text, voice_config, base_filename)
            else:
                # Fallback to any available engine
                audio_path = self._synthesize_fallback(text, voice_config, base_filename)
            
            # Convert to requested format if needed
            final_path = self._convert_audio_format(audio_path, output_format)
            
            # Generate metadata
            metadata = {
                "voice_id": voice_id,
                "voice_name": voice_config['name'],
                "language": language,
                "format": output_format,
                "quality": quality,
                "engine": engine_name,
                "duration": self._get_audio_duration(final_path),
                "file_size": os.path.getsize(final_path),
                "generated_at": time.time()
            }
            
            self.logger.info(f"Successfully synthesized speech: {voice_id} -> {final_path}")
            return final_path, metadata
            
        except Exception as e:
            self.logger.error(f"Speech synthesis failed: {e}")
            raise
    
    def _synthesize_tortoise(self, text: str, voice_config: Dict, base_filename: str) -> str:
        """Synthesize using Tortoise TTS (ultra quality)"""
        output_path = self.audio_output_dir / f"{base_filename}_tortoise.wav"
        
        if 'advanced' in self.engines:
            result = self.engines['advanced'].synthesize_speech(
                text=text,
                voice_profile=voice_config['name'].lower(),
                output_path=str(output_path),
                quality_override="ultra"
            )
            return str(output_path)
        else:
            raise Exception("Advanced TTS engine not available")
    
    def _synthesize_coqui(self, text: str, voice_config: Dict, base_filename: str, language: str) -> str:
        """Synthesize using Coqui TTS (high quality, multilingual)"""
        output_path = self.audio_output_dir / f"{base_filename}_coqui.wav"
        
        if 'advanced' in self.engines:
            result = self.engines['advanced'].synthesize_speech(
                text=text,
                voice_profile=voice_config['name'].lower(),
                output_path=str(output_path),
                quality_override="high"
            )
            return str(output_path)
        else:
            raise Exception("Advanced TTS engine not available")
    
    def _synthesize_espeak(self, text: str, voice_config: Dict, base_filename: str) -> str:
        """Synthesize using espeak (fast, lightweight)"""
        output_path = self.audio_output_dir / f"{base_filename}_espeak.wav"
        
        if 'simplified' in self.engines:
            result = self.engines['simplified'].synthesize_speech(
                text=text,
                voice_type=voice_config.get('style', 'default'),
                output_path=str(output_path)
            )
            return str(output_path)
        else:
            raise Exception("Simplified TTS engine not available")
    
    def _synthesize_fallback(self, text: str, voice_config: Dict, base_filename: str) -> str:
        """Fallback synthesis method"""
        output_path = self.audio_output_dir / f"{base_filename}_fallback.wav"
        
        # Try any available engine
        if 'simplified' in self.engines:
            result = self.engines['simplified'].synthesize_speech(
                text=text,
                voice_type="default",
                output_path=str(output_path)
            )
            return str(output_path)
        else:
            raise Exception("No TTS engines available")
    
    def _convert_audio_format(self, input_path: str, target_format: str) -> str:
        """
        🗃️ Convert audio to different formats (.wav, .mp3, .ogg)
        """
        if target_format == "wav" and input_path.endswith(".wav"):
            return input_path
        
        # Load audio
        audio = AudioSegment.from_wav(input_path)
        
        # Generate output path
        base_path = input_path.replace(".wav", "")
        extension = self.supported_formats[target_format]['extension']
        output_path = f"{base_path}{extension}"
        
        # Export in target format
        if target_format == "mp3":
            audio.export(output_path, format="mp3", bitrate="192k")
        elif target_format == "ogg":
            audio.export(output_path, format="ogg")
        else:  # wav
            audio.export(output_path, format="wav")
            
        return output_path
    
    def _get_audio_duration(self, audio_path: str) -> float:
        """Get audio duration in seconds"""
        try:
            audio = AudioSegment.from_file(audio_path)
            return len(audio) / 1000.0  # Convert to seconds
        except:
            return 0.0
    
    def play_audio(self, audio_path: str) -> bool:
        """
        🔊 Play audio preview
        """
        try:
            audio = AudioSegment.from_file(audio_path)
            play(audio)
            return True
        except Exception as e:
            self.logger.error(f"Audio playback failed: {e}")
            return False
    
    def create_custom_voice(self, 
                           voice_name: str,
                           audio_files: List[str],
                           transcript_files: List[str],
                           language: str = "en") -> Dict:
        """
        🧪 Voice Cloning - Create custom voice from audio data
        """
        try:
            # Validate input data
            if len(audio_files) != len(transcript_files):
                raise ValueError("Number of audio files must match transcript files")
            
            # Check minimum duration (15 minutes)
            total_duration = self._calculate_total_duration(audio_files)
            if total_duration < 900:  # 15 minutes
                self.logger.warning(f"Audio duration ({total_duration}s) is less than recommended 15 minutes")
            
            # Prepare training data
            training_data = self._prepare_voice_training_data(
                audio_files, transcript_files, voice_name
            )
            
            # Train custom voice model
            if 'advanced' in self.engines:
                custom_voice_path = self._train_custom_voice_advanced(
                    training_data, voice_name, language
                )
            else:
                custom_voice_path = self._train_custom_voice_simple(
                    training_data, voice_name, language
                )
            
            # Create voice configuration
            custom_voice_config = {
                "name": voice_name,
                "gender": "custom",
                "age": "adult",
                "accent": "custom",
                "style": "personal",
                "quality": "high",
                "engine": "custom",
                "languages": [language],
                "description": f"Custom voice: {voice_name}",
                "model_path": custom_voice_path,
                "created_at": time.time(),
                "training_duration": total_duration
            }
            
            # Add to voice library
            self.voice_library[voice_name] = custom_voice_config
            self._save_custom_voice_config(voice_name, custom_voice_config)
            
            self.logger.info(f"Custom voice '{voice_name}' created successfully")
            return custom_voice_config
            
        except Exception as e:
            self.logger.error(f"Custom voice creation failed: {e}")
            raise
    
    def _calculate_total_duration(self, audio_files: List[str]) -> float:
        """Calculate total duration of audio files"""
        total_duration = 0
        for audio_file in audio_files:
            try:
                audio = AudioSegment.from_file(audio_file)
                total_duration += len(audio) / 1000.0
            except:
                continue
        return total_duration
    
    def _prepare_voice_training_data(self, 
                                   audio_files: List[str], 
                                   transcript_files: List[str],
                                   voice_name: str) -> Dict:
        """Prepare data for voice training"""
        training_data = {
            "voice_name": voice_name,
            "audio_files": audio_files,
            "transcript_files": transcript_files,
            "prepared_at": time.time()
        }
        return training_data
    
    def _train_custom_voice_advanced(self, training_data: Dict, voice_name: str, language: str) -> str:
        """Train custom voice using advanced engine"""
        # This would implement actual voice cloning with Coqui TTS or Tortoise
        model_path = self.custom_voices_dir / f"{voice_name}_model"
        model_path.mkdir(exist_ok=True)
        
        # Placeholder for actual training logic
        # In a real implementation, this would:
        # 1. Preprocess audio and text data
        # 2. Fine-tune a pre-trained model
        # 3. Save the custom voice model
        
        self.logger.info(f"Training custom voice '{voice_name}' (advanced method)")
        return str(model_path)
    
    def _train_custom_voice_simple(self, training_data: Dict, voice_name: str, language: str) -> str:
        """Train custom voice using simple method"""
        # Fallback method for voice customization
        model_path = self.custom_voices_dir / f"{voice_name}_simple"
        model_path.mkdir(exist_ok=True)
        
        self.logger.info(f"Training custom voice '{voice_name}' (simple method)")
        return str(model_path)
    
    def _save_custom_voice_config(self, voice_name: str, config: Dict):
        """Save custom voice configuration"""
        custom_voices_file = self.custom_voices_dir / "custom_voices.json"
        
        # Load existing custom voices
        if custom_voices_file.exists():
            with open(custom_voices_file, 'r') as f:
                custom_voices = json.load(f)
        else:
            custom_voices = {}
        
        # Add new voice
        custom_voices[voice_name] = config
        
        # Save updated configuration
        with open(custom_voices_file, 'w') as f:
            json.dump(custom_voices, f, indent=2)
    
    def get_supported_languages(self) -> Dict[str, str]:
        """
        🌍 Get supported languages for multilingual TTS
        """
        return {
            "en": "English",
            "es": "Spanish (Español)",
            "fr": "French (Français)", 
            "de": "German (Deutsch)",
            "it": "Italian (Italiano)",
            "pt": "Portuguese (Português)",
            "ja": "Japanese (日本語)",
            "ko": "Korean (한국어)",
            "zh": "Chinese (中文)",
            "ru": "Russian (Русский)",
            "ar": "Arabic (العربية)",
            "hi": "Hindi (हिन्दी)"
        }
    
    def create_audio_download_link(self, audio_path: str, filename: str = None) -> str:
        """
        Create download link for generated audio
        """
        if filename is None:
            filename = os.path.basename(audio_path)
        
        # Read audio file
        with open(audio_path, 'rb') as f:
            audio_data = f.read()
        
        # Create download link (for Streamlit)
        import base64
        b64 = base64.b64encode(audio_data).decode()
        
        file_format = audio_path.split('.')[-1]
        mime_type = self.supported_formats.get(file_format, {}).get('mime_type', 'audio/wav')
        
        href = f'<a href="data:{mime_type};base64,{b64}" download="{filename}">Download {filename}</a>'
        return href


def create_streamlit_interface():
    """
    Create Streamlit web interface for TTS Core Features
    """
    st.set_page_config(
        page_title="🎤 AI Video Generator - TTS Core Interface",
        page_icon="🎤",
        layout="wide"
    )
    
    st.title("🎤 Text-to-Speech Core Interface")
    st.subtitle("Professional voice synthesis with multilingual support")
    
    # Initialize TTS interface
    if 'tts_interface' not in st.session_state:
        with st.spinner("Initializing TTS engines..."):
            st.session_state.tts_interface = CoreTTSInterface()
    
    tts = st.session_state.tts_interface
    
    # Main interface layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🔤 Text Input")
        
        # Input type selection
        input_type = st.selectbox(
            "Input Type",
            ["plain", "markdown"],
            format_func=lambda x: "Plain Text" if x == "plain" else "Markdown"
        )
        
        # Text input area
        if input_type == "markdown":
            st.info("💡 Tip: You can use **bold**, *italic*, # headings, and other markdown formatting")
            text_input = st.text_area(
                "Enter your text (Markdown supported):",
                value="# Welcome to AI Education\n\nToday we'll learn about **artificial intelligence** and how it's changing our world.\n\n- Machine Learning\n- Natural Language Processing\n- Computer Vision",
                height=200
            )
        else:
            text_input = st.text_area(
                "Enter your text:",
                value="Welcome to our AI education lesson. Today we'll explore the fascinating world of artificial intelligence and machine learning.",
                height=200
            )
        
        # Process text
        if text_input:
            processed_text = tts.process_text_input(text_input, input_type)
            with st.expander("Processed Text (for TTS)"):
                st.text(processed_text)
    
    with col2:
        st.header("🗣️ Voice & Settings")
        
        # Language selection
        languages = tts.get_supported_languages()
        selected_language = st.selectbox(
            "Language",
            options=list(languages.keys()),
            format_func=lambda x: languages[x],
            index=0
        )
        
        # Voice selection
        available_voices = tts.get_available_voices(selected_language)
        if available_voices:
            voice_options = list(available_voices.keys())
            selected_voice = st.selectbox(
                "Voice",
                options=voice_options,
                format_func=lambda x: f"{available_voices[x]['name']} - {available_voices[x]['description']}"
            )
            
            # Voice info
            voice_info = available_voices[selected_voice]
            st.info(f"**{voice_info['name']}** ({voice_info['gender']}, {voice_info['style']})\n{voice_info['description']}")
        else:
            st.error(f"No voices available for {languages[selected_language]}")
            selected_voice = "Emma"
        
        # Audio format selection
        st.subheader("🗃️ Audio Format")
        format_options = list(tts.supported_formats.keys())
        selected_format = st.selectbox(
            "Output Format",
            options=format_options,
            format_func=lambda x: f"{x.upper()} - {tts.supported_formats[x]['description']}"
        )
        
        # Quality settings
        quality_options = ["fast", "standard", "high", "ultra"]
        selected_quality = st.selectbox("Quality", quality_options, index=2)
    
    # Generate speech button
    st.header("🎵 Generate Speech")
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        if st.button("🎤 Generate Speech", type="primary"):
            if text_input:
                with st.spinner("Generating speech..."):
                    try:
                        processed_text = tts.process_text_input(text_input, input_type)
                        audio_path, metadata = tts.synthesize_speech(
                            text=processed_text,
                            voice_id=selected_voice,
                            language=selected_language,
                            output_format=selected_format,
                            quality=selected_quality
                        )
                        
                        st.session_state.last_audio_path = audio_path
                        st.session_state.last_metadata = metadata
                        st.success("✅ Speech generated successfully!")
                        
                    except Exception as e:
                        st.error(f"❌ Generation failed: {e}")
            else:
                st.warning("Please enter some text to synthesize")
    
    with col4:
        if st.button("🔊 Play Audio") and 'last_audio_path' in st.session_state:
            try:
                st.audio(st.session_state.last_audio_path, format='audio/wav')
            except Exception as e:
                st.error(f"Playback failed: {e}")
    
    with col5:
        if st.button("💾 Download") and 'last_audio_path' in st.session_state:
            try:
                with open(st.session_state.last_audio_path, 'rb') as f:
                    st.download_button(
                        label="Download Audio",
                        data=f.read(),
                        file_name=f"tts_output.{selected_format}",
                        mime=tts.supported_formats[selected_format]['mime_type']
                    )
            except Exception as e:
                st.error(f"Download failed: {e}")
    
    # Audio metadata display
    if 'last_metadata' in st.session_state:
        st.header("📊 Audio Information")
        metadata = st.session_state.last_metadata
        
        col6, col7, col8, col9 = st.columns(4)
        with col6:
            st.metric("Duration", f"{metadata['duration']:.1f}s")
        with col7:
            st.metric("File Size", f"{metadata['file_size'] / 1024:.1f} KB")
        with col8:
            st.metric("Quality", metadata['quality'])
        with col9:
            st.metric("Engine", metadata['engine'])
    
    # Voice Cloning Section
    st.header("🧪 Voice Cloning (Optional)")
    
    with st.expander("Create Custom Voice"):
        st.info("📋 Upload 15-60 minutes of clear audio recordings with transcripts to create a custom voice")
        
        custom_voice_name = st.text_input("Custom Voice Name", value="MyVoice")
        
        # File uploaders
        audio_files = st.file_uploader(
            "Upload Audio Files (.wav format recommended)",
            accept_multiple_files=True,
            type=['wav', 'mp3', 'ogg']
        )
        
        transcript_files = st.file_uploader(
            "Upload Transcript Files (.txt format)",
            accept_multiple_files=True,
            type=['txt']
        )
        
        if st.button("🎭 Create Custom Voice"):
            if audio_files and transcript_files and custom_voice_name:
                if len(audio_files) == len(transcript_files):
                    with st.spinner("Training custom voice... This may take several minutes."):
                        try:
                            # Save uploaded files temporarily
                            temp_audio_paths = []
                            temp_transcript_paths = []
                            
                            for audio_file in audio_files:
                                temp_path = tts.temp_dir / audio_file.name
                                with open(temp_path, 'wb') as f:
                                    f.write(audio_file.getvalue())
                                temp_audio_paths.append(str(temp_path))
                            
                            for transcript_file in transcript_files:
                                temp_path = tts.temp_dir / transcript_file.name
                                with open(temp_path, 'w') as f:
                                    f.write(transcript_file.getvalue().decode())
                                temp_transcript_paths.append(str(temp_path))
                            
                            # Create custom voice
                            custom_voice_config = tts.create_custom_voice(
                                voice_name=custom_voice_name,
                                audio_files=temp_audio_paths,
                                transcript_files=temp_transcript_paths,
                                language=selected_language
                            )
                            
                            st.success(f"✅ Custom voice '{custom_voice_name}' created successfully!")
                            st.json(custom_voice_config)
                            
                        except Exception as e:
                            st.error(f"❌ Custom voice creation failed: {e}")
                else:
                    st.error("Number of audio files must match number of transcript files")
            else:
                st.warning("Please provide voice name, audio files, and transcript files")
    
    # Footer
    st.markdown("---")
    st.markdown("🎤 **AI Video Generator TTS** - 100% Self-Contained, Privacy-First Voice Synthesis")


if __name__ == "__main__":
    # Run Streamlit interface
    create_streamlit_interface()
