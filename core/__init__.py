"""
🎯 AI Video Generator Core Module
================================

Core components for the AI Video Generator platform:
- Data models and structures
- Base classes and interfaces
- Utility functions
- Configuration management
"""

__version__ = "1.0.0"
__author__ = "AI Video Generator Team"

# Import models first
from .models import (
    Keyframe,
    Transition, 
    Tag,
    UseCase,
    CanvasElement,
    CanvasProject,
    CANVAS_TEMPLATES,
    create_project_from_template
)

# Then import base classes
from .base import (
    BaseEditor,
    BaseManager,
    JSONStorageMixin,
    TagManager,
    UseCaseManager,
    ProjectManager,
    ValidationMixin,
    ErrorHandler,
    EventEmitter
)

__all__ = [
    # Models
    'Keyframe',
    'Transition', 
    'Tag',
    'UseCase',
    'CanvasElement',
    'CanvasProject',
    'CANVAS_TEMPLATES',
    'create_project_from_template',
    
    # Base classes
    'BaseEditor',
    'BaseManager',
    'JSONStorageMixin',
    'TagManager',
    'UseCaseManager',
    'ProjectManager',
    'ValidationMixin',
    'ErrorHandler',
    'EventEmitter'
]
