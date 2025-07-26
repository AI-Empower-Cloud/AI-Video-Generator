# 🧩 API Reference - Canvas Editor

## Class: CanvasEditor

### Initialization
```python
from core.models import *
from core.base import BaseCanvasEditor

editor = CanvasEditor(projects_dir="canvas_projects")
```

## Project Management

### create_project()
Creates a new canvas project.

**Parameters:**
- `name` (str): Project name
- `width` (int, optional): Canvas width in pixels (default: 1920)
- `height` (int, optional): Canvas height in pixels (default: 1080) 
- `fps` (int, optional): Frames per second (default: 30)
- `duration` (float, optional): Project duration in seconds (default: 30.0)

**Returns:** `CanvasProject` object

**Example:**
```python
project = editor.create_project(
    name="Marketing Video",
    width=1920,
    height=1080,
    fps=30,
    duration=60.0
)
```

### load_project()
Loads an existing project from disk.

**Parameters:**
- `project_id` (str): Unique project identifier

**Returns:** `CanvasProject` object or `None` if not found

### list_projects()
Lists all available projects.

**Returns:** List of project summaries (dict)

### export_project_data()
Exports project as JSON data.

**Parameters:**
- `project_id` (str): Project to export

**Returns:** Complete project data (dict)

## Element Management

### add_element()
Generic method to add any element to the canvas.

**Parameters:**
- `project_id` (str): Target project ID
- `element_type` (str): Element type ('text', 'image', 'video', 'audio', 'shape')
- `x` (float): X position
- `y` (float): Y position
- `width` (float): Element width
- `height` (float): Element height
- `start_time` (float, optional): Start time in seconds (default: 0.0)
- `duration` (float, optional): Element duration (default: 5.0)
- `layer` (int, optional): Layer/track number (default: 1)
- `properties` (dict, optional): Element-specific properties

**Returns:** `CanvasElement` object

### add_text_element()
Adds a text element with typography settings.

**Parameters:**
- `project_id` (str): Target project ID
- `text` (str): Text content
- `x` (float): X position
- `y` (float): Y position
- `font_size` (int, optional): Font size in pixels (default: 24)
- `font_family` (str, optional): Font family (default: "Arial")
- `color` (str, optional): Text color in hex (default: "#FFFFFF")
- `**kwargs`: Additional properties
  - `text_align`: "left", "center", "right"
  - `font_weight`: "normal", "bold"
  - `text_shadow`: Shadow configuration
  - `width`, `height`: Override auto-calculated dimensions
  - `start_time`, `duration`, `layer`: Timeline properties

**Returns:** `CanvasElement` object

**Example:**
```python
title = editor.add_text_element(
    project.id,
    text="Welcome to AI Video Generator",
    x=960, y=200,
    font_size=48,
    color="#FFFFFF",
    text_align="center",
    font_weight="bold",
    start_time=0.0,
    duration=5.0
)
```

### add_image_element()
Adds an image element with visual properties.

**Parameters:**
- `project_id` (str): Target project ID
- `image_path` (str): Path to image file
- `x` (float): X position
- `y` (float): Y position
- `width` (float): Image width
- `height` (float): Image height
- `**kwargs`: Additional properties
  - `opacity`: 0.0-1.0 transparency
  - `rotation`: Rotation angle in degrees
  - `scale_x`, `scale_y`: Scaling factors
  - `border_radius`: Corner radius
  - `filter`: Image filter effects
  - `start_time`, `duration`, `layer`: Timeline properties

**Returns:** `CanvasElement` object

**Example:**
```python
logo = editor.add_image_element(
    project.id,
    image_path="/assets/logo.png",
    x=50, y=50,
    width=200, height=100,
    opacity=0.9,
    start_time=0.0,
    duration=10.0
)
```

### add_video_element()
Adds a video element with playback controls.

**Parameters:**
- `project_id` (str): Target project ID
- `video_path` (str): Path to video file
- `x` (float): X position
- `y` (float): Y position
- `width` (float): Video width
- `height` (float): Video height
- `**kwargs`: Additional properties
  - `volume`: 0.0-1.0 audio level
  - `muted`: Boolean mute state
  - `loop`: Boolean loop setting
  - `playback_speed`: Playback speed multiplier
  - `trim_start`: Start trim in seconds
  - `trim_end`: End trim in seconds
  - `filter`: Video filter effects
  - `start_time`, `duration`, `layer`: Timeline properties

