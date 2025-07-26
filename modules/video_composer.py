#!/usr/bin/env python3
"""
Video Composer Module
=====================

Handles video composition using ffmpeg and moviepy.
"""

import asyncio
import os
import logging
import tempfile
import uuid
from typing import Optional, List, Dict, Any, Tuple
from pathlib import Path
import json

logger = logging.getLogger(__name__)

class VideoComposer:
    """Video composition and editing using ffmpeg and moviepy"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="video_composer_")
        self.ffmpeg_available = self._check_ffmpeg()
        self.moviepy_available = self._check_moviepy()
        
        logger.info(f"Video Composer initialized - FFmpeg: {self.ffmpeg_available}, MoviePy: {self.moviepy_available}")
    
    def _check_ffmpeg(self) -> bool:
        """Check if ffmpeg is available"""
        try:
            import subprocess
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            return False
    
    def _check_moviepy(self) -> bool:
        """Check if moviepy is available"""
        try:
            import moviepy
            return True
        except ImportError:
            return False
    
    async def compose_video(
        self,
        video_path: Optional[str] = None,
        audio_path: Optional[str] = None,
        images: Optional[List[str]] = None,
        text_overlays: Optional[List[Dict]] = None,
        output_path: Optional[str] = None,
        settings: Optional[Dict] = None
    ) -> str:
        """Compose video from various inputs"""
        
        if not output_path:
            output_path = os.path.join(self.temp_dir, f"composed_{uuid.uuid4().hex}.mp4")
        
        settings = settings or self._default_settings()
        
        logger.info("Starting video composition")
        
        try:
            if self.moviepy_available:
                return await self._compose_with_moviepy(
                    video_path, audio_path, images, text_overlays, output_path, settings
                )
            elif self.ffmpeg_available:
                return await self._compose_with_ffmpeg(
                    video_path, audio_path, images, text_overlays, output_path, settings
                )
            else:
                raise RuntimeError("Neither MoviePy nor FFmpeg available for video composition")
                
        except Exception as e:
            logger.error(f"Video composition failed: {e}")
            raise
    
    def _default_settings(self) -> Dict:
        """Default video composition settings"""
        return {
            "resolution": "1920x1080",
            "fps": 25,
            "video_codec": "libx264",
            "audio_codec": "aac",
            "bitrate": "2M",
            "preset": "medium",
            "background_color": "#000000"
        }
    
    async def _compose_with_moviepy(
        self,
        video_path: Optional[str],
        audio_path: Optional[str],
        images: Optional[List[str]],
        text_overlays: Optional[List[Dict]],
        output_path: str,
        settings: Dict
    ) -> str:
        """Compose video using MoviePy"""
        logger.info("Composing video with MoviePy")
        
        try:
            from moviepy.editor import (
                VideoFileClip, AudioFileClip, ImageClip, TextClip,
                CompositeVideoClip, concatenate_videoclips
            )
            
            clips = []
            audio_clips = []
            
            # Parse resolution
            width, height = map(int, settings["resolution"].split("x"))
            duration = 10  # Default duration
            
            # Add video clip
            if video_path and os.path.exists(video_path):
                video_clip = VideoFileClip(video_path)
                clips.append(video_clip)
                duration = video_clip.duration
                logger.info(f"Added video clip: {video_path} ({duration}s)")
            
            # Add image clips
            if images:
                for img_path in images:
                    if os.path.exists(img_path):
                        img_clip = ImageClip(img_path).set_duration(duration).resize((width, height))
                        clips.append(img_clip)
                        logger.info(f"Added image clip: {img_path}")
            
            # If no video/images, create a colored background
            if not clips:
                from moviepy.video.tools.drawing import color_gradient
                background = color_gradient(
                    size=(width, height),
                    p1=(0, height//2), p2=(width, height//2),
                    col1=settings["background_color"], col2=settings["background_color"]
                ).set_duration(duration)
                clips.append(background)
            
            # Add text overlays
            if text_overlays:
                for text_overlay in text_overlays:
                    text_clip = self._create_text_clip(text_overlay, duration, width, height)
                    if text_clip:
                        clips.append(text_clip)
            
            # Compose video
            if len(clips) == 1:
                final_video = clips[0]
            else:
                final_video = CompositeVideoClip(clips, size=(width, height))
            
            # Add audio
            if audio_path and os.path.exists(audio_path):
                audio_clip = AudioFileClip(audio_path)
                final_video = final_video.set_audio(audio_clip)
                logger.info(f"Added audio: {audio_path}")
            
            # Set FPS
            final_video = final_video.set_fps(settings["fps"])
            
            # Write video
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: final_video.write_videofile(
                    output_path,
                    codec=settings["video_codec"],
                    audio_codec=settings["audio_codec"],
                    bitrate=settings["bitrate"],
                    preset=settings["preset"],
                    temp_audiofile=os.path.join(self.temp_dir, "temp_audio.m4a"),
                    remove_temp=True
                )
            )
            
            # Clean up clips
            for clip in clips:
                clip.close()
            if audio_path:
                audio_clip.close()
            final_video.close()
            
            logger.info(f"Video composition completed: {output_path}")
            return output_path
            
        except ImportError as e:
            logger.error(f"MoviePy import error: {e}")
            raise
        except Exception as e:
            logger.error(f"MoviePy composition error: {e}")
            raise
    
    def _create_text_clip(self, text_overlay: Dict, duration: float, width: int, height: int):
        """Create text clip from overlay config"""
        try:
            from moviepy.editor import TextClip
            
            text = text_overlay.get("text", "")
            font_size = text_overlay.get("font_size", 50)
            color = text_overlay.get("color", "white")
            position = text_overlay.get("position", "center")
            start_time = text_overlay.get("start_time", 0)
            end_time = text_overlay.get("end_time", duration)
            
            text_clip = TextClip(
                text,
                fontsize=font_size,
                color=color,
                font="Arial-Bold"
            ).set_position(position).set_start(start_time).set_end(end_time)
            
            return text_clip
            
        except Exception as e:
            logger.error(f"Failed to create text clip: {e}")
            return None
    
    async def _compose_with_ffmpeg(
        self,
        video_path: Optional[str],
        audio_path: Optional[str],
        images: Optional[List[str]],
        text_overlays: Optional[List[Dict]],
        output_path: str,
        settings: Dict
    ) -> str:
        """Compose video using FFmpeg"""
        logger.info("Composing video with FFmpeg")
        
        try:
            import subprocess
            
            cmd = ["ffmpeg", "-y"]
            
            # Input video
            if video_path and os.path.exists(video_path):
                cmd.extend(["-i", video_path])
            
            # Input audio
            if audio_path and os.path.exists(audio_path):
                cmd.extend(["-i", audio_path])
            
            # Input images
            if images:
                for img_path in images:
                    if os.path.exists(img_path):
                        cmd.extend(["-i", img_path])
            
            # Video filters
            filters = []
            
            # If no video input, create from images or solid color
            if not video_path:
                if images:
                    # Create slideshow from images
                    filters.append(f"color=c={settings['background_color']}:size={settings['resolution']}:duration=10")
                else:
                    # Create solid color background
                    filters.append(f"color=c={settings['background_color']}:size={settings['resolution']}:duration=10")
            
            # Add text overlays
            if text_overlays:
                for i, text_overlay in enumerate(text_overlays):
                    text = text_overlay.get("text", "")
                    font_size = text_overlay.get("font_size", 50)
                    position = text_overlay.get("position", "center")
                    
                    # Convert position to x,y coordinates
                    if position == "center":
                        x, y = "(w-text_w)/2", "(h-text_h)/2"
                    elif position == "top":
                        x, y = "(w-text_w)/2", "50"
                    elif position == "bottom":
                        x, y = "(w-text_w)/2", "h-text_h-50"
                    else:
                        x, y = "50", "50"
                    
                    filter_text = f"drawtext=text='{text}':fontsize={font_size}:fontcolor=white:x={x}:y={y}"
                    filters.append(filter_text)
            
            # Apply filters
            if filters:
                cmd.extend(["-vf", ",".join(filters)])
            
            # Output settings
            cmd.extend([
                "-c:v", settings["video_codec"],
                "-preset", settings["preset"],
                "-b:v", settings["bitrate"],
                "-r", str(settings["fps"])
            ])
            
            if audio_path:
                cmd.extend(["-c:a", settings["audio_codec"]])
            
            cmd.append(output_path)
            
            # Run FFmpeg
            logger.info(f"Running FFmpeg command: {' '.join(cmd)}")
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown FFmpeg error"
                raise RuntimeError(f"FFmpeg failed: {error_msg}")
            
            logger.info(f"FFmpeg composition completed: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"FFmpeg composition error: {e}")
            raise
    
    async def add_watermark(
        self,
        video_path: str,
        watermark_path: str,
        output_path: Optional[str] = None,
        position: str = "bottom-right",
        opacity: float = 0.5
    ) -> str:
        """Add watermark to video"""
        
        if not output_path:
            output_path = os.path.join(self.temp_dir, f"watermarked_{uuid.uuid4().hex}.mp4")
        
        logger.info(f"Adding watermark to video: {video_path}")
        
        try:
            if self.moviepy_available:
                from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
                
                video = VideoFileClip(video_path)
                watermark = ImageClip(watermark_path).set_duration(video.duration).set_opacity(opacity)
                
                # Set watermark position
                if position == "bottom-right":
                    watermark = watermark.set_position(("right", "bottom"))
                elif position == "bottom-left":
                    watermark = watermark.set_position(("left", "bottom"))
                elif position == "top-right":
                    watermark = watermark.set_position(("right", "top"))
                elif position == "top-left":
                    watermark = watermark.set_position(("left", "top"))
                else:
                    watermark = watermark.set_position("center")
                
                final_video = CompositeVideoClip([video, watermark])
                
                await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: final_video.write_videofile(
                        output_path,
                        temp_audiofile=os.path.join(self.temp_dir, "temp_audio.m4a"),
                        remove_temp=True
                    )
                )
                
                video.close()
                watermark.close()
                final_video.close()
                
            elif self.ffmpeg_available:
                import subprocess
                
                # Position mapping for FFmpeg
                pos_map = {
                    "bottom-right": "main_w-overlay_w-10:main_h-overlay_h-10",
                    "bottom-left": "10:main_h-overlay_h-10",
                    "top-right": "main_w-overlay_w-10:10",
                    "top-left": "10:10",
                    "center": "(main_w-overlay_w)/2:(main_h-overlay_h)/2"
                }
                
                pos = pos_map.get(position, pos_map["bottom-right"])
                
                cmd = [
                    "ffmpeg", "-y",
                    "-i", video_path,
                    "-i", watermark_path,
                    "-filter_complex", f"[1:v]format=rgba,colorchannelmixer=aa={opacity}[wm];[0:v][wm]overlay={pos}",
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
                    raise RuntimeError(f"Watermark addition failed: {error_msg}")
            
            else:
                raise RuntimeError("No video processing tools available")
            
            logger.info(f"Watermark added successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Watermark addition failed: {e}")
            raise
    
    async def resize_video(
        self,
        video_path: str,
        resolution: str,
        output_path: Optional[str] = None
    ) -> str:
        """Resize video to specified resolution"""
        
        if not output_path:
            output_path = os.path.join(self.temp_dir, f"resized_{uuid.uuid4().hex}.mp4")
        
        logger.info(f"Resizing video to {resolution}: {video_path}")
        
        try:
            if self.ffmpeg_available:
                import subprocess
                
                cmd = [
                    "ffmpeg", "-y",
                    "-i", video_path,
                    "-vf", f"scale={resolution}",
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
                    raise RuntimeError(f"Video resize failed: {error_msg}")
                
            elif self.moviepy_available:
                from moviepy.editor import VideoFileClip
                
                width, height = map(int, resolution.split("x"))
                video = VideoFileClip(video_path)
                resized_video = video.resize((width, height))
                
                await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: resized_video.write_videofile(
                        output_path,
                        temp_audiofile=os.path.join(self.temp_dir, "temp_audio.m4a"),
                        remove_temp=True
                    )
                )
                
                video.close()
                resized_video.close()
            
            else:
                raise RuntimeError("No video processing tools available")
            
            logger.info(f"Video resized successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Video resize failed: {e}")
            raise
    
    def cleanup(self):
        """Clean up temporary files"""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
            logger.info("Video composer temporary files cleaned up")
        except Exception as e:
            logger.warning(f"Failed to cleanup video composer temp files: {e}")

# Example usage
if __name__ == "__main__":
    async def test_composer():
        composer = VideoComposer()
        
        # Test video composition
        text_overlays = [
            {
                "text": "Hello World!",
                "font_size": 60,
                "color": "white",
                "position": "center",
                "start_time": 0,
                "end_time": 5
            }
        ]
        
        try:
            output = await composer.compose_video(
                text_overlays=text_overlays,
                settings={"resolution": "1280x720", "fps": 30}
            )
            print(f"Video composed: {output}")
        except Exception as e:
            print(f"Composition failed: {e}")
        
        composer.cleanup()
    
    asyncio.run(test_composer())
