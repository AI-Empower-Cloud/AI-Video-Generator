# 🔗 Integration Reference Guide

## External Service Integrations

### 1. Wasabi Cloud Storage Integration

#### Configuration
```python
# wasabi_config.py
WASABI_CONFIG = {
    'endpoint_url': 'https://s3.wasabisys.com',
    'region_name': 'us-east-1',
    'bucket_name': 'ai-video-generator',
    'access_key_id': os.getenv('WASABI_ACCESS_KEY_ID'),
    'secret_access_key': os.getenv('WASABI_SECRET_ACCESS_KEY')
}
```

#### Usage Examples
```python
from wasabi_node_modules_manager import WasabiNodeModulesManager

# Initialize manager
manager = WasabiNodeModulesManager()

# Upload node_modules
await manager.upload_node_modules('/path/to/frontend')

# Download node_modules
await manager.download_node_modules('/path/to/frontend')

# Sync node_modules (smart upload/download)
await manager.sync_node_modules('/path/to/frontend')

# Check status
status = await manager.get_sync_status('/path/to/frontend')
```

#### Available Commands
```bash
# Upload node_modules to Wasabi
./wasabi_node_modules.sh upload /path/to/project

# Download node_modules from Wasabi
./wasabi_node_modules.sh download /path/to/project

# Check sync status
./wasabi_node_modules.sh status /path/to/project

# List all projects
./wasabi_node_modules.sh list

# Clean up old backups
./wasabi_node_modules.sh cleanup --older-than=30days
```

### 2. FFmpeg Video Processing Integration

#### Basic Usage
```python
import subprocess

def export_video(project_path: str, output_path: str, options: dict = None):
    """Export video using FFmpeg with specified options."""
    
    default_options = {
        'codec': 'libx264',
        'crf': 23,
        'preset': 'medium',
        'fps': 30,
        'resolution': '1920x1080'
    }
    
    if options:
        default_options.update(options)
    
    cmd = [
        'ffmpeg',
        '-f', 'image2pipe',
        '-vcodec', 'png',
        '-r', str(default_options['fps']),
        '-i', '-',
        '-vcodec', default_options['codec'],
        '-crf', str(default_options['crf']),
        '-preset', default_options['preset'],
        '-s', default_options['resolution'],
        output_path
    ]
    
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    return process
```

#### Advanced Filter Chains
```python
def create_complex_filter(elements: List[CanvasElement]) -> str:
    """Create FFmpeg complex filter for multiple elements."""
    
    filters = []
    
    for i, element in enumerate(elements):
        if element.type == 'text':
            filters.append(f"drawtext=text='{element.properties['text']}':x={element.x}:y={element.y}")
        elif element.type == 'image':
            filters.append(f"[{i}:v]scale={element.width}:{element.height}[scaled{i}]")
        elif element.type == 'video':
            filters.append(f"[{i}:v]trim=start={element.start_time}:duration={element.duration}[clip{i}]")
    
    return ';'.join(filters)
```

### 3. GitHub Actions Integration

#### Workflow Triggers
```yaml
# .github/workflows/modular-ci-cd.yml
on:
  push:
    branches: [ main, develop ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        default: 'staging'
        type: choice
        options:
        - staging
        - production
```

#### Custom Actions
```yaml
# Deploy to Wasabi action
- name: Deploy to Wasabi
  uses: ./.github/actions/deploy-wasabi
  with:
    access-key: ${{ secrets.WASABI_ACCESS_KEY_ID }}
    secret-key: ${{ secrets.WASABI_SECRET_ACCESS_KEY }}
    bucket: ai-video-generator
    source-dir: frontend/dist
```

### 4. Docker Integration

#### Multi-service Setup
```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - NODE_ENV=production
      - PYTHONPATH=/app
    volumes:
      - ./projects:/app/projects
      - ./assets:/app/assets
    depends_on:
      - redis
      - postgres

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://app:8000
    depends_on:
      - app

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: ai_video_generator
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  redis_data:
  postgres_data:
```

#### Development vs Production
```bash
# Development with hot reload
docker-compose -f docker-compose.dev.yml up

# Production optimized
docker-compose -f docker-compose.prod.yml up -d

# Build and push to registry
docker build -t myregistry/ai-video-generator:latest .
docker push myregistry/ai-video-generator:latest
```

## API Integration Patterns

### 1. RESTful API Design

#### Endpoint Structure
```python
# FastAPI implementation
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="AI Video Generator API", version="2.0.0")

class ProjectCreate(BaseModel):
    name: str
    width: int = 1920
    height: int = 1080
    fps: int = 30

@app.post("/api/v1/projects/", response_model=CanvasProject)
async def create_project(project: ProjectCreate):
    """Create a new video project."""
    editor = ModularCanvasEditor()
    result = editor.create_project(**project.dict())
    return result

@app.get("/api/v1/projects/{project_id}")
async def get_project(project_id: str):
    """Get project by ID."""
    editor = ModularCanvasEditor()
    project = editor.load_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
```

