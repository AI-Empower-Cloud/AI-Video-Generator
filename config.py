#!/usr/bin/env python3
"""
Configuration Management for AI Video Generator
Handles environment variables, settings, and deployment configurations
"""

import os
from dataclasses import dataclass
from typing import Optional
import json

@dataclass
class AppConfig:
    """Application configuration settings."""
    
    # Server Settings
    host: str = "0.0.0.0"
    port: int = 8503
    debug: bool = False
    
    # Video Generation Settings
    max_video_duration: int = 30
    max_video_resolution: tuple = (1920, 1080)
    default_resolution: tuple = (640, 480)
    default_fps: int = 24
    
    # Processing Limits
    max_text_length: int = 10000
    max_file_size_mb: int = 10
    max_concurrent_generations: int = 5
    
    # NLP Settings
    spacy_model: str = "en_core_web_sm"
    emotion_model: str = "j-hartmann/emotion-english-distilroberta-base"
    use_gpu: bool = False
    
    # Storage Settings
    output_directory: str = "./generated_videos"
    temp_directory: str = "./temp"
    cleanup_temp_files: bool = True
    file_retention_hours: int = 24
    
    # Security Settings
    enable_rate_limiting: bool = True
    requests_per_minute: int = 60
    enable_file_scanning: bool = True
    
    @classmethod
    def from_env(cls) -> 'AppConfig':
        """Create configuration from environment variables."""
        
        # Get environment name
        env = os.getenv('APP_ENV', 'development')
        
        return cls(
            # Server Settings
            host=os.getenv('HOST', '0.0.0.0'),
            port=int(os.getenv('PORT', '8503')),
            debug=os.getenv('DEBUG', 'false').lower() == 'true',
            
            # Video Generation Settings
            max_video_duration=int(os.getenv('MAX_VIDEO_DURATION', '30')),
            max_video_resolution=tuple(map(int, os.getenv('MAX_VIDEO_RESOLUTION', '1920x1080').split('x'))),
            default_resolution=tuple(map(int, os.getenv('DEFAULT_RESOLUTION', '640x480').split('x'))),
            default_fps=int(os.getenv('DEFAULT_FPS', '24')),
            
            # Processing Limits
            max_text_length=int(os.getenv('MAX_TEXT_LENGTH', '10000')),
            max_file_size_mb=int(os.getenv('MAX_FILE_SIZE_MB', '10')),
            max_concurrent_generations=int(os.getenv('MAX_CONCURRENT_GENERATIONS', '5')),
            
            # NLP Settings
            spacy_model=os.getenv('SPACY_MODEL', 'en_core_web_sm'),
            emotion_model=os.getenv('EMOTION_MODEL', 'j-hartmann/emotion-english-distilroberta-base'),
            use_gpu=os.getenv('USE_GPU', 'false').lower() == 'true',
            
            # Storage Settings
            output_directory=os.getenv('OUTPUT_DIRECTORY', './generated_videos'),
            temp_directory=os.getenv('TEMP_DIRECTORY', './temp'),
            cleanup_temp_files=os.getenv('CLEANUP_TEMP_FILES', 'true').lower() == 'true',
            file_retention_hours=int(os.getenv('FILE_RETENTION_HOURS', '24')),
            
            # Security Settings
            enable_rate_limiting=os.getenv('ENABLE_RATE_LIMITING', 'true').lower() == 'true',
            requests_per_minute=int(os.getenv('REQUESTS_PER_MINUTE', '60')),
            enable_file_scanning=os.getenv('ENABLE_FILE_SCANNING', 'true').lower() == 'true',
        )
        return cls(
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8503")),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            
            max_video_duration=int(os.getenv("MAX_VIDEO_DURATION", "30")),
            max_video_resolution=tuple(map(int, os.getenv("MAX_RESOLUTION", "1920,1080").split(","))),
            default_resolution=tuple(map(int, os.getenv("DEFAULT_RESOLUTION", "640,480").split(","))),
            default_fps=int(os.getenv("DEFAULT_FPS", "24")),
            
            max_text_length=int(os.getenv("MAX_TEXT_LENGTH", "10000")),
            max_file_size_mb=int(os.getenv("MAX_FILE_SIZE_MB", "10")),
            max_concurrent_generations=int(os.getenv("MAX_CONCURRENT_GENERATIONS", "5")),
            
            spacy_model=os.getenv("SPACY_MODEL", "en_core_web_sm"),
            emotion_model=os.getenv("EMOTION_MODEL", "j-hartmann/emotion-english-distilroberta-base"),
            use_gpu=os.getenv("USE_GPU", "false").lower() == "true",
            
            output_directory=os.getenv("OUTPUT_DIRECTORY", "./generated_videos"),
            temp_directory=os.getenv("TEMP_DIRECTORY", "./temp"),
            cleanup_temp_files=os.getenv("CLEANUP_TEMP_FILES", "true").lower() == "true",
            file_retention_hours=int(os.getenv("FILE_RETENTION_HOURS", "24")),
            
            enable_rate_limiting=os.getenv("ENABLE_RATE_LIMITING", "true").lower() == "true",
            requests_per_minute=int(os.getenv("REQUESTS_PER_MINUTE", "60")),
            enable_file_scanning=os.getenv("ENABLE_FILE_SCANNING", "true").lower() == "true",
        )
    
    def save_to_file(self, filepath: str):
        """Save configuration to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.__dict__, f, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'AppConfig':
        """Load configuration from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls(**data)

# Global configuration instance
config = AppConfig.from_env()

def get_config() -> AppConfig:
    """Get the global configuration instance."""
    return config

def update_config(**kwargs):
    """Update configuration values."""
    global config
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)

# Environment-specific configurations
class DeploymentConfig:
    """Deployment-specific configurations."""
    
    @staticmethod
    def development():
        """Development environment settings."""
        return AppConfig(
            debug=True,
            max_concurrent_generations=2,
            file_retention_hours=1,
            enable_rate_limiting=False
        )
    
    @staticmethod
    def production():
        """Production environment settings."""
        return AppConfig(
            debug=False,
            max_concurrent_generations=10,
            file_retention_hours=24,
            enable_rate_limiting=True,
            enable_file_scanning=True
        )
    
    @staticmethod
    def docker():
        """Docker container settings."""
        return AppConfig(
            host="0.0.0.0",
            port=8503,
            output_directory="/app/generated_videos",
            temp_directory="/app/temp"
        )

if __name__ == "__main__":
    # Print current configuration
    print("🔧 AI Video Generator Configuration")
    print("=" * 50)
    
    config = get_config()
    for key, value in config.__dict__.items():
        print(f"{key}: {value}")
    
    # Save example configurations
    DeploymentConfig.development().save_to_file("config.dev.json")
    DeploymentConfig.production().save_to_file("config.prod.json")
    DeploymentConfig.docker().save_to_file("config.docker.json")
    
    print("\n✅ Configuration files created:")
    print("  • config.dev.json")
    print("  • config.prod.json") 
    print("  • config.docker.json")
