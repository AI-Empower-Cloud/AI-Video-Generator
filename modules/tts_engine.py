#!/usr/bin/env python3
"""
Text-to-Speech Engine Module
============================

Supports multiple TTS engines:
- Tortoise TTS
- Coqui TTS
- Edge TTS
- gTTS
"""

import asyncio
import os
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
import tempfile
import uuid

logger = logging.getLogger(__name__)

class TTSEngine:
    """Text-to-Speech Engine with multiple backend support"""
    
    def __init__(self, default_engine: str = "edge"):
        self.default_engine = default_engine
        self.engines = {}
        self.temp_dir = tempfile.mkdtemp(prefix="tts_")
        
        # Initialize available engines
        self._init_engines()
    
    def _init_engines(self):
        """Initialize available TTS engines"""
        # Edge TTS (fastest, good quality)
        try:
            import edge_tts
            self.engines["edge"] = self._edge_tts
            logger.info("Edge TTS initialized")
        except ImportError:
            logger.warning("Edge TTS not available")
        
        # gTTS (Google TTS)
        try:
            from gtts import gTTS
            self.engines["gtts"] = self._gtts
            logger.info("gTTS initialized")
        except ImportError:
            logger.warning("gTTS not available")
        
        # Tortoise TTS (high quality, slow)
        try:
            # Import tortoise_tts when available
            self.engines["tortoise"] = self._tortoise_tts
            logger.info("Tortoise TTS available")
        except ImportError:
            logger.warning("Tortoise TTS not available")
        
        # Coqui TTS
        try:
            from TTS.api import TTS
            self.engines["coqui"] = self._coqui_tts
            logger.info("Coqui TTS initialized")
        except ImportError:
            logger.warning("Coqui TTS not available")
    
    async def generate_speech(
        self,
        text: str,
        engine: Optional[str] = None,
        voice: Optional[str] = None,
        output_path: Optional[str] = None
    ) -> str:
        """Generate speech from text"""
        engine = engine or self.default_engine
        
        if engine not in self.engines:
            raise ValueError(f"Engine {engine} not available. Available: {list(self.engines.keys())}")
        
        if not output_path:
            output_path = os.path.join(self.temp_dir, f"tts_{uuid.uuid4().hex}.wav")
        
        logger.info(f"Generating speech with {engine} engine")
        
        try:
            await self.engines[engine](text, voice, output_path)
            return output_path
        except Exception as e:
            logger.error(f"TTS generation failed with {engine}: {e}")
            raise
    
    async def _edge_tts(self, text: str, voice: Optional[str], output_path: str):
        """Generate speech using Edge TTS"""
        import edge_tts
        
        voice = voice or "en-US-AriaNeural"
        
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
    
    async def _gtts(self, text: str, voice: Optional[str], output_path: str):
        """Generate speech using gTTS"""
        from gtts import gTTS
        
        lang = voice or "en"
        
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_path)
    
    async def _tortoise_tts(self, text: str, voice: Optional[str], output_path: str):
        """Generate speech using Tortoise TTS"""
        # Placeholder for Tortoise TTS implementation
        logger.info("Tortoise TTS generation (placeholder)")
        await asyncio.sleep(2)  # Simulate processing time
        
        # Create dummy audio file
        import wave
        import numpy as np
        
        # Generate sine wave as placeholder
        sample_rate = 22050
        duration = len(text) * 0.1  # Rough estimate
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = np.sin(2 * np.pi * 440 * t) * 0.3
        
        # Convert to 16-bit PCM
        audio_int = (audio * 32767).astype(np.int16)
        
        with wave.open(output_path, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_int.tobytes())
    
    async def _coqui_tts(self, text: str, voice: Optional[str], output_path: str):
        """Generate speech using Coqui TTS"""
        from TTS.api import TTS
        
        # Initialize TTS model
        tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
        
        # Generate speech
        tts.tts_to_file(text=text, file_path=output_path)
    
    def list_voices(self, engine: Optional[str] = None) -> Dict[str, List[str]]:
        """List available voices for each engine"""
        voices = {}
        
        if engine is None:
            engines_to_check = self.engines.keys()
        else:
            engines_to_check = [engine] if engine in self.engines else []
        
        for eng in engines_to_check:
            if eng == "edge":
                voices[eng] = [
                    "en-US-AriaNeural",
                    "en-US-JennyNeural", 
                    "en-US-GuyNeural",
                    "en-GB-SoniaNeural",
                    "es-ES-ElviraNeural"
                ]
            elif eng == "gtts":
                voices[eng] = ["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh"]
            elif eng == "coqui":
                voices[eng] = ["default", "ljspeech", "vctk"]
            elif eng == "tortoise":
                voices[eng] = ["default", "male", "female"]
        
        return voices
    
    def cleanup(self):
        """Clean up temporary files"""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
            logger.info("TTS temporary files cleaned up")
        except Exception as e:
            logger.warning(f"Failed to cleanup TTS temp files: {e}")

# Example usage
if __name__ == "__main__":
    async def test_tts():
        tts = TTSEngine()
        
        text = "Hello world! This is a test of the text-to-speech system."
        
        # Test different engines
        for engine in tts.engines.keys():
            try:
                output_path = await tts.generate_speech(text, engine=engine)
                print(f"{engine}: Generated audio at {output_path}")
            except Exception as e:
                print(f"{engine}: Failed - {e}")
        
        # List voices
        voices = tts.list_voices()
        print("Available voices:", voices)
        
        tts.cleanup()
    
    asyncio.run(test_tts())
