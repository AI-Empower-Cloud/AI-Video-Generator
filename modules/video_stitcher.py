#!/usr/bin/env python3
"""
🎬 AUTOMATED VIDEO STITCHING PIPELINE
====================================

User-friendly automated system for combining different media elements:
- Voice audio (TTS engines)
- Lip-synced video (Wav2Lip)
- Visuals/Images (Stable Diffusion)
- Background music
- Subtitles (Whisper)
- Scene clips
- Watermarks and transitions

Tools: moviepy, ffmpeg, pydub, Whisper, OpenCV
"""

import os
import json
import logging
import subprocess
from typing import Dict, List, Optional, Any, Tuple, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import asyncio
from pathlib import Path

# Third-party imports
try:
    from moviepy.editor import (
        VideoFileClip, AudioFileClip, ImageClip, TextClip, CompositeVideoClip,
        concatenate_videoclips, concatenate_audioclips, ColorClip,
        CompositeAudioClip
    )
    from moviepy.video import fx as vfx
    from moviepy.audio import fx as afx
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False

try:
    from pydub import AudioSegment
    from pydub.effects import normalize, compress_dynamic_range
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

logger = logging.getLogger(__name__)

@dataclass
class MediaAsset:
    """Represents a media asset in the stitching pipeline"""
    id: str
    type: str  # 'voice', 'video', 'image', 'music', 'subtitle', 'scene'
    file_path: str
    start_time: float = 0.0
    duration: Optional[float] = None
    volume: float = 1.0
    fade_in: float = 0.0
    fade_out: float = 0.0
    position: Tuple[int, int] = (0, 0)  # For images/videos
    size: Optional[Tuple[int, int]] = None  # For resizing
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Scene:
    """Represents a scene in the video"""
    id: str
    name: str
    script_text: str
    voice_file: Optional[str] = None
    lip_sync_video: Optional[str] = None
    background_images: List[str] = field(default_factory=list)
    duration: Optional[float] = None
    transitions: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class StitchingProject:
    """Complete stitching project configuration"""
    id: str
    name: str
    output_path: str
    resolution: Tuple[int, int] = (1920, 1080)
    fps: int = 30
    background_music: Optional[str] = None
    music_volume: float = 0.3
    subtitle_file: Optional[str] = None
    watermark: Optional[str] = None
    scenes: List[Scene] = field(default_factory=list)
    assets: List[MediaAsset] = field(default_factory=list)
    global_settings: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

