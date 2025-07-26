# 🚨 Troubleshooting Guide

## Common Issues & Solutions

### 🔧 Installation & Setup Issues

#### Python Environment Problems
**Issue:** Import errors or module not found
```bash
ModuleNotFoundError: No module named 'core'
```

**Solutions:**
```bash
# Ensure you're in the right directory
cd /workspaces/AI-Video-Generator

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Reinstall dependencies
pip install -r requirements.txt

# Add current directory to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or for permanent solution, add to .bashrc
echo 'export PYTHONPATH="${PYTHONPATH}:$(pwd)"' >> ~/.bashrc
```

#### Node.js Dependencies Issues
**Issue:** Frontend build fails or packages missing
```bash
npm ERR! Cannot resolve dependency
```

**Solutions:**
```bash
cd frontend

# Clear npm cache
npm cache clean --force

# Remove node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check for Wasabi cached version
../wasabi_node_modules.sh download frontend

# Update to latest versions
npm update
```

#### Docker Issues
**Issue:** Docker build fails or containers won't start

**Solutions:**
```bash
# Check Docker status
docker --version
docker-compose --version

# Clean Docker system
docker system prune -f
docker volume prune -f

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up

# Check logs
docker-compose logs backend
docker-compose logs frontend
```

### 🌐 Wasabi Cloud Issues

#### Connection Failed
**Issue:** Cannot connect to Wasabi S3
```bash
❌ Connection failed: An error occurred (InvalidAccessKeyId)
```

**Solutions:**
```bash
# Check credentials
cat .env.wasabi

# Test connection
python test_wasabi_connection.py

# Verify credentials in Wasabi console
# - Access Key: 5W346VTEQ11HLJLF177I
# - Secret Key: RezjHz3kqkdYU6VEODpgcQud4lR5D9gRPCFkVeMA
# - Bucket: ai-video-generator-content

# Check network connectivity
ping s3.wasabisys.com

# Try alternative endpoint
export WASABI_ENDPOINT=https://s3.us-east-1.wasabisys.com
```

#### Bucket Access Denied
**Issue:** Access denied to bucket operations
```bash
❌ AccessDenied: Access Denied
```

**Solutions:**
```bash
# Check bucket permissions in Wasabi console
# Ensure IAM policy allows:
# - s3:GetObject
# - s3:PutObject
# - s3:DeleteObject
# - s3:ListBucket

# Test with CLI tool
./wasabi_node_modules.sh list

# Check bucket region
./wasabi_node_modules.sh status --all
```

#### Upload/Download Failures
**Issue:** Files fail to upload or download

**Solutions:**
```bash
# Check file permissions
ls -la node_modules/

# Verify disk space
df -h

# Test with smaller files first
echo "test" > test.txt
./wasabi_node_modules.sh upload test.txt

# Check network stability
curl -I https://s3.wasabisys.com

# Enable debug logging
export WASABI_DEBUG=true
./wasabi_node_modules.sh upload frontend
```

### 🎨 Canvas Editor Issues

#### Project Loading Errors
**Issue:** Projects fail to load or save
```python
ValueError: Project 12345 not found
```

**Solutions:**
```python
# Check project directory
import os
print(os.listdir("canvas_projects"))

# Verify JSON format
import json
with open("canvas_projects/project_id.json") as f:
    data = json.load(f)  # Should not raise exception

# Reset projects directory
rm -rf canvas_projects
mkdir canvas_projects

# Check permissions
chmod 755 canvas_projects
chmod 644 canvas_projects/*.json
```

#### Element Creation Failures
**Issue:** Elements not appearing on canvas

**Solutions:**
```python
# Debug element creation
editor = CanvasEditor()
project = editor.create_project("Debug Project")

# Check project is created
print(f"Project ID: {project.id}")
print(f"Projects in memory: {len(editor.projects)}")

# Add element with debug info
element = editor.add_text_element(
    project.id,
    text="Debug Text",
    x=100, y=100
)
print(f"Element created: {element.id}")
print(f"Element properties: {element.properties}")

# Check element in project
print(f"Elements in project: {len(project.elements)}")
```

#### Timeline Generation Issues
**Issue:** Timeline data is empty or malformed

