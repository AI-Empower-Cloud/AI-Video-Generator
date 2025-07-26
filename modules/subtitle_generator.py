#!/usr/bin/env python3
"""
Subtitle Generator Module
========================

Handles subtitle generation and transcription using Whisper and other tools.
"""

import asyncio
import os
import logging
import tempfile
import uuid
from typing import Optional, List, Dict, Any, Tuple
from pathlib import Path
import json
from datetime import timedelta

logger = logging.getLogger(__name__)

class SubtitleGenerator:
    """Subtitle generation and transcription using Whisper"""
    
    def __init__(self, model_size: str = "base"):
        self.model_size = model_size
        self.temp_dir = tempfile.mkdtemp(prefix="subtitle_generator_")
        self.whisper_available = self._check_whisper()
        self.faster_whisper_available = self._check_faster_whisper()
        self.model = None
        
        # Initialize the model
        self._init_model()
        
        logger.info(f"Subtitle Generator initialized - Whisper: {self.whisper_available}, Faster-Whisper: {self.faster_whisper_available}")
    
    def _check_whisper(self) -> bool:
        """Check if OpenAI Whisper is available"""
        try:
            import whisper
            return True
        except ImportError:
            return False
    
    def _check_faster_whisper(self) -> bool:
        """Check if Faster Whisper is available"""
        try:
            from faster_whisper import WhisperModel
            return True
        except ImportError:
            return False
    
    def _init_model(self):
        """Initialize Whisper model"""
        try:
            if self.faster_whisper_available:
                from faster_whisper import WhisperModel
                self.model = WhisperModel(self.model_size, device="cpu")
                logger.info(f"Faster Whisper model ({self.model_size}) initialized")
            elif self.whisper_available:
                import whisper
                self.model = whisper.load_model(self.model_size)
                logger.info(f"OpenAI Whisper model ({self.model_size}) initialized")
            else:
                logger.warning("No Whisper models available")
                
        except Exception as e:
            logger.error(f"Failed to initialize Whisper model: {e}")
            self.model = None
    
    async def transcribe_audio(
        self,
        audio_path: str,
        language: Optional[str] = None,
        output_formats: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """Transcribe audio to text and generate subtitles"""
        
        output_formats = output_formats or ["srt", "vtt", "txt"]
        
        logger.info(f"Transcribing audio: {audio_path}")
        
        try:
            if not self.model:
                raise RuntimeError("No Whisper model available for transcription")
            
            # Transcribe audio
            if self.faster_whisper_available and hasattr(self.model, 'transcribe'):
                segments, info = self.model.transcribe(audio_path, language=language)
                result = {
                    "text": "",
                    "segments": []
                }
                
                for segment in segments:
                    result["segments"].append({
                        "start": segment.start,
                        "end": segment.end,
                        "text": segment.text
                    })
                    result["text"] += segment.text + " "
                
                result["text"] = result["text"].strip()
                result["language"] = info.language
                
            elif self.whisper_available:
                import whisper
                result = self.model.transcribe(audio_path, language=language)
            
            else:
                raise RuntimeError("No working Whisper implementation available")
            
            # Generate output files
            output_files = {}
            
            for format_type in output_formats:
                if format_type == "srt":
                    output_files["srt"] = await self._generate_srt(result["segments"])
                elif format_type == "vtt":
                    output_files["vtt"] = await self._generate_vtt(result["segments"])
                elif format_type == "txt":
                    output_files["txt"] = await self._generate_txt(result["text"])
                elif format_type == "json":
                    output_files["json"] = await self._generate_json(result)
            
            logger.info(f"Transcription completed with {len(output_formats)} formats")
            return output_files
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise
    
    async def _generate_srt(self, segments: List[Dict]) -> str:
        """Generate SRT subtitle file"""
        output_path = os.path.join(self.temp_dir, f"subtitles_{uuid.uuid4().hex}.srt")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(segments, 1):
                start_time = self._seconds_to_srt_time(segment["start"])
                end_time = self._seconds_to_srt_time(segment["end"])
                text = segment["text"].strip()
                
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")
        
        logger.info(f"SRT file generated: {output_path}")
        return output_path
    
    async def _generate_vtt(self, segments: List[Dict]) -> str:
        """Generate VTT subtitle file"""
        output_path = os.path.join(self.temp_dir, f"subtitles_{uuid.uuid4().hex}.vtt")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("WEBVTT\n\n")
            
            for segment in segments:
                start_time = self._seconds_to_vtt_time(segment["start"])
                end_time = self._seconds_to_vtt_time(segment["end"])
                text = segment["text"].strip()
                
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")
        
        logger.info(f"VTT file generated: {output_path}")
        return output_path
    
    async def _generate_txt(self, text: str) -> str:
        """Generate plain text file"""
        output_path = os.path.join(self.temp_dir, f"transcript_{uuid.uuid4().hex}.txt")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        logger.info(f"TXT file generated: {output_path}")
        return output_path
    
    async def _generate_json(self, result: Dict) -> str:
        """Generate JSON transcript file"""
        output_path = os.path.join(self.temp_dir, f"transcript_{uuid.uuid4().hex}.json")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        logger.info(f"JSON file generated: {output_path}")
        return output_path
    
    def _seconds_to_srt_time(self, seconds: float) -> str:
        """Convert seconds to SRT time format (HH:MM:SS,mmm)"""
        td = timedelta(seconds=seconds)
        total_seconds = int(td.total_seconds())
        milliseconds = int((seconds - total_seconds) * 1000)
        
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
    
    def _seconds_to_vtt_time(self, seconds: float) -> str:
        """Convert seconds to VTT time format (HH:MM:SS.mmm)"""
        td = timedelta(seconds=seconds)
        total_seconds = int(td.total_seconds())
        milliseconds = int((seconds - total_seconds) * 1000)
        
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds_part = total_seconds % 60
        
        return f"{hours:02d}:{minutes:02d}:{seconds_part:02d}.{milliseconds:03d}"
    
    async def embed_subtitles_in_video(
        self,
        video_path: str,
        subtitle_path: str,
        output_path: Optional[str] = None,
        subtitle_style: Optional[Dict] = None
    ) -> str:
        """Embed subtitles into video"""
        
        if not output_path:
            output_path = os.path.join(self.temp_dir, f"subtitled_{uuid.uuid4().hex}.mp4")
        
        # Default subtitle style
        default_style = {
            "fontsize": 24,
            "fontcolor": "white",
            "bordercolor": "black",
            "borderw": 2,
            "fontname": "Arial"
        }
        
        style = {**default_style, **(subtitle_style or {})}
        
        logger.info(f"Embedding subtitles in video: {video_path}")
        
        try:
            import subprocess
            
            # Build FFmpeg filter for subtitles
            subtitle_filter = (
                f"subtitles={subtitle_path}:"
                f"force_style='Fontname={style['fontname']},"
                f"Fontsize={style['fontsize']},"
                f"PrimaryColour=&H{self._color_to_hex(style['fontcolor'])},"
                f"OutlineColour=&H{self._color_to_hex(style['bordercolor'])},"
                f"BorderStyle=1,Outline={style['borderw']}'"
            )
            
            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-vf", subtitle_filter,
                "-c:a", "copy",
                output_path
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown FFmpeg error"
                raise RuntimeError(f"Subtitle embedding failed: {error_msg}")
            
            logger.info(f"Subtitles embedded successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Subtitle embedding failed: {e}")
            raise
    
    def _color_to_hex(self, color: str) -> str:
        """Convert color name to hex for FFmpeg"""
        color_map = {
            "white": "FFFFFF",
            "black": "000000",
            "red": "FF0000",
            "green": "00FF00",
            "blue": "0000FF",
            "yellow": "FFFF00",
            "cyan": "00FFFF",
            "magenta": "FF00FF"
        }
        
        return color_map.get(color.lower(), "FFFFFF")
    
    async def translate_subtitles(
        self,
        subtitle_path: str,
        target_language: str,
        output_path: Optional[str] = None
    ) -> str:
        """Translate subtitles to target language"""
        
        if not output_path:
            base_name = os.path.splitext(os.path.basename(subtitle_path))[0]
            ext = os.path.splitext(subtitle_path)[1]
            output_path = os.path.join(self.temp_dir, f"{base_name}_{target_language}{ext}")
        
        logger.info(f"Translating subtitles to {target_language}")
        
        try:
            # Read original subtitles
            with open(subtitle_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract text for translation
            texts_to_translate = []
            
            if subtitle_path.endswith('.srt'):
                texts_to_translate = self._extract_srt_texts(content)
            elif subtitle_path.endswith('.vtt'):
                texts_to_translate = self._extract_vtt_texts(content)
            
            # Translate texts (placeholder - in real implementation, use translation API)
            translated_texts = await self._translate_texts(texts_to_translate, target_language)
            
            # Replace texts in subtitle file
            translated_content = self._replace_subtitle_texts(content, texts_to_translate, translated_texts)
            
            # Write translated subtitles
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(translated_content)
            
            logger.info(f"Subtitles translated: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Subtitle translation failed: {e}")
            raise
    
    def _extract_srt_texts(self, content: str) -> List[str]:
        """Extract texts from SRT content"""
        texts = []
        lines = content.strip().split('\n')
        
        i = 0
        while i < len(lines):
            if lines[i].strip().isdigit():  # Subtitle number
                i += 1
                if i < len(lines) and '-->' in lines[i]:  # Timeline
                    i += 1
                    # Collect subtitle text lines
                    text_lines = []
                    while i < len(lines) and lines[i].strip():
                        text_lines.append(lines[i].strip())
                        i += 1
                    if text_lines:
                        texts.append(' '.join(text_lines))
            i += 1
        
        return texts
    
    def _extract_vtt_texts(self, content: str) -> List[str]:
        """Extract texts from VTT content"""
        texts = []
        lines = content.strip().split('\n')
        
        i = 0
        while i < len(lines):
            if '-->' in lines[i]:  # Timeline
                i += 1
                # Collect subtitle text lines
                text_lines = []
                while i < len(lines) and lines[i].strip():
                    text_lines.append(lines[i].strip())
                    i += 1
                if text_lines:
                    texts.append(' '.join(text_lines))
            i += 1
        
        return texts
    
    async def _translate_texts(self, texts: List[str], target_language: str) -> List[str]:
        """Translate list of texts (placeholder implementation)"""
        # Placeholder implementation - in practice, use Google Translate API or similar
        logger.info(f"Translating {len(texts)} texts to {target_language}")
        
        # Simulate translation delay
        await asyncio.sleep(1)
        
        # Return texts with language prefix (placeholder)
        return [f"[{target_language}] {text}" for text in texts]
    
    def _replace_subtitle_texts(self, content: str, original_texts: List[str], translated_texts: List[str]) -> str:
        """Replace original texts with translations in subtitle content"""
        result = content
        
        for original, translated in zip(original_texts, translated_texts):
            result = result.replace(original, translated, 1)
        
        return result
    
    def cleanup(self):
        """Clean up temporary files"""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
            logger.info("Subtitle generator temporary files cleaned up")
        except Exception as e:
            logger.warning(f"Failed to cleanup subtitle generator temp files: {e}")

# Example usage
if __name__ == "__main__":
    async def test_subtitle_generator():
        generator = SubtitleGenerator()
        
        # Test with dummy audio file (replace with actual path)
        audio_path = "test_audio.wav"
        
        if os.path.exists(audio_path):
            try:
                # Transcribe audio
                outputs = await generator.transcribe_audio(
                    audio_path,
                    output_formats=["srt", "vtt", "txt", "json"]
                )
                
                for format_type, file_path in outputs.items():
                    print(f"{format_type.upper()}: {file_path}")
                
                # Test subtitle translation if SRT was generated
                if "srt" in outputs:
                    translated = await generator.translate_subtitles(
                        outputs["srt"],
                        "es"  # Spanish
                    )
                    print(f"Translated SRT: {translated}")
                
            except Exception as e:
                print(f"Subtitle generation test failed: {e}")
        else:
            print("Test audio file not found")
        
        generator.cleanup()
    
    asyncio.run(test_subtitle_generator())