class VideoStitcher:
    """Advanced automated video stitching system"""
    
    def __init__(self, workspace_dir: str = "video_stitching"):
        self.workspace_dir = Path(workspace_dir)
        self.temp_dir = self.workspace_dir / "temp"
        self.output_dir = self.workspace_dir / "output"
        self.assets_dir = self.workspace_dir / "assets"
        
        self._ensure_directories()
        self._check_dependencies()
        
        # Whisper model for subtitle generation
        self.whisper_model = None
    
    def _ensure_directories(self):
        """Create necessary directories"""
        for dir_path in [self.workspace_dir, self.temp_dir, self.output_dir, self.assets_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
            
        # Create subdirectories for different asset types
        for subdir in ['voice', 'video', 'images', 'music', 'subtitles', 'scenes']:
            (self.assets_dir / subdir).mkdir(exist_ok=True)
    
    def _check_dependencies(self):
        """Check and report available dependencies"""
        self.capabilities = {
            'moviepy': MOVIEPY_AVAILABLE,
            'pydub': PYDUB_AVAILABLE,
            'whisper': WHISPER_AVAILABLE,
            'opencv': OPENCV_AVAILABLE,
            'ffmpeg': self._check_ffmpeg()
        }
        
        logger.info("🎬 Video Stitcher Capabilities:")
        for dep, available in self.capabilities.items():
            status = "✅ Available" if available else "❌ Missing"
            logger.info(f"  {dep}: {status}")
        
        if not any(self.capabilities.values()):
            logger.warning("⚠️  No video processing capabilities available!")
            logger.warning("   Install moviepy, ffmpeg, or other dependencies for full functionality")
    
    def _check_ffmpeg(self) -> bool:
        """Check FFmpeg availability"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
            logger.warning("  ffmpeg: ❌ Missing - some features may not work")
    
    def create_project(self, name: str, resolution: Tuple[int, int] = (1920, 1080), 
                      fps: int = 30) -> StitchingProject:
        """Create a new stitching project"""
        project_id = f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        output_path = str(self.output_dir / f"{name}_{project_id}.mp4")
        
        project = StitchingProject(
            id=project_id,
            name=name,
            output_path=output_path,
            resolution=resolution,
            fps=fps
        )
        
        logger.info(f"Created stitching project: {name} ({project_id})")
        return project
    
    def add_scene(self, project: StitchingProject, scene_name: str, 
                  script_text: str) -> Scene:
        """Add a scene to the project"""
        scene_id = f"scene_{len(project.scenes) + 1:03d}"
        
        scene = Scene(
            id=scene_id,
            name=scene_name,
            script_text=script_text
        )
        
        project.scenes.append(scene)
        logger.info(f"Added scene: {scene_name}")
        return scene
    
    def add_asset(self, project: StitchingProject, asset_type: str, 
                  file_path: str, **kwargs) -> MediaAsset:
        """Add a media asset to the project"""
        asset_id = f"asset_{len(project.assets) + 1:03d}"
        
        asset = MediaAsset(
            id=asset_id,
            type=asset_type,
            file_path=file_path,
            **kwargs
        )
        
        project.assets.append(asset)
        logger.info(f"Added {asset_type} asset: {os.path.basename(file_path)}")
        return asset
    
    async def generate_voice_audio(self, text: str, output_path: str, 
                                 voice_engine: str = "tts") -> str:
        """Generate voice audio from text using TTS"""
        try:
            if voice_engine == "tts":
                # Using system TTS (basic fallback)
                cmd = [
                    "espeak", "-s", "150", "-a", "50", 
                    "-w", output_path, text
                ]
                
                process = await asyncio.create_subprocess_exec(
                    *cmd, stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                await process.communicate()
                
                if process.returncode == 0 and os.path.exists(output_path):
                    logger.info(f"Generated voice audio: {output_path}")
                    return output_path
            
            # Fallback: Create a silent audio file
            logger.warning("TTS engine not available, creating silent audio")
            return self._create_silent_audio(len(text) * 0.1, output_path)
            
        except Exception as e:
            logger.error(f"Voice generation failed: {e}")
            return self._create_silent_audio(10.0, output_path)
    
    def _create_silent_audio(self, duration: float, output_path: str) -> str:
        """Create a silent audio file for fallback"""
        try:
            if PYDUB_AVAILABLE:
                silent = AudioSegment.silent(duration=int(duration * 1000))
                silent.export(output_path, format="wav")
                return output_path
        except Exception:
            pass
        
        # FFmpeg fallback
        try:
            cmd = [
                "ffmpeg", "-y", "-f", "lavfi", 
                "-i", f"anullsrc=channel_layout=mono:sample_rate=22050",
                "-t", str(duration), output_path
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return output_path
        except Exception:
            logger.error("Could not create silent audio")
            return ""
    
    async def generate_lip_sync_video(self, face_video: str, audio_file: str, 
                                    output_path: str) -> str:
        """Generate lip-synced video using Wav2Lip (placeholder)"""
        # This is a placeholder for Wav2Lip integration
        # In a real implementation, you would call Wav2Lip here
        
        logger.info("Lip-sync generation (placeholder implementation)")
        
        try:
            # For now, just copy the original face video
            # In real implementation, this would run Wav2Lip
            cmd = ["cp", face_video, output_path]
            process = await asyncio.create_subprocess_exec(*cmd)
            await process.communicate()
            
            if process.returncode == 0:
                logger.info(f"Lip-sync video created: {output_path}")
                return output_path
            
        except Exception as e:
            logger.error(f"Lip-sync generation failed: {e}")
        
        return face_video  # Return original if failed
    
    def generate_subtitles(self, audio_file: str, output_srt: str, 
                          language: str = "en") -> str:
        """Generate subtitles from audio using Whisper"""
        if not WHISPER_AVAILABLE:
            logger.warning("Whisper not available, creating placeholder subtitles")
            return self._create_placeholder_srt(output_srt)
        
        try:
            if self.whisper_model is None:
                logger.info("Loading Whisper model...")
                self.whisper_model = whisper.load_model("base")
            
            logger.info(f"Transcribing audio: {audio_file}")
            result = self.whisper_model.transcribe(audio_file, language=language)
            
            # Write SRT file
            with open(output_srt, 'w', encoding='utf-8') as f:
                segments = result.get('segments', [])
                for i, segment in enumerate(segments, 1):
                    if isinstance(segment, dict):
                        start_time = self._format_srt_time(float(segment.get('start', 0)))
                        end_time = self._format_srt_time(float(segment.get('end', 0)))
                        text = str(segment.get('text', '')).strip()
                    else:
                        # Fallback for unexpected segment format
                        start_time = self._format_srt_time(0.0)
                        end_time = self._format_srt_time(5.0)
                        text = str(segment).strip()
                    
                    f.write(f"{i}\n")
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{text}\n\n")
            
            logger.info(f"Subtitles generated: {output_srt}")
            return output_srt
            
        except Exception as e:
            logger.error(f"Subtitle generation failed: {e}")
            return self._create_placeholder_srt(output_srt)
    
    def _format_srt_time(self, seconds: float) -> str:
        """Format time for SRT subtitle format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"
    
    def _create_placeholder_srt(self, output_path: str) -> str:
        """Create placeholder subtitle file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("1\n00:00:00,000 --> 00:00:05,000\n[Generated Content]\n\n")
        return output_path
    
    def optimize_audio(self, input_path: str, output_path: str, 
                      volume: float = 1.0, normalize: bool = True) -> str:
        """Optimize audio using pydub"""
        if not PYDUB_AVAILABLE:
            logger.warning("pydub not available, copying original audio")
            subprocess.run(["cp", input_path, output_path])
            return output_path
        
        try:
            audio = AudioSegment.from_file(input_path)
            
            # Normalize audio levels
            if normalize:
                audio = audio.normalize()
            
            # Adjust volume
            if volume != 1.0:
                audio = audio + (20 * np.log10(volume))
            
            # Apply compression for better quality
            audio = compress_dynamic_range(audio)
            
            # Export optimized audio
            audio.export(output_path, format="wav")
            logger.info(f"Audio optimized: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Audio optimization failed: {e}")
            subprocess.run(["cp", input_path, output_path])
            return output_path
    
    async def stitch_video(self, project: StitchingProject, 
                          progress_callback: Optional[Callable] = None) -> str:
        """Main stitching function - combines all media elements"""
        if not MOVIEPY_AVAILABLE:
            return await self._stitch_with_ffmpeg(project, progress_callback)
        
        logger.info(f"Starting video stitching for project: {project.name}")
        
        try:
            clips = []
            audio_clips = []
            
            # Process scenes
            for i, scene in enumerate(project.scenes):
                if progress_callback:
                    progress_callback(f"Processing scene {i+1}/{len(project.scenes)}")
                
                scene_clip = await self._process_scene(scene, project)
                if scene_clip:
                    clips.append(scene_clip)
            
            # Process additional assets
            for asset in project.assets:
                if progress_callback:
                    progress_callback(f"Processing asset: {asset.type}")
                
                clip = self._process_asset(asset, project)
                if clip:
                    if asset.type in ['voice', 'music']:
                        audio_clips.append(clip)
                    else:
                        clips.append(clip)
            
            # Combine all video clips
            if clips:
                if progress_callback:
                    progress_callback("Combining video clips...")
                
                final_video = concatenate_videoclips(clips, method="compose")
                
                # Add background music
                if project.background_music and os.path.exists(project.background_music):
                    music = AudioFileClip(project.background_music)
                    music = music.volumex(project.music_volume)
                    
                    # Loop music if shorter than video
                    if music.duration < final_video.duration:
                        music = music.loop(duration=final_video.duration)
                    else:
                        music = music.subclip(0, final_video.duration)
                    
                    # Mix with existing audio
                    if final_video.audio:
                        final_audio = CompositeAudioClip([final_video.audio, music])
                    else:
                        final_audio = music
                    
                    final_video = final_video.set_audio(final_audio)
                
                # Add subtitles
                if project.subtitle_file and os.path.exists(project.subtitle_file):
                    final_video = self._add_subtitles(final_video, project.subtitle_file)
                
                # Add watermark
                if project.watermark and os.path.exists(project.watermark):
                    final_video = self._add_watermark(final_video, project.watermark)
                
                # Export final video
                if progress_callback:
                    progress_callback("Exporting final video...")
                
                final_video.write_videofile(
                    project.output_path,
                    fps=project.fps,
                    codec='libx264',
                    audio_codec='aac',
                    temp_audiofile=str(self.temp_dir / 'temp_audio.m4a'),
                    remove_temp=True,
                    verbose=False,
                    logger=None
                )
                
                # Cleanup
                final_video.close()
                for clip in clips:
                    clip.close()
                
                logger.info(f"Video stitching completed: {project.output_path}")
                return project.output_path
            
        except Exception as e:
            logger.error(f"Video stitching failed: {e}")
            raise
        
        return ""
    
    async def _process_scene(self, scene: Scene, project: StitchingProject):
        """Process a single scene"""
        clips = []
        
        # Add lip-sync video if available
        if scene.lip_sync_video and os.path.exists(scene.lip_sync_video):
            video_clip = VideoFileClip(scene.lip_sync_video)
            clips.append(video_clip)
        
        # Add background images as slides
        for img_path in scene.background_images:
            if os.path.exists(img_path):
                img_clip = ImageClip(img_path)
                img_clip = img_clip.set_duration(5.0)  # Default 5 seconds per image
                img_clip = img_clip.resize(project.resolution)
                clips.append(img_clip)
        
        # Add voice audio
        if scene.voice_file and os.path.exists(scene.voice_file):
            audio_clip = AudioFileClip(scene.voice_file)
            if clips:
                # Set video duration to match audio
                for clip in clips:
                    clip.set_duration(audio_clip.duration)
                clips[0] = clips[0].set_audio(audio_clip)
        
        if clips:
            # Add transitions between elements in scene
            if len(clips) > 1:
                for i, clip in enumerate(clips[1:], 1):
                    clips[i] = clip.fadein(1.0)
                    clips[i-1] = clips[i-1].fadeout(1.0)
            
            return concatenate_videoclips(clips)
        
        return None
    
    def _process_asset(self, asset: MediaAsset, project: StitchingProject):
        """Process a single media asset"""
        if not os.path.exists(asset.file_path):
            logger.warning(f"Asset file not found: {asset.file_path}")
            return None
        
        try:
            if asset.type == 'video':
                clip = VideoFileClip(asset.file_path)
                
                if asset.duration:
                    clip = clip.subclip(0, asset.duration)
                
                if asset.size:
                    clip = clip.resize(asset.size)
                
                if asset.fade_in > 0:
                    clip = clip.fadein(asset.fade_in)
                
                if asset.fade_out > 0:
                    clip = clip.fadeout(asset.fade_out)
                
                return clip
            
            elif asset.type == 'image':
                clip = ImageClip(asset.file_path)
                
                if asset.duration:
                    clip = clip.set_duration(asset.duration)
                
                if asset.size:
                    clip = clip.resize(asset.size)
                
                return clip
            
            elif asset.type in ['voice', 'music']:
                clip = AudioFileClip(asset.file_path)
                
                if asset.volume != 1.0:
                    clip = clip.volumex(asset.volume)
                
                if asset.fade_in > 0:
                    clip = clip.audio_fadein(asset.fade_in)
                
                if asset.fade_out > 0:
                    clip = clip.audio_fadeout(asset.fade_out)
                
                return clip
                
        except Exception as e:
            logger.error(f"Error processing asset {asset.file_path}: {e}")
            return None
    
    def _add_subtitles(self, video_clip, subtitle_file: str):
        """Add subtitles to video"""
        try:
            # Parse SRT file and create text clips
            subtitle_clips = []
            
            with open(subtitle_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple SRT parsing
            entries = content.strip().split('\n\n')
            
            for entry in entries:
                lines = entry.strip().split('\n')
                if len(lines) >= 3:
                    time_line = lines[1]
                    text = ' '.join(lines[2:])
                    
                    # Parse timing
                    start_str, end_str = time_line.split(' --> ')
                    start_time = self._parse_srt_time(start_str)
                    end_time = self._parse_srt_time(end_str)
                    
                    # Create text clip
                    txt_clip = TextClip(
                        text,
                        fontsize=24,
                        color='white',
                        stroke_color='black',
                        stroke_width=2
                    ).set_position(('center', 'bottom')).set_start(start_time).set_duration(end_time - start_time)
                    
                    subtitle_clips.append(txt_clip)
            
            if subtitle_clips:
                return CompositeVideoClip([video_clip] + subtitle_clips)
            
        except Exception as e:
            logger.error(f"Error adding subtitles: {e}")
        
        return video_clip
    
    def _parse_srt_time(self, time_str: str) -> float:
        """Parse SRT time format to seconds"""
        try:
            time_part, ms_part = time_str.split(',')
            h, m, s = map(int, time_part.split(':'))
            ms = int(ms_part)
            return h * 3600 + m * 60 + s + ms / 1000.0
        except:
            return 0.0
    
    def _add_watermark(self, video_clip, watermark_path: str):
        """Add watermark to video"""
        try:
            watermark = ImageClip(watermark_path)
            watermark = watermark.resize(height=50)  # Resize watermark
            watermark = watermark.set_position(('right', 'top')).set_duration(video_clip.duration)
            watermark = watermark.set_opacity(0.7)  # Semi-transparent
            
            return CompositeVideoClip([video_clip, watermark])
            
        except Exception as e:
            logger.error(f"Error adding watermark: {e}")
            return video_clip
    
    async def _stitch_with_ffmpeg(self, project: StitchingProject, 
                                progress_callback: Optional[Callable] = None) -> str:
        """Fallback stitching using FFmpeg when MoviePy is not available"""
        logger.info("Using FFmpeg for video stitching")
        
        try:
            # Create file list for concatenation
            concat_file = self.temp_dir / "concat_list.txt"
            
            with open(concat_file, 'w') as f:
                for scene in project.scenes:
                    if scene.lip_sync_video and os.path.exists(scene.lip_sync_video):
                        f.write(f"file '{os.path.abspath(scene.lip_sync_video)}'\n")
                
                for asset in project.assets:
                    if asset.type == 'video' and os.path.exists(asset.file_path):
                        f.write(f"file '{os.path.abspath(asset.file_path)}'\n")
            
            # Build FFmpeg command
            cmd = [
                'ffmpeg', '-y',
                '-f', 'concat',
                '-safe', '0',
                '-i', str(concat_file),
                '-c', 'copy',
                project.output_path
            ]
            
            if progress_callback:
                progress_callback("Running FFmpeg concatenation...")
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                logger.info(f"FFmpeg stitching completed: {project.output_path}")
                return project.output_path
            else:
                logger.error(f"FFmpeg failed: {stderr.decode()}")
                
        except Exception as e:
            logger.error(f"FFmpeg stitching failed: {e}")
        
        return ""
    
    def create_scene_based_project(self, script: str, scenes_per_chapter: int = 5) -> StitchingProject:
        """Create a project with automatic scene division for long videos"""
        project = self.create_project("Scene-Based Video")
        
        # Split script into sentences
        sentences = script.split('. ')
        
        # Group sentences into scenes
        scenes = []
        current_scene = []
        
        for i, sentence in enumerate(sentences):
            current_scene.append(sentence)
            
            # Create new scene every N sentences or at natural breaks
            if (i + 1) % scenes_per_chapter == 0 or i == len(sentences) - 1:
                scene_text = '. '.join(current_scene)
                scene_name = f"Scene {len(scenes) + 1}"
                
                scene = self.add_scene(project, scene_name, scene_text)
                scenes.append(scene)
                current_scene = []
        
        logger.info(f"Created {len(scenes)} scenes from script")
        return project
    
    async def render_scene_by_scene(self, project: StitchingProject, 
                                  render_individual: bool = True) -> List[str]:
        """Render each scene individually, then combine"""
        scene_videos = []
        
        for i, scene in enumerate(project.scenes):
            logger.info(f"Rendering scene {i+1}/{len(project.scenes)}: {scene.name}")
            
            # Create temporary project for this scene
            scene_project = self.create_project(f"{project.name}_Scene_{i+1}")
            scene_project.scenes = [scene]
            scene_project.resolution = project.resolution
            scene_project.fps = project.fps
            
            # Render individual scene
            scene_output = await self.stitch_video(scene_project)
            
            if scene_output and os.path.exists(scene_output):
                scene_videos.append(scene_output)
                logger.info(f"Scene {i+1} rendered: {scene_output}")
            else:
                logger.error(f"Failed to render scene {i+1}")
        
        # Combine all scene videos
        if scene_videos and not render_individual:
            logger.info("Combining all scenes into final video...")
            
            # Update project with scene videos as assets
            project.assets = []
            for video_path in scene_videos:
                self.add_asset(project, 'video', video_path)
            
            project.scenes = []  # Clear scenes since we're using assets now
            final_video = await self.stitch_video(project)
            
            # Clean up individual scene files
            for video_path in scene_videos:
                try:
                    os.remove(video_path)
                except:
                    pass
            
            return [final_video] if final_video else []
        
        return scene_videos
    
    def save_project(self, project: StitchingProject, file_path: Optional[str] = None) -> str:
        """Save project configuration to JSON"""
        if file_path is None:
            file_path = str(self.workspace_dir / f"{project.id}.json")
        
        # Convert project to dict for JSON serialization
        project_dict = {
            'id': project.id,
            'name': project.name,
            'output_path': project.output_path,
            'resolution': project.resolution,
            'fps': project.fps,
            'background_music': project.background_music,
            'music_volume': project.music_volume,
            'subtitle_file': project.subtitle_file,
            'watermark': project.watermark,
            'scenes': [
                {
                    'id': scene.id,
                    'name': scene.name,
                    'script_text': scene.script_text,
                    'voice_file': scene.voice_file,
                    'lip_sync_video': scene.lip_sync_video,
                    'background_images': scene.background_images,
                    'duration': scene.duration,
                    'transitions': scene.transitions,
                    'metadata': scene.metadata
                }
                for scene in project.scenes
            ],
            'assets': [
                {
                    'id': asset.id,
                    'type': asset.type,
                    'file_path': asset.file_path,
                    'start_time': asset.start_time,
                    'duration': asset.duration,
                    'volume': asset.volume,
                    'fade_in': asset.fade_in,
                    'fade_out': asset.fade_out,
                    'position': asset.position,
                    'size': asset.size,
                    'metadata': asset.metadata
                }
                for asset in project.assets
            ],
            'global_settings': project.global_settings,
            'created_at': project.created_at.isoformat()
        }
        
        with open(file_path, 'w') as f:
            json.dump(project_dict, f, indent=2)
        
        logger.info(f"Project saved: {file_path}")
        return file_path
    
    def load_project(self, file_path: str) -> Optional[StitchingProject]:
        """Load project from JSON file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Reconstruct project object
            project = StitchingProject(
                id=data['id'],
                name=data['name'],
                output_path=data['output_path'],
                resolution=tuple(data['resolution']),
                fps=data['fps'],
                background_music=data.get('background_music'),
                music_volume=data.get('music_volume', 0.3),
                subtitle_file=data.get('subtitle_file'),
                watermark=data.get('watermark'),
                global_settings=data.get('global_settings', {}),
                created_at=datetime.fromisoformat(data['created_at'])
            )
            
            # Reconstruct scenes
            for scene_data in data.get('scenes', []):
                scene = Scene(
                    id=scene_data['id'],
                    name=scene_data['name'],
                    script_text=scene_data['script_text'],
                    voice_file=scene_data.get('voice_file'),
                    lip_sync_video=scene_data.get('lip_sync_video'),
                    background_images=scene_data.get('background_images', []),
                    duration=scene_data.get('duration'),
                    transitions=scene_data.get('transitions', {}),
                    metadata=scene_data.get('metadata', {})
                )
                project.scenes.append(scene)
            
            # Reconstruct assets
            for asset_data in data.get('assets', []):
                asset = MediaAsset(
                    id=asset_data['id'],
                    type=asset_data['type'],
                    file_path=asset_data['file_path'],
                    start_time=asset_data.get('start_time', 0.0),
                    duration=asset_data.get('duration'),
                    volume=asset_data.get('volume', 1.0),
                    fade_in=asset_data.get('fade_in', 0.0),
                    fade_out=asset_data.get('fade_out', 0.0),
                    position=tuple(asset_data.get('position', (0, 0))),
                    size=tuple(asset_data['size']) if asset_data.get('size') else None,
                    metadata=asset_data.get('metadata', {})
                )
                project.assets.append(asset)
            
            logger.info(f"Project loaded: {file_path}")
            return project
            
        except Exception as e:
            logger.error(f"Failed to load project: {e}")
            return None

# Example usage and demo functions
async def demo_simple_stitching():
    """Demo: Simple video stitching"""
    print("🎬 Video Stitching Demo")
    
    stitcher = VideoStitcher()
    
    # Create project
    project = stitcher.create_project("Demo Video", resolution=(1280, 720))
    
    # Add a scene
    scene = stitcher.add_scene(project, "Introduction", 
                              "Welcome to our automated video stitching system!")
    
    # Generate voice audio (placeholder)
    voice_path = str(stitcher.assets_dir / "voice" / "intro.wav")
    await stitcher.generate_voice_audio(scene.script_text, voice_path)
    scene.voice_file = voice_path
    
    # Generate subtitles
    subtitle_path = str(stitcher.assets_dir / "subtitles" / "intro.srt")
    stitcher.generate_subtitles(voice_path, subtitle_path)
    project.subtitle_file = subtitle_path
    
    # Add background music (if available)
    music_files = list(stitcher.assets_dir.glob("music/*.mp3"))
    if music_files:
        project.background_music = str(music_files[0])
    
    # Stitch video
    try:
        def progress(msg):
            print(f"Progress: {msg}")
        
        output_path = await stitcher.stitch_video(project, progress)
        print(f"✅ Video created: {output_path}")
        
        # Save project
        project_file = stitcher.save_project(project)
        print(f"📁 Project saved: {project_file}")
        
    except Exception as e:
        print(f"❌ Stitching failed: {e}")

if __name__ == "__main__":
    import asyncio
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Run demo
    asyncio.run(demo_simple_stitching())