**Solutions:**
```python
# Check timeline step by step
timeline = editor.get_project_timeline(project.id)
print(f"Timeline duration: {timeline['duration']}")
print(f"Timeline tracks: {list(timeline['tracks'].keys())}")

# Verify elements have proper timing
for element in project.elements:
    print(f"Element {element.id}: {element.start_time} - {element.start_time + element.duration}")

# Check for overlapping elements
elements_by_layer = {}
for element in project.elements:
    if element.layer not in elements_by_layer:
        elements_by_layer[element.layer] = []
    elements_by_layer[element.layer].append(element)

for layer, elements in elements_by_layer.items():
    print(f"Layer {layer}: {len(elements)} elements")
```

### 🎬 Video Export Issues

#### FFmpeg Not Found
**Issue:** Video export fails with FFmpeg error
```bash
FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
```

**Solutions:**
```bash
# Install FFmpeg (Ubuntu/Debian)
sudo apt update
sudo apt install ffmpeg

# Install FFmpeg (macOS)
brew install ffmpeg

# Install FFmpeg (Windows)
# Download from https://ffmpeg.org/download.html

# Verify installation
ffmpeg -version

# Check PATH
which ffmpeg

# Set custom FFmpeg path
export FFMPEG_PATH=/usr/local/bin/ffmpeg
```

#### Video Export Fails
**Issue:** Export process fails or hangs

**Solutions:**
```python
# Test with minimal project
editor = CanvasEditor()
project = editor.create_project("Test Export", duration=5.0)
text = editor.add_text_element(project.id, "Test", x=100, y=100)

# Test export with debug
import asyncio
import logging
logging.basicConfig(level=logging.DEBUG)

try:
    output = await editor.export_to_video(project.id, quality="low")
    print(f"Export successful: {output}")
except Exception as e:
    print(f"Export failed: {e}")
    import traceback
    traceback.print_exc()
```

#### Missing Assets
**Issue:** Export fails due to missing files

**Solutions:**
```python
# Check all asset paths
for element in project.elements:
    if element.type in ["image", "video", "audio"]:
        source = element.properties.get("source")
        if source and not os.path.exists(source):
            print(f"Missing asset: {source}")

# Update asset paths
editor.update_element(project.id, element.id, {
    "properties": {"source": "/path/to/existing/file.jpg"}
})

# Use relative paths
assets_dir = os.path.join(editor.assets_dir, "images")
image_path = os.path.join(assets_dir, "logo.png")
```

### 🧪 Testing Issues

#### Test Failures
**Issue:** Tests fail unexpectedly

**Solutions:**
```bash
# Run tests with verbose output
python -m pytest -v -s

# Run specific test
python -m pytest test_core_modules.py::TestCanvasEditor::test_create_project -v

# Check test environment
python -c "import pytest; print(pytest.__version__)"

# Clear test cache
rm -rf .pytest_cache __pycache__

# Run with coverage
python -m pytest --cov=core --cov-report=html
open htmlcov/index.html
```

#### Mock/Fixture Issues
**Issue:** Test fixtures not working properly

**Solutions:**
```python
# Debug fixture
@pytest.fixture
def debug_editor():
    import tempfile
    temp_dir = tempfile.mkdtemp()
    print(f"Temp directory: {temp_dir}")
    
    editor = CanvasEditor(projects_dir=temp_dir)
    print(f"Editor created with {len(editor.projects)} projects")
    
    yield editor
    
    import shutil
    shutil.rmtree(temp_dir)
    print(f"Cleaned up {temp_dir}")

# Check fixture scope
@pytest.fixture(scope="function")  # or "session", "module"
def my_fixture():
    pass
```

### 🚀 CI/CD Pipeline Issues

#### GitHub Actions Failing
**Issue:** CI/CD pipeline fails

**Solutions:**
```yaml
# Check workflow status
# Go to: https://github.com/your-repo/actions

# Debug workflow locally with act
npm install -g @nektos/act
act -j test

# Check secrets
# Go to: https://github.com/your-repo/settings/secrets/actions
# Ensure all required secrets are set:
# - WASABI_ACCESS_KEY
# - WASABI_SECRET_KEY
# - WASABI_BUCKET
# - WASABI_REGION
# - WASABI_ENDPOINT
```

#### Docker Build Failures in CI
**Issue:** Docker builds work locally but fail in CI

**Solutions:**
```yaml
# Add debug steps to workflow
- name: Debug Docker
  run: |
    docker --version
    docker-compose --version
    df -h
    free -h

# Use explicit platform
- name: Build Docker Image
  run: |
    docker build --platform linux/amd64 -t app .

# Check for large files
- name: Check File Sizes
  run: |
    find . -size +100M -ls
```

#### Deployment Issues
**Issue:** Deployment fails or containers don't start

