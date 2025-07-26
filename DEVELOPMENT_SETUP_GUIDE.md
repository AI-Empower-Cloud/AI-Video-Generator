# 🛠️ Development Setup Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ with pip
- Node.js 18+ with npm
- Docker and Docker Compose
- Git
- FFmpeg (for video export)

### Initial Setup
```bash
# Clone the repository
git clone https://github.com/AI-Empower-Cloud/AI-Video-Generator.git
cd AI-Video-Generator

# Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up frontend dependencies
cd frontend
npm install
cd ..

# Configure Wasabi credentials
cp .env.wasabi.example .env.wasabi
# Edit .env.wasabi with your credentials

# Initialize project
python -m pytest test_core_modules.py -v
```

## 📁 Project Structure Deep Dive

### Core Modules (`/core/`)
```
core/
├── __init__.py          # Package initialization
├── models.py            # Data classes and models
└── base.py              # Abstract base classes
```

**Purpose:** Reusable, modular components for the canvas editor

### Canvas Editors
- `modular_canvas_editor.py` - **New modular implementation** (recommended)
- `modules/canvas_editor.py` - Original monolithic version (legacy)

### Cloud Integration (`/wasabi_*`)
- `wasabi_node_modules_manager.py` - Python S3 client
- `wasabi_node_modules.sh` - CLI interface
- `test_wasabi_node_modules.py` - Test suite

### Frontend (`/frontend/`)
```
frontend/
├── pages/               # Next.js pages
├── components/          # React components
├── styles/              # CSS and styling
├── public/              # Static assets
└── package.json         # Dependencies
```

### DevOps (`/.github/`, `/docker*`)
- `.github/workflows/modular-ci-cd.yml` - CI/CD pipeline
- `Dockerfile` - Production container
- `Dockerfile.dev` - Development container
- `docker-compose.yml` - Production orchestration
- `docker-compose.dev.yml` - Development services

## 🧑‍💻 Development Workflows

### Working with Core Modules

#### Creating New Models
```python
# Add to core/models.py
@dataclass
class MyNewModel:
    id: str
    name: str
    properties: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)
```

#### Extending Base Classes
```python
# Add to core/base.py
class MyNewManager(BaseManager):
    def __init__(self):
        super().__init__()
    
    def my_custom_method(self):
        # Implementation
        pass
```

#### Using in Canvas Editor
```python
# In modular_canvas_editor.py
from core.models import MyNewModel
from core.base import MyNewManager

class CanvasEditor(BaseCanvasEditor):
    def __init__(self):
        super().__init__()
        self.my_manager = MyNewManager()
```

### Frontend Development

#### Running Development Server
```bash
cd frontend
npm run dev
# Access at http://localhost:3000
```

#### Adding New Components
```jsx
// components/MyComponent.tsx
import React from 'react'

interface MyComponentProps {
  title: string
  children: React.ReactNode
}

export const MyComponent: React.FC<MyComponentProps> = ({ title, children }) => {
  return (
    <div className="my-component">
      <h2>{title}</h2>
      {children}
    </div>
  )
}
```

#### Integrating with Backend
```tsx
// hooks/useCanvasEditor.ts
import { useState, useEffect } from 'react'

export const useCanvasEditor = () => {
  const [projects, setProjects] = useState([])
  
  useEffect(() => {
    fetch('/api/projects')
      .then(res => res.json())
      .then(setProjects)
  }, [])
  
  return { projects }
}
```

### Wasabi Cloud Integration

#### Testing Connection
```bash
# Test credentials
python test_wasabi_connection.py

# Check status
./wasabi_node_modules.sh status --all
```

#### Uploading New Dependencies
```bash
# After npm install
./wasabi_node_modules.sh upload frontend

# Verify upload
./wasabi_node_modules.sh list
```

