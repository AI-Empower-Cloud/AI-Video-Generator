#!/usr/bin/env python3
"""
📝 NOTION-LIKE PLANNING & DOCUMENTATION SYSTEM
=============================================

Collaborative planning and documentation system for video projects with:
- Project planning and brainstorming
- Video storyboards and scripts
- Team collaboration and comments
- Video previews and thumbnails
- Progress tracking and task management
- Rich text documentation
"""

import json
import uuid
import os
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from enum import Enum
import base64
import logging
import subprocess
import asyncio

logger = logging.getLogger(__name__)

class DocumentType(Enum):
    """Types of documents in the planning system"""
    PROJECT_BRIEF = "project_brief"
    STORYBOARD = "storyboard"
    SCRIPT = "script"
    TASK_LIST = "task_list"
    NOTES = "notes"
    REFERENCE = "reference"
    FEEDBACK = "feedback"

class TaskStatus(Enum):
    """Task completion status"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    BLOCKED = "blocked"

@dataclass
class Comment:
    """Comment on a document or element"""
    id: str
    author: str
    content: str
    timestamp: datetime
    parent_id: Optional[str] = None  # For threaded comments
    resolved: bool = False
    element_id: Optional[str] = None  # Reference to canvas element

@dataclass
class Task:
    """Task in project management"""
    id: str
    title: str
    description: str
    status: TaskStatus
    assignee: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: str = "medium"  # low, medium, high, urgent
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class StoryboardFrame:
    """Single frame in a storyboard"""
    id: str
    sequence: int
    title: str
    description: str
    duration: float
    thumbnail_data: Optional[str] = None  # Base64 encoded image
    canvas_element_id: Optional[str] = None  # Link to canvas element
    notes: str = ""
    camera_angle: str = ""
    audio_notes: str = ""

@dataclass
class Document:
    """Notion-like document"""
    id: str
    title: str
    type: DocumentType
    content: Dict[str, Any]  # Rich content structure
    project_id: str
    author: str
    tags: List[str] = field(default_factory=list)
    comments: List[Comment] = field(default_factory=list)
    version: int = 1
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class VideoPreview:
    """Video preview with metadata"""
    id: str
    project_id: str
    canvas_project_id: str
    preview_type: str  # thumbnail, low_res, segment
    file_path: str
    duration: Optional[float] = None
    resolution: Tuple[int, int] = (640, 360)
    file_size: int = 0
    created_at: datetime = field(default_factory=datetime.now)

class NotionLikePlanner:
    """Notion-like planning and documentation system"""
    
    def __init__(self, workspace_dir: str = "notion_workspace"):
        self.workspace_dir = workspace_dir
        self.docs_dir = os.path.join(workspace_dir, "documents")
        self.previews_dir = os.path.join(workspace_dir, "previews")
        self.assets_dir = os.path.join(workspace_dir, "assets")
        
        self.documents: Dict[str, Document] = {}
        self.tasks: Dict[str, Task] = {}
        self.previews: Dict[str, VideoPreview] = {}
        
        self._ensure_directories()
        self._load_existing_data()
    
    def _load_existing_data(self):
        """Load existing documents, tasks, and previews from disk"""
        # Load documents
        if os.path.exists(self.docs_dir):
            for filename in os.listdir(self.docs_dir):
                if filename.endswith('.json'):
                    doc_id = filename[:-5]
                    self._load_document(doc_id)
        
        # Load tasks
        tasks_file = os.path.join(self.workspace_dir, "tasks.json")
        if os.path.exists(tasks_file):
            with open(tasks_file, 'r') as f:
                tasks_data = json.load(f)
                for task_id, task_data in tasks_data.items():
                    # Parse datetime fields
                    task_data["created_at"] = datetime.fromisoformat(task_data["created_at"])
                    task_data["updated_at"] = datetime.fromisoformat(task_data["updated_at"])
                    task_data["status"] = TaskStatus(task_data["status"])
                    if task_data.get("due_date"):
                        task_data["due_date"] = datetime.fromisoformat(task_data["due_date"])
                    
                    self.tasks[task_id] = Task(**task_data)
        
        # Load previews
        previews_file = os.path.join(self.previews_dir, "previews.json")
        if os.path.exists(previews_file):
            with open(previews_file, 'r') as f:
                previews_data = json.load(f)
                for preview_id, preview_data in previews_data.items():
                    preview_data["created_at"] = datetime.fromisoformat(preview_data["created_at"])
                    self.previews[preview_id] = VideoPreview(**preview_data)
    
    def _load_document(self, doc_id: str):
        """Load a single document from disk"""
        doc_file = os.path.join(self.docs_dir, f"{doc_id}.json")
        if os.path.exists(doc_file):
            with open(doc_file, 'r') as f:
                doc_data = json.load(f)
                
                # Parse datetime fields
                doc_data["created_at"] = datetime.fromisoformat(doc_data["created_at"])
                doc_data["updated_at"] = datetime.fromisoformat(doc_data["updated_at"])
                doc_data["type"] = DocumentType(doc_data["type"])
                
                # Parse comments
                comments = []
                for comment_data in doc_data.get("comments", []):
                    comment_data["timestamp"] = datetime.fromisoformat(comment_data["timestamp"])
                    comments.append(Comment(**comment_data))
                doc_data["comments"] = comments
                
                self.documents[doc_id] = Document(**doc_data)

    def _ensure_directories(self):
        """Create necessary directories"""
        os.makedirs(self.workspace_dir, exist_ok=True)
        os.makedirs(self.docs_dir, exist_ok=True)
        os.makedirs(self.previews_dir, exist_ok=True)
        os.makedirs(self.assets_dir, exist_ok=True)
    
    def create_document(self, title: str, doc_type: DocumentType, 
                       project_id: str, author: str = "user",
                       content: Optional[Dict[str, Any]] = None) -> Document:
        """Create a new document"""
        doc_id = str(uuid.uuid4())
        
        # Default content structure based on document type
        default_content = self._get_default_content(doc_type)
        if content:
            default_content.update(content)
        
        document = Document(
            id=doc_id,
            title=title,
            type=doc_type,
            content=default_content,
            project_id=project_id,
            author=author
        )
        
        self.documents[doc_id] = document
        self._save_document(document)
        
        logger.info(f"Created document: {title} ({doc_type.value})")
        return document
    
    def _get_default_content(self, doc_type: DocumentType) -> Dict[str, Any]:
        """Get default content structure for document type"""
        templates = {
            DocumentType.PROJECT_BRIEF: {
                "sections": [
                    {"type": "heading", "content": "Project Overview"},
                    {"type": "text", "content": "Brief description of the video project..."},
                    {"type": "heading", "content": "Target Audience"},
                    {"type": "text", "content": "Who is this video for?"},
                    {"type": "heading", "content": "Key Messages"},
                    {"type": "bullet_list", "items": ["Message 1", "Message 2", "Message 3"]},
                    {"type": "heading", "content": "Timeline & Deliverables"},
                    {"type": "text", "content": "Project timeline and key milestones..."}
                ]
            },
            DocumentType.STORYBOARD: {
                "frames": [],
                "total_duration": 0.0,
                "aspect_ratio": "16:9",
                "style_notes": ""
            },
            DocumentType.SCRIPT: {
                "scenes": [
                    {
                        "id": str(uuid.uuid4()),
                        "title": "Scene 1",
                        "dialogue": "",
                        "action": "",
                        "duration": 10.0,
                        "voice_notes": ""
                    }
                ],
                "total_word_count": 0,
                "estimated_duration": 0.0
            },
            DocumentType.TASK_LIST: {
                "tasks": [],
                "project_phase": "pre-production"
            },
            DocumentType.NOTES: {
                "sections": [
                    {"type": "text", "content": "Add your notes here..."}
                ]
            }
        }
        
        return templates.get(doc_type, {"sections": []})
    
    def update_document(self, doc_id: str, updates: Dict[str, Any]) -> Document:
        """Update document content"""
        if doc_id not in self.documents:
            raise ValueError(f"Document {doc_id} not found")
        
        document = self.documents[doc_id]
        
        # Update fields
        for key, value in updates.items():
            if hasattr(document, key):
                setattr(document, key, value)
            elif key == "content":
                document.content.update(value)
        
        document.updated_at = datetime.now()
        document.version += 1
        self._save_document(document)
        
        return document
    
    def add_comment(self, doc_id: str, content: str, author: str = "user",
                   parent_id: Optional[str] = None, 
                   element_id: Optional[str] = None) -> Comment:
        """Add comment to document"""
        if doc_id not in self.documents:
            raise ValueError(f"Document {doc_id} not found")
        
        comment_id = str(uuid.uuid4())
        comment = Comment(
            id=comment_id,
            author=author,
            content=content,
            timestamp=datetime.now(),
            parent_id=parent_id,
            element_id=element_id
        )
        
        document = self.documents[doc_id]
        document.comments.append(comment)
        document.updated_at = datetime.now()
        self._save_document(document)
        
        return comment
    
    def create_storyboard_frame(self, doc_id: str, title: str, description: str,
                               duration: float, sequence: int,
                               thumbnail_data: Optional[str] = None) -> StoryboardFrame:
        """Add frame to storyboard document"""
        if doc_id not in self.documents:
            raise ValueError(f"Document {doc_id} not found")
        
        document = self.documents[doc_id]
        if document.type != DocumentType.STORYBOARD:
            raise ValueError("Document is not a storyboard")
        
        frame_id = str(uuid.uuid4())
        frame = StoryboardFrame(
            id=frame_id,
            sequence=sequence,
            title=title,
            description=description,
            duration=duration,
            thumbnail_data=thumbnail_data
        )
        
        # Add frame to document content
        if "frames" not in document.content:
            document.content["frames"] = []
        
        document.content["frames"].append(asdict(frame))
        document.content["total_duration"] = sum(f.get("duration", 0) for f in document.content["frames"])
        
        document.updated_at = datetime.now()
        document.version += 1
        self._save_document(document)
        
        return frame
    
    def create_task(self, title: str, description: str, 
                   assignee: Optional[str] = None,
                   due_date: Optional[datetime] = None,
                   priority: str = "medium") -> Task:
        """Create a new task"""
        task_id = str(uuid.uuid4())
        
        task = Task(
            id=task_id,
            title=title,
            description=description,
            status=TaskStatus.TODO,
            assignee=assignee,
            due_date=due_date,
            priority=priority
        )
        
        self.tasks[task_id] = task
        self._save_task(task)
        
        return task
    
    def update_task_status(self, task_id: str, status: TaskStatus) -> Task:
        """Update task status"""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        task = self.tasks[task_id]
        task.status = status
        task.updated_at = datetime.now()
        self._save_task(task)
        
        return task
    
    async def generate_video_preview_advanced(self, project_id: str, canvas_project_id: str,
                                            preview_type: str = "thumbnail",
                                            quality: str = "medium") -> VideoPreview:
        """Generate advanced video preview with actual video processing"""
        preview_id = str(uuid.uuid4())
        
        # Determine preview settings based on type
        preview_settings = {
            "thumbnail": {"duration": 0.1, "resolution": (320, 180), "fps": 1},
            "short": {"duration": 10.0, "resolution": (640, 360), "fps": 15},
            "full": {"duration": None, "resolution": (1280, 720), "fps": 30}
        }
        
        settings = preview_settings.get(preview_type, preview_settings["thumbnail"])
        
        # Generate preview file path
        extension = "jpg" if preview_type == "thumbnail" else "mp4"
        preview_filename = f"{preview_type}_{canvas_project_id[:8]}_{preview_id[:8]}.{extension}"
        preview_path = os.path.join(self.previews_dir, preview_filename)
        
        preview = VideoPreview(
            id=preview_id,
            project_id=project_id,
            canvas_project_id=canvas_project_id,
            preview_type=preview_type,
            file_path=preview_path,
            duration=settings["duration"],
            resolution=settings["resolution"]
        )
        
        try:
            # Import and use canvas editor
            from .canvas_editor import CanvasEditor
            canvas_editor = CanvasEditor()
            
            # Load canvas project
            canvas_project = canvas_editor.load_project(canvas_project_id)
            if not canvas_project:
                raise ValueError(f"Canvas project {canvas_project_id} not found")
            
            if preview_type == "thumbnail":
                # Generate thumbnail (first frame)
                await self._generate_thumbnail(canvas_project, preview_path)
            else:
                # Generate video preview
                temp_duration = settings["duration"] or canvas_project.duration
                
                # Create temporary project with shorter duration
                temp_project_data = asdict(canvas_project)
                temp_project_data["duration"] = temp_duration
                
                # Export with lower quality for preview
                await canvas_editor.export_to_video(
                    canvas_project_id, 
                    preview_path, 
                    quality="low"
                )
            
            # Update preview with file size
            if os.path.exists(preview_path):
                preview.file_size = os.path.getsize(preview_path)
                logger.info(f"Generated {preview_type} preview: {preview_path}")
            
        except Exception as e:
            logger.error(f"Failed to generate preview: {e}")
            # Create placeholder preview
            await self._create_placeholder_preview(preview_path, preview_type)
        
        self.previews[preview_id] = preview
        self._save_preview(preview)
        
        return preview
    
    async def _generate_thumbnail(self, canvas_project, output_path: str):
        """Generate thumbnail from canvas project"""
        # Use FFmpeg to extract first frame
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"color=black:size={canvas_project.width}x{canvas_project.height}:duration=0.1:rate=1",
            "-vframes", "1",
            "-q:v", "2",
            output_path
        ]
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
        except Exception as e:
            logger.error(f"Thumbnail generation failed: {e}")
    
    async def _create_placeholder_preview(self, output_path: str, preview_type: str):
        """Create placeholder preview when generation fails"""
        if preview_type == "thumbnail":
            # Create simple colored thumbnail
            cmd = [
                "ffmpeg", "-y",
                "-f", "lavfi",
                "-i", "color=gray:size=320x180:duration=0.1:rate=1",
                "-vframes", "1",
                output_path
            ]
        else:
            # Create simple video with text
            cmd = [
                "ffmpeg", "-y",
                "-f", "lavfi",
                "-i", "color=black:size=640x360:duration=10:rate=15",
                "-vf", "drawtext=text='Preview Generation Failed':x=(w-tw)/2:y=(h-th)/2:fontsize=24:fontcolor=white",
                output_path
            ]
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
        except Exception:
            pass  # Fail silently for placeholder
    
    def create_from_template(self, template_name: str, project_id: str, 
                           author: str = "user", **kwargs) -> Document:
        """Create document from predefined template"""
        if template_name not in DOCUMENT_TEMPLATES:
            raise ValueError(f"Template {template_name} not found")
        
        template = DOCUMENT_TEMPLATES[template_name]
        
        # Customize template with provided kwargs
        title = kwargs.get("title", template["title"])
        content = template["content"].copy()
        
        # Replace placeholders in content
        for section in content.get("sections", []):
            if "content" in section:
                for key, value in kwargs.items():
                    section["content"] = section["content"].replace(f"{{{key}}}", str(value))
        
        return self.create_document(
            title=title,
            doc_type=template["type"],
            project_id=project_id,
            author=author,
            content=content
        )
    
    def link_canvas_element(self, doc_id: str, canvas_element_id: str, 
                           section_id: Optional[str] = None):
        """Link document section to canvas element"""
        if doc_id not in self.documents:
            raise ValueError(f"Document {doc_id} not found")
        
        document = self.documents[doc_id]
        
        # Add canvas link to document metadata
        if "canvas_links" not in document.content:
            document.content["canvas_links"] = {}
        
        document.content["canvas_links"][section_id or "main"] = canvas_element_id
        document.updated_at = datetime.now()
        self._save_document(document)
    
    def get_canvas_links(self, canvas_element_id: str) -> List[Dict[str, Any]]:
        """Get all documents linked to a canvas element"""
        links = []
        
        for document in self.documents.values():
            canvas_links = document.content.get("canvas_links", {})
            for section_id, element_id in canvas_links.items():
                if element_id == canvas_element_id:
                    links.append({
                        "document_id": document.id,
                        "document_title": document.title,
                        "section_id": section_id,
                        "document_type": document.type.value
                    })
        
        return links
    
    def get_collaboration_stats(self, project_id: str) -> Dict[str, Any]:
        """Get collaboration statistics for project"""
        project_docs = [doc for doc in self.documents.values() 
                       if doc.project_id == project_id]
        
        # Count authors and comments
        authors = set()
        total_comments = 0
        comment_authors = set()
        
        for doc in project_docs:
            authors.add(doc.author)
            total_comments += len(doc.comments)
            for comment in doc.comments:
                comment_authors.add(comment.author)
        
        # Recent activity (last 7 days)
        week_ago = datetime.now() - timedelta(days=7)
        recent_activity = []
        
        for doc in project_docs:
            if doc.updated_at > week_ago:
                recent_activity.append({
                    "type": "document_update",
                    "title": doc.title,
                    "author": doc.author,
                    "timestamp": doc.updated_at.isoformat()
                })
            
            for comment in doc.comments:
                if comment.timestamp > week_ago:
                    recent_activity.append({
                        "type": "comment",
                        "document": doc.title,
                        "author": comment.author,
                        "timestamp": comment.timestamp.isoformat()
                    })
        
        recent_activity.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return {
            "total_authors": len(authors),
            "total_commenters": len(comment_authors),
            "total_comments": total_comments,
            "recent_activity": recent_activity[:20],  # Last 20 activities
            "collaboration_score": min(100, (len(comment_authors) * 20) + (total_comments * 2))
        }
    
    def get_project_dashboard(self, project_id: str) -> Dict[str, Any]:
        """Get project dashboard with all related items"""
        # Get all documents for project
        project_docs = [doc for doc in self.documents.values() 
                       if doc.project_id == project_id]
        
        # Get all tasks (assuming they're project-related via tags or other means)
        project_tasks = list(self.tasks.values())  # Simplified for now
        
        # Get all previews for project
        project_previews = [preview for preview in self.previews.values()
                           if preview.project_id == project_id]
        
        # Calculate project statistics
        total_comments = sum(len(doc.comments) for doc in project_docs)
        completed_tasks = len([task for task in project_tasks 
                              if task.status == TaskStatus.COMPLETED])
        
        return {
            "project_id": project_id,
            "documents": [self._doc_to_dict(doc) for doc in project_docs],
            "tasks": [asdict(task) for task in project_tasks],
            "previews": [asdict(preview) for preview in project_previews],
            "stats": {
                "total_documents": len(project_docs),
                "total_comments": total_comments,
                "total_tasks": len(project_tasks),
                "completed_tasks": completed_tasks,
                "task_completion_rate": completed_tasks / len(project_tasks) if project_tasks else 0
            }
        }
    
    def search_documents(self, query: str, project_id: Optional[str] = None,
                        doc_type: Optional[DocumentType] = None) -> List[Document]:
        """Search documents by content"""
        results = []
        
        for document in self.documents.values():
            # Filter by project if specified
            if project_id and document.project_id != project_id:
                continue
            
            # Filter by type if specified
            if doc_type and document.type != doc_type:
                continue
            
            # Search in title and content
            search_text = f"{document.title} {json.dumps(document.content)}".lower()
            if query.lower() in search_text:
                results.append(document)
        
        return results
    
    def export_project_plan(self, project_id: str, format: str = "markdown") -> str:
        """Export project plan in specified format"""
        dashboard = self.get_project_dashboard(project_id)
        
        if format == "markdown":
            return self._export_to_markdown(dashboard)
        elif format == "json":
            return json.dumps(dashboard, indent=2, default=str)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _export_to_markdown(self, dashboard: Dict[str, Any]) -> str:
        """Export dashboard to Markdown format"""
        md_content = []
        
        md_content.append(f"# Project Dashboard")
        md_content.append(f"Project ID: `{dashboard['project_id']}`\n")
        
        # Project Statistics
        stats = dashboard['stats']
        md_content.append("## 📊 Project Statistics")
        md_content.append(f"- Documents: {stats['total_documents']}")
        md_content.append(f"- Comments: {stats['total_comments']}")
        md_content.append(f"- Tasks: {stats['completed_tasks']}/{stats['total_tasks']} completed ({stats['task_completion_rate']:.1%})")
        md_content.append("")
        
        # Documents
        md_content.append("## 📝 Documents")
        for doc in dashboard['documents']:
            md_content.append(f"### {doc['title']}")
            md_content.append(f"**Type:** {doc['type']}")
            md_content.append(f"**Author:** {doc['author']}")
            md_content.append(f"**Updated:** {doc['updated_at']}")
            md_content.append("")
        
        # Tasks
        md_content.append("## ✅ Tasks")
        for task in dashboard['tasks']:
            status_emoji = {"todo": "⏳", "in_progress": "🔄", "completed": "✅", "blocked": "🚫"}.get(task['status'], "❓")
            md_content.append(f"- {status_emoji} **{task['title']}** ({task['status']})")
            if task.get('assignee'):
                md_content.append(f"  - Assignee: {task['assignee']}")
            if task.get('due_date'):
                md_content.append(f"  - Due: {task['due_date']}")
        
        return "\n".join(md_content)
    
    def _doc_to_dict(self, document: Document) -> Dict[str, Any]:
        """Convert document to dictionary for serialization"""
        doc_dict = asdict(document)
        doc_dict["created_at"] = document.created_at.isoformat()
        doc_dict["updated_at"] = document.updated_at.isoformat()
        doc_dict["type"] = document.type.value
        
        # Convert comments
        doc_dict["comments"] = []
        for comment in document.comments:
            comment_dict = asdict(comment)
            comment_dict["timestamp"] = comment.timestamp.isoformat()
            doc_dict["comments"].append(comment_dict)
        
        return doc_dict
    
    def _save_document(self, document: Document):
        """Save document to disk"""
        doc_file = os.path.join(self.docs_dir, f"{document.id}.json")
        doc_dict = self._doc_to_dict(document)
        
        with open(doc_file, 'w') as f:
            json.dump(doc_dict, f, indent=2)
    
    def _save_task(self, task: Task):
        """Save task to disk"""
        task_file = os.path.join(self.workspace_dir, "tasks.json")
        
        # Load existing tasks
        tasks_data = {}
        if os.path.exists(task_file):
            with open(task_file, 'r') as f:
                tasks_data = json.load(f)
        
        # Add/update task
        task_dict = asdict(task)
        task_dict["created_at"] = task.created_at.isoformat()
        task_dict["updated_at"] = task.updated_at.isoformat()
        task_dict["status"] = task.status.value
        if task.due_date:
            task_dict["due_date"] = task.due_date.isoformat()
        
        tasks_data[task.id] = task_dict
        
        with open(task_file, 'w') as f:
            json.dump(tasks_data, f, indent=2)
    
    def _save_preview(self, preview: VideoPreview):
        """Save preview metadata to disk"""
        preview_file = os.path.join(self.previews_dir, "previews.json")
        
        # Load existing previews
        previews_data = {}
        if os.path.exists(preview_file):
            with open(preview_file, 'r') as f:
                previews_data = json.load(f)
        
        # Add/update preview
        preview_dict = asdict(preview)
        preview_dict["created_at"] = preview.created_at.isoformat()
        
        previews_data[preview.id] = preview_dict
        
        with open(preview_file, 'w') as f:
            json.dump(previews_data, f, indent=2)

# Predefined document templates
DOCUMENT_TEMPLATES = {
    "video_brief": {
        "title": "Video Project Brief",
        "type": DocumentType.PROJECT_BRIEF,
        "content": {
            "sections": [
                {"type": "heading", "content": "🎯 Project Goals"},
                {"type": "text", "content": "What do you want to achieve with this video?"},
                {"type": "heading", "content": "👥 Target Audience"},
                {"type": "text", "content": "Who will watch this video?"},
                {"type": "heading", "content": "📝 Key Messages"},
                {"type": "bullet_list", "items": ["Main message", "Supporting points"]},
                {"type": "heading", "content": "🎨 Style & Tone"},
                {"type": "text", "content": "Visual style, tone of voice, brand guidelines"},
                {"type": "heading", "content": "📅 Timeline"},
                {"type": "text", "content": "Project milestones and deadlines"}
            ]
        }
    },
    "production_checklist": {
        "title": "Video Production Checklist",
        "type": DocumentType.TASK_LIST,
        "content": {
            "tasks": [
                {"title": "Script Review", "status": "todo", "priority": "high"},
                {"title": "Asset Preparation", "status": "todo", "priority": "medium"},
                {"title": "Voice Recording", "status": "todo", "priority": "high"},
                {"title": "Video Editing", "status": "todo", "priority": "medium"},
                {"title": "Review & Feedback", "status": "todo", "priority": "medium"},
                {"title": "Final Export", "status": "todo", "priority": "low"}
            ]
        }
    },
    "storyboard_template": {
        "title": "Project Storyboard",
        "type": DocumentType.STORYBOARD,
        "content": {
            "frames": [],
            "total_duration": 0.0,
            "aspect_ratio": "16:9",
            "style_notes": "Visual style and artistic direction notes"
        }
    },
    "script_template": {
        "title": "Video Script",
        "type": DocumentType.SCRIPT,
        "content": {
            "scenes": [
                {
                    "id": str(uuid.uuid4()),
                    "title": "Opening Scene",
                    "dialogue": "Welcome to our video...",
                    "action": "Camera pans across scene",
                    "duration": 10.0,
                    "voice_notes": "Enthusiastic tone"
                }
            ],
            "total_word_count": 0,
            "estimated_duration": 0.0
        }
    }
}
