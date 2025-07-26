#!/usr/bin/env python3
"""
Freesound Integration Module
===========================

Handles integration with Freesound.org for free music and sound effects.
Provides volume balancing, looping, trimming using pydub/ffmpeg.
"""

import asyncio
import os
import logging
import tempfile
import uuid
from typing import Optional, List, Dict, Any, Tuple
from pathlib import Path
import json
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

class FreesoundIntegrator:
    """Freesound.org API integration for free music and SFX"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("FREESOUND_API_KEY")
        self.base_url = "https://freesound.org/apiv2"
        self.temp_dir = tempfile.mkdtemp(prefix="freesound_")
        self.session = requests.Session()
        
        # Check if dependencies are available
        self.freesound_available = self._check_freesound()
        self.pydub_available = self._check_pydub()
        
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Token {self.api_key}'
            })
            logger.info("Freesound API initialized with authentication")
        else:
            logger.warning("No Freesound API key provided. Some features may be limited.")
        
        logger.info(f"Freesound Integrator initialized - API: {bool(self.api_key)}, PyDub: {self.pydub_available}")
    
    def _check_freesound(self) -> bool:
        """Check if freesound-python is available"""
        try:
            import freesound
            return True
        except ImportError:
            return False
    
    def _check_pydub(self) -> bool:
        """Check if pydub is available"""
        try:
            import pydub
            return True
        except ImportError:
            return False
    
    async def search_sounds(
        self,
        query: str,
        filter_params: Optional[Dict] = None,
        sort_by: str = "score",
        limit: int = 20
    ) -> List[Dict]:
        """Search for sounds on Freesound.org"""
        
        logger.info(f"Searching Freesound for: {query}")
        
        try:
            params = {
                'query': query,
                'sort': sort_by,
                'page_size': limit,
                'fields': 'id,name,description,username,duration,filesize,bitrate,samplerate,channels,tags,license,download,previews'
            }
            
            # Add filter parameters
            if filter_params:
                params.update(filter_params)
            
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.session.get(f"{self.base_url}/search/text/", params=params)
            )
            
            if response.status_code == 200:
                data = response.json()
                sounds = data.get('results', [])
                
                logger.info(f"Found {len(sounds)} sounds for query: {query}")
                return sounds
            else:
                logger.error(f"Freesound search failed: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Freesound search error: {e}")
            return []
    
    async def search_music(
        self,
        genre: Optional[str] = None,
        mood: Optional[str] = None,
        duration_min: Optional[int] = None,
        duration_max: Optional[int] = None,
        limit: int = 20
    ) -> List[Dict]:
        """Search for music tracks on Freesound.org"""
        
        # Build search query
        query_parts = ["music"]
        
        if genre:
            query_parts.append(genre)
        if mood:
            query_parts.append(mood)
        
        query = " ".join(query_parts)
        
        # Build filter parameters
        filter_params = {
            'filter': 'tag:music'
        }
        
        if duration_min or duration_max:
            duration_filter = []
            if duration_min:
                duration_filter.append(f"duration:[{duration_min} TO *]")
            if duration_max:
                duration_filter.append(f"duration:[* TO {duration_max}]")
            
            if duration_filter:
                filter_params['filter'] += f" {' '.join(duration_filter)}"
        
        return await self.search_sounds(query, filter_params, limit=limit)
    
    async def search_sfx(
        self,
        category: str,
        tags: Optional[List[str]] = None,
        limit: int = 20
    ) -> List[Dict]:
        """Search for sound effects on Freesound.org"""
        
        query_parts = [category]
        
        if tags:
            query_parts.extend(tags)
        
        query = " ".join(query_parts)
        
        # Filter for sound effects
        filter_params = {
            'filter': f'tag:{category}'
        }
        
        if tags:
            for tag in tags:
                filter_params['filter'] += f' tag:{tag}'
        
        return await self.search_sounds(query, filter_params, limit=limit)
    
    async def download_sound(
        self,
        sound_id: int,
        output_path: Optional[str] = None,
        quality: str = "hq"
    ) -> str:
        """Download a sound from Freesound.org"""
        
        if not self.api_key:
            raise ValueError("API key required for downloading sounds")
        
        if not output_path:
            output_path = os.path.join(self.temp_dir, f"freesound_{sound_id}.wav")
        
        logger.info(f"Downloading sound {sound_id} from Freesound")
        
        try:
            # Get sound details first
            sound_info = await self._get_sound_info(sound_id)
            
            if not sound_info:
                raise ValueError(f"Sound {sound_id} not found")
            
            # Get download URL
            download_url = sound_info.get('download')
            if not download_url:
                raise ValueError(f"No download URL available for sound {sound_id}")
            
            # Download the file
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.session.get(download_url, stream=True)
            )
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                logger.info(f"Sound downloaded: {output_path}")
                return output_path
            else:
                raise Exception(f"Download failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Sound download failed: {e}")
            raise
    
    async def _get_sound_info(self, sound_id: int) -> Optional[Dict]:
        """Get detailed information about a sound"""
        
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.session.get(f"{self.base_url}/sounds/{sound_id}/")
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get sound info: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting sound info: {e}")
            return None
    
    async def mix_with_voice(
        self,
        voice_path: str,
        music_path: str,
        output_path: Optional[str] = None,
        music_volume: float = 0.3,
        voice_volume: float = 1.0,
        fade_in_duration: int = 2000,
        fade_out_duration: int = 2000
    ) -> str:
        """Mix music with voice using pydub with volume balancing"""
        
        if not self.pydub_available:
            raise RuntimeError("PyDub not available for audio mixing")
        
        if not output_path:
            output_path = os.path.join(self.temp_dir, f"mixed_{uuid.uuid4().hex}.wav")
        
        logger.info("Mixing music with voice using pydub")
        
        try:
            from pydub import AudioSegment
            import math
            
            # Load audio files
            voice = AudioSegment.from_file(voice_path)
            music = AudioSegment.from_file(music_path)
            
            # Adjust volumes (convert to dB)
            if voice_volume != 1.0:
                voice_gain = 20 * math.log10(voice_volume)
                voice = voice + voice_gain
            
            if music_volume != 1.0:
                music_gain = 20 * math.log10(music_volume)
                music = music + music_gain
            
            # Loop music if it's shorter than voice
            if len(music) < len(voice):
                loops_needed = math.ceil(len(voice) / len(music))
                music = music * loops_needed
            
            # Trim music to voice length
            music = music[:len(voice)]
            
            # Add fade effects to music
            if fade_in_duration > 0:
                music = music.fade_in(fade_in_duration)
            if fade_out_duration > 0:
                music = music.fade_out(fade_out_duration)
            
            # Mix voice and music
            mixed = voice.overlay(music)
            
            # Export result
            mixed.export(output_path, format="wav")
            
            logger.info(f"Audio mixed successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Audio mixing failed: {e}")
            raise
    
    async def loop_audio(
        self,
        audio_path: str,
        target_duration: float,
        output_path: Optional[str] = None,
        fade_overlap: int = 1000
    ) -> str:
        """Loop audio to match target duration with seamless transitions"""
        
        if not self.pydub_available:
            raise RuntimeError("PyDub not available for audio looping")
        
        if not output_path:
            output_path = os.path.join(self.temp_dir, f"looped_{uuid.uuid4().hex}.wav")
        
        logger.info(f"Looping audio to {target_duration}s duration")
        
        try:
            from pydub import AudioSegment
            import math
            
            # Load audio
            audio = AudioSegment.from_file(audio_path)
            target_duration_ms = int(target_duration * 1000)
            
            if len(audio) >= target_duration_ms:
                # Trim if longer than target
                looped = audio[:target_duration_ms]
            else:
                # Loop if shorter than target
                loops_needed = math.ceil(target_duration_ms / len(audio))
                looped = audio * loops_needed
                
                # Trim to exact target duration
                looped = looped[:target_duration_ms]
                
                # Add crossfade for seamless looping
                if fade_overlap > 0 and loops_needed > 1:
                    # Create seamless loop with crossfade
                    loop_segments = []
                    remaining_duration = target_duration_ms
                    
                    while remaining_duration > 0:
                        if remaining_duration >= len(audio):
                            loop_segments.append(audio)
                            remaining_duration -= len(audio)
                        else:
                            loop_segments.append(audio[:remaining_duration])
                            remaining_duration = 0
                    
                    # Crossfade segments
                    if len(loop_segments) > 1:
                        result = loop_segments[0]
                        for segment in loop_segments[1:]:
                            result = result.append(segment, crossfade=fade_overlap)
                        looped = result
            
            # Export looped audio
            looped.export(output_path, format="wav")
            
            logger.info(f"Audio looped successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Audio looping failed: {e}")
            raise
    
    async def trim_audio(
        self,
        audio_path: str,
        start_time: float,
        end_time: float,
        output_path: Optional[str] = None,
        fade_in: int = 500,
        fade_out: int = 500
    ) -> str:
        """Trim audio with optional fade in/out"""
        
        if not self.pydub_available:
            raise RuntimeError("PyDub not available for audio trimming")
        
        if not output_path:
            output_path = os.path.join(self.temp_dir, f"trimmed_{uuid.uuid4().hex}.wav")
        
        logger.info(f"Trimming audio from {start_time}s to {end_time}s")
        
        try:
            from pydub import AudioSegment
            
            # Load audio
            audio = AudioSegment.from_file(audio_path)
            
            # Convert times to milliseconds
            start_ms = int(start_time * 1000)
            end_ms = int(end_time * 1000)
            
            # Trim audio
            trimmed = audio[start_ms:end_ms]
            
            # Add fades
            if fade_in > 0:
                trimmed = trimmed.fade_in(fade_in)
            if fade_out > 0:
                trimmed = trimmed.fade_out(fade_out)
            
            # Export trimmed audio
            trimmed.export(output_path, format="wav")
            
            logger.info(f"Audio trimmed successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Audio trimming failed: {e}")
            raise
    
    async def balance_volumes(
        self,
        audio_files: List[str],
        target_lufs: float = -23.0,
        output_dir: Optional[str] = None
    ) -> List[str]:
        """Balance volumes across multiple audio files to target LUFS"""
        
        if not self.pydub_available:
            raise RuntimeError("PyDub not available for volume balancing")
        
        if not output_dir:
            output_dir = self.temp_dir
        
        logger.info(f"Balancing volumes for {len(audio_files)} files to {target_lufs} LUFS")
        
        try:
            from pydub import AudioSegment
            import math
            
            balanced_files = []
            
            for audio_path in audio_files:
                # Load audio
                audio = AudioSegment.from_file(audio_path)
                
                # Calculate current RMS (approximation of loudness)
                current_rms = audio.rms
                
                # Calculate target RMS from LUFS (simplified conversion)
                # This is a rough approximation - proper LUFS calculation requires specialized tools
                target_rms = int(10 ** ((target_lufs + 20) / 20) * 32767)
                
                # Calculate gain adjustment
                if current_rms > 0:
                    gain_db = 20 * math.log10(target_rms / current_rms)
                    # Limit gain to prevent clipping
                    gain_db = max(-30, min(gain_db, 30))
                else:
                    gain_db = 0
                
                # Apply gain
                balanced_audio = audio + gain_db
                
                # Generate output filename
                filename = os.path.basename(audio_path)
                name, ext = os.path.splitext(filename)
                output_path = os.path.join(output_dir, f"{name}_balanced{ext}")
                
                # Export balanced audio
                balanced_audio.export(output_path, format="wav")
                balanced_files.append(output_path)
                
                logger.info(f"Balanced {filename}: {gain_db:.2f}dB adjustment")
            
            logger.info(f"Volume balancing completed: {len(balanced_files)} files")
            return balanced_files
            
        except Exception as e:
            logger.error(f"Volume balancing failed: {e}")
            raise
    
    def get_license_info(self, sound_data: Dict) -> Dict[str, Any]:
        """Extract license information from sound data"""
        
        license_info = {
            'license': sound_data.get('license', 'Unknown'),
            'attribution_required': True,  # Default to safe side
            'commercial_use': False,       # Default to safe side
            'attribution_text': '',
            'license_url': ''
        }
        
        license_name = sound_data.get('license', '').lower()
        
        # Common Creative Commons licenses
        if 'cc0' in license_name:
            license_info.update({
                'attribution_required': False,
                'commercial_use': True,
                'attribution_text': 'CC0 - Public Domain'
            })
        elif 'cc by' in license_name:
            license_info.update({
                'attribution_required': True,
                'commercial_use': True,
                'attribution_text': f"'{sound_data.get('name', 'Unknown')}' by {sound_data.get('username', 'Unknown')} (freesound.org)"
            })
        elif 'cc by-nc' in license_name:
            license_info.update({
                'attribution_required': True,
                'commercial_use': False,
                'attribution_text': f"'{sound_data.get('name', 'Unknown')}' by {sound_data.get('username', 'Unknown')} (freesound.org) - Non-Commercial"
            })
        
        return license_info
    
    def cleanup(self):
        """Clean up temporary files"""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
            logger.info("Freesound integrator temporary files cleaned up")
        except Exception as e:
            logger.warning(f"Failed to cleanup freesound temp files: {e}")

# Example usage
if __name__ == "__main__":
    async def test_freesound():
        # Initialize with API key (get from https://freesound.org/apiv2/apply/)
        integrator = FreesoundIntegrator(api_key="your_api_key_here")
        
        try:
            # Search for background music
            music_results = await integrator.search_music(
                genre="ambient",
                mood="calm",
                duration_min=30,
                duration_max=300,
                limit=5
            )
            
            print(f"Found {len(music_results)} music tracks")
            for track in music_results[:3]:
                print(f"- {track['name']} by {track['username']} ({track['duration']:.1f}s)")
                license_info = integrator.get_license_info(track)
                print(f"  License: {license_info['license']}")
            
            # Search for sound effects
            sfx_results = await integrator.search_sfx(
                category="notification",
                tags=["bell", "chime"],
                limit=3
            )
            
            print(f"\nFound {len(sfx_results)} sound effects")
            for sfx in sfx_results:
                print(f"- {sfx['name']} by {sfx['username']}")
            
            # Test audio processing (with dummy files)
            # voice_path = "test_voice.wav"
            # music_path = "test_music.wav"
            # 
            # if os.path.exists(voice_path) and os.path.exists(music_path):
            #     mixed = await integrator.mix_with_voice(
            #         voice_path, music_path,
            #         music_volume=0.3,
            #         fade_in_duration=2000
            #     )
            #     print(f"Mixed audio: {mixed}")
            
        except Exception as e:
            print(f"Test failed: {e}")
        finally:
            integrator.cleanup()
    
    asyncio.run(test_freesound())
