"""
AI Video Generator Modules
==========================

Modular components for the AI Video Generator:
- TTS Engine (Tortoise, Coqui, XTTS-v2)
- Lip Sync (Wav2Lip)
- Video Composition
- Audio Processing
- Subtitle Generation
- Cloud Storage
- Freesound Integration
- BBC Sound FX Library
- XTTS-v2 Voice Cloning
"""

__version__ = "1.0.0"
__author__ = "AI Video Generator Team"

from .tts_engine import TTSEngine
from .lip_sync import LipSyncProcessor
from .video_composer import VideoComposer
from .audio_processor import AudioProcessor
from .subtitle_generator import SubtitleGenerator
from .cloud_storage import CloudStorage
from .freesound_integrator import FreesoundIntegrator
from .bbc_sound_fx import BBCSoundFXLibrary
from .xtts_v2_cloner import XTTSv2VoiceCloner

__all__ = [
    "TTSEngine",
    "LipSyncProcessor", 
    "VideoComposer",
    "AudioProcessor",
    "SubtitleGenerator",
    "CloudStorage",
    "FreesoundIntegrator",
    "BBCSoundFXLibrary",
    "XTTSv2VoiceCloner"
]
