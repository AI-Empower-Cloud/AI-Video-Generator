#!/bin/bash

# =============================================================================
# AI VIDEO GENERATOR SETUP SCRIPT
# =============================================================================
# This script sets up the complete AI Video Generator environment
# =============================================================================

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PYTHON_VERSION="3.9"
FFMPEG_REQUIRED="4.4"
CUDA_REQUIRED="11.8"

# Logging functions
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS] $1${NC}"
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

# Detect operating system
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        warning "Running as root. Some operations may behave differently."
    fi
}

# Install system dependencies
install_system_dependencies() {
    local os=$(detect_os)
    log "Installing system dependencies for $os..."
    
    case $os in
        "linux")
            # Ubuntu/Debian
            if command -v apt-get &> /dev/null; then
                sudo apt-get update
                sudo apt-get install -y \
                    python3 \
                    python3-pip \
                    python3-venv \
                    python3-dev \
                    ffmpeg \
                    libsm6 \
                    libxext6 \
                    libxrender-dev \
                    libglib2.0-0 \
                    libgomp1 \
                    git \
                    curl \
                    wget \
                    build-essential \
                    cmake \
                    pkg-config \
                    libjpeg-dev \
                    libpng-dev \
                    libtiff-dev \
                    libavcodec-dev \
                    libavformat-dev \
                    libswscale-dev \
                    libv4l-dev \
                    libxvidcore-dev \
                    libx264-dev \
                    libgtk-3-dev \
                    libatlas-base-dev \
                    gfortran \
                    libportaudio2 \
                    libportaudiocpp0 \
                    portaudio19-dev \
                    libasound2-dev \
                    libpulse-dev
            # CentOS/RHEL/Fedora
            elif command -v yum &> /dev/null; then
                sudo yum update -y
                sudo yum install -y \
                    python3 \
                    python3-pip \
                    python3-devel \
                    ffmpeg \
                    git \
                    curl \
                    wget \
                    gcc \
                    gcc-c++ \
                    cmake \
                    pkg-config \
                    libjpeg-turbo-devel \
                    libpng-devel \
                    libtiff-devel \
                    opencv-devel \
                    atlas-devel \
                    portaudio-devel \
                    alsa-lib-devel \
                    pulseaudio-libs-devel
            fi
            ;;
        "macos")
            # macOS with Homebrew
            if ! command -v brew &> /dev/null; then
                error "Homebrew not found. Please install Homebrew first:"
                error "https://brew.sh/"
                exit 1
            fi
            
            brew update
            brew install \
                python@3.9 \
                ffmpeg \
                git \
                cmake \
                pkg-config \
                jpeg \
                libpng \
                libtiff \
                opencv \
                portaudio
            ;;
        "windows")
            warning "Windows detected. Please install dependencies manually:"
            warning "1. Python 3.9+ from https://python.org"
            warning "2. FFmpeg from https://ffmpeg.org"
            warning "3. Git from https://git-scm.com"
            warning "4. Visual Studio Build Tools"
            ;;
        *)
            error "Unsupported operating system: $os"
            exit 1
            ;;
    esac
    
    success "System dependencies installed"
}

# Check Python version
check_python() {
    log "Checking Python version..."
    
    if command -v python3 &> /dev/null; then
        local python_version=$(python3 --version | cut -d' ' -f2)
        local major_version=$(echo $python_version | cut -d'.' -f1)
        local minor_version=$(echo $python_version | cut -d'.' -f2)
        
        if [[ $major_version -eq 3 && $minor_version -ge 8 ]]; then
            success "Python $python_version is compatible"
        else
            error "Python 3.8+ required. Found: $python_version"
            exit 1
        fi
    else
        error "Python 3 not found. Please install Python 3.8+"
        exit 1
    fi
}

# Setup Python virtual environment
setup_python_env() {
    log "Setting up Python virtual environment..."
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        success "Virtual environment created"
    else
        success "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip setuptools wheel
    
    success "Python environment ready"
}

# Install Python dependencies
install_python_dependencies() {
    log "Installing Python dependencies..."
    
    source venv/bin/activate
    
    # Install dependencies from requirements file
    if [ -f "requirements_comprehensive_ai_video.txt" ]; then
        log "Installing from requirements_comprehensive_ai_video.txt..."
        pip install -r requirements_comprehensive_ai_video.txt
    else
        error "Requirements file not found"
        exit 1
    fi
    
    success "Python dependencies installed"
}

