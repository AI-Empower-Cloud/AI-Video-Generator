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
- Video export and rendering
- Animation keyframes
- Waveform visualization
"""

import json
import uuid
import os
import subprocess
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
import asyncio
import logging

logger = logging.getLogger(__name__)

@dataclass
class Keyframe:
    """Animation keyframe"""
    time: float
    property: str
    value: Any
    easing: str = "linear"  # linear, ease-in, ease-out, ease-in-out

@dataclass
class Transition:
    """Transition between elements"""
    id: str
    type: str  # fade, slide, zoom, wipe, etc.
    duration: float
    start_time: float
    from_element: str
    to_element: str
    properties: Dict[str, Any]

@dataclass
class Tag:
    """Tag for organizing and categorizing elements/projects"""
    id: str
    name: str
    color: str
    category: str  # project, element, workflow, template, etc.
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class UseCase:
    """Predefined use case with templates and workflow"""
    id: str
    name: str
    description: str
    category: str  # education, marketing, entertainment, corporate, etc.
    tags: List[str]
    templates: List[str]  # Template IDs
    workflow_steps: List[Dict[str, Any]]
    estimated_time: str
    difficulty: str  # beginner, intermediate, advanced
    assets_needed: List[str]
    output_specs: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)

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
    keyframes: List[Keyframe]
    created_at: datetime
    updated_at: datetime
    tags: List[str] = field(default_factory=list)  # Added tags

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
    transitions: List[Transition]
    timeline_zoom: float
    created_at: datetime
    updated_at: datetime
    tags: List[str] = field(default_factory=list)  # Added tags
    use_case_id: Optional[str] = None  # Link to use case
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional metadata

class CanvasEditor:
    """Advanced Canvas-like Video Editor"""
    
    def __init__(self, projects_dir: str = "canvas_projects"):
        self.projects_dir = projects_dir
        self.projects: Dict[str, CanvasProject] = {}
        self.assets_dir = os.path.join(projects_dir, "assets")
        self.renders_dir = os.path.join(projects_dir, "renders")
        self.tags: Dict[str, Tag] = {}
        self.use_cases: Dict[str, UseCase] = {}
        self._ensure_directories()
        self._load_tags_and_use_cases()
    
    def _ensure_directories(self):
        """Create necessary directories"""
        os.makedirs(self.projects_dir, exist_ok=True)
        os.makedirs(self.assets_dir, exist_ok=True)
        os.makedirs(self.renders_dir, exist_ok=True)
        os.makedirs(os.path.join(self.assets_dir, "images"), exist_ok=True)
        os.makedirs(os.path.join(self.assets_dir, "videos"), exist_ok=True)
        os.makedirs(os.path.join(self.assets_dir, "audio"), exist_ok=True)
        os.makedirs(os.path.join(self.assets_dir, "fonts"), exist_ok=True)
    
    def _load_tags_and_use_cases(self):
        """Load default tags and use cases"""
        # Load existing tags and use cases from storage if they exist
        tags_file = os.path.join(self.projects_dir, "tags.json")
        use_cases_file = os.path.join(self.projects_dir, "use_cases.json")
        
        if os.path.exists(tags_file):
            try:
                with open(tags_file, 'r') as f:
                    tags_data = json.load(f)
                    for tag_id, tag_dict in tags_data.items():
                        tag_dict['created_at'] = datetime.fromisoformat(tag_dict['created_at'])
                        self.tags[tag_id] = Tag(**tag_dict)
            except Exception as e:
                logger.warning(f"Error loading tags: {e}")
        
        if os.path.exists(use_cases_file):
            try:
                with open(use_cases_file, 'r') as f:
                    use_cases_data = json.load(f)
                    for uc_id, uc_dict in use_cases_data.items():
                        uc_dict['created_at'] = datetime.fromisoformat(uc_dict['created_at'])
                        self.use_cases[uc_id] = UseCase(**uc_dict)
            except Exception as e:
                logger.warning(f"Error loading use cases: {e}")
        
        # Create default tags if none exist
        if not self.tags:
            self._create_default_tags()
        
        # Create default use cases if none exist
        if not self.use_cases:
            self._create_default_use_cases()
    
    def _create_default_tags(self):
        """Create default tags for the system"""
        default_tags = [
            # Content Categories
            {"name": "Educational", "color": "#4CAF50", "category": "content", "description": "Educational and learning content"},
            {"name": "Marketing", "color": "#FF9800", "category": "content", "description": "Marketing and promotional content"},
            {"name": "Entertainment", "color": "#E91E63", "category": "content", "description": "Entertainment and fun content"},
            {"name": "Corporate", "color": "#2196F3", "category": "content", "description": "Corporate and business content"},
            {"name": "Social Media", "color": "#9C27B0", "category": "content", "description": "Social media content"},
            {"name": "News", "color": "#607D8B", "category": "content", "description": "News and current events"},
            
            # Format Types
            {"name": "Short Form", "color": "#FFEB3B", "category": "format", "description": "Short videos under 60 seconds"},
            {"name": "Long Form", "color": "#8BC34A", "category": "format", "description": "Long videos over 5 minutes"},
            {"name": "Tutorial", "color": "#00BCD4", "category": "format", "description": "Step-by-step tutorials"},
            {"name": "Presentation", "color": "#795548", "category": "format", "description": "Presentation format"},
            {"name": "Animation", "color": "#FF5722", "category": "format", "description": "Animated content"},
            
            # Production Stage
            {"name": "Draft", "color": "#9E9E9E", "category": "status", "description": "Work in progress"},
            {"name": "Review", "color": "#FFC107", "category": "status", "description": "Under review"},
            {"name": "Final", "color": "#4CAF50", "category": "status", "description": "Final version"},
            {"name": "Published", "color": "#3F51B5", "category": "status", "description": "Published content"},
            
            # Technical
            {"name": "AI Generated", "color": "#673AB7", "category": "technical", "description": "Content generated using AI"},
            {"name": "High Quality", "color": "#F44336", "category": "technical", "description": "High quality production"},
            {"name": "Mobile Optimized", "color": "#009688", "category": "technical", "description": "Optimized for mobile viewing"},
        ]
        
        for tag_data in default_tags:
            tag_id = str(uuid.uuid4())
            tag = Tag(
                id=tag_id,
                name=tag_data["name"],
                color=tag_data["color"],
                category=tag_data["category"],
                description=tag_data["description"]
            )
            self.tags[tag_id] = tag
        
        self._save_tags()
    
    def _create_default_use_cases(self):
        """Create default use cases for common video scenarios"""
        default_use_cases = [
            {
                "name": "Educational Explainer Video",
                "description": "Create engaging educational content with animations and clear explanations",
                "category": "education",
                "tags": ["Educational", "Tutorial", "Animation"],
                "templates": ["educational_video"],
                "workflow_steps": [
                    {"step": "Script Writing", "description": "Write clear, concise script"},
                    {"step": "Storyboard", "description": "Plan visual elements and transitions"},
                    {"step": "Recording", "description": "Record voiceover and gather assets"},
                    {"step": "Editing", "description": "Assemble video with animations"},
                    {"step": "Review", "description": "Review and refine content"},
                ],
                "estimated_time": "4-6 hours",
                "difficulty": "intermediate",
                "assets_needed": ["Script", "Images", "Audio", "Background Music"],
                "output_specs": {"resolution": "1920x1080", "fps": 30, "format": "MP4"}
            },
            {
                "name": "Social Media Marketing Video",
                "description": "Create engaging short-form content for social media platforms",
                "category": "marketing",
                "tags": ["Marketing", "Social Media", "Short Form"],
                "templates": ["social_media_post"],
                "workflow_steps": [
                    {"step": "Concept", "description": "Define key message and hook"},
                    {"step": "Visual Planning", "description": "Plan eye-catching visuals"},
                    {"step": "Production", "description": "Create or gather content"},
                    {"step": "Editing", "description": "Fast-paced editing with music"},
                    {"step": "Optimization", "description": "Optimize for platform"},
                ],
                "estimated_time": "2-3 hours",
                "difficulty": "beginner",
                "assets_needed": ["Brand Assets", "Music", "Text Overlays"],
                "output_specs": {"resolution": "1080x1920", "fps": 30, "format": "MP4"}
            },
            {
                "name": "Corporate Presentation",
                "description": "Professional presentations for business meetings and conferences",
                "category": "corporate",
                "tags": ["Corporate", "Presentation", "Professional"],
                "templates": ["corporate_presentation"],
                "workflow_steps": [
                    {"step": "Content Structure", "description": "Organize key points and data"},
                    {"step": "Design", "description": "Apply corporate branding"},
                    {"step": "Data Visualization", "description": "Create charts and graphs"},
                    {"step": "Narration", "description": "Add professional voiceover"},
                    {"step": "Final Review", "description": "Ensure brand compliance"},
                ],
                "estimated_time": "3-4 hours",
                "difficulty": "intermediate",
                "assets_needed": ["Brand Guidelines", "Data", "Corporate Assets"],
                "output_specs": {"resolution": "1920x1080", "fps": 30, "format": "MP4"}
            },
            {
                "name": "Podcast Intro/Outro",
                "description": "Create professional intros and outros for podcast episodes",
                "category": "entertainment",
                "tags": ["Entertainment", "Short Form", "Audio Focus"],
                "templates": ["podcast_intro"],
                "workflow_steps": [
                    {"step": "Branding", "description": "Define podcast visual identity"},
                    {"step": "Audio", "description": "Create or select theme music"},
                    {"step": "Animation", "description": "Design animated logo/text"},
                    {"step": "Templates", "description": "Create reusable templates"},
                ],
                "estimated_time": "2-3 hours",
                "difficulty": "beginner",
                "assets_needed": ["Logo", "Theme Music", "Brand Colors"],
                "output_specs": {"resolution": "1920x1080", "fps": 30, "format": "MP4"}
            }
        ]
        
        for uc_data in default_use_cases:
            uc_id = str(uuid.uuid4())
            use_case = UseCase(
                id=uc_id,
                name=uc_data["name"],
                description=uc_data["description"],
                category=uc_data["category"],
                tags=uc_data["tags"],
                templates=uc_data["templates"],
                workflow_steps=uc_data["workflow_steps"],
                estimated_time=uc_data["estimated_time"],
                difficulty=uc_data["difficulty"],
                assets_needed=uc_data["assets_needed"],
                output_specs=uc_data["output_specs"]
            )
            self.use_cases[uc_id] = use_case
        
        self._save_use_cases()
    
    def _save_tags(self):
        """Save tags to JSON file"""
        tags_file = os.path.join(self.projects_dir, "tags.json")
        tags_data = {}
        for tag_id, tag in self.tags.items():
            tag_dict = asdict(tag)
            tag_dict['created_at'] = tag.created_at.isoformat()
            tags_data[tag_id] = tag_dict
        
        with open(tags_file, 'w') as f:
            json.dump(tags_data, f, indent=2)
    
    def _save_use_cases(self):
        """Save use cases to JSON file"""
        use_cases_file = os.path.join(self.projects_dir, "use_cases.json")
        use_cases_data = {}
        for uc_id, use_case in self.use_cases.items():
            uc_dict = asdict(use_case)
            uc_dict['created_at'] = use_case.created_at.isoformat()
            use_cases_data[uc_id] = uc_dict
        
        with open(use_cases_file, 'w') as f:
            json.dump(use_cases_data, f, indent=2)
    
    # Tag Management Methods
    def create_tag(self, name: str, color: str, category: str, description: str = "") -> Tag:
        """Create a new tag"""
        tag_id = str(uuid.uuid4())
        tag = Tag(
            id=tag_id,
            name=name,
            color=color,
            category=category,
            description=description
        )
        self.tags[tag_id] = tag
        self._save_tags()
        logger.info(f"Created tag: {name}")
        return tag
    
    def get_tags(self, category: Optional[str] = None) -> List[Tag]:
        """Get all tags, optionally filtered by category"""
        tags = list(self.tags.values())
        if category:
            tags = [tag for tag in tags if tag.category == category]
        return sorted(tags, key=lambda t: t.name)
    
    def get_tag_by_name(self, name: str) -> Optional[Tag]:
        """Get tag by name"""
        for tag in self.tags.values():
            if tag.name.lower() == name.lower():
                return tag
        return None
    
    def delete_tag(self, tag_id: str) -> bool:
        """Delete a tag"""
        if tag_id in self.tags:
            del self.tags[tag_id]
            self._save_tags()
            logger.info(f"Deleted tag: {tag_id}")
            return True
        return False
    
    def assign_tags_to_project(self, project_id: str, tag_names: List[str]) -> bool:
        """Assign tags to a project"""
        if project_id not in self.projects:
            return False
        
        project = self.projects[project_id]
        for tag_name in tag_names:
            if tag_name not in project.tags:
                project.tags.append(tag_name)
        
        project.updated_at = datetime.now()
        self._save_project(project)
        return True
    
    def assign_tags_to_element(self, project_id: str, element_id: str, tag_names: List[str]) -> bool:
        """Assign tags to an element"""
        if project_id not in self.projects:
            return False
        
        project = self.projects[project_id]
        element = next((e for e in project.elements if e.id == element_id), None)
        if not element:
            return False
        
        for tag_name in tag_names:
            if tag_name not in element.tags:
                element.tags.append(tag_name)
        
        element.updated_at = datetime.now()
        project.updated_at = datetime.now()
        self._save_project(project)
        return True
    
    def search_projects_by_tags(self, tag_names: List[str], match_all: bool = False) -> List[CanvasProject]:
        """Search projects by tags"""
        matching_projects = []
        for project in self.projects.values():
            if match_all:
                if all(tag in project.tags for tag in tag_names):
                    matching_projects.append(project)
            else:
                if any(tag in project.tags for tag in tag_names):
                    matching_projects.append(project)
        return matching_projects
    
    # Use Case Management Methods
    def create_use_case(self, name: str, description: str, category: str, 
                       tags: List[str], templates: List[str], 
                       workflow_steps: List[Dict[str, Any]], 
                       estimated_time: str, difficulty: str,
                       assets_needed: List[str], 
                       output_specs: Dict[str, Any]) -> UseCase:
        """Create a new use case"""
        uc_id = str(uuid.uuid4())
        use_case = UseCase(
            id=uc_id,
            name=name,
            description=description,
            category=category,
            tags=tags,
            templates=templates,
            workflow_steps=workflow_steps,
            estimated_time=estimated_time,
            difficulty=difficulty,
            assets_needed=assets_needed,
            output_specs=output_specs
        )
        self.use_cases[uc_id] = use_case
        self._save_use_cases()
        logger.info(f"Created use case: {name}")
        return use_case
    
    def get_use_cases(self, category: Optional[str] = None, difficulty: Optional[str] = None) -> List[UseCase]:
        """Get all use cases, optionally filtered by category or difficulty"""
        use_cases = list(self.use_cases.values())
        if category:
            use_cases = [uc for uc in use_cases if uc.category == category]
        if difficulty:
            use_cases = [uc for uc in use_cases if uc.difficulty == difficulty]
        return sorted(use_cases, key=lambda uc: uc.name)
    
    def get_recommended_use_cases(self, project_tags: List[str]) -> List[UseCase]:
        """Get recommended use cases based on project tags"""
        recommended = []
        for use_case in self.use_cases.values():
            # Calculate similarity score based on matching tags
            matching_tags = set(project_tags) & set(use_case.tags)
            if matching_tags:
                score = len(matching_tags) / len(use_case.tags)
                recommended.append((use_case, score))
        
        # Sort by score and return top recommendations
        recommended.sort(key=lambda x: x[1], reverse=True)
        return [uc for uc, score in recommended[:5]]
    
    def apply_use_case_to_project(self, project_id: str, use_case_id: str) -> bool:
        """Apply a use case to a project"""
        if project_id not in self.projects or use_case_id not in self.use_cases:
            return False
        
        project = self.projects[project_id]
        use_case = self.use_cases[use_case_id]
        
        # Link use case to project
        project.use_case_id = use_case_id
        
        # Apply recommended tags
        for tag_name in use_case.tags:
            if tag_name not in project.tags:
                project.tags.append(tag_name)
        
        # Apply output specs to project metadata
        project.metadata.update({
            'use_case': use_case.name,
            'recommended_specs': use_case.output_specs,
            'workflow_steps': use_case.workflow_steps,
            'assets_needed': use_case.assets_needed
        })
        
        project.updated_at = datetime.now()
        self._save_project(project)
        logger.info(f"Applied use case {use_case.name} to project {project.name}")
        return True
    
    def get_tag_analytics(self) -> Dict[str, Any]:
        """Get analytics about tag usage"""
        tag_usage = {}
        category_usage = {}
        
        # Count tag usage across projects and elements
        for project in self.projects.values():
            for tag in project.tags:
                tag_usage[tag] = tag_usage.get(tag, 0) + 1
            
            for element in project.elements:
                for tag in element.tags:
                    tag_usage[tag] = tag_usage.get(tag, 0) + 1
        
        # Count tags by category
        for tag in self.tags.values():
            category_usage[tag.category] = category_usage.get(tag.category, 0) + 1
        
        return {
            "total_tags": len(self.tags),
            "total_use_cases": len(self.use_cases),
            "tag_usage": tag_usage,
            "category_distribution": category_usage,
            "most_used_tags": sorted(tag_usage.items(), key=lambda x: x[1], reverse=True)[:10]
        }

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
            transitions=[],
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
                   properties: Optional[Dict[str, Any]] = None) -> CanvasElement:
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
            keyframes=[],
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
                "properties": element.properties,
                "keyframes": [asdict(kf) for kf in element.keyframes]
            })
        
        # Add transitions
        timeline["transitions"] = [asdict(t) for t in project.transitions]
        
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
    
    def auto_arrange_elements(self, project_id: str, arrangement: str = "sequence") -> bool:
        """Auto-arrange elements on timeline"""
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        
        project = self.projects[project_id]
        
        if arrangement == "sequence":
            # Arrange elements in sequence
            current_time = 0.0
            for element in sorted(project.elements, key=lambda x: x.layer):
                element.start_time = current_time
                current_time += element.duration
            
            # Update project duration
            project.duration = max(project.duration, current_time)
        
        elif arrangement == "parallel":
            # Arrange all elements to start at the same time
            for element in project.elements:
                element.start_time = 0.0
        
        project.updated_at = datetime.now()
        self._save_project(project)
        return True
    
    def duplicate_element(self, project_id: str, element_id: str, 
                         offset_x: float = 50, offset_y: float = 50) -> CanvasElement:
        """Duplicate an existing element"""
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        
        project = self.projects[project_id]
        original_element = None
        
        for elem in project.elements:
            if elem.id == element_id:
                original_element = elem
                break
        
        if not original_element:
            raise ValueError(f"Element {element_id} not found")
        
        # Create new element with offset position
        new_element = self.add_element(
            project_id=project_id,
            element_type=original_element.type,
            x=original_element.x + offset_x,
            y=original_element.y + offset_y,
            width=original_element.width,
            height=original_element.height,
            start_time=original_element.start_time,
            duration=original_element.duration,
            layer=original_element.layer + 1,
            properties=original_element.properties.copy()
        )
        
        # Copy keyframes
        for keyframe in original_element.keyframes:
            new_element.keyframes.append(Keyframe(
                time=keyframe.time,
                property=keyframe.property,
                value=keyframe.value,
                easing=keyframe.easing
            ))
        
        return new_element
    
    def _save_project(self, project: CanvasProject):
        """Save project to disk"""
        project_file = os.path.join(self.projects_dir, f"{project.id}.json")
        
        # Convert project to dict for JSON serialization
        project_data = asdict(project)
        
        # Handle datetime serialization
        project_data["created_at"] = project.created_at.isoformat()
        project_data["updated_at"] = project.updated_at.isoformat()
        
        for element in project_data["elements"]:
            element["created_at"] = element["created_at"].isoformat()
            element["updated_at"] = element["updated_at"].isoformat()
        
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
            
            # Handle backwards compatibility for transitions
            if "transitions" not in data:
                data["transitions"] = []
            
            for element_data in data["elements"]:
                element_data["created_at"] = datetime.fromisoformat(element_data["created_at"])
                element_data["updated_at"] = datetime.fromisoformat(element_data["updated_at"])
                
                # Handle backwards compatibility for keyframes
                if "keyframes" not in element_data:
                    element_data["keyframes"] = []
                else:
                    # Convert keyframe dicts to Keyframe objects
                    keyframes = []
                    for kf_data in element_data["keyframes"]:
                        keyframes.append(Keyframe(**kf_data))
                    element_data["keyframes"] = keyframes
            
            # Convert elements to CanvasElement objects
            elements = [CanvasElement(**elem) for elem in data["elements"]]
            data["elements"] = elements
            
            # Convert transitions to Transition objects
            transitions = [Transition(**trans) for trans in data["transitions"]]
            data["transitions"] = transitions
            
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
                "transition_count": len(project.transitions),
                "created_at": project.created_at.isoformat(),
                "updated_at": project.updated_at.isoformat()
            })
        
        return sorted(projects, key=lambda x: x["updated_at"], reverse=True)
    
    def add_keyframe(self, project_id: str, element_id: str, time: float, 
                    property: str, value: Any, easing: str = "linear") -> bool:
        """Add animation keyframe to an element"""
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
        
        keyframe = Keyframe(time=time, property=property, value=value, easing=easing)
        element.keyframes.append(keyframe)
        element.updated_at = datetime.now()
        project.updated_at = datetime.now()
        self._save_project(project)
        
        return True
    
    def add_transition(self, project_id: str, transition_type: str, duration: float,
                      start_time: float, from_element: str, to_element: str,
                      properties: Optional[Dict[str, Any]] = None) -> Transition:
        """Add a transition between elements"""
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        
        transition_id = str(uuid.uuid4())
        
        transition = Transition(
            id=transition_id,
            type=transition_type,
            duration=duration,
            start_time=start_time,
            from_element=from_element,
            to_element=to_element,
            properties=properties or {}
        )
        
        project = self.projects[project_id]
        project.transitions.append(transition)
        project.updated_at = datetime.now()
        self._save_project(project)
        
        return transition
    
    def generate_waveform_data(self, audio_path: str, width: int = 800, 
                              height: int = 100) -> List[float]:
        """Generate waveform visualization data for audio"""
        try:
            import librosa
            import soundfile as sf
            
            # Load audio file
            y, sr = librosa.load(audio_path)
            
            # Calculate the number of samples per pixel
            samples_per_pixel = len(y) // width
            
            # Generate waveform data
            waveform = []
            for i in range(width):
                start_idx = i * samples_per_pixel
                end_idx = min((i + 1) * samples_per_pixel, len(y))
                
                if start_idx < len(y):
                    # Get RMS (Root Mean Square) for this segment
                    segment = y[start_idx:end_idx]
                    rms = np.sqrt(np.mean(segment**2))
                    # Normalize to height
                    normalized = min(rms * height * 10, height)
                    waveform.append(normalized)
                else:
                    waveform.append(0)
            
            return waveform
            
        except ImportError:
            logger.warning("librosa not available for waveform generation")
            # Fallback: generate random waveform for demo
            return [np.random.random() * height * 0.5 for _ in range(width)]
        except Exception as e:
            logger.error(f"Error generating waveform: {e}")
            return [0] * width
    
    async def export_to_video(self, project_id: str, output_path: Optional[str] = None,
                             quality: str = "high") -> str:
        """Export project to video file using FFmpeg"""
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        
        project = self.projects[project_id]
        
        if output_path is None:
            output_path = os.path.join(self.renders_dir, f"{project.name}_{project_id[:8]}.mp4")
        
        # Generate FFmpeg filter complex for composition
        filter_complex = self._generate_ffmpeg_filter(project)
        
        # Quality settings
        quality_settings = {
            "low": ["-preset", "fast", "-crf", "28"],
            "medium": ["-preset", "medium", "-crf", "23"],
            "high": ["-preset", "slow", "-crf", "18"],
            "ultra": ["-preset", "veryslow", "-crf", "15"]
        }
        
        # Build FFmpeg command
        cmd = [
            "ffmpeg", "-y",  # Overwrite output
            "-f", "lavfi",
            "-i", f"color=black:size={project.width}x{project.height}:duration={project.duration}:rate={project.fps}",
        ]
        
        # Add input files for each media element
        input_files = []
        for element in project.elements:
            if element.type in ["video", "audio", "image"]:
                source = element.properties.get("source")
                if source and os.path.exists(source):
                    cmd.extend(["-i", source])
                    input_files.append(source)
        
        # Add filter complex
        if filter_complex:
            cmd.extend(["-filter_complex", filter_complex])
        
        # Add quality settings
        cmd.extend(quality_settings.get(quality, quality_settings["medium"]))
        
        # Output settings
        cmd.extend([
            "-r", str(project.fps),
            "-t", str(project.duration),
            output_path
        ])
        
        try:
            logger.info(f"Starting video export: {' '.join(cmd)}")
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                logger.info(f"Video exported successfully: {output_path}")
                return output_path
            else:
                error_msg = stderr.decode() if stderr else "Unknown error"
                logger.error(f"FFmpeg export failed: {error_msg}")
                raise RuntimeError(f"Video export failed: {error_msg}")
                
        except Exception as e:
            logger.error(f"Error during video export: {e}")
            raise
    
    def _generate_ffmpeg_filter(self, project: CanvasProject) -> str:
        """Generate FFmpeg filter complex for video composition"""
        filters = []
        input_idx = 1  # Start from 1 (0 is the background)
        
        # Sort elements by layer and start time
        sorted_elements = sorted(project.elements, key=lambda x: (x.layer, x.start_time))
        
        for element in sorted_elements:
            if element.type == "video":
                # Video overlay with positioning and timing
                filters.append(
                    f"[{input_idx}:v]scale={int(element.width)}:{int(element.height)}[v{input_idx}];"
                    f"[0:v][v{input_idx}]overlay={int(element.x)}:{int(element.y)}:enable='between(t,{element.start_time},{element.start_time + element.duration})'[tmp{input_idx}]"
                )
                input_idx += 1
            
            elif element.type == "image":
                # Image overlay with duration
                filters.append(
                    f"[{input_idx}:v]scale={int(element.width)}:{int(element.height)}[img{input_idx}];"
                    f"[0:v][img{input_idx}]overlay={int(element.x)}:{int(element.y)}:enable='between(t,{element.start_time},{element.start_time + element.duration})'[tmp{input_idx}]"
                )
                input_idx += 1
            
            elif element.type == "text":
                # Text overlay using drawtext filter
                text = element.properties.get("text", "")
                font_size = element.properties.get("font_size", 24)
                color = element.properties.get("color", "#FFFFFF").replace("#", "")
                
                filters.append(
                    f"drawtext=text='{text}':x={int(element.x)}:y={int(element.y)}:fontsize={font_size}:fontcolor={color}:enable='between(t,{element.start_time},{element.start_time + element.duration})'"
                )
        
        return ";".join(filters) if filters else ""

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
    },
    "podcast_intro": {
        "name": "Podcast Intro",
        "width": 1920,
        "height": 1080,
        "duration": 30.0,
        "elements": [
            {
                "type": "text",
                "text": "Welcome to Our Podcast",
                "x": 960,
                "y": 400,
                "font_size": 56,
                "color": "#00FF88",
                "text_align": "center"
            }
        ]
    }
}

if __name__ == "__main__":
    # Demo usage
    import asyncio
    
    async def demo():
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
        
        # Add keyframe animation
        editor.add_keyframe(project.id, title.id, 0.0, "opacity", 0.0)
        editor.add_keyframe(project.id, title.id, 2.0, "opacity", 1.0)
        
        # Get timeline
        timeline = editor.get_project_timeline(project.id)
        print(f"Timeline tracks: {list(timeline['tracks'].keys())}")
        
        # Export video (if FFmpeg is available)
        try:
            output_path = await editor.export_to_video(project.id)
            print(f"Video exported to: {output_path}")
        except Exception as e:
            print(f"Video export failed: {e}")
    
    asyncio.run(demo())
