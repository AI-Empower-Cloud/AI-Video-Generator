"""
🏗️ Base Classes and Interfaces
==============================

Abstract base classes and interfaces for the AI Video Generator platform.
Provides common functionality and enforces contracts for implementations.
"""

import os
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union, Callable
from datetime import datetime

# Import models directly to avoid circular imports
try:
    from .models import CanvasProject, CanvasElement, Tag, UseCase
except ImportError:
    # For now, we'll define placeholder types
    CanvasProject = Any
    CanvasElement = Any
    Tag = Any
    UseCase = Any

logger = logging.getLogger(__name__)


class BaseManager(ABC):
    """Abstract base class for all managers"""
    
    def __init__(self, storage_dir: str):
        self.storage_dir = storage_dir
        self._ensure_storage_dir()
    
    def _ensure_storage_dir(self):
        """Ensure storage directory exists"""
        os.makedirs(self.storage_dir, exist_ok=True)
    
    @abstractmethod
    def save(self, item: Any) -> bool:
        """Save an item to storage"""
        pass
    
    @abstractmethod
    def load(self, item_id: str) -> Optional[Any]:
        """Load an item from storage"""
        pass
    
    @abstractmethod
    def delete(self, item_id: str) -> bool:
        """Delete an item from storage"""
        pass
    
    @abstractmethod
    def list_all(self) -> List[Any]:
        """List all items"""
        pass


class BaseEditor(ABC):
    """Abstract base class for editors"""
    
    def __init__(self, projects_dir: str = "projects"):
        self.projects_dir = projects_dir
        self.logger = logging.getLogger(self.__class__.__name__)
        self._setup_directories()
    
    def _setup_directories(self):
        """Setup required directories"""
        os.makedirs(self.projects_dir, exist_ok=True)
    
    @abstractmethod
    def create_project(self, name: str, **kwargs) -> CanvasProject:
        """Create a new project"""
        pass
    
    @abstractmethod
    def load_project(self, project_id: str) -> Optional[CanvasProject]:
        """Load a project"""
        pass
    
    @abstractmethod
    def save_project(self, project: CanvasProject) -> bool:
        """Save a project"""
        pass
    
    @abstractmethod
    def delete_project(self, project_id: str) -> bool:
        """Delete a project"""
        pass