# Download and setup models
setup_models() {
    log "Setting up AI models..."
    
    # Create models directory
    mkdir -p models
    
    # Download Wav2Lip model (placeholder URLs - replace with actual)
    if [ ! -f "models/wav2lip_gan.pth" ]; then
        warning "Wav2Lip model not found. Please download manually:"
        warning "https://github.com/Rudrabha/Wav2Lip/releases/download/v1.0/wav2lip_gan.pth"
        # wget -O models/wav2lip_gan.pth "https://github.com/Rudrabha/Wav2Lip/releases/download/v1.0/wav2lip_gan.pth"
    fi
    
    # Download face detection model
    if [ ! -f "models/face_detection_yunet_2023mar.onnx" ]; then
        warning "Face detection model not found. Please download manually."
    fi
    
    success "Model setup completed"
}

# Setup directories
setup_directories() {
    log "Setting up project directories..."
    
    # Create necessary directories
    mkdir -p output
    mkdir -p temp
    mkdir -p static
    mkdir -p logs
    mkdir -p models
    mkdir -p data
    mkdir -p tests
    
    success "Directories created"
}

# Setup configuration files
setup_config() {
    log "Setting up configuration files..."
    
    # Create environment file template
    if [ ! -f ".env" ]; then
        cat > .env << 'EOF'
# AI Video Generator Configuration

# Wasabi/S3 Cloud Storage
WASABI_ENDPOINT_URL=https://s3.wasabisys.com
WASABI_ACCESS_KEY=your_access_key
WASABI_SECRET_KEY=your_secret_key
WASABI_BUCKET_NAME=your_bucket_name

# OpenAI API (if using)
OPENAI_API_KEY=your_openai_api_key

# Application Settings
APP_ENV=development
APP_DEBUG=true
APP_LOG_LEVEL=INFO

# Database (if using)
DATABASE_URL=sqlite:///./app.db

# Redis (if using)
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_here

# TTS Settings
DEFAULT_TTS_ENGINE=edge
TTS_CACHE_DIR=./temp/tts_cache

# Video Settings
DEFAULT_VIDEO_RESOLUTION=1920x1080
DEFAULT_VIDEO_FPS=25
DEFAULT_VIDEO_CODEC=libx264

# Audio Settings
DEFAULT_AUDIO_CODEC=aac
DEFAULT_AUDIO_BITRATE=128k
EOF
        success "Environment file created (.env)"
        warning "Please edit .env file with your actual configuration"
    fi
    
    # Create logging configuration
    if [ ! -f "logging.conf" ]; then
        cat > logging.conf << 'EOF'
[loggers]
keys=root,uvicorn,app

[handlers]
keys=console,file

[formatters]
keys=default

[logger_root]
level=INFO
handlers=console,file

[logger_uvicorn]
level=INFO
handlers=console,file
qualname=uvicorn
propagate=0

[logger_app]
level=INFO
handlers=console,file
qualname=app
propagate=0

[handler_console]
class=StreamHandler
level=INFO
formatter=default
args=(sys.stdout,)

[handler_file]
class=FileHandler
level=INFO
formatter=default
args=('logs/app.log',)

[formatter_default]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=%Y-%m-%d %H:%M:%S
EOF
        success "Logging configuration created"
    fi
}

# Setup Docker
setup_docker() {
    log "Setting up Docker configuration..."
    
    # Create Docker Compose file
    if [ ! -f "docker-compose.yml" ]; then
        cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  ai-video-generator:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./output:/app/output
      - ./temp:/app/temp
      - ./models:/app/models
      - ./logs:/app/logs
    environment:
      - APP_ENV=production
    env_file:
      - .env
    restart: unless-stopped
    depends_on:
      - redis
      - postgres

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=ai_video_generator
      - POSTGRES_USER=app_user
      - POSTGRES_PASSWORD=app_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./static:/usr/share/nginx/html/static
    depends_on:
      - ai-video-generator
    restart: unless-stopped

volumes:
  redis_data:
  postgres_data:
EOF
        success "Docker Compose file created"
    fi
    
    # Create nginx configuration
    if [ ! -f "nginx.conf" ]; then
        cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream app {
        server ai-video-generator:8000;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /static/ {
            alias /usr/share/nginx/html/static/;
        }
    }
}
EOF
        success "Nginx configuration created"
    fi
}

