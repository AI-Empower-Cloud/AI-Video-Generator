"""
🎨 Modular Canvas Editor
========================

A modular, component-based canvas editor built using the core modules.
This demonstrates how to use the small blocks approach.
"""

import uuid
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from core import (
    CanvasProject, CanvasElement, Tag, UseCase,
    BaseEditor, TagManager, UseCaseManager, ProjectManager,
    ValidationMixin, ErrorHandler, EventEmitter,
    create_project_from_template
)

logger = logging.getLogger(__name__)


class ModularCanvasEditor(BaseEditor, ValidationMixin):
    """
    Modular Canvas Editor using composition pattern
    
    This editor is built from small, reusable components:
    - ProjectManager: Handles project CRUD operations
    - TagManager: Manages tags and categorization  
    - UseCaseManager: Manages use cases and templates
    - ValidationMixin: Provides validation utilities
    - EventEmitter: Enables event-driven architecture
    """
    
    def __init__(self, projects_dir: str = "canvas_projects"):
        super().__init__(projects_dir)
        
        # Initialize managers
        self.project_manager = ProjectManager(projects_dir)
        self.tag_manager = TagManager(projects_dir)
        self.use_case_manager = UseCaseManager(projects_dir)
        
        # Event system for extensibility
        self.events = EventEmitter()
        
        # Initialize default data
        self._initialize_defaults()
        
        logger.info(f"ModularCanvasEditor initialized with projects_dir: {projects_dir}")
    
    def _initialize_defaults(self):
        """Initialize default tags and use cases if none exist"""
        if not self.tag_manager.list_all():
            self._create_default_tags()
        
        if not self.use_case_manager.list_all():
            self._create_default_use_cases()
    
    def _create_default_tags(self):
        """Create default system tags"""
        default_tags = [
            {"name": "Educational", "color": "#4CAF50", "category": "content"},
            {"name": "Marketing", "color": "#FF9800", "category": "content"},
            {"name": "Entertainment", "color": "#E91E63", "category": "content"},
            {"name": "Corporate", "color": "#2196F3", "category": "content"},
            {"name": "Short Form", "color": "#FFEB3B", "category": "format"},
            {"name": "Long Form", "color": "#8BC34A", "category": "format"},
            {"name": "Draft", "color": "#9E9E9E", "category": "status"},
            {"name": "Final", "color": "#4CAF50", "category": "status"},
        ]
        
        for tag_data in default_tags:
            tag = Tag(
                id=str(uuid.uuid4()),
                name=tag_data["name"],
                color=tag_data["color"],
                category=tag_data["category"],
                description=f"{tag_data['name']} content"
            )
            self.tag_manager.save(tag)
        
        logger.info("Created default tags")
    
    def _create_default_use_cases(self):
        """Create default use cases"""
        default_use_cases = [
            {
                "name": "Educational Video",
                "description": "Create engaging educational content",
                "category": "education",
                "tags": ["Educational", "Long Form"],
                "difficulty": "intermediate",
                "estimated_time": "4-6 hours"
            },
            {
                "name": "Social Media Post",
                "description": "Quick social media content",
                "category": "marketing",
                "tags": ["Marketing", "Short Form"],
                "difficulty": "beginner",
                "estimated_time": "1-2 hours"
            }
        ]
        
        for uc_data in default_use_cases:
            use_case = UseCase(
                id=str(uuid.uuid4()),
                name=uc_data["name"],
                description=uc_data["description"],
                category=uc_data["category"],
                tags=uc_data["tags"],
                difficulty=uc_data["difficulty"],
                estimated_time=uc_data["estimated_time"],
                templates=[],
                workflow_steps=[],
                assets_needed=[],
                output_specs={}
            )
            self.use_case_manager.save(use_case)
        
        logger.info("Created default use cases")
    
    # Project Management Methods
    def create_project(self, name: str, width: int = 1920, height: int = 1080, 
                      fps: int = 30, duration: float = 30.0, **kwargs) -> CanvasProject:
        """Create a new project with validation"""
        # Validate inputs
        if not self.validate_dimensions(width, height):
            raise ErrorHandler.handle_validation_error(f"Invalid dimensions: {width}x{height}")
        
        if not self.validate_duration(duration):
            raise ErrorHandler.handle_validation_error(f"Invalid duration: {duration}")
        
        if not self.validate_fps(fps):
            raise ErrorHandler.handle_validation_error(f"Invalid FPS: {fps}")
        
        # Create project
        project = CanvasProject(
            id=str(uuid.uuid4()),
            name=name,
            width=width,
            height=height,
            fps=fps,
            duration=duration
        )
        
        # Save project
        if self.project_manager.save(project):
            self.events.emit('project_created', project)
            logger.info(f"Created project: {name} ({project.id})")
            return project
        else:
            raise ErrorHandler.handle_storage_error("create", "project", Exception("Save failed"))
    
    def create_project_from_template(self, template_name: str, project_name: str) -> CanvasProject:
        """Create a project from a template"""
        try:
            project = create_project_from_template(template_name, project_name)
            if self.project_manager.save(project):
                self.events.emit('project_created', project)
                logger.info(f"Created project from template {template_name}: {project_name}")
                return project
            else:
                raise ErrorHandler.handle_storage_error("create", "project", Exception("Save failed"))
        except Exception as e:
            raise ErrorHandler.handle_validation_error(f"Failed to create from template: {e}")
    
    def load_project(self, project_id: str) -> Optional[CanvasProject]:
        """Load a project"""
        project = self.project_manager.load(project_id)
        if project:
            self.events.emit('project_loaded', project)
        return project
    
    def save_project(self, project: CanvasProject) -> bool:
        """Save a project"""
        project.updated_at = datetime.now()
        success = self.project_manager.save(project)
        if success:
            self.events.emit('project_saved', project)
        return success
    
    def delete_project(self, project_id: str) -> bool:
        """Delete a project"""
        success = self.project_manager.delete(project_id)
        if success:
            self.events.emit('project_deleted', project_id)
            logger.info(f"Deleted project: {project_id}")
        return success
    
    def list_projects(self) -> List[Dict[str, Any]]:
        """List all projects"""
        return self.project_manager.list_all()
    
    # Element Management Methods
    def add_element(self, project_id: str, element_type: str, x: float, y: float,
                   width: float, height: float, **kwargs) -> CanvasElement:
        """Add an element to a project"""
        project = self.load_project(project_id)
        if not project:
            raise ErrorHandler.handle_not_found_error("Project", project_id)
        
        element = CanvasElement(
            id=str(uuid.uuid4()),
            type=element_type,
            x=x,
            y=y,
            width=width,
            height=height,
            start_time=kwargs.get('start_time', 0.0),
            duration=kwargs.get('duration', 5.0),
            layer=kwargs.get('layer', 1),
            properties=kwargs.get('properties', {})
        )
        
        project.add_element(element)
        
        if self.save_project(project):
            self.events.emit('element_added', project, element)
            logger.info(f"Added {element_type} element to project {project_id}")
            return element
        else:
            raise ErrorHandler.handle_storage_error("add", "element", Exception("Save failed"))
    
    def add_text_element(self, project_id: str, text: str, x: float, y: float, 
                        font_size: int = 24, **kwargs) -> CanvasElement:
        """Add a text element"""
        properties = {
            "text": text,
            "font_size": font_size,
            "font_family": kwargs.get("font_family", "Arial"),
            "color": kwargs.get("color", "#FFFFFF"),
            "text_align": kwargs.get("text_align", "left")
        }
        
        return self.add_element(
            project_id=project_id,
            element_type="text",
            x=x, y=y,
            width=kwargs.get("width", len(text) * font_size * 0.6),
            height=kwargs.get("height", font_size * 1.2),
            properties=properties,
            **kwargs
        )
    
    def remove_element(self, project_id: str, element_id: str) -> bool:
        """Remove an element from a project"""
        project = self.load_project(project_id)
        if not project:
            return False
        
        success = project.remove_element(element_id)
        if success and self.save_project(project):
            self.events.emit('element_removed', project, element_id)
            logger.info(f"Removed element {element_id} from project {project_id}")
            return True
        return False
    
    # Tag Management Methods
    def create_tag(self, name: str, color: str, category: str, description: str = "") -> Tag:
        """Create a new tag"""
        if not self.validate_color(color):
            raise ErrorHandler.handle_validation_error(f"Invalid color format: {color}")
        
        tag = Tag(
            id=str(uuid.uuid4()),
            name=name,
            color=color,
            category=category,
            description=description
        )
        
        if self.tag_manager.save(tag):
            self.events.emit('tag_created', tag)
            logger.info(f"Created tag: {name}")
            return tag
        else:
            raise ErrorHandler.handle_storage_error("create", "tag", Exception("Save failed"))
    
    def get_tags(self, category: Optional[str] = None) -> List[Tag]:
        """Get tags, optionally filtered by category"""
        if category:
            return self.tag_manager.get_by_category(category)
        return self.tag_manager.list_all()
    
    def assign_tags_to_project(self, project_id: str, tag_names: List[str]) -> bool:
        """Assign tags to a project"""
        project = self.load_project(project_id)
        if not project:
            return False
        
        for tag_name in tag_names:
            if tag_name not in project.tags:
                project.tags.append(tag_name)
        
        success = self.save_project(project)
        if success:
            self.events.emit('tags_assigned', project, tag_names)
        return success
    
    # Use Case Management Methods
    def get_use_cases(self, category: Optional[str] = None) -> List[UseCase]:
        """Get use cases, optionally filtered by category"""
        if category:
            return self.use_case_manager.get_by_category(category)
        return self.use_case_manager.list_all()
    
    def get_recommended_use_cases(self, project_tags: List[str]) -> List[UseCase]:
        """Get recommended use cases based on project tags"""
        return self.use_case_manager.get_recommended(project_tags)
    
    # Analytics and Reporting
    def get_analytics(self) -> Dict[str, Any]:
        """Get platform analytics"""
        projects = self.list_projects()
        tags = self.get_tags()
        use_cases = self.get_use_cases()
        
        return {
            "total_projects": len(projects),
            "total_tags": len(tags),
            "total_use_cases": len(use_cases),
            "projects_by_status": self._group_projects_by_status(projects),
            "popular_tags": self._get_popular_tags(projects),
            "recent_activity": self._get_recent_activity(projects)
        }
    
    def _group_projects_by_status(self, projects: List[Dict[str, Any]]) -> Dict[str, int]:
        """Group projects by status tags"""
        status_counts = {}
        for project in projects:
            for tag in project.get('tags', []):
                if tag in ['Draft', 'Review', 'Final', 'Published']:
                    status_counts[tag] = status_counts.get(tag, 0) + 1
        return status_counts
    
    def _get_popular_tags(self, projects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get most popular tags"""
        tag_counts = {}
        for project in projects:
            for tag in project.get('tags', []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        return [
            {"name": tag, "count": count}
            for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        ]
    
    def _get_recent_activity(self, projects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get recent activity"""
        return sorted(projects, key=lambda x: x["updated_at"], reverse=True)[:5]


# Usage example
if __name__ == "__main__":
    # Create editor instance
    editor = ModularCanvasEditor()
    
    # Set up event listeners
    editor.events.on('project_created', lambda project: print(f"Project created: {project.name}"))
    editor.events.on('element_added', lambda project, element: print(f"Element added: {element.type}"))
    
    # Create a project
    project = editor.create_project("My Video", duration=60.0)
    
    # Add some elements
    title = editor.add_text_element(project.id, "Welcome!", 100, 100, font_size=48)
    
    # Get analytics
    analytics = editor.get_analytics()
    print(f"Analytics: {analytics}")
    
    # List projects
    projects = editor.list_projects()
    print(f"Projects: {len(projects)}")
