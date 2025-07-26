# 🏗️ AI Video Generator - Architecture Reference

## System Overview

The AI Video Generator is a modular, scalable video creation platform with the following key components:

### Core Architecture

```
AI-Video-Generator/
├── core/                           # Core modules and base classes
│   ├── __init__.py                # Core package initialization
│   ├── models.py                  # Data models and structures
│   └── base.py                    # Base classes and interfaces
├── modules/                       # Feature modules
│   └── canvas_editor.py          # Original monolithic canvas editor
├── modular_canvas_editor.py       # New modular canvas editor
├── frontend/                      # Next.js frontend application
├── .github/workflows/             # CI/CD pipelines
└── docker/                       # Containerization files
```

## Component Details

### 1. Core Framework (`/core/`)

**Purpose**: Provides fundamental data structures and base classes for the entire system.

**Key Files**:
- `models.py`: Core data models (CanvasElement, CanvasProject, Tag, UseCase, etc.)
- `base.py`: Base classes and interfaces for extensibility
- `__init__.py`: Package initialization and exports

**Design Patterns**:
- Dataclasses for structured data
- Observer pattern for event handling
- Factory pattern for element creation
- Strategy pattern for different export formats

### 2. Canvas Editor System

**Modular Editor** (`modular_canvas_editor.py`):
- Event-driven architecture
- Plugin-based system for effects and transitions
- Separation of concerns between UI and business logic
- Async operations for video processing

**Legacy Editor** (`modules/canvas_editor.py`):
- Monolithic implementation (kept for backward compatibility)
- Contains all functionality in a single class
- Will be gradually deprecated

### 3. Frontend Application (`/frontend/`)

**Technology Stack**:
- Next.js 14+ with App Router
- React 18+ with TypeScript
- Tailwind CSS for styling
- WebSocket for real-time communication

**Key Features**:
- Drag-and-drop canvas interface
- Timeline-based editing
- Real-time preview
- Asset library management

### 4. CI/CD Pipeline (`.github/workflows/`)

**Workflow Features**:
- Automated testing for Python and Node.js
- Docker image building and deployment
- Automated versioning and releases
- Wasabi cloud deployment

## Data Flow Architecture

### 1. Project Creation Flow
```
User Input → Canvas Editor → Core Models → File System → Database
```

### 2. Element Management Flow
```
UI Interaction → Event Handler → Business Logic → Data Persistence → UI Update
```

### 3. Export Pipeline
```
Project Data → FFmpeg Filter Generation → Video Rendering → Output File
```

## Key Design Principles

### 1. Modularity
- Each component has a single responsibility
- Loose coupling between modules
- High cohesion within modules

### 2. Extensibility
- Plugin architecture for new features
- Interface-based design
- Event-driven communication

### 3. Scalability
- Async operations for heavy tasks
- Containerized deployment
- Cloud storage integration

### 4. Maintainability
- Clear separation of concerns
- Comprehensive testing
- Documentation-driven development

## Integration Points

### 1. External Services
- **Wasabi Cloud**: Asset storage and backup
- **FFmpeg**: Video processing and export
- **OpenAI/AI Services**: Content generation
- **GitHub**: Version control and CI/CD

### 2. Data Persistence
- **JSON Files**: Project and metadata storage
- **File System**: Asset and render storage
- **Future**: Database integration for larger scale

### 3. Communication Protocols
- **HTTP/REST**: API communication
- **WebSocket**: Real-time updates
- **File System Events**: Asset monitoring

## Security Considerations

### 1. File Upload Security
- File type validation
- Size limitations
- Virus scanning (future)

### 2. Environment Security
- Environment variable management
- Secret key rotation
- Access control

### 3. Cloud Security
- Encrypted storage
- Access token management
- Audit logging

## Performance Optimization

### 1. Video Processing
- Async/await for non-blocking operations
- Chunked processing for large files
- Memory management for video data

### 2. Frontend Performance
- Code splitting and lazy loading
- Image optimization
- Caching strategies

### 3. Storage Optimization
- Compression for assets
- CDN for static content
- Cleanup of temporary files

## Future Architecture Considerations

### 1. Microservices Migration
- API Gateway implementation
- Service mesh for communication
- Container orchestration

### 2. Database Integration
- PostgreSQL for metadata
- Redis for caching
- Elasticsearch for search

### 3. Real-time Collaboration
- Operational Transform for concurrent editing
- WebRTC for real-time communication
- Conflict resolution algorithms

## Technology Stack Summary

| Component | Technology | Purpose |
|-----------|------------|---------|
| Backend | Python 3.8+ | Core business logic |
| Frontend | Next.js 14+ | User interface |
| Database | JSON Files (transitional) | Data persistence |
| Video Processing | FFmpeg | Video rendering |
| Cloud Storage | Wasabi S3 | Asset storage |
| CI/CD | GitHub Actions | Automated deployment |
| Containerization | Docker | Environment consistency |
| Monitoring | Logging (built-in) | System observability |

## Development Guidelines

### 1. Code Organization
- Follow the established module structure
- Use type hints for all Python code
- Implement comprehensive error handling

### 2. Testing Strategy
- Unit tests for core functionality
- Integration tests for workflows
- End-to-end tests for user journeys

### 3. Documentation
- Inline code documentation
- API documentation
- User guides and tutorials

---

*Last Updated: July 2025*
*Version: 2.0.0*
