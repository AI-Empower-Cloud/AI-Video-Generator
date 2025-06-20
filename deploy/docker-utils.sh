#!/bin/bash

# Docker deployment utilities

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to build and push to registry
build_and_push() {
    local tag=${1:-latest}
    local registry=${2:-ghcr.io}
    
    log_info "Building and pushing Docker image with tag: $tag"
    
    # Build image
    docker build -t ai-video-generator:$tag .
    
    # Tag for registry
    docker tag ai-video-generator:$tag $registry/yourusername/ai-video-generator:$tag
    
    # Push to registry
    docker push $registry/yourusername/ai-video-generator:$tag
    
    log_info "Image pushed successfully ✅"
}

# Function to deploy to production
deploy_production() {
    log_info "Deploying to production..."
    
    # Pull latest image
    docker-compose -f docker-compose.prod.yml pull
    
    # Deploy with zero downtime
    docker-compose -f docker-compose.prod.yml up -d --force-recreate
    
    # Wait for health check
    sleep 30
    
    if curl -f http://localhost/health > /dev/null 2>&1; then
        log_info "Production deployment successful ✅"
    else
        log_error "Production deployment failed ❌"
        exit 1
    fi
}

# Function to deploy to staging
deploy_staging() {
    log_info "Deploying to staging..."
    
    # Use development compose file for staging
    docker-compose -f docker-compose.dev.yml down || true
    docker-compose -f docker-compose.dev.yml up -d --build
    
    log_info "Staging deployment completed ✅"
}

# Function to run health checks
health_check() {
    log_info "Running health checks..."
    
    local endpoints=(
        "http://localhost:8503/_stcore/health"
        "http://localhost/health"
    )
    
    for endpoint in "${endpoints[@]}"; do
        if curl -f "$endpoint" > /dev/null 2>&1; then
            log_info "✅ $endpoint is healthy"
        else
            log_warn "⚠️ $endpoint is not responding"
        fi
    done
}

# Function to backup data
backup_data() {
    local backup_path="./backups/$(date +%Y%m%d_%H%M%S)"
    
    log_info "Creating backup at $backup_path"
    
    mkdir -p "$backup_path"
    
    # Backup generated videos
    if [ -d "./generated_videos" ]; then
        cp -r ./generated_videos "$backup_path/"
    fi
    
    # Backup logs
    if [ -d "./logs" ]; then
        cp -r ./logs "$backup_path/"
    fi
    
    # Backup database if exists
    if [ -f "./app.db" ]; then
        cp ./app.db "$backup_path/"
    fi
    
    log_info "Backup completed ✅"
}

# Function to restore from backup
restore_backup() {
    local backup_path=$1
    
    if [ -z "$backup_path" ] || [ ! -d "$backup_path" ]; then
        log_error "Invalid backup path: $backup_path"
        exit 1
    fi
    
    log_info "Restoring from backup: $backup_path"
    
    # Stop services
    docker-compose -f docker-compose.prod.yml down
    
    # Restore data
    if [ -d "$backup_path/generated_videos" ]; then
        rm -rf ./generated_videos
        cp -r "$backup_path/generated_videos" ./
    fi
    
    if [ -d "$backup_path/logs" ]; then
        rm -rf ./logs
        cp -r "$backup_path/logs" ./
    fi
    
    if [ -f "$backup_path/app.db" ]; then
        cp "$backup_path/app.db" ./
    fi
    
    # Restart services
    docker-compose -f docker-compose.prod.yml up -d
    
    log_info "Restore completed ✅"
}

# Function to monitor logs
monitor_logs() {
    local service=${1:-ai-video-generator}
    
    log_info "Monitoring logs for service: $service"
    docker-compose -f docker-compose.prod.yml logs -f $service
}

# Function to scale services
scale_service() {
    local service=${1:-ai-video-generator}
    local replicas=${2:-2}
    
    log_info "Scaling $service to $replicas replicas"
    docker-compose -f docker-compose.prod.yml up -d --scale $service=$replicas
}

# Main menu
show_menu() {
    echo "🐳 Docker Deployment Manager"
    echo "============================"
    echo "1. Build and Push Image"
    echo "2. Deploy to Production"
    echo "3. Deploy to Staging"
    echo "4. Run Health Checks"
    echo "5. Backup Data"
    echo "6. Restore from Backup"
    echo "7. Monitor Logs"
    echo "8. Scale Services"
    echo "9. Exit"
    echo ""
}

# Main execution
case "${1:-menu}" in
    build)
        build_and_push "${2:-latest}" "${3:-ghcr.io}"
        ;;
    prod)
        deploy_production
        ;;
    staging)
        deploy_staging
        ;;
    health)
        health_check
        ;;
    backup)
        backup_data
        ;;
    restore)
        restore_backup "$2"
        ;;
    logs)
        monitor_logs "$2"
        ;;
    scale)
        scale_service "$2" "$3"
        ;;
    menu)
        while true; do
            show_menu
            read -p "Choose an option [1-9]: " choice
            case $choice in
                1) read -p "Enter tag (default: latest): " tag; build_and_push "${tag:-latest}" ;;
                2) deploy_production ;;
                3) deploy_staging ;;
                4) health_check ;;
                5) backup_data ;;
                6) read -p "Enter backup path: " path; restore_backup "$path" ;;
                7) read -p "Enter service name (default: ai-video-generator): " service; monitor_logs "${service:-ai-video-generator}" ;;
                8) read -p "Service name: " service; read -p "Replicas: " replicas; scale_service "$service" "$replicas" ;;
                9) log_info "Goodbye! 👋"; exit 0 ;;
                *) log_error "Invalid option" ;;
            esac
            echo ""
        done
        ;;
    *)
        echo "Usage: $0 {build|prod|staging|health|backup|restore|logs|scale|menu}"
        exit 1
        ;;
esac
