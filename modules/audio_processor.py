#!/usr/bin/env python3
"""
Audio Processor Module
=====================

Handles audio editing, music integration, and sound processing using pydub and other libraries.
"""

import asyncio
import os
import logging
import tempfile
import uuid
from typing import Optional, List, Dict, Any, Tuple
from pathlib import Path
import numpy as np

logger = logging.getLogger(__name__)

class AudioProcessor:
    """Audio processing and editing using pydub and other libraries"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="audio_processor_")
        self.pydub_available = self._check_pydub()
        self.librosa_available = self._check_librosa()
        
        logger.info(f"Audio Processor initialized - PyDub: {self.pydub_available}, Librosa: {self.librosa_available}")
    
    def _check_pydub(self) -> bool:
        """Check if pydub is available"""
        try:
            import pydub
            return True
        except ImportError:
            return False
    
    def _check_librosa(self) -> bool:
        """Check if librosa is available"""
        try:
            import librosa
            return True
        except ImportError:
            return False
    
    async def process_audio(
        self,
        audio_path: str,
        operations: List[Dict[str, Any]],
        output_path: Optional[str] = None
    ) -> str:
        """Process audio with multiple operations"""
        
        if not output_path:
            output_path = os.path.join(self.temp_dir, f"processed_{uuid.uuid4().hex}.wav")
        
        logger.info(f"Processing audio with {len(operations)} operations")
        
        try:
            if not self.pydub_available:
                raise RuntimeError("PyDub not available for audio processing")
            
            from pydub import AudioSegment
            
            # Load audio
            audio = AudioSegment.from_file(audio_path)
            
            # Apply operations
            for op in operations:
                audio = await self._apply_operation(audio, op)
            
            # Export processed audio
            audio.export(output_path, format="wav")
            
            logger.info(f"Audio processing completed: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Audio processing failed: {e}")
            raise
    
    async def _apply_operation(self, audio, operation: Dict[str, Any]):
        """Apply single audio operation"""
        op_type = operation.get("type")
        
        if op_type == "normalize":
            return await self._normalize_audio(audio, operation)
        elif op_type == "volume":
            return await self._adjust_volume(audio, operation)
        elif op_type == "fade":
            return await self._apply_fade(audio, operation)
        elif op_type == "trim":
            return await self._trim_audio(audio, operation)
        elif op_type == "speed":
            return await self._change_speed(audio, operation)
        elif op_type == "pitch":
            return await self._change_pitch(audio, operation)
        elif op_type == "reverse":
            return await self._reverse_audio(audio, operation)
        elif op_type == "echo":
            return await self._add_echo(audio, operation)
        else:
            logger.warning(f"Unknown operation type: {op_type}")
            return audio
    
    async def _normalize_audio(self, audio, operation: Dict):
        """Normalize audio levels"""
        target_dBFS = operation.get("target_dBFS", -20.0)
        change_in_dBFS = target_dBFS - audio.dBFS
        return audio.apply_gain(change_in_dBFS)
    
    async def _adjust_volume(self, audio, operation: Dict):
        """Adjust audio volume"""
        gain_db = operation.get("gain_db", 0)
        return audio + gain_db
    
    async def _apply_fade(self, audio, operation: Dict):
        """Apply fade in/out effects"""
        fade_type = operation.get("fade_type", "in")
        duration_ms = operation.get("duration_ms", 1000)
        
        if fade_type == "in":
            return audio.fade_in(duration_ms)
        elif fade_type == "out":
            return audio.fade_out(duration_ms)
        elif fade_type == "both":
            return audio.fade_in(duration_ms).fade_out(duration_ms)
        else:
            return audio
    
    async def _trim_audio(self, audio, operation: Dict):
        """Trim audio to specified duration"""
        start_ms = operation.get("start_ms", 0)
        end_ms = operation.get("end_ms", len(audio))
        return audio[start_ms:end_ms]
    
    async def _change_speed(self, audio, operation: Dict):
        """Change audio playback speed"""
        speed_factor = operation.get("speed_factor", 1.0)
        
        # Changing speed affects both pitch and duration
        frame_rate = int(audio.frame_rate * speed_factor)
        return audio._spawn(audio.raw_data, overrides={"frame_rate": frame_rate})
    
    async def _change_pitch(self, audio, operation: Dict):
        """Change audio pitch without affecting speed"""
        semitones = operation.get("semitones", 0)
        
        if semitones == 0:
            return audio
        
        # This is a simplified pitch shift - in practice, you'd use more sophisticated algorithms
        # Using speed change as approximation (not ideal but works)
        pitch_factor = 2 ** (semitones / 12.0)
        frame_rate = int(audio.frame_rate * pitch_factor)
        pitched_audio = audio._spawn(audio.raw_data, overrides={"frame_rate": frame_rate})
        
        # Resample back to original duration
        return pitched_audio.set_frame_rate(audio.frame_rate)
    
    async def _reverse_audio(self, audio, operation: Dict):
        """Reverse audio"""
        return audio.reverse()
    
    async def _add_echo(self, audio, operation: Dict):
        """Add echo effect"""
        delay_ms = operation.get("delay_ms", 500)
        decay_factor = operation.get("decay_factor", 0.6)
        
        # Create echo by overlaying delayed and attenuated audio
        echo = audio - (20 * np.log10(decay_factor))  # Convert to dB
        
        # Add delay
        silence = AudioSegment.silent(duration=delay_ms)
        echo = silence + echo
        
        # Overlay with original
        return audio.overlay(echo)
    
    async def mix_audio(
        self,
        audio_files: List[str],
        volumes: Optional[List[float]] = None,
        output_path: Optional[str] = None
    ) -> str:
        """Mix multiple audio files together"""
        
        if not output_path:
            output_path = os.path.join(self.temp_dir, f"mixed_{uuid.uuid4().hex}.wav")
        
        logger.info(f"Mixing {len(audio_files)} audio files")
        
        try:
            if not self.pydub_available:
                raise RuntimeError("PyDub not available for audio mixing")
            
            from pydub import AudioSegment
            
            if not audio_files:
                raise ValueError("No audio files provided for mixing")
            
            # Load first audio file as base
            mixed_audio = AudioSegment.from_file(audio_files[0])
            
            if volumes and len(volumes) > 0:
                mixed_audio = mixed_audio + (20 * np.log10(volumes[0]))
            
            # Mix in other audio files
            for i, audio_file in enumerate(audio_files[1:], 1):
                audio = AudioSegment.from_file(audio_file)
                
                if volumes and i < len(volumes):
                    audio = audio + (20 * np.log10(volumes[i]))
                
                # Overlay with existing mix
                mixed_audio = mixed_audio.overlay(audio)
            
            # Export mixed audio
            mixed_audio.export(output_path, format="wav")
            
            logger.info(f"Audio mixing completed: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Audio mixing failed: {e}")
            raise
    
    async def add_background_music(
        self,
        speech_path: str,
        music_path: str,
        output_path: Optional[str] = None,
        music_volume: float = 0.3,
        fade_in_duration: int = 2000,
        fade_out_duration: int = 2000
    ) -> str:
        """Add background music to speech audio"""
        
        if not output_path:
            output_path = os.path.join(self.temp_dir, f"with_music_{uuid.uuid4().hex}.wav")
        
        logger.info("Adding background music to speech")
        
        try:
            if not self.pydub_available:
                raise RuntimeError("PyDub not available for background music")
            
            from pydub import AudioSegment
            
            # Load audio files
            speech = AudioSegment.from_file(speech_path)
            music = AudioSegment.from_file(music_path)
            
            # Adjust music volume
            music = music + (20 * np.log10(music_volume))
            
            # Loop music if it's shorter than speech
            if len(music) < len(speech):
                loops_needed = (len(speech) // len(music)) + 1
                music = music * loops_needed
            
            # Trim music to speech length
            music = music[:len(speech)]
            
            # Add fade effects to music
            music = music.fade_in(fade_in_duration).fade_out(fade_out_duration)
            
            # Mix speech and music
            result = speech.overlay(music)
            
            # Export result
            result.export(output_path, format="wav")
            
            logger.info(f"Background music added: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Background music addition failed: {e}")
            raise
    
    async def extract_audio_from_video(
        self,
        video_path: str,
        output_path: Optional[str] = None
    ) -> str:
        """Extract audio from video file"""
        
        if not output_path:
            output_path = os.path.join(self.temp_dir, f"extracted_{uuid.uuid4().hex}.wav")
        
        logger.info(f"Extracting audio from video: {video_path}")
        
        try:
            # Try with pydub first
            if self.pydub_available:
                from pydub import AudioSegment
                audio = AudioSegment.from_file(video_path)
                audio.export(output_path, format="wav")
            else:
                # Fallback to ffmpeg
                import subprocess
                cmd = [
                    "ffmpeg", "-y",
                    "-i", video_path,
                    "-vn",  # No video
                    "-acodec", "pcm_s16le",  # Audio codec
                    "-ar", "44100",  # Sample rate
                    "-ac", "2",  # Channels
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
                    raise RuntimeError(f"Audio extraction failed: {error_msg}")
            
            logger.info(f"Audio extracted: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Audio extraction failed: {e}")
            raise
    
    async def generate_silence(
        self,
        duration_ms: int,
        output_path: Optional[str] = None
    ) -> str:
        """Generate silence audio"""
        
        if not output_path:
            output_path = os.path.join(self.temp_dir, f"silence_{uuid.uuid4().hex}.wav")
        
        logger.info(f"Generating {duration_ms}ms of silence")
        
        try:
            if not self.pydub_available:
                raise RuntimeError("PyDub not available for silence generation")
            
            from pydub import AudioSegment
            
            silence = AudioSegment.silent(duration=duration_ms)
            silence.export(output_path, format="wav")
            
            logger.info(f"Silence generated: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Silence generation failed: {e}")
            raise
    
    def get_audio_info(self, audio_path: str) -> Dict[str, Any]:
        """Get audio file information"""
        try:
            if self.pydub_available:
                from pydub import AudioSegment
                audio = AudioSegment.from_file(audio_path)
                
                return {
                    "duration_ms": len(audio),
                    "frame_rate": audio.frame_rate,
                    "channels": audio.channels,
                    "sample_width": audio.sample_width,
                    "dBFS": audio.dBFS,
                    "max_dBFS": audio.max_dBFS
                }
            else:
                # Fallback using librosa if available
                if self.librosa_available:
                    import librosa
                    y, sr = librosa.load(audio_path)
                    duration = len(y) / sr
                    
                    return {
                        "duration_ms": int(duration * 1000),
                        "frame_rate": sr,
                        "channels": 1 if len(y.shape) == 1 else y.shape[0],
                        "sample_width": 2,  # Assuming 16-bit
                        "dBFS": None,
                        "max_dBFS": None
                    }
                else:
                    return {"error": "No audio processing libraries available"}
                    
        except Exception as e:
            logger.error(f"Failed to get audio info: {e}")
            return {"error": str(e)}
    
    def cleanup(self):
        """Clean up temporary files"""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
            logger.info("Audio processor temporary files cleaned up")
        except Exception as e:
            logger.warning(f"Failed to cleanup audio processor temp files: {e}")

# Example usage
if __name__ == "__main__":
    async def test_audio_processor():
        processor = AudioProcessor()
        
        # Test operations
        operations = [
            {"type": "normalize", "target_dBFS": -20.0},
            {"type": "volume", "gain_db": 5},
            {"type": "fade", "fade_type": "both", "duration_ms": 1000}
        ]
        
        # Generate test silence
        silence_path = await processor.generate_silence(5000)  # 5 seconds
        
        try:
            # Process the silence (just for testing)
            processed = await processor.process_audio(silence_path, operations)
            print(f"Audio processed: {processed}")
            
            # Get audio info
            info = processor.get_audio_info(processed)
            print(f"Audio info: {info}")
            
        except Exception as e:
            print(f"Audio processing test failed: {e}")
        
        processor.cleanup()
    
    asyncio.run(test_audio_processor())
