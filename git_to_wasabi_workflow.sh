#!/bin/bash

# =============================================================================
# GIT TO WASABI WORKFLOW SCRIPT
# =============================================================================
# This script automates the process of:
# 1. Pulling latest changes from Git
# 2. Building the AI Video Generator
# 3. Running tests
# 4. Deploying to Wasabi Cloud Storage
# 5. Updating production environment
# =============================================================================

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WASABI_BUCKET="${WASABI_BUCKET:-ai-video-generator}"
WASABI_REGION="${WASABI_REGION:-us-east-1}"
DEPLOYMENT_ENV="${DEPLOYMENT_ENV:-production}"
BACKUP_COUNT="${BACKUP_COUNT:-5}"

# Logging function
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

# Check if required tools are installed
check_dependencies() {
    log "Checking dependencies..."
    
    local deps=("git" "python3" "pip" "docker" "aws")
    local missing_deps=()
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing_deps+=("$dep")
        fi
    done
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        error "Missing dependencies: ${missing_deps[*]}"
        error "Please install missing dependencies and try again."
        exit 1
    fi
    
    success "All dependencies are installed"
}

# Check environment variables
check_environment() {
    log "Checking environment variables..."
    
    local required_vars=("WASABI_ACCESS_KEY" "WASABI_SECRET_KEY" "WASABI_ENDPOINT_URL")
    local missing_vars=()
    
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing_vars+=("$var")
        fi
    done
    
    if [ ${#missing_vars[@]} -ne 0 ]; then
        error "Missing environment variables: ${missing_vars[*]}"
        error "Please set the required environment variables and try again."
        exit 1
    fi
    
    success "Environment variables are set"
}

# Pull latest changes from Git
git_pull() {
    log "Pulling latest changes from Git..."
    
    cd "$PROJECT_DIR"
    
    # Check if we're in a git repository
    if [ ! -d ".git" ]; then
        error "Not a Git repository. Please initialize Git first."
        exit 1
    fi
    
    # Stash any local changes
    if ! git diff-index --quiet HEAD --; then
        warning "Local changes detected. Stashing..."
        git stash push -m "Auto-stash before deployment $(date)"
    fi
    
    # Pull latest changes
    git fetch origin
    local current_branch=$(git rev-parse --abbrev-ref HEAD)
    git pull origin "$current_branch"
    
    success "Git pull completed"
}

# Install Python dependencies
install_dependencies() {
    log "Installing Python dependencies..."
    
    cd "$PROJECT_DIR"
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install dependencies
    if [ -f "requirements_comprehensive_ai_video.txt" ]; then
        pip install -r requirements_comprehensive_ai_video.txt
    else
        error "Requirements file not found"
        exit 1
    fi
    
    success "Dependencies installed"
}

# Run tests
run_tests() {
    log "Running tests..."
    
    cd "$PROJECT_DIR"
    source venv/bin/activate
    
    # Run Python tests
    if [ -f "tests/test_main.py" ]; then
        python -m pytest tests/ -v
    else
        warning "No tests found. Creating basic test structure..."
        mkdir -p tests
        cat > tests/test_main.py << 'EOF'
import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that main modules can be imported"""
    try:
        from modules import TTSEngine, LipSyncProcessor, VideoComposer
        from modules import AudioProcessor, SubtitleGenerator, CloudStorage
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")

def test_fastapi_app():
    """Test that FastAPI app can be created"""
    try:
        from fastapi_ai_video_controller import app
        assert app is not None
    except ImportError as e:
        pytest.fail(f"FastAPI app import failed: {e}")
EOF
        python -m pytest tests/ -v
    fi
    
    success "Tests completed"
}

# Build Docker image
build_docker() {
    log "Building Docker image..."
    
    cd "$PROJECT_DIR"
    
    # Create Dockerfile if it doesn't exist
    if [ ! -f "Dockerfile" ]; then
        warning "Dockerfile not found. Creating default Dockerfile..."
        cat > Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements_comprehensive_ai_video.txt .
RUN pip install --no-cache-dir -r requirements_comprehensive_ai_video.txt

# Copy application code
COPY . .

# Create directories
RUN mkdir -p output static temp

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "fastapi_ai_video_controller:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
    fi
    
    # Build Docker image
    local image_tag="ai-video-generator:$(date +%Y%m%d_%H%M%S)"
    docker build -t "$image_tag" .
    docker tag "$image_tag" "ai-video-generator:latest"
    
    success "Docker image built: $image_tag"
}

# Create deployment package
create_package() {
    log "Creating deployment package..."
    
    cd "$PROJECT_DIR"
    
    local package_name="ai-video-generator-$(date +%Y%m%d_%H%M%S).tar.gz"
    local temp_dir=$(mktemp -d)
    
    # Copy necessary files
    cp -r modules "$temp_dir/"
    cp fastapi_ai_video_controller.py "$temp_dir/"
    cp requirements_comprehensive_ai_video.txt "$temp_dir/"
    cp Dockerfile "$temp_dir/"
    cp docker-compose.yml "$temp_dir/" 2>/dev/null || true
    
    # Create package
    cd "$temp_dir"
    tar -czf "$PROJECT_DIR/$package_name" .
    
    # Cleanup
    rm -rf "$temp_dir"
    
    echo "$package_name"
    success "Deployment package created: $package_name"
}

# Upload to Wasabi
upload_to_wasabi() {
    local package_file="$1"
    log "Uploading to Wasabi Cloud Storage..."
    
    cd "$PROJECT_DIR"
    
    # Configure AWS CLI for Wasabi
    aws configure set aws_access_key_id "$WASABI_ACCESS_KEY"
    aws configure set aws_secret_access_key "$WASABI_SECRET_KEY"
    aws configure set default.region "$WASABI_REGION"
    
    # Upload deployment package
    local s3_key="deployments/$(basename "$package_file")"
    aws s3 cp "$package_file" "s3://$WASABI_BUCKET/$s3_key" --endpoint-url "$WASABI_ENDPOINT_URL"
    
    # Upload individual files
    aws s3 sync . "s3://$WASABI_BUCKET/source/" \
        --endpoint-url "$WASABI_ENDPOINT_URL" \
        --exclude "*.git/*" \
        --exclude "venv/*" \
        --exclude "__pycache__/*" \
        --exclude "*.pyc" \
        --exclude "*.log" \
        --exclude "temp/*" \
        --exclude "output/*"
    
    # Create deployment manifest
    local manifest_file="deployment_manifest_$(date +%Y%m%d_%H%M%S).json"
    cat > "$manifest_file" << EOF
{
    "deployment_id": "$(date +%Y%m%d_%H%M%S)",
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "git_commit": "$(git rev-parse HEAD)",
    "git_branch": "$(git rev-parse --abbrev-ref HEAD)",
    "package_file": "$s3_key",
    "environment": "$DEPLOYMENT_ENV",
    "wasabi_bucket": "$WASABI_BUCKET",
    "files_uploaded": [
        "source/",
        "$s3_key"
    ]
}
EOF
    
    # Upload manifest
    aws s3 cp "$manifest_file" "s3://$WASABI_BUCKET/deployments/manifest_$(date +%Y%m%d_%H%M%S).json" --endpoint-url "$WASABI_ENDPOINT_URL"
    
    # Cleanup
    rm -f "$manifest_file"
    
    success "Files uploaded to Wasabi"
}

# Create backup
create_backup() {
    log "Creating backup of current deployment..."
    
    cd "$PROJECT_DIR"
    
    local backup_name="backup_$(date +%Y%m%d_%H%M%S)"
    local backup_file="${backup_name}.tar.gz"
    
    # Create backup
    tar -czf "$backup_file" \
        --exclude='venv' \
        --exclude='__pycache__' \
        --exclude='.git' \
        --exclude='*.pyc' \
        --exclude='*.log' \
        --exclude='temp' \
        --exclude='output' \
        .
    
    # Upload backup to Wasabi
    aws s3 cp "$backup_file" "s3://$WASABI_BUCKET/backups/$backup_file" --endpoint-url "$WASABI_ENDPOINT_URL"
    
    # Cleanup local backup
    rm -f "$backup_file"
    
    success "Backup created: $backup_name"
}

# Clean old backups
cleanup_old_backups() {
    log "Cleaning up old backups..."
    
    # List backups and keep only the latest N
    local backups=$(aws s3 ls "s3://$WASABI_BUCKET/backups/" --endpoint-url "$WASABI_ENDPOINT_URL" | sort -k1,2 | tail -n +$((BACKUP_COUNT + 1)) | awk '{print $4}')
    
    for backup in $backups; do
        aws s3 rm "s3://$WASABI_BUCKET/backups/$backup" --endpoint-url "$WASABI_ENDPOINT_URL"
        log "Removed old backup: $backup"
    done
    
    success "Old backups cleaned up"
}

# Update production environment
update_production() {
    log "Updating production environment..."
    
    # This would typically involve:
    # 1. Pulling from Wasabi to production servers
    # 2. Restarting services
    # 3. Running health checks
    
    # For now, we'll create a deployment script
    cat > deploy_production.sh << 'EOF'
#!/bin/bash
# Production deployment script
# This script should be run on production servers

set -e

WASABI_BUCKET="ai-video-generator"
WASABI_ENDPOINT_URL="${WASABI_ENDPOINT_URL}"
DEPLOYMENT_DIR="/opt/ai-video-generator"

# Download latest deployment
mkdir -p "$DEPLOYMENT_DIR"
cd "$DEPLOYMENT_DIR"

# Download and extract latest package
LATEST_PACKAGE=$(aws s3 ls "s3://$WASABI_BUCKET/deployments/" --endpoint-url "$WASABI_ENDPOINT_URL" | sort | tail -n 1 | awk '{print $4}')
aws s3 cp "s3://$WASABI_BUCKET/deployments/$LATEST_PACKAGE" . --endpoint-url "$WASABI_ENDPOINT_URL"
tar -xzf "$LATEST_PACKAGE"

# Restart services
docker-compose down || true
docker-compose up -d

# Health check
sleep 30
curl -f http://localhost:8000/health || exit 1

echo "Production deployment completed successfully"
EOF
    
    chmod +x deploy_production.sh
    
    # Upload deployment script
    aws s3 cp deploy_production.sh "s3://$WASABI_BUCKET/scripts/deploy_production.sh" --endpoint-url "$WASABI_ENDPOINT_URL"
    
    success "Production deployment script updated"
}

# Send notification
send_notification() {
    local status="$1"
    local message="$2"
    
    log "Sending notification..."
    
    # Create notification payload
    local notification_file="notification_$(date +%Y%m%d_%H%M%S).json"
    cat > "$notification_file" << EOF
{
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "status": "$status",
    "message": "$message",
    "deployment_id": "$(date +%Y%m%d_%H%M%S)",
    "git_commit": "$(git rev-parse HEAD)",
    "git_branch": "$(git rev-parse --abbrev-ref HEAD)"
}
EOF
    
    # Upload notification
    aws s3 cp "$notification_file" "s3://$WASABI_BUCKET/notifications/$notification_file" --endpoint-url "$WASABI_ENDPOINT_URL"
    
    # Cleanup
    rm -f "$notification_file"
    
    success "Notification sent"
}

# Main deployment function
main() {
    log "Starting Git to Wasabi deployment workflow..."
    
    local start_time=$(date +%s)
    
    # Check if running in CI/CD or manually
    if [ "${CI:-false}" = "true" ]; then
        log "Running in CI/CD mode"
    else
        log "Running in manual mode"
    fi
    
    # Main workflow
    check_dependencies
    check_environment
    
    # Create backup before deployment
    create_backup
    
    # Git operations
    git_pull
    
    # Build and test
    install_dependencies
    run_tests
    build_docker
    
    # Package and deploy
    local package_file=$(create_package)
    upload_to_wasabi "$package_file"
    
    # Update production
    update_production
    
    # Cleanup
    cleanup_old_backups
    rm -f "$package_file"
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    success "Deployment completed successfully in ${duration}s"
    send_notification "success" "Deployment completed successfully in ${duration}s"
}

# Error handling
trap 'error "Deployment failed at line $LINENO"; send_notification "error" "Deployment failed at line $LINENO"; exit 1' ERR

# Run main function if script is executed directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi
