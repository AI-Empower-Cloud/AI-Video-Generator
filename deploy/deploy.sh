#!/bin/bash

# Production deployment script for AI Video Generator

set -e

echo "🚀 Starting production deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.prod.yml"
BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi
    
    log_info "Prerequisites check passed ✅"
}

# Create backup
create_backup() {
    if [ -d "./generated_videos" ] || [ -d "./logs" ]; then
        log_info "Creating backup..."
        mkdir -p "$BACKUP_DIR"
        
        if [ -d "./generated_videos" ]; then
            cp -r ./generated_videos "$BACKUP_DIR/"
        fi
        
        if [ -d "./logs" ]; then
            cp -r ./logs "$BACKUP_DIR/"
        fi
        
        log_info "Backup created at $BACKUP_DIR ✅"
    fi
}

# Pull latest changes
pull_latest() {
    log_info "Pulling latest changes from Git..."
    git pull origin main || log_warn "Git pull failed, continuing with local version"
}

# Build and deploy
deploy() {
    log_info "Building and deploying application..."
    
    # Stop existing containers
    docker-compose -f "$COMPOSE_FILE" down || true
    
    # Build new images
    docker-compose -f "$COMPOSE_FILE" build --no-cache
    
    # Start services
    docker-compose -f "$COMPOSE_FILE" up -d
    
    # Wait for services to be healthy
    log_info "Waiting for services to be healthy..."
    sleep 30
    
    # Check health
    if curl -f http://localhost:8503/_stcore/health > /dev/null 2>&1; then
        log_info "Application is healthy ✅"
    else
        log_error "Application health check failed ❌"
        log_info "Checking logs..."
        docker-compose -f "$COMPOSE_FILE" logs --tail=50
        exit 1
    fi
}

# Cleanup old images
cleanup() {
    log_info "Cleaning up old Docker images..."
    docker image prune -f
    docker system prune -f --volumes
    log_info "Cleanup completed ✅"
}

# Main deployment flow
main() {
    echo "🎬 AI Video Generator - Production Deployment"
    echo "=============================================="
    
    check_prerequisites
    create_backup
    pull_latest
    deploy
    cleanup
    
    log_info "🎉 Deployment completed successfully!"
    log_info "Application is running at: http://localhost"
    log_info "Health check: http://localhost/health"
    log_info "Logs: docker-compose -f $COMPOSE_FILE logs -f"
}

# Handle script interruption
trap 'log_error "Deployment interrupted"; exit 1' INT TERM

# Run main function
main "$@"
