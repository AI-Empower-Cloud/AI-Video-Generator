#!/bin/bash

# Development environment setup script

set -e

echo "🛠️ Setting up development environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Create development environment
setup_dev() {
    log_info "Setting up development environment..."
    
    # Create necessary directories
    mkdir -p generated_videos logs temp data
    
    # Build and start development containers
    docker-compose -f docker-compose.dev.yml down || true
    docker-compose -f docker-compose.dev.yml build
    docker-compose -f docker-compose.dev.yml up -d
    
    log_info "Development environment is ready! ✅"
    log_info "Application: http://localhost:8503"
    log_info "Logs: docker-compose -f docker-compose.dev.yml logs -f"
}

# Run tests
run_tests() {
    log_info "Running tests..."
    docker-compose -f docker-compose.dev.yml exec ai-video-generator python -m pytest tests/ -v
}

# Stop development environment
stop_dev() {
    log_info "Stopping development environment..."
    docker-compose -f docker-compose.dev.yml down
    log_info "Development environment stopped ✅"
}

# Show logs
show_logs() {
    docker-compose -f docker-compose.dev.yml logs -f
}

# Main function
case "${1:-setup}" in
    setup)
        setup_dev
        ;;
    test)
        run_tests
        ;;
    stop)
        stop_dev
        ;;
    logs)
        show_logs
        ;;
    *)
        echo "Usage: $0 {setup|test|stop|logs}"
        echo "  setup - Set up development environment"
        echo "  test  - Run tests"
        echo "  stop  - Stop development environment"
        echo "  logs  - Show application logs"
        exit 1
        ;;
esac