# Setup systemd service (Linux only)
setup_systemd() {
    local os=$(detect_os)
    
    if [[ "$os" != "linux" ]]; then
        return 0
    fi
    
    log "Setting up systemd service..."
    
    local service_file="/etc/systemd/system/ai-video-generator.service"
    
    if [ ! -f "$service_file" ]; then
        sudo tee "$service_file" > /dev/null << EOF
[Unit]
Description=AI Video Generator Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/venv/bin
ExecStart=$(pwd)/venv/bin/uvicorn fastapi_ai_video_controller:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
        
        sudo systemctl daemon-reload
        sudo systemctl enable ai-video-generator
        
        success "Systemd service created and enabled"
    fi
}

# Run tests
run_tests() {
    log "Running initial tests..."
    
    source venv/bin/activate
    
    # Create basic test if it doesn't exist
    if [ ! -f "tests/test_setup.py" ]; then
        mkdir -p tests
        cat > tests/test_setup.py << 'EOF'
import pytest
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_python_version():
    """Test Python version compatibility"""
    import sys
    assert sys.version_info >= (3, 8)

def test_required_packages():
    """Test that required packages are installed"""
    import importlib
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'boto3',
        'requests',
        'numpy',
        'opencv-python'
    ]
    
    for package in required_packages:
        try:
            importlib.import_module(package.replace('-', '_'))
        except ImportError:
            pytest.fail(f"Required package {package} not installed")

def test_directories():
    """Test that required directories exist"""
    required_dirs = ['output', 'temp', 'static', 'logs', 'models']
    
    for dir_name in required_dirs:
        assert os.path.exists(dir_name), f"Directory {dir_name} not found"

def test_config_files():
    """Test that configuration files exist"""
    config_files = ['.env', 'logging.conf']
    
    for config_file in config_files:
        assert os.path.exists(config_file), f"Config file {config_file} not found"
EOF
    fi
    
    # Run tests
    python -m pytest tests/test_setup.py -v
    
    success "Setup tests completed"
}

# Generate startup script
generate_startup_script() {
    log "Generating startup scripts..."
    
    # Create startup script
    cat > start_server.sh << 'EOF'
#!/bin/bash

# AI Video Generator Startup Script

set -e

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export PYTHONPATH="$(pwd):$PYTHONPATH"

# Start the FastAPI server
uvicorn fastapi_ai_video_controller:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --log-level info \
    --access-log \
    --use-colors
EOF
    
    chmod +x start_server.sh
    
    # Create development startup script
    cat > start_dev.sh << 'EOF'
#!/bin/bash

# AI Video Generator Development Startup Script

set -e

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export PYTHONPATH="$(pwd):$PYTHONPATH"
export APP_ENV=development
export APP_DEBUG=true

# Start the FastAPI server in development mode
uvicorn fastapi_ai_video_controller:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload \
    --log-level debug \
    --access-log \
    --use-colors
EOF
    
    chmod +x start_dev.sh
    
    success "Startup scripts created"
}

# Print setup summary
print_summary() {
    log "Setup Summary"
    echo "============================================="
    echo "AI Video Generator setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Edit .env file with your configuration"
    echo "2. Download required AI models (see models/ directory)"
    echo "3. Start the development server: ./start_dev.sh"
    echo "4. Visit http://localhost:8000/docs for API documentation"
    echo ""
    echo "Available scripts:"
    echo "- ./start_dev.sh     : Start development server"
    echo "- ./start_server.sh  : Start production server"
    echo "- ./git_to_wasabi_workflow.sh : Deploy to Wasabi"
    echo ""
    echo "Configuration files:"
    echo "- .env              : Environment variables"
    echo "- logging.conf      : Logging configuration"
    echo "- docker-compose.yml: Docker configuration"
    echo ""
    echo "For help, visit: https://github.com/your-repo/ai-video-generator"
    echo "============================================="
}

# Main setup function
main() {
    log "Starting AI Video Generator setup..."
    
    local start_time=$(date +%s)
    
    # Run setup steps
    check_root
    install_system_dependencies
    check_python
    setup_directories
    setup_python_env
    install_python_dependencies
    setup_models
    setup_config
    setup_docker
    setup_systemd
    run_tests
    generate_startup_script
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    success "Setup completed in ${duration}s"
    print_summary
}

# Error handling
trap 'error "Setup failed at line $LINENO"; exit 1' ERR

# Run main function if script is executed directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi
