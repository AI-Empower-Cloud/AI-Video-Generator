#!/usr/bin/env python3
"""
🎨 CANVAS API ENDPOINTS
======================

FastAPI endpoints for the Canvas visual video editor:
- Project management
- Element manipulation
- Timeline operations
- Real-time preview
- Video rendering
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field

# Import our canvas modules
from modules.canvas_editor import CanvasEditor, CanvasProject, CanvasElement
from modules.canvas_timeline import CanvasTimeline, TimelineTrack, Keyframe
from modules.canvas_renderer import CanvasRenderer, RenderSettings, QUALITY_PRESETS

logger = logging.getLogger(__name__)

# Initialize Canvas components
canvas_editor = CanvasEditor()
canvas_renderer = CanvasRenderer()

# Create router
router = APIRouter(prefix="/canvas", tags=["canvas"])

# =============================================================================
# PYDANTIC MODELS
# =============================================================================

class CreateProjectRequest(BaseModel):
    name: str = Field(..., description="Project name")
    width: int = Field(default=1920, description="Canvas width")
    height: int = Field(default=1080, description="Canvas height")
    fps: int = Field(default=30, description="Frames per second")
    duration: float = Field(default=30.0, description="Duration in seconds")

class AddElementRequest(BaseModel):
    project_id: str
    element_type: str  # text, image, video, audio, shape
    x: float = 0
    y: float = 0
    width: float = 100
    height: float = 100
    start_time: float = 0.0
    duration: float = 5.0
    layer: int = 1
    properties: Dict[str, Any] = {}

class UpdateElementRequest(BaseModel):
    project_id: str
    element_id: str
    updates: Dict[str, Any]

class AddKeyframeRequest(BaseModel):
    project_id: str
    element_id: str
    time: float
    property: str
    value: Any
    easing: str = "linear"

class RenderRequest(BaseModel):
    project_id: str
    quality: str = "high"  # low, medium, high, ultra
    format: str = "mp4"
    custom_settings: Optional[Dict[str, Any]] = None

# =============================================================================
# PROJECT MANAGEMENT ENDPOINTS
# =============================================================================

@router.post("/projects", response_model=Dict[str, Any])
async def create_project(request: CreateProjectRequest):
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
        logger.error(f"Failed to create project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projects", response_model=List[Dict[str, Any]])
async def list_projects():
    """List all canvas projects"""
    try:
        projects = canvas_editor.list_projects()
        return projects
    except Exception as e:
        logger.error(f"Failed to list projects: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/projects/{project_id}", response_model=Dict[str, Any])
async def get_project(project_id: str):
    """Get a specific project"""
    try:
        project = canvas_editor.load_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Create timeline for this project
        timeline = CanvasTimeline()
        
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
            "timeline": timeline.get_timeline_data(project)
        }
    except Exception as e:
        logger.error(f"Failed to get project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/projects/{project_id}")
async def delete_project(project_id: str):
    """Delete a project"""
    try:
        if project_id in canvas_editor.projects:
            del canvas_editor.projects[project_id]
            
            # Delete project file
            project_file = os.path.join(canvas_editor.projects_dir, f"{project_id}.json")
            if os.path.exists(project_file):
                os.remove(project_file)
            
            return {"success": True, "message": "Project deleted"}
        else:
            raise HTTPException(status_code=404, detail="Project not found")
    except Exception as e:
        logger.error(f"Failed to delete project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# ELEMENT MANAGEMENT ENDPOINTS
# =============================================================================

@router.post("/elements", response_model=Dict[str, Any])
async def add_element(request: AddElementRequest):
    """Add an element to the canvas"""
    try:
        element = canvas_editor.add_element(
            project_id=request.project_id,
            element_type=request.element_type,
            x=request.x,
            y=request.y,
            width=request.width,
            height=request.height,
            start_time=request.start_time,
            duration=request.duration,
            layer=request.layer,
            properties=request.properties
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
        logger.error(f"Failed to add element: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/elements/text", response_model=Dict[str, Any])
async def add_text_element(
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
    """Add a text element with specific properties"""
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

@router.post("/elements/upload")
async def upload_asset(
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
    """Upload and add an asset (image/video/audio)"""
    try:
        # Save uploaded file
        file_ext = os.path.splitext(file.filename)[1].lower()
        asset_type = "image"
        
        if file_ext in ['.mp4', '.avi', '.mov', '.mkv']:
            asset_type = "video"
        elif file_ext in ['.mp3', '.wav', '.aac', '.flac']:
            asset_type = "audio"
        
        # Create asset directory
        asset_dir = os.path.join(canvas_editor.assets_dir, f"{asset_type}s")
        os.makedirs(asset_dir, exist_ok=True)
        
        # Save file
        file_path = os.path.join(asset_dir, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Add element to canvas
        if asset_type == "image":
            element = canvas_editor.add_image_element(
                project_id=project_id,
                image_path=file_path,
                x=x, y=y, width=width, height=height,
                start_time=start_time, duration=duration, layer=layer
            )
        elif asset_type == "video":
            element = canvas_editor.add_video_element(
                project_id=project_id,
                video_path=file_path,
                x=x, y=y, width=width, height=height,
                start_time=start_time, duration=duration, layer=layer
            )
        elif asset_type == "audio":
            element = canvas_editor.add_audio_element(
                project_id=project_id,
                audio_path=file_path,
                start_time=start_time, duration=duration
            )
        
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
        logger.error(f"Failed to upload asset: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/elements", response_model=Dict[str, Any])
async def update_element(request: UpdateElementRequest):
    """Update an element's properties"""
    try:
        element = canvas_editor.update_element(
            project_id=request.project_id,
            element_id=request.element_id,
            updates=request.updates
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
        logger.error(f"Failed to update element: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/elements/{project_id}/{element_id}")
async def delete_element(project_id: str, element_id: str):
    """Delete an element from the canvas"""
    try:
        success = canvas_editor.delete_element(project_id, element_id)
        if success:
            return {"success": True, "message": "Element deleted"}
        else:
            raise HTTPException(status_code=404, detail="Element not found")
    except Exception as e:
        logger.error(f"Failed to delete element: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# TIMELINE & ANIMATION ENDPOINTS
# =============================================================================

@router.get("/timeline/{project_id}", response_model=Dict[str, Any])
async def get_timeline(project_id: str):
    """Get timeline data for a project"""
    try:
        project = canvas_editor.load_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        timeline = CanvasTimeline()
        timeline_data = timeline.get_timeline_data(project)
        
        return {
            "success": True,
            "timeline": timeline_data
        }
    except Exception as e:
        logger.error(f"Failed to get timeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/keyframes", response_model=Dict[str, Any])
async def add_keyframe(request: AddKeyframeRequest):
    """Add an animation keyframe"""
    try:
        # This would be expanded to work with persistent timeline storage
        timeline = CanvasTimeline()
        
        keyframe = timeline.add_keyframe(
            element_id=request.element_id,
            time=request.time,
            property=request.property,
            value=request.value,
            easing=request.easing
        )
        
        return {
            "success": True,
            "keyframe": {
                "time": keyframe.time,
                "property": keyframe.property,
                "value": keyframe.value,
                "easing": keyframe.easing
            }
        }
    except Exception as e:
        logger.error(f"Failed to add keyframe: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# PREVIEW & RENDERING ENDPOINTS
# =============================================================================

@router.get("/preview/{project_id}")
async def generate_preview(project_id: str, time: float = 0.0, quality: str = "medium"):
    """Generate a preview frame at specific time"""
    try:
        project = canvas_editor.load_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        timeline = CanvasTimeline()
        settings = QUALITY_PRESETS.get(quality, QUALITY_PRESETS["medium"])
        
        preview_path = canvas_renderer.generate_preview(project, timeline, time, settings)
        
        if preview_path and os.path.exists(preview_path):
            return FileResponse(preview_path, media_type="image/png")
        else:
            raise HTTPException(status_code=500, detail="Failed to generate preview")
    except Exception as e:
        logger.error(f"Failed to generate preview: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/render")
async def start_render(request: RenderRequest, background_tasks: BackgroundTasks):
    """Start video rendering in background"""
    try:
        project = canvas_editor.load_project(request.project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Get render settings
        settings = QUALITY_PRESETS.get(request.quality, QUALITY_PRESETS["high"])
        
        if request.custom_settings:
            # Apply custom settings
            for key, value in request.custom_settings.items():
                if hasattr(settings, key):
                    setattr(settings, key, value)
        
        # Generate output filename
        output_dir = "renders"
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"{project.name}_{timestamp}.{request.format}")
        
        # Start background render
        background_tasks.add_task(
            render_video_background,
            project, output_path, settings
        )
        
        return {
            "success": True,
            "message": "Render started",
            "output_path": output_path,
            "estimated_duration": "5-10 minutes"
        }
    except Exception as e:
        logger.error(f"Failed to start render: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/render/status")
async def get_render_status():
    """Get current render status"""
    try:
        status = canvas_renderer.get_render_progress()
        return {"success": True, "status": status}
    except Exception as e:
        logger.error(f"Failed to get render status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

async def render_video_background(project, output_path: str, settings: RenderSettings):
    """Background task for video rendering"""
    try:
        timeline = CanvasTimeline()
        success = canvas_renderer.render_project(project, timeline, output_path, settings)
        
        if success:
            logger.info(f"Render completed successfully: {output_path}")
        else:
            logger.error(f"Render failed: {output_path}")
    except Exception as e:
        logger.error(f"Background render error: {e}")

# =============================================================================
# TEMPLATE & PRESET ENDPOINTS
# =============================================================================

@router.get("/templates", response_model=Dict[str, Any])
async def get_templates():
    """Get available project templates"""
    from modules.canvas_editor import CANVAS_TEMPLATES
    
    return {
        "success": True,
        "templates": CANVAS_TEMPLATES
    }

@router.post("/templates/{template_name}")
async def create_from_template(template_name: str, project_name: str = "New Project"):
    """Create a project from template"""
    try:
        from modules.canvas_editor import CANVAS_TEMPLATES
        
        if template_name not in CANVAS_TEMPLATES:
            raise HTTPException(status_code=404, detail="Template not found")
        
        template = CANVAS_TEMPLATES[template_name]
        
        # Create project
        project = canvas_editor.create_project(
            name=project_name,
            width=template["width"],
            height=template["height"],
            duration=template["duration"]
        )
        
        # Add template elements
        for elem_data in template.get("elements", []):
            if elem_data["type"] == "text":
                canvas_editor.add_text_element(
                    project_id=project.id,
                    text=elem_data["text"],
                    x=elem_data["x"],
                    y=elem_data["y"],
                    font_size=elem_data["font_size"],
                    color=elem_data["color"]
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

# Export the router
canvas_router = router