**Solutions:**
```bash
# Check container logs
docker logs container_name

# Debug container interactively
docker run -it --entrypoint /bin/bash your_image

# Check resource limits
docker stats

# Verify environment variables
docker exec container_name env

# Test health checks
docker exec container_name curl http://localhost:8000/health
```

### 📱 Frontend Issues

#### Next.js Build Errors
**Issue:** Frontend build fails

**Solutions:**
```bash
cd frontend

# Check Node.js version
node --version  # Should be 18+

# Clear Next.js cache
rm -rf .next

# Check for syntax errors
npm run lint

# Build with debug
npm run build -- --debug

# Check for missing dependencies
npm install --legacy-peer-deps
```

#### API Connection Issues
**Issue:** Frontend can't connect to backend

**Solutions:**
```bash
# Check backend is running
curl http://localhost:8000/api/health

# Verify CORS settings
# In backend, ensure CORS allows frontend origin

# Check environment variables
echo $NEXT_PUBLIC_API_URL

# Test API endpoints
curl -X GET http://localhost:8000/api/projects
curl -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Project"}'
```

### 🔍 Performance Issues

#### Slow Operations
**Issue:** Video operations are very slow

**Solutions:**
```python
# Profile operations
import cProfile
import pstats

def profile_operation():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Your slow operation here
    result = editor.export_to_video(project.id)
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)
    return result

# Monitor memory usage
import psutil
import os

def monitor_memory():
    process = psutil.Process(os.getpid())
    memory_mb = process.memory_info().rss / 1024 / 1024
    print(f"Memory usage: {memory_mb:.2f} MB")

# Optimize for large projects
# - Use generators instead of lists
# - Process elements in batches
# - Enable caching for repeated operations
```

#### High Memory Usage
**Issue:** Application uses too much memory

**Solutions:**
```python
# Use memory profiling
from memory_profiler import profile

@profile
def memory_intensive_function():
    # Your function here
    pass

# Clear caches periodically
editor._clear_cache()

# Use weak references for large objects
import weakref

class ProjectCache:
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()
```

### 🔒 Security Issues

#### File Permission Errors
**Issue:** Cannot read/write files

**Solutions:**
```bash
# Check file permissions
ls -la canvas_projects/

# Fix permissions
chmod 755 canvas_projects/
chmod 644 canvas_projects/*.json

# Check disk space
df -h

# Check user permissions
whoami
groups
```

#### Path Traversal Attempts
**Issue:** Security warnings about file paths

**Solutions:**
```python
# Validate file paths
import os
import os.path

def validate_path(path, base_dir):
    # Resolve any .. or . in the path
    normalized = os.path.normpath(path)
    
    # Ensure it's within base directory
    full_path = os.path.abspath(os.path.join(base_dir, normalized))
    base_abs = os.path.abspath(base_dir)
    
    if not full_path.startswith(base_abs):
        raise ValueError("Path traversal attempt detected")
    
    return full_path

# Use in canvas editor
def add_image_element(self, project_id, image_path, ...):
    safe_path = validate_path(image_path, self.assets_dir)
    # Continue with safe path
```

## 🆘 Getting Help

### Debugging Checklist
1. ✅ Check error messages carefully
2. ✅ Verify all dependencies are installed
3. ✅ Ensure credentials are correct
4. ✅ Test with minimal examples
5. ✅ Check logs and debug output
6. ✅ Verify file permissions
7. ✅ Test network connectivity
8. ✅ Clear caches and restart services

### Useful Commands
```bash
# System information
python --version
node --version
docker --version
ffmpeg -version

# Check running processes
ps aux | grep python
ps aux | grep node

# Check ports
netstat -tlnp | grep :8000
netstat -tlnp | grep :3000

# Check disk space
df -h
du -sh *

# Check memory
free -h
top -p $(pgrep python)
```

### Log Analysis
```bash
# View recent logs
tail -f app.log
tail -f /var/log/syslog

# Search for errors
grep -i error app.log
grep -i "failed" app.log

# Monitor resource usage
iotop
htop
```

### Contact & Support
- **GitHub Issues:** Report bugs and feature requests
- **Discussions:** Ask questions and share ideas
- **Documentation:** Check all reference files
- **Email:** For sensitive security issues

---

*This troubleshooting guide covers common issues with Canvas Editor v2.0.0+*  
*For specific API documentation, see API_REFERENCE_DETAILED.md*  
*For development setup, see DEVELOPMENT_SETUP_GUIDE.md*