**Returns:** `CanvasElement` object

### add_audio_element()
Adds an audio element (no visual position).

**Parameters:**
- `project_id` (str): Target project ID
- `audio_path` (str): Path to audio file
- `**kwargs`: Additional properties
  - `volume`: 0.0-1.0 audio level
  - `loop`: Boolean loop setting
  - `fade_in`: Fade in duration
  - `fade_out`: Fade out duration
  - `trim_start`: Start trim in seconds
  - `trim_end`: End trim in seconds
  - `start_time`, `duration`: Timeline properties

**Returns:** `CanvasElement` object

### update_element()
Updates properties of an existing element.

**Parameters:**
- `project_id` (str): Target project ID
- `element_id` (str): Element to update
- `updates` (dict): Properties to update

**Returns:** Updated `CanvasElement` object

**Example:**
```python
editor.update_element(project.id, element.id, {
    "x": 200,
    "y": 150,
    "properties": {
        "opacity": 0.8,
        "color": "#FF0000"
    }
})
```

### delete_element()
Removes an element from the canvas.

**Parameters:**
- `project_id` (str): Target project ID
- `element_id` (str): Element to delete

**Returns:** Boolean success status

### duplicate_element()
Creates a copy of an existing element.

**Parameters:**
- `project_id` (str): Target project ID
- `element_id` (str): Element to duplicate
- `offset_x` (float, optional): X offset for copy (default: 50)
- `offset_y` (float, optional): Y offset for copy (default: 50)

**Returns:** New `CanvasElement` object

## Animation & Timeline

### add_keyframe()
Adds an animation keyframe to an element.

**Parameters:**
- `project_id` (str): Target project ID
- `element_id` (str): Target element ID
- `time` (float): Keyframe time in seconds
- `property` (str): Property to animate
- `value` (Any): Property value at this time
- `easing` (str, optional): Easing function (default: "linear")

**Easing Options:** "linear", "ease-in", "ease-out", "ease-in-out"

**Returns:** Boolean success status

**Example:**
```python
# Fade in animation
editor.add_keyframe(project.id, title.id, 0.0, "opacity", 0.0)
editor.add_keyframe(project.id, title.id, 2.0, "opacity", 1.0, "ease-in-out")

# Movement animation
editor.add_keyframe(project.id, logo.id, 0.0, "x", 100)
editor.add_keyframe(project.id, logo.id, 3.0, "x", 800, "ease-out")
```

### add_transition()
Adds a transition between two elements.

**Parameters:**
- `project_id` (str): Target project ID
- `transition_type` (str): Transition type
- `duration` (float): Transition duration in seconds
- `start_time` (float): When transition starts
- `from_element` (str): Source element ID
- `to_element` (str): Target element ID
- `properties` (dict, optional): Transition-specific properties

**Transition Types:** "fade", "slide", "zoom", "wipe", "dissolve"

**Returns:** `Transition` object

### get_project_timeline()
Gets the timeline representation of a project.

**Parameters:**
- `project_id` (str): Target project ID

**Returns:** Timeline data structure (dict)

**Timeline Structure:**
```python
{
    "duration": 30.0,
    "fps": 30,
    "tracks": {
        0: {  # Audio track
            "layer": 0,
            "elements": [...]
        },
        1: {  # Video/Image track
            "layer": 1,
            "elements": [...]
        },
        2: {  # Text overlay track
            "layer": 2,
            "elements": [...]
        }
    },
    "transitions": [...]
}
```

### auto_arrange_elements()
Automatically arranges elements on the timeline.

**Parameters:**
- `project_id` (str): Target project ID
- `arrangement` (str): Arrangement type

**Arrangement Types:**
- `"sequence"`: Elements in sequence (one after another)
- `"parallel"`: All elements start at the same time

**Returns:** Boolean success status

## Tag Management

### create_tag()
Creates a new organizational tag.

**Parameters:**
- `name` (str): Tag name
- `color` (str): Hex color code
- `category` (str): Tag category
- `description` (str, optional): Tag description

**Categories:** "content", "format", "status", "technical"

**Returns:** `Tag` object

### get_tags()
Retrieves tags, optionally filtered by category.

**Parameters:**
- `category` (str, optional): Filter by category

