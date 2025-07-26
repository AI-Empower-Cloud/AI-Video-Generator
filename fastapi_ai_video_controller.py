#!/usr/bin/env python3
"""
FastAPI-Powered AI Video Generator Controller
============================================

Comprehensive controller for AI Video Generation with modular components:
- TTS Engine (Tortoise, Coqui)
- Lip Sync (Wav2Lip)
- Video Composition (ffmpeg, moviepy)
- Audio Editing & Music (pydub, Mubert)
- Subtitles (Whisper)
- Cloud Storage (Wasabi/S3)
"""

import asyncio
import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import uuid

from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# PYDANTIC MODELS
# =============================================================================

class VideoGenerationRequest(BaseModel):
    """Request model for video generation"""
    text: str = Field(..., description="Text to convert to video")
    voice_model: str = Field(default="tortoise", description="TTS model to use")
    video_style: str = Field(default="default", description="Video style")
    add_music: bool = Field(default=True, description="Add background music")
    add_subtitles: bool = Field(default=True, description="Add subtitles")
    output_format: str = Field(default="mp4", description="Output video format")
    resolution: str = Field(default="1920x1080", description="Video resolution")

class VideoGenerationResponse(BaseModel):
    """Response model for video generation"""
    task_id: str
    status: str
    message: str
    estimated_time: Optional[int] = None

class TaskStatus(BaseModel):
    """Task status model"""
    task_id: str
    status: str
    progress: float
    current_step: str
    output_url: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class DocumentRequest(BaseModel):
    """Request model for creating documents"""
    title: str = Field(..., description="Document title")
    doc_type: str = Field(..., description="Document type")
    project_id: str = Field(..., description="Project ID")
    author: str = Field(default="user", description="Document author")
    content: Optional[Dict[str, Any]] = Field(default=None, description="Document content")

class TaskRequest(BaseModel):
    """Request model for creating tasks"""
    title: str = Field(..., description="Task title")
    description: str = Field(default="", description="Task description")
    assignee: Optional[str] = Field(default=None, description="Task assignee")
    due_date: Optional[str] = Field(default=None, description="Due date (ISO format)")
    priority: str = Field(default="medium", description="Task priority")

class CommentRequest(BaseModel):
    """Request model for adding comments"""
    content: str = Field(..., description="Comment content")
    author: str = Field(default="user", description="Comment author")
    parent_id: Optional[str] = Field(default=None, description="Parent comment ID")
    element_id: Optional[str] = Field(default=None, description="Canvas element ID")

class StoryboardFrameRequest(BaseModel):
    """Request model for storyboard frames"""
    title: str = Field(..., description="Frame title")
    description: str = Field(..., description="Frame description")
    duration: float = Field(..., description="Frame duration in seconds")
    sequence: int = Field(..., description="Frame sequence number")
    thumbnail_data: Optional[str] = Field(default=None, description="Base64 thumbnail data")

class VideoPreviewRequest(BaseModel):
    """Request model for video preview generation"""
    project_id: str = Field(..., description="Project ID")
    canvas_project_id: str = Field(..., description="Canvas project ID")
    preview_type: str = Field(default="thumbnail", description="Preview type")
    quality: str = Field(default="medium", description="Preview quality")

# =============================================================================
# FASTAPI APPLICATION
# =============================================================================

