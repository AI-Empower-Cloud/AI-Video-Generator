# 📚 AI Video Generator - Complete Reference Guide

## 🏗️ Project Architecture Overview

### Core Structure
```
AI-Video-Generator/
├── core/                          # Modular backend core
│   ├── __init__.py
│   ├── models.py                  # Data models & classes
│   └── base.py                    # Base classes & utilities
├── modular_canvas_editor.py       # Modern modular editor
├── modules/canvas_editor.py       # Original monolithic editor
├── wasabi_node_modules_manager.py # Wasabi cloud integration
├── wasabi_node_modules.sh         # CLI tool for node_modules
├── frontend/                      # Next.js React frontend
├── .github/workflows/             # CI/CD automation
├── docker-compose.yml             # Container orchestration
└── docs/                          # Documentation
```

### 🎯 Key Features

#### Backend Capabilities
- **Canvas-based Video Editor** with drag-and-drop functionality
- **Timeline Management** with layers, keyframes, and transitions
- **Asset Management** for images, videos, audio, and fonts
- **Tag System** for project organization and categorization
- **Use Case Templates** for common video scenarios
- **FFmpeg Integration** for video export and rendering
- **Waveform Visualization** for audio tracks
- **Project Serialization** with JSON storage

#### Cloud Integration
- **Wasabi S3 Storage** for dependency caching
- **Node Modules Management** with smart sync/upload/download
- **Multi-project Support** with individual cache management
- **Automated Backup** and restoration workflows

#### Development Workflow
- **Modular Architecture** with reusable components
- **Professional Git Workflow** with semantic versioning
- **CI/CD Pipeline** with automated testing and deployment
- **Docker Containerization** for consistent environments
- **Comprehensive Testing** with pytest integration

## 🧩 Core Components Reference

### Data Models (core/models.py)
- `Keyframe` - Animation keyframe with timing and easing
- `Transition` - Visual transitions between elements
- `Tag` - Organizational tags with categories and colors
- `UseCase` - Predefined workflows and templates
- `CanvasElement` - Individual canvas items (text, image, video, audio)
- `CanvasProject` - Complete project container

### Base Classes (core/base.py)
- `BaseCanvasEditor` - Abstract editor foundation
- `ElementManager` - Element lifecycle management
- `TimelineManager` - Timeline and track operations
- `AssetManager` - Asset loading and management
- `TagManager` - Tag creation and assignment
- `UseCaseManager` - Template and workflow management

### Canvas Editor (modular_canvas_editor.py)
```python
from core.models import *
from core.base import BaseCanvasEditor

editor = CanvasEditor()
project = editor.create_project("My Video", width=1920, height=1080)
text_element = editor.add_text_element(project.id, "Hello World", x=100, y=100)
timeline = editor.get_project_timeline(project.id)
```

## 🌐 Wasabi Cloud Integration

### Configuration (.env.wasabi)
```bash
WASABI_ACCESS_KEY=5W346VTEQ11HLJLF177I
WASABI_SECRET_KEY=RezjHz3kqkdYU6VEODpgcQud4lR5D9gRPCFkVeMA
WASABI_BUCKET=ai-video-generator-content
WASABI_REGION=us-east-1
WASABI_ENDPOINT=https://s3.wasabisys.com
```

### CLI Commands
```bash
# Check node_modules status
./wasabi_node_modules.sh status --all

# Upload dependencies to Wasabi
./wasabi_node_modules.sh upload frontend

# Download cached dependencies
./wasabi_node_modules.sh download frontend

# Smart sync (upload if newer, download if missing)
./wasabi_node_modules.sh sync frontend

# List all cached projects
./wasabi_node_modules.sh list
```

### Python API
```python
from wasabi_node_modules_manager import WasabiNodeModulesManager

manager = WasabiNodeModulesManager()
manager.upload_node_modules('/path/to/project')
manager.download_node_modules('/path/to/project')
status = manager.get_sync_status('/path/to/project')
```

## 🚀 Development Workflows

### Git Workflow
```bash
# Automated modular commits and versioning
./git_workflow_manager.sh

# Manual commands
git add .
git commit -m "feat: add new feature"
git tag v2.1.0
git push origin main --tags
```

### Docker Operations
```bash
# Build containers
./docker-build.sh

# Deploy to production
./deploy-containers.sh

# Development environment
docker-compose -f docker-compose.dev.yml up
```

### Testing
```bash
# Test core modules
python -m pytest test_core_modules.py -v

# Test Wasabi integration
python -m pytest test_wasabi_node_modules.py -v

# Test Wasabi connection
python test_wasabi_connection.py
```

## 📋 Available Templates

### Social Media Post (1080x1080, 15s)
- Perfect for Instagram, Facebook posts
- Square format with text overlays
- Short duration for social engagement

### YouTube Intro (1920x1080, 10s)
- Standard HD format for YouTube
- Brand introduction template
- Optimized for video platforms

### Educational Video (1920x1080, 300s)
- Long-form educational content
- Tutorial and presentation ready
- Academic and training focused

### Podcast Intro (1920x1080, 30s)
- Audio-focused with visual branding
- Podcast episode introductions
- Professional audio treatment