**Returns:** List of `Tag` objects

### assign_tags_to_project()
Assigns tags to a project.

**Parameters:**
- `project_id` (str): Target project ID
- `tag_names` (List[str]): Tag names to assign

**Returns:** Boolean success status

### assign_tags_to_element()
Assigns tags to an element.

**Parameters:**
- `project_id` (str): Target project ID
- `element_id` (str): Target element ID
- `tag_names` (List[str]): Tag names to assign

**Returns:** Boolean success status

### search_projects_by_tags()
Searches projects by tags.

**Parameters:**
- `tag_names` (List[str]): Tags to search for
- `match_all` (bool, optional): Require all tags (default: False)

**Returns:** List of matching `CanvasProject` objects

## Use Case Management

### create_use_case()
Creates a new use case template.

**Parameters:**
- `name` (str): Use case name
- `description` (str): Description
- `category` (str): Use case category
- `tags` (List[str]): Associated tags
- `templates` (List[str]): Template IDs
- `workflow_steps` (List[dict]): Step-by-step workflow
- `estimated_time` (str): Time estimate
- `difficulty` (str): Difficulty level
- `assets_needed` (List[str]): Required assets
- `output_specs` (dict): Output specifications

**Returns:** `UseCase` object

### get_use_cases()
Retrieves use cases with optional filtering.

**Parameters:**
- `category` (str, optional): Filter by category
- `difficulty` (str, optional): Filter by difficulty

**Returns:** List of `UseCase` objects

### get_recommended_use_cases()
Gets recommended use cases based on project tags.

**Parameters:**
- `project_tags` (List[str]): Project tags for matching

**Returns:** List of recommended `UseCase` objects (top 5)

### apply_use_case_to_project()
Applies a use case template to a project.

**Parameters:**
- `project_id` (str): Target project ID
- `use_case_id` (str): Use case to apply

**Returns:** Boolean success status

## Video Export

### export_to_video()
Exports project to video file using FFmpeg.

**Parameters:**
- `project_id` (str): Project to export
- `output_path` (str, optional): Output file path (auto-generated if None)
- `quality` (str, optional): Export quality (default: "high")

**Quality Options:**
- `"low"`: Fast encoding, larger file size (CRF 28)
- `"medium"`: Balanced quality and speed (CRF 23)
- `"high"`: High quality, slower encoding (CRF 18)
- `"ultra"`: Maximum quality, very slow (CRF 15)

**Returns:** Output file path (str)

**Example:**
```python
output = await editor.export_to_video(
    project.id,
    output_path="/renders/my_video.mp4",
    quality="high"
)
```

## Audio Visualization

### generate_waveform_data()
Generates waveform visualization data for audio files.

**Parameters:**
- `audio_path` (str): Path to audio file
- `width` (int, optional): Waveform width in pixels (default: 800)
- `height` (int, optional): Waveform height in pixels (default: 100)

**Returns:** List of amplitude values (List[float])

**Requirements:** `librosa` and `soundfile` packages

## Analytics

### get_tag_analytics()
Provides analytics about tag usage across projects.

**Returns:** Analytics data structure (dict)

**Analytics Structure:**
```python
{
    "total_tags": 15,
    "total_use_cases": 4,
    "tag_usage": {
        "Educational": 5,
        "Marketing": 3,
        ...
    },
    "category_distribution": {
        "content": 6,
        "format": 5,
        "status": 4
    },
    "most_used_tags": [
        ("Educational", 5),
        ("Marketing", 3),
        ...
    ]
}
```

## Error Handling

### Common Exceptions
- `ValueError`: Invalid project ID or element ID
- `FileNotFoundError`: Missing asset files
- `RuntimeError`: FFmpeg export failures
- `ImportError`: Missing optional dependencies

### Best Practices
```python
try:
    project = editor.load_project(project_id)
    if not project:
        print("Project not found")
        return
    
    element = editor.add_text_element(
        project.id, "Hello", x=100, y=100
    )
    
    output = await editor.export_to_video(project.id)
    print(f"Exported to: {output}")
    
except ValueError as e:
    print(f"Invalid parameters: {e}")
except RuntimeError as e:
    print(f"Export failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

*This API reference covers Canvas Editor v2.0.0+*  
*For complete examples, see the demo section in the main module.*
