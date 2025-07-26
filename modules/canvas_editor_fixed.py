#!/usr/bin/env python3
"""
🎨 CANVAS-LIKE VISUAL VIDEO EDITOR
==================================

Advanced drag-and-drop visual editor for video creation with:
- Timeline-based editing
- Layer management
- Real-time preview
- Asset library integration
- Visual effects and transitions
"""

import json
import uuid
import os
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import asyncio
import logging

logger = logging.getLogger(__name__)

@dataclass
class CanvasElement:
    """Represents an element on the canvas"""
    id: str
    type: str  # 'text', 'image', 'video', 'audio', 'shape', 'effect'
    x: float
    y: float
    width: float
    height: float
    start_time: float  # in seconds
    duration: float    # in seconds
    layer: int
    properties: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

@dataclass
class CanvasProject:
    """Canvas project container"""
    id: str
    name: str
    width: int
    height: int
    fps: int
    duration: float
    elements: List[CanvasElement]
    timeline_zoom: float
    created_at: datetime
    updated_at: datetime

class CanvasEditor:
    """Advanced Canvas-like Video Editor"""
    
    def __init__(self, projects_dir: str = "canvas_projects"):
        self.projects_dir = projects_dir
        self.projects: Dict[str, CanvasProject] = {}
        self.assets_dir = os.path.join(projects_dir, "assets")
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create necessary directories"""
        os.makedirs(self.projects_dir, exist_ok=True)
        os.makedirs(self.assets_dir, exist_ok=True)
        os.makedirs(os.path.join(self.assets_dir, "images"), exist_ok=True)
        os.makedirs(os.path.join(self.assets_dir, "videos"), exist_ok=True)
        os.makedirs(os.path.join(self.assets_dir, "audio"), exist_ok=True)
        os.makedirs(os.path.join(self.assets_dir, "fonts"), exist_ok=True)
    
    def create_project(self, name: str, width: int = 1920, height: int = 1080, 
                      fps: int = 30, duration: float = 30.0) -> CanvasProject:
        """Create a new canvas project"""
        project_id = str(uuid.uuid4())
        now = datetime.now()
        
        project = CanvasProject(
            id=project_id,
            name=name,
            width=width,
            height=height,
            fps=fps,
            duration=duration,
            elements=[],
            timeline_zoom=1.0,
            created_at=now,
            updated_at=now
        )
        
        self.projects[project_id] = project
        self._save_project(project)
        
        logger.info(f"Created new canvas project: {name} ({project_id})")
        return project
    
    def add_element(self, project_id: str, element_type: str, x: float, y: float,
                   width: float, height: float, start_time: float = 0.0,
                   duration: float = 5.0, layer: int = 1, 
                   properties: Dict[str, Any] = None) -> CanvasElement:
        """Add an element to the canvas"""
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        
        element_id = str(uuid.uuid4())
        now = datetime.now()
        
        element = CanvasElement(
            id=element_id,
            type=element_type,
            x=x,
            y=y,
            width=width,
            height=height,
            start_time=start_time,
            duration=duration,
            layer=layer,
            properties=properties or {},
            created_at=now,
            updated_at=now
        )
        
        project = self.projects[project_id]
        project.elements.append(element)
        project.updated_at = now
        self._save_project(project)
        
        logger.info(f"Added {element_type} element to project {project_id}")
        return element
    
    def add_text_element(self, project_id: str, text: str, x: float, y: float,
                        font_size: int = 24, font_family: str = "Arial",
                        color: str = "#FFFFFF", **kwargs) -> CanvasElement:
        """Add a text element with specific properties"""
        properties = {
            "text": text,
            "font_size": font_size,
            "font_family": font_family,
            "color": color,
            "text_align": kwargs.get("text_align", "left"),
            "font_weight": kwargs.get("font_weight", "normal"),
            "text_shadow": kwargs.get("text_shadow", None),
            "animation": kwargs.get("animation", None)
        }
        
        # Auto-calculate dimensions based on text
        estimated_width = len(text) * font_size * 0.6
        estimated_height = font_size * 1.2
        
        return self.add_element(
            project_id=project_id,
            element_type="text",
            x=x,
            y=y,
            width=kwargs.get("width", estimated_width),
            height=kwargs.get("height", estimated_height),
            start_time=kwargs.get("start_time", 0.0),
            duration=kwargs.get("duration", 5.0),
            layer=kwargs.get("layer", 2),
            properties=properties
        )
    
    def add_image_element(self, project_id: str, image_path: str, x: float, y: float,
                         width: float, height: float, **kwargs) -> CanvasElement:
        """Add an image element"""
        properties = {
            "source": image_path,
            "opacity": kwargs.get("opacity", 1.0),
            "rotation": kwargs.get("rotation", 0),
            "scale_x": kwargs.get("scale_x", 1.0),
            "scale_y": kwargs.get("scale_y", 1.0),
            "border_radius": kwargs.get("border_radius", 0),
            "filter": kwargs.get("filter", None),
            "animation": kwargs.get("animation", None)
        }
        
        return self.add_element(
            project_id=project_id,
            element_type="image",
            x=x,
            y=y,
            width=width,
            height=height,
            start_time=kwargs.get("start_time", 0.0),
            duration=kwargs.get("duration", 5.0),
            layer=kwargs.get("layer", 1),
            properties=properties
        )
    
    def add_video_element(self, project_id: str, video_path: str, x: float, y: float,
                         width: float, height: float, **kwargs) -> CanvasElement:
        """Add a video element"""
        properties = {
            "source": video_path,
            "volume": kwargs.get("volume", 1.0),
            "muted": kwargs.get("muted", False),
            "loop": kwargs.get("loop", False),
            "playback_speed": kwargs.get("playback_speed", 1.0),
            "trim_start": kwargs.get("trim_start", 0.0),
            "trim_end": kwargs.get("trim_end", None),
            "filter": kwargs.get("filter", None),
            "animation": kwargs.get("animation", None)
        }
        
        return self.add_element(
            project_id=project_id,
            element_type="video",
            x=x,
            y=y,
            width=width,
            height=height,
            start_time=kwargs.get("start_time", 0.0),
            duration=kwargs.get("duration", 10.0),
            layer=kwargs.get("layer", 1),
            properties=properties
        )
    
    def add_audio_element(self, project_id: str, audio_path: str, **kwargs) -> CanvasElement:
        """Add an audio element (no visual position)"""
        properties = {
            "source": audio_path,
            "volume": kwargs.get("volume", 1.0),
            "loop": kwargs.get("loop", False),
            "fade_in": kwargs.get("fade_in", 0.0),
            "fade_out": kwargs.get("fade_out", 0.0),
            "trim_start": kwargs.get("trim_start", 0.0),
            "trim_end": kwargs.get("trim_end", None),
            "filter": kwargs.get("filter", None)
        }
        
        return self.add_element(
            project_id=project_id,
            element_type="audio",
            x=0,  # Audio elements don't have visual position
            y=0,
            width=0,
            height=0,
            start_time=kwargs.get("start_time", 0.0),
            duration=kwargs.get("duration", 10.0),
            layer=kwargs.get("layer", 0),  # Audio layer
            properties=properties
        )
    
    def update_element(self, project_id: str, element_id: str, 
                      updates: Dict[str, Any]) -> CanvasElement:
        """Update an element's properties"""
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        
        project = self.projects[project_id]
        element = None
        
        for elem in project.elements:
            if elem.id == element_id:
                element = elem
                break
        
        if not element:
            raise ValueError(f"Element {element_id} not found")
        
        # Update basic properties
        for key, value in updates.items():
            if hasattr(element, key):
                setattr(element, key, value)
            elif key == "properties":
                element.properties.update(value)
        
        element.updated_at = datetime.now()
        project.updated_at = datetime.now()
        self._save_project(project)
        
        return element
    
    def delete_element(self, project_id: str, element_id: str) -> bool:
        """Delete an element from the canvas"""
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        
        project = self.projects[project_id]
        original_count = len(project.elements)
        
        project.elements = [elem for elem in project.elements if elem.id != element_id]
        
        if len(project.elements) < original_count:
            project.updated_at = datetime.now()
            self._save_project(project)
            logger.info(f"Deleted element {element_id} from project {project_id}")
            return True
        
        return False
    
    def get_project_timeline(self, project_id: str) -> Dict[str, Any]:
        """Get timeline representation of the project"""
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        
        project = self.projects[project_id]
        
        # Organize elements by timeline
        timeline = {
            "duration": project.duration,
            "fps": project.fps,
            "tracks": {}
        }
        
        # Group elements by layer (track)
        for element in project.elements:
            layer = element.layer
            if layer not in timeline["tracks"]:
                timeline["tracks"][layer] = {
                    "layer": layer,
                    "elements": []
                }
            
            timeline["tracks"][layer]["elements"].append({
                "id": element.id,
                "type": element.type,
                "start": element.start_time,
                "duration": element.duration,
                "end": element.start_time + element.duration,
                "properties": element.properties
            })
        
        # Sort tracks by layer number
        timeline["tracks"] = dict(sorted(timeline["tracks"].items()))
        
        return timeline
    
    def export_project_data(self, project_id: str) -> Dict[str, Any]:
        """Export project as JSON data"""
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        
        project = self.projects[project_id]
        
        return {
            "project": asdict(project),
            "timeline": self.get_project_timeline(project_id),
            "export_timestamp": datetime.now().isoformat()
        }
    
    def _save_project(self, project: CanvasProject):
        """Save project to disk"""
        project_file = os.path.join(self.projects_dir, f"{project.id}.json")
        
        # Convert project to dict for JSON serialization
        project_data = asdict(project)
        
        # Handle datetime serialization
        project_data["created_at"] = project.created_at.isoformat()
        project_data["updated_at"] = project.updated_at.isoformat()
        
        for element in project_data["elements"]:
            element["created_at"] = element["created_at"]
            element["updated_at"] = element["updated_at"]
        
        with open(project_file, 'w') as f:
            json.dump(project_data, f, indent=2)
    
    def load_project(self, project_id: str) -> Optional[CanvasProject]:
        """Load project from disk"""
        project_file = os.path.join(self.projects_dir, f"{project_id}.json")
        
        if not os.path.exists(project_file):
            return None
        
        try:
            with open(project_file, 'r') as f:
                data = json.load(f)
            
            # Parse datetime fields
            data["created_at"] = datetime.fromisoformat(data["created_at"])
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
            
            for element_data in data["elements"]:
                element_data["created_at"] = datetime.fromisoformat(element_data["created_at"])
                element_data["updated_at"] = datetime.fromisoformat(element_data["updated_at"])
            
            # Convert elements to CanvasElement objects
            elements = [CanvasElement(**elem) for elem in data["elements"]]
            data["elements"] = elements
            
            project = CanvasProject(**data)
            self.projects[project_id] = project
            
            return project
            
        except Exception as e:
            logger.error(f"Failed to load project {project_id}: {e}")
            return None
    
    def list_projects(self) -> List[Dict[str, Any]]:
        """List all available projects"""
        projects = []
        
        # Load projects from disk if not in memory
        if os.path.exists(self.projects_dir):
            for filename in os.listdir(self.projects_dir):
                if filename.endswith('.json'):
                    project_id = filename[:-5]  # Remove .json extension
                    if project_id not in self.projects:
                        self.load_project(project_id)
        
        # Return project summaries
        for project in self.projects.values():
            projects.append({
                "id": project.id,
                "name": project.name,
                "width": project.width,
                "height": project.height,
                "duration": project.duration,
                "element_count": len(project.elements),
                "created_at": project.created_at.isoformat(),
                "updated_at": project.updated_at.isoformat()
            })
        
        return sorted(projects, key=lambda x: x["updated_at"], reverse=True)