app = FastAPI(
    title="AI Video Generator API",
    description="Comprehensive AI Video Generation Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# =============================================================================
# GLOBAL VARIABLES
# =============================================================================

# Task storage (in production, use Redis or database)
tasks: Dict[str, TaskStatus] = {}

# =============================================================================
# AI VIDEO GENERATOR CLASS
# =============================================================================

class AIVideoGenerator:
    """Main AI Video Generator class with modular components"""
    
    def __init__(self):
        self.tts_engines = {
            "tortoise": self._init_tortoise_tts,
            "coqui": self._init_coqui_tts,
            "edge": self._init_edge_tts
        }
        self.lip_sync_model = None
        self.video_composer = None
        self.audio_processor = None
        self.subtitle_generator = None
        self.cloud_storage = None
        self.freesound_integrator = None
        
        # Initialize components
        self._init_components()
        
    def _init_components(self):
        """Initialize all components"""
        try:
            from modules import (
                AudioProcessor, 
                CloudStorage, 
                FreesoundIntegrator,
                SubtitleGenerator,
                VideoComposer
            )
            
            self.audio_processor = AudioProcessor()
            self.cloud_storage = CloudStorage()
            self.freesound_integrator = FreesoundIntegrator()
            self.subtitle_generator = SubtitleGenerator()
            self.video_composer = VideoComposer()
            
            logger.info("All components initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
        
    def _init_tortoise_tts(self):
        """Initialize Tortoise TTS"""
        try:
            logger.info("Initializing Tortoise TTS...")
            # Import and initialize Tortoise TTS
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Tortoise TTS: {e}")
            return False
    
    def _init_coqui_tts(self):
        """Initialize Coqui TTS"""
        try:
            logger.info("Initializing Coqui TTS...")
            # Import and initialize Coqui TTS
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Coqui TTS: {e}")
            return False
    
    def _init_edge_tts(self):
        """Initialize Edge TTS"""
        try:
            logger.info("Initializing Edge TTS...")
            # Import and initialize Edge TTS
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Edge TTS: {e}")
            return False
    
    async def generate_video(self, request: VideoGenerationRequest, task_id: str):
        """Main video generation pipeline"""
        try:
            # Update task status
            tasks[task_id].status = "processing"
            tasks[task_id].current_step = "Initializing"
            tasks[task_id].progress = 0.0
            
            # Step 1: Text-to-Speech
            tasks[task_id].current_step = "Generating speech"
            tasks[task_id].progress = 20.0
            audio_path = await self._generate_speech(request.text, request.voice_model)
            
            # Step 2: Generate visuals/avatars
            tasks[task_id].current_step = "Generating visuals"
            tasks[task_id].progress = 40.0
            visual_path = await self._generate_visuals(request.text, request.video_style)
            
            # Step 3: Lip sync
            tasks[task_id].current_step = "Applying lip sync"
            tasks[task_id].progress = 60.0
            synced_video_path = await self._apply_lip_sync(visual_path, audio_path)
            
            # Step 4: Add music
            if request.add_music:
                tasks[task_id].current_step = "Adding background music"
                tasks[task_id].progress = 75.0
                synced_video_path = await self._add_background_music(synced_video_path)
            
            # Step 5: Add subtitles
            if request.add_subtitles:
                tasks[task_id].current_step = "Adding subtitles"
                tasks[task_id].progress = 85.0
                synced_video_path = await self._add_subtitles(synced_video_path, request.text)
            
            # Step 6: Final composition
            tasks[task_id].current_step = "Final composition"
            tasks[task_id].progress = 95.0
            final_video_path = await self._compose_final_video(synced_video_path, request)
            
            # Step 7: Upload to cloud storage
            tasks[task_id].current_step = "Uploading to cloud"
            tasks[task_id].progress = 100.0
            cloud_url = await self._upload_to_cloud(final_video_path, task_id)
            
            # Update task completion
            tasks[task_id].status = "completed"
            tasks[task_id].output_url = cloud_url
            tasks[task_id].updated_at = datetime.now()
            
            logger.info(f"Video generation completed for task {task_id}")
            
        except Exception as e:
            logger.error(f"Video generation failed for task {task_id}: {e}")
            tasks[task_id].status = "failed"
            tasks[task_id].error = str(e)
            tasks[task_id].updated_at = datetime.now()
    
    async def _generate_speech(self, text: str, voice_model: str) -> str:
        """Generate speech from text"""
        # Implement TTS generation
        await asyncio.sleep(2)  # Simulate processing
        return f"output/audio_{uuid.uuid4().hex}.wav"
    
    async def _generate_visuals(self, text: str, style: str) -> str:
        """Generate visuals/avatars"""
        # Implement visual generation
        await asyncio.sleep(2)  # Simulate processing
        return f"output/visual_{uuid.uuid4().hex}.mp4"
    
    async def _apply_lip_sync(self, visual_path: str, audio_path: str) -> str:
        """Apply lip sync using Wav2Lip"""
        # Implement Wav2Lip integration
        await asyncio.sleep(3)  # Simulate processing
        return f"output/synced_{uuid.uuid4().hex}.mp4"
    
    async def _add_background_music(self, video_path: str) -> str:
        """Add background music"""
        # Implement music addition
        await asyncio.sleep(1)  # Simulate processing
        return f"output/music_{uuid.uuid4().hex}.mp4"
    
    async def _add_subtitles(self, video_path: str, text: str) -> str:
        """Add subtitles to video"""
        # Implement subtitle generation
        await asyncio.sleep(1)  # Simulate processing
        return f"output/subtitled_{uuid.uuid4().hex}.mp4"
    
    async def _compose_final_video(self, video_path: str, request: VideoGenerationRequest) -> str:
        """Compose final video with all elements"""
        # Implement final composition
        await asyncio.sleep(2)  # Simulate processing
        return f"output/final_{uuid.uuid4().hex}.mp4"
    
    async def _upload_to_cloud(self, video_path: str, task_id: str) -> str:
        """Upload video to Wasabi/S3"""
        # Implement cloud upload
        await asyncio.sleep(1)  # Simulate processing
        return f"https://wasabi.example.com/videos/{task_id}.mp4"

# Initialize the generator
video_generator = AIVideoGenerator()

# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Video Generator API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "generate": "/generate",
            "status": "/status/{task_id}",
            "download": "/download/{task_id}",
            "docs": "/docs"
        }
    }