class JSONStorageMixin:
    """Mixin for JSON-based storage operations"""
    
    def save_json(self, data: Dict[str, Any], file_path: str) -> bool:
        """Save data to JSON file"""
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            return True
        except Exception as e:
            logger.error(f"Failed to save JSON to {file_path}: {e}")
            return False
    
    def load_json(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Load data from JSON file"""
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load JSON from {file_path}: {e}")
            return None


class TagManager(BaseManager, JSONStorageMixin):
    """Manager for tags"""
    
    def __init__(self, storage_dir: str):
        super().__init__(storage_dir)
        self.tags: Dict[str, Tag] = {}
        self.tags_file = os.path.join(storage_dir, "tags.json")
        self.load_all()
    
    def save(self, tag: Tag) -> bool:
        """Save a tag"""
        self.tags[tag.id] = tag
        return self._save_all()
    
    def load(self, tag_id: str) -> Optional[Tag]:
        """Load a tag by ID"""
        return self.tags.get(tag_id)
    
    def delete(self, tag_id: str) -> bool:
        """Delete a tag"""
        if tag_id in self.tags:
            del self.tags[tag_id]
            return self._save_all()
        return False
    
    def list_all(self) -> List[Tag]:
        """List all tags"""
        return list(self.tags.values())
    
    def get_by_name(self, name: str) -> Optional[Tag]:
        """Get tag by name"""
        for tag in self.tags.values():
            if tag.name.lower() == name.lower():
                return tag
        return None
    
    def get_by_category(self, category: str) -> List[Tag]:
        """Get tags by category"""
        return [tag for tag in self.tags.values() if tag.category == category]
    
    def load_all(self):
        """Load all tags from storage"""
        data = self.load_json(self.tags_file)
        if data:
            for tag_id, tag_data in data.items():
                try:
                    self.tags[tag_id] = Tag.from_dict(tag_data)
                except Exception as e:
                    logger.warning(f"Failed to load tag {tag_id}: {e}")
    
    def _save_all(self) -> bool:
        """Save all tags to storage"""
        data = {tag_id: tag.to_dict() for tag_id, tag in self.tags.items()}
        return self.save_json(data, self.tags_file)


class UseCaseManager(BaseManager, JSONStorageMixin):
    """Manager for use cases"""
    
    def __init__(self, storage_dir: str):
        super().__init__(storage_dir)
        self.use_cases: Dict[str, UseCase] = {}
        self.use_cases_file = os.path.join(storage_dir, "use_cases.json")
        self.load_all()
    
    def save(self, use_case: UseCase) -> bool:
        """Save a use case"""
        self.use_cases[use_case.id] = use_case
        return self._save_all()
    
    def load(self, use_case_id: str) -> Optional[UseCase]:
        """Load a use case by ID"""
        return self.use_cases.get(use_case_id)
    
    def delete(self, use_case_id: str) -> bool:
        """Delete a use case"""
        if use_case_id in self.use_cases:
            del self.use_cases[use_case_id]
            return self._save_all()
        return False
    
    def list_all(self) -> List[UseCase]:
        """List all use cases"""
        return list(self.use_cases.values())
    
    def get_by_category(self, category: str) -> List[UseCase]:
        """Get use cases by category"""
        return [uc for uc in self.use_cases.values() if uc.category == category]
    
    def get_by_difficulty(self, difficulty: str) -> List[UseCase]:
        """Get use cases by difficulty"""
        return [uc for uc in self.use_cases.values() if uc.difficulty == difficulty]
    
    def get_recommended(self, project_tags: List[str], limit: int = 5) -> List[UseCase]:
        """Get recommended use cases based on project tags"""
        recommendations = []
        
        for use_case in self.use_cases.values():
            matching_tags = set(project_tags) & set(use_case.tags)
            if matching_tags:
                score = len(matching_tags) / len(use_case.tags)
                recommendations.append((use_case, score))
        
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return [uc for uc, score in recommendations[:limit]]
    
    def load_all(self):
        """Load all use cases from storage"""
        data = self.load_json(self.use_cases_file)
        if data:
            for uc_id, uc_data in data.items():
                try:
                    self.use_cases[uc_id] = UseCase.from_dict(uc_data)
                except Exception as e:
                    logger.warning(f"Failed to load use case {uc_id}: {e}")
    
    def _save_all(self) -> bool:
        """Save all use cases to storage"""
        data = {uc_id: uc.to_dict() for uc_id, uc in self.use_cases.items()}
        return self.save_json(data, self.use_cases_file)


class ProjectManager(BaseManager, JSONStorageMixin):
    """Manager for canvas projects"""
    
    def __init__(self, storage_dir: str):
        super().__init__(storage_dir)
        self.projects: Dict[str, CanvasProject] = {}
    
    def save(self, project: CanvasProject) -> bool:
        """Save a project"""
        self.projects[project.id] = project
        project_file = os.path.join(self.storage_dir, f"{project.id}.json")
        return self.save_json(project.to_dict(), project_file)
    
    def load(self, project_id: str) -> Optional[CanvasProject]:
        """Load a project by ID"""
        if project_id in self.projects:
            return self.projects[project_id]
        
        project_file = os.path.join(self.storage_dir, f"{project_id}.json")
        data = self.load_json(project_file)
        
        if data:
            try:
                project = CanvasProject.from_dict(data)
                self.projects[project_id] = project
                return project
            except Exception as e:
                logger.error(f"Failed to load project {project_id}: {e}")
        
        return None
    
    def delete(self, project_id: str) -> bool:
        """Delete a project"""
        project_file = os.path.join(self.storage_dir, f"{project_id}.json")
        
        # Remove from memory
        if project_id in self.projects:
            del self.projects[project_id]
        
        # Remove file
        if os.path.exists(project_file):
            try:
                os.remove(project_file)
                return True
            except Exception as e:
                logger.error(f"Failed to delete project file {project_file}: {e}")
        
        return False
    
    def list_all(self) -> List[Dict[str, Any]]:
        """List all projects (summaries)"""
        projects = []
        
        # Load project summaries from disk
        if os.path.exists(self.storage_dir):
            for filename in os.listdir(self.storage_dir):
                if filename.endswith('.json') and filename != 'tags.json' and filename != 'use_cases.json':
                    project_id = filename[:-5]
                    project = self.load(project_id)
                    if project:
                        projects.append({
                            "id": project.id,
                            "name": project.name,
                            "width": project.width,
                            "height": project.height,
                            "duration": project.duration,
                            "element_count": len(project.elements),
                            "transition_count": len(project.transitions),
                            "created_at": project.created_at.isoformat(),
                            "updated_at": project.updated_at.isoformat(),
                            "tags": project.tags
                        })
        
        return sorted(projects, key=lambda x: x["updated_at"], reverse=True)
    
    def search_by_tags(self, tag_names: List[str], match_all: bool = False) -> List[CanvasProject]:
        """Search projects by tags"""
        matching_projects = []
        
        for project_summary in self.list_all():
            project_tags = project_summary.get('tags', [])
            
            if match_all:
                if all(tag in project_tags for tag in tag_names):
                    project = self.load(project_summary['id'])
                    if project:
                        matching_projects.append(project)
            else:
                if any(tag in project_tags for tag in tag_names):
                    project = self.load(project_summary['id'])
                    if project:
                        matching_projects.append(project)
        
        return matching_projects


class ValidationMixin:
    """Mixin for common validation operations"""
    
    def validate_dimensions(self, width: int, height: int) -> bool:
        """Validate project dimensions"""
        return width > 0 and height > 0 and width <= 7680 and height <= 4320
    
    def validate_duration(self, duration: float) -> bool:
        """Validate duration"""
        return duration > 0 and duration <= 3600  # Max 1 hour
    
    def validate_fps(self, fps: int) -> bool:
        """Validate frame rate"""
        return fps in [24, 25, 30, 50, 60]
    
    def validate_color(self, color: str) -> bool:
        """Validate color format"""
        if color.startswith('#') and len(color) in [4, 7]:
            try:
                int(color[1:], 16)
                return True
            except ValueError:
                pass
        return False


class ErrorHandler:
    """Centralized error handling"""
    
    @staticmethod
    def handle_validation_error(message: str) -> ValueError:
        """Handle validation errors"""
        logger.error(f"Validation error: {message}")
        return ValueError(message)
    
    @staticmethod
    def handle_not_found_error(item_type: str, item_id: str) -> ValueError:
        """Handle not found errors"""
        message = f"{item_type} {item_id} not found"
        logger.error(message)
        return ValueError(message)
    
    @staticmethod
    def handle_storage_error(operation: str, item_type: str, error: Exception) -> RuntimeError:
        """Handle storage errors"""
        message = f"Failed to {operation} {item_type}: {error}"
        logger.error(message)
        return RuntimeError(message)


# Event system for extensibility
class EventEmitter:
    """Simple event emitter for extensibility"""
    
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}
    
    def on(self, event: str, callback: Callable):
        """Add event listener"""
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)
    
    def emit(self, event: str, *args, **kwargs):
        """Emit an event"""
        if event in self._listeners:
            for callback in self._listeners[event]:
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Error in event callback for {event}: {e}")
    
    def off(self, event: str, callback: Callable):
        """Remove event listener"""
        if event in self._listeners and callback in self._listeners[event]:
            self._listeners[event].remove(callback)