#### Custom S3 Operations
```python
from wasabi_node_modules_manager import WasabiNodeModulesManager

manager = WasabiNodeModulesManager()

# Custom upload
manager.s3_client.upload_file(
    'local_file.txt',
    manager.bucket_name,
    'remote_path/file.txt'
)

# Custom download
manager.s3_client.download_file(
    manager.bucket_name,
    'remote_path/file.txt',
    'local_file.txt'
)
```

## 🐳 Docker Development

### Development Environment
```bash
# Start all services
docker-compose -f docker-compose.dev.yml up

# Just backend
docker-compose -f docker-compose.dev.yml up backend

# Just frontend
docker-compose -f docker-compose.dev.yml up frontend
```

### Production Build
```bash
# Build production images
./docker-build.sh

# Deploy to production
./deploy-containers.sh

# Custom deployment
docker-compose up -d
```

### Custom Docker Configuration
```dockerfile
# Custom Dockerfile.custom
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "app.py"]
```

## 🧪 Testing Framework

### Running Tests
```bash
# All tests
python -m pytest -v

# Specific test file
python -m pytest test_core_modules.py -v

# With coverage
python -m pytest --cov=core --cov-report=html

# Wasabi integration tests
python -m pytest test_wasabi_node_modules.py -v
```

### Writing New Tests
```python
# test_my_feature.py
import pytest
from core.models import MyNewModel
from modular_canvas_editor import CanvasEditor

class TestMyFeature:
    def test_my_new_model(self):
        model = MyNewModel(
            id="test_id",
            name="Test Model",
            properties={"key": "value"}
        )
        assert model.name == "Test Model"
        assert "key" in model.properties
    
    def test_canvas_editor_integration(self):
        editor = CanvasEditor()
        project = editor.create_project("Test Project")
        
        assert project.name == "Test Project"
        assert len(editor.projects) == 1
```

### Test Configuration
```python
# conftest.py
import pytest
import tempfile
import shutil
from modular_canvas_editor import CanvasEditor

@pytest.fixture
def temp_editor():
    """Provides a temporary canvas editor for testing"""
    temp_dir = tempfile.mkdtemp()
    editor = CanvasEditor(projects_dir=temp_dir)
    yield editor
    shutil.rmtree(temp_dir)

@pytest.fixture
def sample_project(temp_editor):
    """Provides a sample project for testing"""
    return temp_editor.create_project("Test Project")
```

## 🚀 CI/CD Pipeline

### GitHub Actions Workflow
The pipeline automatically:
1. **Tests** - Runs Python and Node.js tests
2. **Builds** - Creates Docker images
3. **Caches** - Manages Wasabi node_modules cache
4. **Deploys** - Pushes to container registry
5. **Releases** - Creates GitHub releases with tags

### Triggering Builds
```bash
# Commit triggers CI
git add .
git commit -m "feat: add new feature"
git push origin main

# Manual release
git tag v2.1.0
git push origin v2.1.0
```

### Custom Deployment
```yaml
# .github/workflows/custom.yml
name: Custom Deployment
on:
  push:
    branches: [custom-branch]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Custom Deploy
        run: |
          echo "Custom deployment logic"
```

## 🔧 Configuration Management

### Environment Variables
```bash
# .env.local (development)
NEXT_PUBLIC_API_URL=http://localhost:8000
WASABI_BUCKET=ai-video-generator-dev

# .env.production
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
WASABI_BUCKET=ai-video-generator-prod
```

### Feature Flags
```python
# config.py
import os

class Config:
    # Features
    ENABLE_WASABI_CACHE = os.getenv('ENABLE_WASABI_CACHE', 'true').lower() == 'true'
    ENABLE_REAL_TIME_PREVIEW = os.getenv('ENABLE_REAL_TIME_PREVIEW', 'false').lower() == 'true'
    
    # Performance
    MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE', '100000000'))  # 100MB
    CACHE_TTL = int(os.getenv('CACHE_TTL', '3600'))  # 1 hour
    
    # Integration
    FFMPEG_PATH = os.getenv('FFMPEG_PATH', 'ffmpeg')
    TEMP_DIR = os.getenv('TEMP_DIR', '/tmp')
```