#### Authentication Middleware
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token."""
    token = credentials.credentials
    # Verify token logic here
    if not is_valid_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return get_user_from_token(token)
```

### 2. WebSocket Real-time Updates

#### Server-side Implementation
```python
from fastapi import WebSocket, WebSocketDisconnect
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))

manager = ConnectionManager()

@app.websocket("/ws/{project_id}")
async def websocket_endpoint(websocket: WebSocket, project_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Process real-time updates
            if message['type'] == 'element_update':
                # Update element in real-time
                await manager.broadcast({
                    'type': 'element_updated',
                    'project_id': project_id,
                    'element': message['element']
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

#### Client-side Implementation (React)
```typescript
// useWebSocket hook
import { useEffect, useRef, useState } from 'react';

export function useWebSocket(projectId: string) {
  const ws = useRef<WebSocket | null>(null);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    ws.current = new WebSocket(`ws://localhost:8000/ws/${projectId}`);
    
    ws.current.onopen = () => setConnected(true);
    ws.current.onclose = () => setConnected(false);
    
    ws.current.onmessage = (event) => {
      const message = JSON.parse(event.data);
      handleMessage(message);
    };

    return () => {
      ws.current?.close();
    };
  }, [projectId]);

  const sendMessage = (message: any) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message));
    }
  };

  return { connected, sendMessage };
}
```

### 3. Database Integration (Future)

#### Model Definitions
```python
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    width = Column(Integer, default=1920)
    height = Column(Integer, default=1080)
    fps = Column(Integer, default=30)
    duration = Column(Float, default=30.0)
    background_color = Column(String, default="#000000")
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    elements = relationship("Element", back_populates="project")

class Element(Base):
    __tablename__ = "elements"
    
    id = Column(String, primary_key=True)
    project_id = Column(String, ForeignKey("projects.id"))
    type = Column(String, nullable=False)
    x = Column(Float, default=0.0)
    y = Column(Float, default=0.0)
    width = Column(Float, default=100.0)
    height = Column(Float, default=100.0)
    rotation = Column(Float, default=0.0)
    opacity = Column(Float, default=1.0)
    start_time = Column(Float, default=0.0)
    duration = Column(Float, default=5.0)
    z_index = Column(Integer, default=0)
    properties = Column(JSON)
    animations = Column(JSON)
    
    project = relationship("Project", back_populates="elements")
```

#### Repository Pattern
```python
from abc import ABC, abstractmethod
from typing import List, Optional

class ProjectRepository(ABC):
    @abstractmethod
    async def create(self, project: CanvasProject) -> CanvasProject:
        pass
    
    @abstractmethod
    async def get_by_id(self, project_id: str) -> Optional[CanvasProject]:
        pass
    
    @abstractmethod
    async def update(self, project: CanvasProject) -> CanvasProject:
        pass
    
    @abstractmethod
    async def delete(self, project_id: str) -> bool:
        pass

class SQLAlchemyProjectRepository(ProjectRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, project: CanvasProject) -> CanvasProject:
        db_project = Project(**project.to_dict())
        self.session.add(db_project)
        await self.session.commit()
        return project
```

## Performance Integration

### 1. Caching Strategy

#### Redis Integration
```python
import redis
import json
from typing import Optional

class RedisCache:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        self.redis_client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
    
    async def get_project(self, project_id: str) -> Optional[CanvasProject]:
        """Get project from cache."""
        cached_data = self.redis_client.get(f"project:{project_id}")
        if cached_data:
            return CanvasProject.from_dict(json.loads(cached_data))
        return None
    
    async def set_project(self, project: CanvasProject, ttl: int = 3600):
        """Cache project data."""
        self.redis_client.setex(
            f"project:{project.id}",
            ttl,
            json.dumps(project.to_dict())
        )
    
    async def invalidate_project(self, project_id: str):
        """Remove project from cache."""
        self.redis_client.delete(f"project:{project_id}")
```

### 2. Background Tasks

#### Celery Integration
```python
from celery import Celery

app = Celery('ai_video_generator')
app.config_from_object('celeryconfig')

@app.task
def export_video_task(project_id: str, export_options: dict):
    """Background task for video export."""
    editor = ModularCanvasEditor()
    project = editor.load_project(project_id)
    
    if not project:
        raise ValueError(f"Project {project_id} not found")
    
    output_file = editor.export_project(
        format=export_options.get('format', 'mp4'),
        quality=export_options.get('quality', 'high')
    )
    
    # Notify completion via WebSocket
    notify_export_completion(project_id, output_file)
    
    return output_file
```

### 3. Monitoring Integration

#### Health Check Endpoints
```python
@app.get("/health")
async def health_check():
    """System health check."""
    checks = {
        'database': await check_database_connection(),
        'redis': await check_redis_connection(),
        'wasabi': await check_wasabi_connection(),
        'ffmpeg': check_ffmpeg_availability(),
        'disk_space': check_disk_space()
    }
    
    status = "healthy" if all(checks.values()) else "unhealthy"
    
    return {
        'status': status,
        'timestamp': datetime.utcnow().isoformat(),
        'checks': checks
    }
```

#### Metrics Collection
```python
from prometheus_client import Counter, Histogram, generate_latest

# Metrics
project_created_counter = Counter('projects_created_total', 'Total projects created')
export_duration_histogram = Histogram('export_duration_seconds', 'Video export duration')

@app.middleware("http")
async def metrics_middleware(request, call_next):
    """Collect request metrics."""
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    # Record metrics
    if request.url.path.startswith('/api/v1/projects') and request.method == 'POST':
        project_created_counter.inc()
    
    return response

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(generate_latest(), media_type="text/plain")
```

---

*This integration reference provides comprehensive guidance for connecting the AI Video Generator with external services and implementing scalable architecture patterns.*

**Last Updated**: July 2025  
**Version**: 2.0.0