# Example usage and templates
CANVAS_TEMPLATES = {
    "social_media_post": {
        "name": "Social Media Post",
        "width": 1080,
        "height": 1080,
        "duration": 15.0,
        "elements": [
            {
                "type": "text",
                "text": "Your Title Here",
                "x": 540,
                "y": 200,
                "font_size": 48,
                "color": "#FFFFFF",
                "text_align": "center"
            }
        ]
    },
    "youtube_intro": {
        "name": "YouTube Intro",
        "width": 1920,
        "height": 1080,
        "duration": 10.0,
        "elements": [
            {
                "type": "text",
                "text": "Welcome to My Channel",
                "x": 960,
                "y": 540,
                "font_size": 64,
                "color": "#FF0000",
                "text_align": "center"
            }
        ]
    },
    "educational_video": {
        "name": "Educational Video",
        "width": 1920,
        "height": 1080,
        "duration": 300.0,
        "elements": [
            {
                "type": "text",
                "text": "Lesson Title",
                "x": 100,
                "y": 100,
                "font_size": 36,
                "color": "#000000"
            }
        ]
    }
}

if __name__ == "__main__":
    # Demo usage
    editor = CanvasEditor()
    
    # Create a project
    project = editor.create_project("My First Video", duration=30.0)
    print(f"Created project: {project.name}")
    
    # Add elements
    title = editor.add_text_element(
        project.id, 
        "Welcome to AI Video Generator!", 
        x=960, y=200, 
        font_size=48, 
        color="#FFFFFF",
        text_align="center"
    )
    
    # Get timeline
    timeline = editor.get_project_timeline(project.id)
    print(f"Timeline tracks: {list(timeline['tracks'].keys())}")