## 📊 Monitoring & Debugging

### Logging Configuration
```python
# logging_config.py
import logging
import sys

def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

# Usage in modules
import logging
logger = logging.getLogger(__name__)

logger.info("Operation completed successfully")
logger.error("Error occurred", exc_info=True)
```

### Performance Monitoring
```python
# performance.py
import time
import functools

def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper

# Usage
@timing_decorator
def expensive_operation():
    # Your code here
    pass
```

### Memory Usage Tracking
```python
# memory_tracker.py
import psutil
import os

def log_memory_usage(operation_name):
    process = psutil.Process(os.getpid())
    memory_mb = process.memory_info().rss / 1024 / 1024
    logger.info(f"{operation_name}: Memory usage: {memory_mb:.2f} MB")

# Usage
log_memory_usage("Before video export")
await editor.export_to_video(project_id)
log_memory_usage("After video export")
```

## 🔒 Security Best Practices

### Credential Management
```bash
# Never commit sensitive data
echo ".env*" >> .gitignore
echo "*.key" >> .gitignore
echo "secrets/" >> .gitignore

# Use environment variables
export WASABI_ACCESS_KEY="your-key"
export WASABI_SECRET_KEY="your-secret"
```

### Input Validation
```python
# validation.py
from typing import Dict, Any
import re

class InputValidator:
    @staticmethod
    def validate_project_name(name: str) -> bool:
        """Validate project name"""
        if not name or len(name) > 100:
            return False
        return re.match(r'^[a-zA-Z0-9\s\-_]+$', name) is not None
    
    @staticmethod
    def validate_file_path(path: str) -> bool:
        """Validate file path for security"""
        # Prevent path traversal
        if '..' in path or path.startswith('/'):
            return False
        return True
    
    @staticmethod
    def sanitize_properties(props: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize user input properties"""
        safe_props = {}
        for key, value in props.items():
            if isinstance(value, str):
                # Remove potential script injections
                safe_props[key] = re.sub(r'<script.*?</script>', '', value, flags=re.IGNORECASE)
            else:
                safe_props[key] = value
        return safe_props
```

### API Security
```python
# security_middleware.py
from functools import wraps
import jwt

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'error': 'Token missing'}, 401
        
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.InvalidTokenError:
            return {'error': 'Invalid token'}, 401
        
        return f(*args, **kwargs)
    return decorated_function
```

## 📈 Performance Optimization

### Caching Strategies
```python
# cache.py
from functools import lru_cache
import json
import hashlib

class ProjectCache:
    def __init__(self):
        self.cache = {}
    
    def cache_key(self, project_id: str, operation: str) -> str:
        return f"{project_id}:{operation}"
    
    @lru_cache(maxsize=100)
    def get_project_timeline(self, project_id: str) -> dict:
        """Cached timeline generation"""
        if project_id not in self.projects:
            return None
        
        # Expensive timeline calculation
        return self._generate_timeline(project_id)
```

### Lazy Loading
```python
# lazy_loading.py
class LazyAssetLoader:
    def __init__(self):
        self._assets = {}
    
    def get_asset(self, asset_path: str):
        if asset_path not in self._assets:
            self._assets[asset_path] = self._load_asset(asset_path)
        return self._assets[asset_path]
    
    def _load_asset(self, path: str):
        # Load asset only when needed
        with open(path, 'rb') as f:
            return f.read()
```

### Async Operations
```python
# async_operations.py
import asyncio
from concurrent.futures import ThreadPoolExecutor

class AsyncVideoProcessor:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def process_multiple_videos(self, video_configs):
        tasks = []
        for config in video_configs:
            task = asyncio.create_task(
                self.process_single_video(config)
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return results
    
    async def process_single_video(self, config):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self._blocking_video_process,
            config
        )
```

---

*This development guide covers Canvas Editor v2.0.0+*  
*For specific API documentation, see API_REFERENCE_DETAILED.md*
