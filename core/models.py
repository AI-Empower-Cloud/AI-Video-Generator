"""
🎨 Canvas Editor Data Models
============================

Core data structures for the canvas-based video editor.
All models are designed to be JSON serializable and type-safe.
"""

import json
import uuid
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from datetime import datetime


@dataclass
class Keyframe:
    """Animation keyframe for element properties"""
    time: float
    property: str
    value: Any
    easing: str = "linear"  # linear, ease-in, ease-out, ease-in-out

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Keyframe':
        """Create from dictionary"""
        return cls(**data)


@dataclass
class Transition:
    """Transition between elements"""
    id: str
    type: str  # fade, slide, zoom, wipe, etc.
    duration: float
    start_time: float
    from_element: str
    to_element: str
    properties: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transition':
        """Create from dictionary"""
        return cls(**data)


@dataclass
class Tag:
    """Tag for organizing and categorizing elements/projects"""
    id: str
    name: str
    color: str
    category: str  # project, element, workflow, template, etc.
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Tag':
        """Create from dictionary"""
        if isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        return cls(**data)


@dataclass
class UseCase:
    """Predefined use case with templates and workflow"""
    id: str
    name: str
    description: str
    category: str  # education, marketing, entertainment, corporate, etc.
    tags: List[str] = field(default_factory=list)
    templates: List[str] = field(default_factory=list)  # Template IDs
    workflow_steps: List[Dict[str, Any]] = field(default_factory=list)
    estimated_time: str = "1-2 hours"
    difficulty: str = "beginner"  # beginner, intermediate, advanced
    assets_needed: List[str] = field(default_factory=list)
    output_specs: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UseCase':
        """Create from dictionary"""
        if isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        return cls(**data)


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
    properties: Dict[str, Any] = field(default_factory=dict)
    keyframes: List[Keyframe] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        data['keyframes'] = [kf.to_dict() for kf in self.keyframes]
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CanvasElement':
        """Create from dictionary"""
        if isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if isinstance(data['updated_at'], str):
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        
        # Convert keyframes
        keyframes = []
        for kf_data in data.get('keyframes', []):
            if isinstance(kf_data, dict):
                keyframes.append(Keyframe.from_dict(kf_data))
        data['keyframes'] = keyframes
        
        return cls(**data)

    def add_keyframe(self, time: float, property: str, value: Any, easing: str = "linear"):
        """Add a keyframe to this element"""
        keyframe = Keyframe(time=time, property=property, value=value, easing=easing)
        self.keyframes.append(keyframe)
        self.updated_at = datetime.now()

    def get_property_at_time(self, property: str, time: float) -> Any:
        """Get the interpolated value of a property at a specific time"""
        relevant_keyframes = [kf for kf in self.keyframes if kf.property == property]
        
        if not relevant_keyframes:
            return self.properties.get(property)
        
        # Sort by time
        relevant_keyframes.sort(key=lambda kf: kf.time)
        
        # Find the keyframes to interpolate between
        before = None
        after = None
        
        for kf in relevant_keyframes:
            if kf.time <= time:
                before = kf
            elif kf.time > time and after is None:
                after = kf
                break
        
        if before is None:
            return relevant_keyframes[0].value
        if after is None:
            return before.value
        
        # Simple linear interpolation for now
        t = (time - before.time) / (after.time - before.time)
        
        # Handle different value types
        if isinstance(before.value, (int, float)) and isinstance(after.value, (int, float)):
            return before.value + (after.value - before.value) * t
        else:
            return before.value if t < 0.5 else after.value