## 🎨 Canvas Editor API Reference

### Project Management
```python
# Create project
project = editor.create_project(
    name="My Video",
    width=1920,
    height=1080,
    fps=30,
    duration=60.0
)

# Load existing project
project = editor.load_project(project_id)

# List all projects
projects = editor.list_projects()

# Export project data
data = editor.export_project_data(project_id)
```

### Element Operations
```python
# Add text element
text = editor.add_text_element(
    project_id, 
    text="Hello World",
    x=100, y=100,
    font_size=24,
    color="#FFFFFF"
)

# Add image element
image = editor.add_image_element(
    project_id,
    image_path="/path/to/image.jpg",
    x=0, y=0,
    width=300, height=200
)

# Add video element
video = editor.add_video_element(
    project_id,
    video_path="/path/to/video.mp4",
    x=100, y=100,
    width=640, height=480
)

# Update element
editor.update_element(project_id, element_id, {
    "x": 200,
    "y": 150,
    "properties": {"opacity": 0.8}
})

# Delete element
editor.delete_element(project_id, element_id)
```

### Animation & Timeline
```python
# Add keyframe animation
editor.add_keyframe(
    project_id, element_id,
    time=2.0,
    property="opacity",
    value=1.0,
    easing="ease-in-out"
)

# Add transition
transition = editor.add_transition(
    project_id,
    transition_type="fade",
    duration=1.0,
    start_time=5.0,
    from_element=element1_id,
    to_element=element2_id
)

# Get timeline
timeline = editor.get_project_timeline(project_id)
```

### Tag & Use Case Management
```python
# Create tag
tag = editor.create_tag(
    name="Educational",
    color="#4CAF50",
    category="content",
    description="Educational content"
)

# Assign tags to project
editor.assign_tags_to_project(project_id, ["Educational", "Tutorial"])

# Get recommended use cases
recommendations = editor.get_recommended_use_cases(["Educational"])

# Apply use case to project
editor.apply_use_case_to_project(project_id, use_case_id)
```

### Video Export
```python
# Export to video file
output_path = await editor.export_to_video(
    project_id,
    output_path="/path/to/output.mp4",
    quality="high"  # low, medium, high, ultra
)
```

## 🔧 Configuration Files

### CI/CD Pipeline (.github/workflows/modular-ci-cd.yml)
- Automated testing on push/PR
- Python and Node.js environments
- Docker building and pushing
- Wasabi dependency caching
- Automated releases and tagging

### Docker Configuration
- `Dockerfile` - Production multi-stage build
- `Dockerfile.dev` - Development environment
- `docker-compose.yml` - Production orchestration
- `docker-compose.dev.yml` - Development services

### Environment Files
- `.env.wasabi` - Wasabi S3 credentials
- `.env.local` - Local development variables
- `.env.production` - Production environment

## 📊 Monitoring & Analytics

### Tag Analytics
```python
analytics = editor.get_tag_analytics()
# Returns:
# - total_tags: int
# - total_use_cases: int
# - tag_usage: Dict[str, int]
# - category_distribution: Dict[str, int]
# - most_used_tags: List[Tuple[str, int]]
```

### Project Metrics
- Element count per project
- Timeline duration tracking
- Asset usage statistics
- Export success rates

## 🚨 Troubleshooting Guide

### Common Issues

#### Wasabi Connection Failed
```bash
# Test connection
python test_wasabi_connection.py

# Check credentials
cat .env.wasabi

# Verify bucket access
./wasabi_node_modules.sh list
```

#### Docker Build Fails
```bash
# Check Docker service
docker --version

# Clean build
docker system prune -f
./docker-build.sh
```

#### Module Import Errors
```bash
# Install dependencies
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"

# Run tests
python -m pytest test_core_modules.py -v
```

#### FFmpeg Export Issues
```bash
# Check FFmpeg installation
ffmpeg -version

# Test simple export
ffmpeg -f lavfi -i testsrc=duration=1:size=320x240:rate=1 test.mp4
```

## 🔮 Future Development Roadmap

### Phase 1: Enhanced Features
- Real-time collaboration
- Advanced animation curves
- Plugin system for effects
- Mobile responsive editor

### Phase 2: AI Integration
- Automatic video generation
- Smart asset recommendations
- Voice-to-text integration
- AI-powered transitions

### Phase 3: Enterprise Features
- Multi-tenant architecture
- Advanced user management
- Enterprise SSO integration
- Advanced analytics dashboard

### Phase 4: Platform Expansion
- Mobile app development
- Desktop application
- API marketplace
- Third-party integrations

## 📞 Support & Resources

### Documentation
- `README_MODULAR.md` - Modular architecture guide
- `WASABI_NODE_MODULES_GUIDE.md` - Cloud integration guide
- `PROJECT_COMPLETION_SUMMARY.md` - Current project status
- `CHANGELOG.md` - Version history

### Community
- GitHub Issues for bug reports
- Discussions for feature requests
- Wiki for community documentation
- Examples repository for templates

---

*Last Updated: July 9, 2025*  
*AI Video Generator v2.0.0+*