@app.post("/generate", response_model=VideoGenerationResponse)
async def generate_video(
    request: VideoGenerationRequest,
    background_tasks: BackgroundTasks
):
    """Generate AI video from text"""
    try:
        # Generate unique task ID
        task_id = str(uuid.uuid4())
        
        # Create task status
        tasks[task_id] = TaskStatus(
            task_id=task_id,
            status="queued",
            progress=0.0,
            current_step="Queued",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Add background task
        background_tasks.add_task(
            video_generator.generate_video,
            request,
            task_id
        )
        
        return VideoGenerationResponse(
            task_id=task_id,
            status="queued",
            message="Video generation started",
            estimated_time=300  # 5 minutes estimate
        )
        
    except Exception as e:
        logger.error(f"Failed to start video generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status/{task_id}", response_model=TaskStatus)
async def get_task_status(task_id: str):
    """Get task status"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return tasks[task_id]

@app.get("/download/{task_id}")
async def download_video(task_id: str):
    """Download generated video"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks[task_id]
    
    if task.status != "completed":
        raise HTTPException(status_code=400, detail="Video not ready")
    
    if not task.output_url:
        raise HTTPException(status_code=404, detail="Video file not found")
    
    return {"download_url": task.output_url}

@app.get("/tasks")
async def list_tasks():
    """List all tasks"""
    return {"tasks": list(tasks.values())}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """Delete a task"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    del tasks[task_id]
    return {"message": "Task deleted successfully"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_tasks": len([t for t in tasks.values() if t.status == "processing"]),
        "total_tasks": len(tasks)
    }

@app.get("/search/music")
async def search_music(
    genre: Optional[str] = None,
    mood: Optional[str] = None,
    duration_min: Optional[int] = None,
    duration_max: Optional[int] = None,
    limit: int = 10
):
    """Search for music on Freesound.org"""
    try:
        if not video_generator.freesound_integrator:
            raise HTTPException(status_code=503, detail="Freesound integration not available")
        
        results = await video_generator.freesound_integrator.search_music(
            genre=genre,
            mood=mood,
            duration_min=duration_min,
            duration_max=duration_max,
            limit=limit
        )
        
        return {
            "query": {
                "genre": genre,
                "mood": mood,
                "duration_min": duration_min,
                "duration_max": duration_max
            },
            "results": results,
            "count": len(results)
        }
        
    except Exception as e:
        logger.error(f"Music search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search/sfx")
async def search_sfx(
    category: str,
    tags: Optional[str] = None,
    limit: int = 10
):
    """Search for sound effects on Freesound.org"""
    try:
        if not video_generator.freesound_integrator:
            raise HTTPException(status_code=503, detail="Freesound integration not available")
        
        tag_list = tags.split(",") if tags else None
        
        results = await video_generator.freesound_integrator.search_sfx(
            category=category,
            tags=tag_list,
            limit=limit
        )
        
        return {
            "query": {
                "category": category,
                "tags": tag_list
            },
            "results": results,
            "count": len(results)
        }
        
    except Exception as e:
        logger.error(f"SFX search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/audio/mix")
async def mix_audio(
    voice_file: UploadFile = File(...),
    music_file: UploadFile = File(...),
    music_volume: float = 0.3,
    voice_volume: float = 1.0,
    fade_in_duration: int = 2000,
    fade_out_duration: int = 2000
):
    """Mix voice and music files with volume balancing"""
    try:
        if not video_generator.freesound_integrator:
            raise HTTPException(status_code=503, detail="Audio processing not available")
        
        # Save uploaded files
        voice_path = f"temp/voice_{uuid.uuid4().hex}.wav"
        music_path = f"temp/music_{uuid.uuid4().hex}.wav"
        
        with open(voice_path, "wb") as f:
            f.write(await voice_file.read())
        
        with open(music_path, "wb") as f:
            f.write(await music_file.read())
        
        # Mix audio
        mixed_path = await video_generator.freesound_integrator.mix_with_voice(
            voice_path=voice_path,
            music_path=music_path,
            music_volume=music_volume,
            voice_volume=voice_volume,
            fade_in_duration=fade_in_duration,
            fade_out_duration=fade_out_duration
        )
        
        # Upload to cloud storage
        if video_generator.cloud_storage:
            cloud_url = await video_generator.cloud_storage.upload_file(
                mixed_path,
                f"mixed_audio/{uuid.uuid4().hex}.wav",
                public_read=True
            )
            
            # Cleanup local files
            for path in [voice_path, music_path, mixed_path]:
                if os.path.exists(path):
                    os.remove(path)
            
            return {
                "message": "Audio mixed successfully",
                "download_url": cloud_url,
                "settings": {
                    "music_volume": music_volume,
                    "voice_volume": voice_volume,
                    "fade_in_duration": fade_in_duration,
                    "fade_out_duration": fade_out_duration
                }
            }
        else:
            return FileResponse(
                mixed_path,
                filename="mixed_audio.wav",
                media_type="audio/wav"
            )
        
    except Exception as e:
        logger.error(f"Audio mixing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# CANVAS VISUAL EDITOR MODELS
# =============================================================================

from dataclasses import dataclass, asdict

@dataclass
class CanvasElement:
    """Canvas element for visual editor"""
    id: str
    type: str  # 'text', 'image', 'video', 'audio'
    x: float
    y: float
    width: float
    height: float
    start_time: float
    duration: float
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

class CreateCanvasProjectRequest(BaseModel):
    """Canvas project creation request"""
    name: str = Field(..., description="Project name")
    width: int = Field(default=1920, description="Canvas width")
    height: int = Field(default=1080, description="Canvas height")
    fps: int = Field(default=30, description="Frames per second")
    duration: float = Field(default=30.0, description="Duration in seconds")

class AddCanvasElementRequest(BaseModel):
    """Add element to canvas request"""
    project_id: str
    element_type: str
    x: float = 0
    y: float = 0
    width: float = 100
    height: float = 100
    start_time: float = 0.0
    duration: float = 5.0
    layer: int = 1
    properties: Dict[str, Any] = {}

# Canvas storage (in production, use database)
canvas_projects: Dict[str, CanvasProject] = {}

# =============================================================================
# CANVAS VISUAL EDITOR CLASS
# =============================================================================

class CanvasEditor:
    """Canvas-like visual video editor"""
    
    def __init__(self):
        self.projects = canvas_projects
        self.assets_dir = "canvas_assets"
        os.makedirs(self.assets_dir, exist_ok=True)
    
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
        logger.info(f"Created canvas project: {name}")
        return project
    
    def add_text_element(self, project_id: str, text: str, x: float, y: float,
                        font_size: int = 24, **kwargs) -> CanvasElement:
        """Add a text element to the canvas"""
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        
        element_id = str(uuid.uuid4())
        now = datetime.now()
        
        element = CanvasElement(
            id=element_id,
            type="text",
            x=x,
            y=y,
            width=len(text) * font_size * 0.6,  # Estimated width
            height=font_size * 1.2,  # Estimated height
            start_time=kwargs.get("start_time", 0.0),
            duration=kwargs.get("duration", 5.0),
            layer=kwargs.get("layer", 1),
            properties={
                "text": text,
                "font_size": font_size,
                "font_family": kwargs.get("font_family", "Arial"),
                "color": kwargs.get("color", "#FFFFFF"),
                "text_align": kwargs.get("text_align", "left")
            },
            created_at=now,
            updated_at=now
        )
        
        self.projects[project_id].elements.append(element)
        self.projects[project_id].updated_at = now
        return element
    
    def add_image_element(self, project_id: str, image_path: str, x: float, y: float,
                         width: float, height: float, **kwargs) -> CanvasElement:
        """Add an image element to the canvas"""
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        
        element_id = str(uuid.uuid4())
        now = datetime.now()
        
        element = CanvasElement(
            id=element_id,
            type="image",
            x=x,
            y=y,
            width=width,
            height=height,
            start_time=kwargs.get("start_time", 0.0),
            duration=kwargs.get("duration", 5.0),
            layer=kwargs.get("layer", 1),
            properties={
                "source": image_path,
                "opacity": kwargs.get("opacity", 1.0),
                "rotation": kwargs.get("rotation", 0)
            },
            created_at=now,
            updated_at=now
        )
        
        self.projects[project_id].elements.append(element)
        self.projects[project_id].updated_at = now
        return element
    
    def get_project_timeline(self, project_id: str) -> Dict[str, Any]:
        """Get timeline data for a project"""
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        
        project = self.projects[project_id]
        timeline = {
            "duration": project.duration,
            "fps": project.fps,
            "tracks": {}
        }
        
        # Group elements by layer
        for element in project.elements:
            layer = element.layer
            if layer not in timeline["tracks"]:
                timeline["tracks"][layer] = {"layer": layer, "elements": []}
            
            timeline["tracks"][layer]["elements"].append({
                "id": element.id,
                "type": element.type,
                "start": element.start_time,
                "duration": element.duration,
                "properties": element.properties
            })
        
        return timeline

# Initialize Canvas Editor with enhanced features
try:
    from modules.canvas_editor import CanvasEditor as EnhancedCanvasEditor
    canvas_editor = EnhancedCanvasEditor()
    logger.info("✅ Enhanced Canvas Editor loaded successfully")
except ImportError as e:
    logger.warning(f"Could not load enhanced canvas editor: {e}")
    # Fallback to basic canvas editor
    canvas_editor = CanvasEditor()

# Initialize Notion-like Planner
try:
    from modules.notion_planner import NotionLikePlanner
    from modules.notion_planner import DocumentType as NotionDocumentType
    from modules.notion_planner import TaskStatus as NotionTaskStatus
    notion_planner = NotionLikePlanner()
    logger.info("✅ Notion-like Planner loaded successfully")
except ImportError as e:
    logger.warning(f"Could not load notion planner: {e}")
    notion_planner = None

# Canvas templates
CANVAS_TEMPLATES = {
    "social_media_post": {
        "name": "Social Media Post",
        "width": 1080,
        "height": 1080,
        "duration": 15.0
    },
    "youtube_intro": {
        "name": "YouTube Intro", 
        "width": 1920,
        "height": 1080,
        "duration": 10.0
    },
    "educational_video": {
        "name": "Educational Video",
        "width": 1920,
        "height": 1080,
        "duration": 300.0
    }
}

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    # Create output directory
    os.makedirs("output", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    
    # Run the FastAPI server
    uvicorn.run(
        "fastapi_ai_video_controller:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

# =============================================================================
# CANVAS VISUAL EDITOR ENDPOINTS
# =============================================================================

@app.post("/canvas/projects", response_model=Dict[str, Any])
async def create_canvas_project(request: CreateCanvasProjectRequest):
    """Create a new canvas project"""
    try:
        project = canvas_editor.create_project(
            name=request.name,
            width=request.width,
            height=request.height,
            fps=request.fps,
            duration=request.duration
        )
        
        return {
            "success": True,
            "project": {
                "id": project.id,
                "name": project.name,
                "width": project.width,
                "height": project.height,
                "fps": project.fps,
                "duration": project.duration,
                "created_at": project.created_at.isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Failed to create canvas project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/canvas/projects", response_model=List[Dict[str, Any]])
async def list_canvas_projects():
    """List all canvas projects"""
    try:
        projects = []
        for project in canvas_projects.values():
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
    except Exception as e:
        logger.error(f"Failed to list canvas projects: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/canvas/projects/{project_id}", response_model=Dict[str, Any])
async def get_canvas_project(project_id: str):
    """Get a specific canvas project"""
    try:
        if project_id not in canvas_projects:
            raise HTTPException(status_code=404, detail="Project not found")
        
        project = canvas_projects[project_id]
        timeline = canvas_editor.get_project_timeline(project_id)
        
        return {
            "project": {
                "id": project.id,
                "name": project.name,
                "width": project.width,
                "height": project.height,
                "fps": project.fps,
                "duration": project.duration,
                "elements": [
                    {
                        "id": elem.id,
                        "type": elem.type,
                        "x": elem.x,
                        "y": elem.y,
                        "width": elem.width,
                        "height": elem.height,
                        "start_time": elem.start_time,
                        "duration": elem.duration,
                        "layer": elem.layer,
                        "properties": elem.properties
                    }
                    for elem in project.elements
                ],
                "created_at": project.created_at.isoformat(),
                "updated_at": project.updated_at.isoformat()
            },
            "timeline": timeline
        }
    except Exception as e:
        logger.error(f"Failed to get canvas project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/canvas/elements/text", response_model=Dict[str, Any])
async def add_text_element_to_canvas(
    project_id: str = Form(...),
    text: str = Form(...),
    x: float = Form(0),
    y: float = Form(0),
    font_size: int = Form(24),
    font_family: str = Form("Arial"),
    color: str = Form("#FFFFFF"),
    start_time: float = Form(0.0),
    duration: float = Form(5.0),
    layer: int = Form(2)
):
    """Add a text element to the canvas"""
    try:
        element = canvas_editor.add_text_element(
            project_id=project_id,
            text=text,
            x=x,
            y=y,
            font_size=font_size,
            font_family=font_family,
            color=color,
            start_time=start_time,
            duration=duration,
            layer=layer
        )
        
        return {
            "success": True,
            "element": {
                "id": element.id,
                "type": element.type,
                "x": element.x,
                "y": element.y,
                "width": element.width,
                "height": element.height,
                "start_time": element.start_time,
                "duration": element.duration,
                "layer": element.layer,
                "properties": element.properties
            }
        }
    except Exception as e:
        logger.error(f"Failed to add text element: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/canvas/elements/upload")
async def upload_canvas_asset(
    project_id: str = Form(...),
    file: UploadFile = File(...),
    x: float = Form(0),
    y: float = Form(0),
    width: float = Form(300),
    height: float = Form(200),
    start_time: float = Form(0.0),
    duration: float = Form(5.0),
    layer: int = Form(1)
):
    """Upload and add an asset to the canvas"""
    try:
        # Save uploaded file
        file_ext = os.path.splitext(file.filename)[1].lower()
        filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(canvas_editor.assets_dir, filename)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Add element to canvas
        if file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            element = canvas_editor.add_image_element(
                project_id=project_id,
                image_path=file_path,
                x=x, y=y, width=width, height=height,
                start_time=start_time, duration=duration, layer=layer
            )
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        return {
            "success": True,
            "asset_path": file_path,
            "element": {
                "id": element.id,
                "type": element.type,
                "properties": element.properties
            }
        }
    except Exception as e:
        logger.error(f"Failed to upload canvas asset: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/canvas/timeline/{project_id}", response_model=Dict[str, Any])
async def get_canvas_timeline(project_id: str):
    """Get timeline data for a canvas project"""
    try:
        timeline = canvas_editor.get_project_timeline(project_id)
        return {"success": True, "timeline": timeline}
    except Exception as e:
        logger.error(f"Failed to get canvas timeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/canvas/templates", response_model=Dict[str, Any])
async def get_canvas_templates():
    """Get available canvas templates"""
    return {"success": True, "templates": CANVAS_TEMPLATES}

@app.post("/canvas/templates/{template_name}")
async def create_canvas_from_template(template_name: str, project_name: str = "New Project"):
    """Create a canvas project from template"""
    try:
        if template_name not in CANVAS_TEMPLATES:
            raise HTTPException(status_code=404, detail="Template not found")
        
        template = CANVAS_TEMPLATES[template_name]
        
        project = canvas_editor.create_project(
            name=project_name,
            width=template["width"],
            height=template["height"],
            duration=template["duration"]
        )
        
        return {
            "success": True,
            "project": {
                "id": project.id,
                "name": project.name,
                "template": template_name
            }
        }
    except Exception as e:
        logger.error(f"Failed to create from template: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# ADVANCED CANVAS EDITOR ENDPOINTS
# =============================================================================

class AddKeyframeRequest(BaseModel):
    """Add animation keyframe request"""
    project_id: str
    element_id: str
    time: float
    property: str
    value: Any
    easing: str = "linear"

class AddTransitionRequest(BaseModel):
    """Add transition request"""
    project_id: str
    transition_type: str
    duration: float
    start_time: float
    from_element: str
    to_element: str
    properties: Dict[str, Any] = {}

class ExportVideoRequest(BaseModel):
    """Export video request"""
    project_id: str
    output_path: Optional[str] = None
    quality: str = "medium"  # low, medium, high, ultra

@app.post("/canvas/keyframes", response_model=Dict[str, Any])
async def add_keyframe(request: AddKeyframeRequest):
    """Add animation keyframe to element"""
    try:
        success = canvas_editor.add_keyframe(
            project_id=request.project_id,
            element_id=request.element_id,
            time=request.time,
            property=request.property,
            value=request.value,
            easing=request.easing
        )
        
        return {
            "success": success,
            "message": "Keyframe added successfully"
        }
    except Exception as e:
        logger.error(f"Failed to add keyframe: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/canvas/transitions", response_model=Dict[str, Any])
async def add_transition(request: AddTransitionRequest):
    """Add transition between elements"""
    try:
        transition = canvas_editor.add_transition(
            project_id=request.project_id,
            transition_type=request.transition_type,
            duration=request.duration,
            start_time=request.start_time,
            from_element=request.from_element,
            to_element=request.to_element,
            properties=request.properties
        )
        
        return {
            "success": True,
            "transition": {
                "id": transition.id,
                "type": transition.type,
                "duration": transition.duration
            }
        }
    except Exception as e:
        logger.error(f"Failed to add transition: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/canvas/export", response_model=Dict[str, Any])
async def export_canvas_video(request: ExportVideoRequest, background_tasks: BackgroundTasks):
    """Export canvas project to video"""
    try:
        task_id = str(uuid.uuid4())
        
        # Create background task for video export
        background_tasks.add_task(
            export_video_background,
            task_id,
            request.project_id,
            request.output_path,
            request.quality
        )
        
        # Store task status
        tasks[task_id] = TaskStatus(
            task_id=task_id,
            status="processing",
            progress=0.0,
            current_step="Initializing video export",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        return {
            "success": True,
            "task_id": task_id,
            "message": "Video export started"
        }
    except Exception as e:
        logger.error(f"Failed to start video export: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/canvas/waveform/{audio_file}")
async def get_audio_waveform(audio_file: str, width: int = 800, height: int = 100):
    """Generate waveform visualization for audio file"""
    try:
        # Construct audio file path
        audio_path = os.path.join("canvas_assets", "audio", audio_file)
        
        if not os.path.exists(audio_path):
            raise HTTPException(status_code=404, detail="Audio file not found")
        
        waveform_data = canvas_editor.generate_waveform_data(
            audio_path=audio_path,
            width=width,
            height=height
        )
        
        return {
            "success": True,
            "waveform": waveform_data,
            "width": width,
            "height": height
        }
    except Exception as e:
        logger.error(f"Failed to generate waveform: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/canvas/elements/{element_id}", response_model=Dict[str, Any])
async def update_canvas_element(
    element_id: str,
    project_id: str = Form(...),
    updates: str = Form(...)  # JSON string of updates
):
    """Update canvas element properties"""
    try:
        updates_dict = json.loads(updates)
        
        updated_element = canvas_editor.update_element(
            project_id=project_id,
            element_id=element_id,
            updates=updates_dict
        )
        
        return {
            "success": True,
            "element": {
                "id": updated_element.id,
                "type": updated_element.type,
                "updated_at": updated_element.updated_at.isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Failed to update element: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/canvas/elements/{element_id}")
async def delete_canvas_element(element_id: str, project_id: str):
    """Delete canvas element"""
    try:
        success = canvas_editor.delete_element(
            project_id=project_id,
            element_id=element_id
        )
        
        return {
            "success": success,
            "message": "Element deleted successfully" if success else "Element not found"
        }
    except Exception as e:
        logger.error(f"Failed to delete element: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/canvas/elements/{element_id}/duplicate")
async def duplicate_canvas_element(
    element_id: str,
    project_id: str = Form(...),
    offset_x: float = Form(50),
    offset_y: float = Form(50)
):
    """Duplicate canvas element"""
    try:
        new_element = canvas_editor.duplicate_element(
            project_id=project_id,
            element_id=element_id,
            offset_x=offset_x,
            offset_y=offset_y
        )
        
        return {
            "success": True,
            "new_element": {
                "id": new_element.id,
                "type": new_element.type,
                "x": new_element.x,
                "y": new_element.y
            }
        }
    except Exception as e:
        logger.error(f"Failed to duplicate element: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/canvas/projects/{project_id}/arrange")
async def auto_arrange_elements(project_id: str, arrangement: str = "sequence"):
    """Auto-arrange elements on timeline"""
    try:
        success = canvas_editor.auto_arrange_elements(
            project_id=project_id,
            arrangement=arrangement
        )
        
        return {
            "success": success,
            "arrangement": arrangement,
            "message": f"Elements arranged in {arrangement} mode"
        }
    except Exception as e:
        logger.error(f"Failed to arrange elements: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def export_video_background(task_id: str, project_id: str, 
                                output_path: Optional[str], quality: str):
    """Background task for video export"""
    try:
        # Update task status
        tasks[task_id].status = "processing"
        tasks[task_id].current_step = "Preparing video export"
        tasks[task_id].progress = 10.0
        tasks[task_id].updated_at = datetime.now()
        
        # Export video
        output_file = await canvas_editor.export_to_video(
            project_id=project_id,
            output_path=output_path,
            quality=quality
        )
        
        # Update task status - success
        tasks[task_id].status = "completed"
        tasks[task_id].current_step = "Video export completed"
        tasks[task_id].progress = 100.0
        tasks[task_id].output_url = f"/static/renders/{os.path.basename(output_file)}"
        tasks[task_id].updated_at = datetime.now()
        
    except Exception as e:
        # Update task status - error
        tasks[task_id].status = "failed"
        tasks[task_id].current_step = "Video export failed"
        tasks[task_id].error = str(e)
        tasks[task_id].updated_at = datetime.now()
        logger.error(f"Video export failed for task {task_id}: {e}")

# =============================================================================
# AI TEXT-TO-VIDEO INTEGRATION WITH CANVAS
# =============================================================================

class AIVideoRequest(BaseModel):
    """AI-powered video creation request"""
    text: str = Field(..., description="Text to convert to video")
    project_id: Optional[str] = Field(None, description="Existing canvas project ID")
    voice_model: str = Field(default="xtts", description="TTS model")
    add_lip_sync: bool = Field(default=True, description="Add lip sync")
    add_music: bool = Field(default=True, description="Add background music")
    style: str = Field(default="professional", description="Video style")

@app.post("/canvas/ai-video", response_model=Dict[str, Any])
async def create_ai_video_in_canvas(request: AIVideoRequest, background_tasks: BackgroundTasks):
    """Create AI-generated video content in canvas project"""
    try:
        task_id = str(uuid.uuid4())
        
        # Create new project if not provided
        if not request.project_id:
            project = canvas_editor.create_project(
                name=f"AI Video - {datetime.now().strftime('%Y%m%d_%H%M')}",
                duration=60.0  # Default 60 seconds
            )
            project_id = project.id
        else:
            project_id = request.project_id
        
        # Start background AI video generation
        background_tasks.add_task(
            generate_ai_video_background,
            task_id,
            project_id,
            request
        )
        
        # Store task status
        tasks[task_id] = TaskStatus(
            task_id=task_id,
            status="processing",
            progress=0.0,
            current_step="Starting AI video generation",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        return {
            "success": True,
            "task_id": task_id,
            "project_id": project_id,
            "message": "AI video generation started"
        }
    except Exception as e:
        logger.error(f"Failed to start AI video generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def generate_ai_video_background(task_id: str, project_id: str, request: AIVideoRequest):
    """Background task for AI video generation"""
    try:
        # Update progress: TTS generation
        tasks[task_id].current_step = "Generating speech audio"
        tasks[task_id].progress = 20.0
        tasks[task_id].updated_at = datetime.now()
        
        # TODO: Integrate with existing TTS modules
        # For now, add placeholder elements
        
        # Add text element
        canvas_editor.add_text_element(
            project_id=project_id,
            text=request.text,
            x=100,
            y=100,
            font_size=32,
            color="#FFFFFF"
        )
        
        # Update progress: Video generation
        tasks[task_id].current_step = "Creating video elements"
        tasks[task_id].progress = 60.0
        tasks[task_id].updated_at = datetime.now()
        
        # Add background
        # TODO: Generate or select appropriate background
        
        # Update progress: Audio integration
        tasks[task_id].current_step = "Integrating audio elements"
        tasks[task_id].progress = 80.0
        tasks[task_id].updated_at = datetime.now()
        
        # TODO: Add generated audio to canvas
        
        # Complete
        tasks[task_id].status = "completed"
        tasks[task_id].current_step = "AI video generation completed"
        tasks[task_id].progress = 100.0
        tasks[task_id].updated_at = datetime.now()
        
    except Exception as e:
        tasks[task_id].status = "failed"
        tasks[task_id].error = str(e)
        tasks[task_id].updated_at = datetime.now()
        logger.error(f"AI video generation failed for task {task_id}: {e}")

# =============================================================================
# NOTION-LIKE PLANNER MODELS
# =============================================================================

class DocumentRequest(BaseModel):
    """Request model for creating documents"""
    title: str = Field(..., description="Document title")
    doc_type: str = Field(..., description="Document type")
    project_id: str = Field(..., description="Project ID")
    author: str = Field(default="user", description="Document author")
    content: Optional[Dict[str, Any]] = Field(default=None, description="Document content")

class TaskRequest(BaseModel):
    """Request model for creating tasks"""
    title: str = Field(..., description="Task title")
    description: str = Field(default="", description="Task description")
    assignee: Optional[str] = Field(default=None, description="Task assignee")
    due_date: Optional[str] = Field(default=None, description="Due date (ISO format)")
    priority: str = Field(default="medium", description="Task priority")

class CommentRequest(BaseModel):
    """Request model for adding comments"""
    content: str = Field(..., description="Comment content")
    author: str = Field(default="user", description="Comment author")
    parent_id: Optional[str] = Field(default=None, description="Parent comment ID")
    element_id: Optional[str] = Field(default=None, description="Canvas element ID")

class StoryboardFrameRequest(BaseModel):
    """Request model for storyboard frames"""
    title: str = Field(..., description="Frame title")
    description: str = Field(..., description="Frame description")
    duration: float = Field(..., description="Frame duration in seconds")
    sequence: int = Field(..., description="Frame sequence number")
    thumbnail_data: Optional[str] = Field(default=None, description="Base64 thumbnail data")

class VideoPreviewRequest(BaseModel):
    """Request model for video preview generation"""
    project_id: str = Field(..., description="Project ID")
    canvas_project_id: str = Field(..., description="Canvas project ID")
    preview_type: str = Field(default="thumbnail", description="Preview type")
    quality: str = Field(default="medium", description="Preview quality")

# =============================================================================
# NOTION-LIKE PLANNER ENDPOINTS
# =============================================================================

@app.post("/api/notion/documents", tags=["Notion Planner"])
async def create_document(request: DocumentRequest):
    """Create a new document in the planning system"""
    if not notion_planner:
        raise HTTPException(status_code=503, detail="Notion planner not available")
    
    try:
        # Convert string doc_type to enum
        doc_type = NotionDocumentType(request.doc_type)
        
        document = notion_planner.create_document(
            title=request.title,
            doc_type=doc_type,
            project_id=request.project_id,
            author=request.author,
            content=request.content
        )
        
        return {
            "success": True,
            "document": {
                "id": document.id,
                "title": document.title,
                "type": document.type.value,
                "project_id": document.project_id,
                "author": document.author,
                "created_at": document.created_at.isoformat(),
                "updated_at": document.updated_at.isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Failed to create document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/notion/documents/{project_id}", tags=["Notion Planner"])
async def get_project_documents(project_id: str):
    """Get all documents for a project"""
    if not notion_planner:
        raise HTTPException(status_code=503, detail="Notion planner not available")
    
    try:
        project_docs = [doc for doc in notion_planner.documents.values() 
                       if doc.project_id == project_id]
        
        return {
            "success": True,
            "documents": [
                {
                    "id": doc.id,
                    "title": doc.title,
                    "type": doc.type.value,
                    "author": doc.author,
                    "tags": doc.tags,
                    "comment_count": len(doc.comments),
                    "version": doc.version,
                    "created_at": doc.created_at.isoformat(),
                    "updated_at": doc.updated_at.isoformat()
                }
                for doc in project_docs
            ]
        }
    except Exception as e:
        logger.error(f"Failed to get documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/notion/documents/detail/{doc_id}", tags=["Notion Planner"])
async def get_document_detail(doc_id: str):
    """Get detailed document content"""
    if not notion_planner:
        raise HTTPException(status_code=503, detail="Notion planner not available")
    
    if doc_id not in notion_planner.documents:
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        document = notion_planner.documents[doc_id]
        
        return {
            "success": True,
            "document": {
                "id": document.id,
                "title": document.title,
                "type": document.type.value,
                "content": document.content,
                "project_id": document.project_id,
                "author": document.author,
                "tags": document.tags,
                "version": document.version,
                "comments": [
                    {
                        "id": comment.id,
                        "author": comment.author,
                        "content": comment.content,
                        "timestamp": comment.timestamp.isoformat(),
                        "parent_id": comment.parent_id,
                        "element_id": comment.element_id,
                        "resolved": comment.resolved
                    }
                    for comment in document.comments
                ],
                "created_at": document.created_at.isoformat(),
                "updated_at": document.updated_at.isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Failed to get document detail: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/notion/documents/{doc_id}/comments", tags=["Notion Planner"])
async def add_comment(doc_id: str, request: CommentRequest):
    """Add comment to a document"""
    if not notion_planner:
        raise HTTPException(status_code=503, detail="Notion planner not available")
    
    try:
        comment = notion_planner.add_comment(
            doc_id=doc_id,
            content=request.content,
            author=request.author,
            parent_id=request.parent_id,
            element_id=request.element_id
        )
        
        return {
            "success": True,
            "comment": {
                "id": comment.id,
                "author": comment.author,
                "content": comment.content,
                "timestamp": comment.timestamp.isoformat(),
                "parent_id": comment.parent_id,
                "element_id": comment.element_id
            }
        }
    except Exception as e:
        logger.error(f"Failed to add comment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/notion/tasks", tags=["Notion Planner"])
async def create_task(request: TaskRequest):
    """Create a new task"""
    if not notion_planner:
        raise HTTPException(status_code=503, detail="Notion planner not available")
    
    try:
        due_date = None
        if request.due_date:
            due_date = datetime.fromisoformat(request.due_date)
        
        task = notion_planner.create_task(
            title=request.title,
            description=request.description,
            assignee=request.assignee,
            due_date=due_date,
            priority=request.priority
        )
        
        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status.value,
                "assignee": task.assignee,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "priority": task.priority,
                "tags": task.tags,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Failed to create task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/notion/tasks/{task_id}/status", tags=["Notion Planner"])
async def update_task_status(task_id: str, status: str):
    """Update task status"""
    if not notion_planner:
        raise HTTPException(status_code=503, detail="Notion planner not available")
    
    try:
        task_status = NotionTaskStatus(status)
        updated_task = notion_planner.update_task_status(task_id, task_status)
        
        return {
            "success": True,
            "task": {
                "id": updated_task.id,
                "title": updated_task.title,
                "status": updated_task.status.value,
                "updated_at": updated_task.updated_at.isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Failed to update task status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/notion/tasks", tags=["Notion Planner"])
async def get_all_tasks():
    """Get all tasks"""
    if not notion_planner:
        raise HTTPException(status_code=503, detail="Notion planner not available")
    
    try:
        tasks = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status.value,
                "assignee": task.assignee,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "priority": task.priority,
                "tags": task.tags,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
            for task in notion_planner.tasks.values()
        ]
        
        return {
            "success": True,
            "tasks": tasks
        }
    except Exception as e:
        logger.error(f"Failed to get tasks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/notion/documents/{doc_id}/storyboard/frames", tags=["Notion Planner"])
async def add_storyboard_frame(doc_id: str, request: StoryboardFrameRequest):
    """Add frame to storyboard document"""
    if not notion_planner:
        raise HTTPException(status_code=503, detail="Notion planner not available")
    
    try:
        frame = notion_planner.create_storyboard_frame(
            doc_id=doc_id,
            title=request.title,
            description=request.description,
            duration=request.duration,
            sequence=request.sequence,
            thumbnail_data=request.thumbnail_data
        )
        
        return {
            "success": True,
            "frame": {
                "id": frame.id,
                "sequence": frame.sequence,
                "title": frame.title,
                "description": frame.description,
                "duration": frame.duration,
                "thumbnail_data": frame.thumbnail_data
            }
        }
    except Exception as e:
        logger.error(f"Failed to add storyboard frame: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/notion/previews/generate", tags=["Notion Planner"])
async def generate_video_preview(request: VideoPreviewRequest, background_tasks: BackgroundTasks):
    """Generate video preview for project"""
    if not notion_planner:
        raise HTTPException(status_code=503, detail="Notion planner not available")
    
    try:
        # Start preview generation in background
        async def generate_preview():
            await notion_planner.generate_video_preview_advanced(
                project_id=request.project_id,
                canvas_project_id=request.canvas_project_id,
                preview_type=request.preview_type,
                quality=request.quality
            )
        
        background_tasks.add_task(generate_preview)
        
        return {
            "success": True,
            "message": "Video preview generation started",
            "project_id": request.project_id,
            "canvas_project_id": request.canvas_project_id,
            "preview_type": request.preview_type
        }
    except Exception as e:
        logger.error(f"Failed to start preview generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/notion/dashboard/{project_id}", tags=["Notion Planner"])
async def get_project_dashboard(project_id: str):
    """Get project dashboard with all planning data"""
    if not notion_planner:
        raise HTTPException(status_code=503, detail="Notion planner not available")
    
    try:
        dashboard = notion_planner.get_project_dashboard(project_id)
        collaboration_stats = notion_planner.get_collaboration_stats(project_id)
        
        return {
            "success": True,
            "dashboard": dashboard,
            "collaboration": collaboration_stats
        }
    except Exception as e:
        logger.error(f"Failed to get dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/notion/search", tags=["Notion Planner"])
async def search_documents(query: str, project_id: Optional[str] = None, doc_type: Optional[str] = None):
    """Search documents and content"""
    if not notion_planner:
        raise HTTPException(status_code=503, detail="Notion planner not available")
    
    try:
        notion_doc_type = None
        if doc_type:
            notion_doc_type = NotionDocumentType(doc_type)
        
        results = notion_planner.search_documents(
            query=query,
            project_id=project_id,
            doc_type=notion_doc_type
        )
        
        return {
            "success": True,
            "results": [
                {
                    "id": doc.id,
                    "title": doc.title,
                    "type": doc.type.value,
                    "project_id": doc.project_id,
                    "author": doc.author,
                    "updated_at": doc.updated_at.isoformat()
                }
                for doc in results
            ]
        }
    except Exception as e:
        logger.error(f"Failed to search documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/notion/export/{project_id}", tags=["Notion Planner"])
async def export_project_plan(project_id: str, format: str = "markdown"):
    """Export project plan in specified format"""
    if not notion_planner:
        raise HTTPException(status_code=503, detail="Notion planner not available")
    
    try:
        exported_data = notion_planner.export_project_plan(project_id, format)
        
        if format == "markdown":
            return JSONResponse(
                content={"success": True, "content": exported_data},
                headers={"Content-Type": "text/markdown"}
            )
        else:
            return {
                "success": True,
                "content": exported_data
            }
    except Exception as e:
        logger.error(f"Failed to export project plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/notion/templates/{template_name}", tags=["Notion Planner"])
async def create_from_template(template_name: str, project_id: str, title: Optional[str] = None, author: str = "user"):
    """Create document from predefined template"""
    if not notion_planner:
        raise HTTPException(status_code=503, detail="Notion planner not available")
    
    try:
        document = notion_planner.create_from_template(
            template_name=template_name,
            project_id=project_id,
            author=author,
            title=title or f"New {template_name.replace('_', ' ').title()}"
        )
        
        return {
            "success": True,
            "document": {
                "id": document.id,
                "title": document.title,
                "type": document.type.value,
                "project_id": document.project_id,
                "author": document.author,
                "created_at": document.created_at.isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Failed to create from template: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/notion/templates", tags=["Notion Planner"])
async def get_available_templates():
    """Get list of available document templates"""
    try:
        from modules.notion_planner import DOCUMENT_TEMPLATES
        
        templates = [
            {
                "name": name,
                "title": template["title"],
                "type": template["type"].value,
                "description": f"Template for {name.replace('_', ' ')}"
            }
            for name, template in DOCUMENT_TEMPLATES.items()
        ]
        
        return {
            "success": True,
            "templates": templates
        }
    except Exception as e:
        logger.error(f"Failed to get templates: {e}")
        raise HTTPException(status_code=500, detail=str(e))