@dataclass
class CanvasProject:
    """Canvas project container"""
    id: str
    name: str
    width: int = 1920
    height: int = 1080
    fps: int = 30
    duration: float = 30.0
    elements: List[CanvasElement] = field(default_factory=list)
    transitions: List[Transition] = field(default_factory=list)
    timeline_zoom: float = 1.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    use_case_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        data['elements'] = [elem.to_dict() for elem in self.elements]
        data['transitions'] = [trans.to_dict() for trans in self.transitions]
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CanvasProject':
        """Create from dictionary"""
        if isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if isinstance(data['updated_at'], str):
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        
        # Convert elements
        elements = []
        for elem_data in data.get('elements', []):
            if isinstance(elem_data, dict):
                elements.append(CanvasElement.from_dict(elem_data))
        data['elements'] = elements
        
        # Convert transitions
        transitions = []
        for trans_data in data.get('transitions', []):
            if isinstance(trans_data, dict):
                transitions.append(Transition.from_dict(trans_data))
        data['transitions'] = transitions
        
        return cls(**data)

    def add_element(self, element: CanvasElement):
        """Add an element to the project"""
        self.elements.append(element)
        self.updated_at = datetime.now()

    def remove_element(self, element_id: str) -> bool:
        """Remove an element from the project"""
        original_count = len(self.elements)
        self.elements = [elem for elem in self.elements if elem.id != element_id]
        
        if len(self.elements) < original_count:
            self.updated_at = datetime.now()
            return True
        return False

    def get_element(self, element_id: str) -> Optional[CanvasElement]:
        """Get an element by ID"""
        return next((elem for elem in self.elements if elem.id == element_id), None)

    def get_elements_by_layer(self, layer: int) -> List[CanvasElement]:
        """Get all elements on a specific layer"""
        return [elem for elem in self.elements if elem.layer == layer]

    def get_elements_at_time(self, time: float) -> List[CanvasElement]:
        """Get all elements visible at a specific time"""
        return [
            elem for elem in self.elements 
            if elem.start_time <= time <= (elem.start_time + elem.duration)
        ]

    def get_timeline_summary(self) -> Dict[str, Any]:
        """Get a summary of the timeline"""
        return {
            "duration": self.duration,
            "fps": self.fps,
            "element_count": len(self.elements),
            "transition_count": len(self.transitions),
            "layers": sorted(list(set(elem.layer for elem in self.elements))),
            "total_elements_by_type": {
                elem_type: len([elem for elem in self.elements if elem.type == elem_type])
                for elem_type in set(elem.type for elem in self.elements)
            }
        }


# Template definitions
CANVAS_TEMPLATES = {
    "social_media_post": {
        "name": "Social Media Post",
        "width": 1080,
        "height": 1080,
        "duration": 15.0,
        "fps": 30,
        "elements": [
            {
                "type": "text",
                "x": 540,
                "y": 200,
                "width": 800,
                "height": 100,
                "properties": {
                    "text": "Your Title Here",
                    "font_size": 48,
                    "color": "#FFFFFF",
                    "text_align": "center"
                }
            }
        ]
    },
    "youtube_intro": {
        "name": "YouTube Intro",
        "width": 1920,
        "height": 1080,
        "duration": 10.0,
        "fps": 30,
        "elements": [
            {
                "type": "text",
                "x": 960,
                "y": 540,
                "width": 1200,
                "height": 120,
                "properties": {
                    "text": "Welcome to My Channel",
                    "font_size": 64,
                    "color": "#FF0000",
                    "text_align": "center"
                }
            }
        ]
    },
    "educational_video": {
        "name": "Educational Video",
        "width": 1920,
        "height": 1080,
        "duration": 300.0,
        "fps": 30,
        "elements": [
            {
                "type": "text",
                "x": 100,
                "y": 100,
                "width": 800,
                "height": 80,
                "properties": {
                    "text": "Lesson Title",
                    "font_size": 36,
                    "color": "#000000"
                }
            }
        ]
    },
    "podcast_intro": {
        "name": "Podcast Intro",
        "width": 1920,
        "height": 1080,
        "duration": 30.0,
        "fps": 30,
        "elements": [
            {
                "type": "text",
                "x": 960,
                "y": 400,
                "width": 1400,
                "height": 120,
                "properties": {
                    "text": "Welcome to Our Podcast",
                    "font_size": 56,
                    "color": "#00FF88",
                    "text_align": "center"
                }
            }
        ]
    }
}


def create_project_from_template(template_name: str, project_name: str) -> CanvasProject:
    """Create a new project from a template"""
    if template_name not in CANVAS_TEMPLATES:
        raise ValueError(f"Template '{template_name}' not found")
    
    template = CANVAS_TEMPLATES[template_name]
    project_id = str(uuid.uuid4())
    
    project = CanvasProject(
        id=project_id,
        name=project_name,
        width=template["width"],
        height=template["height"],
        duration=template["duration"],
        fps=template["fps"]
    )
    
    # Add template elements
    for elem_data in template["elements"]:
        element_id = str(uuid.uuid4())
        element = CanvasElement(
            id=element_id,
            type=elem_data["type"],
            x=elem_data["x"],
            y=elem_data["y"],
            width=elem_data["width"],
            height=elem_data["height"],
            start_time=0.0,
            duration=template["duration"],
            layer=1,
            properties=elem_data["properties"]
        )
        project.add_element(element)
    
    return project
