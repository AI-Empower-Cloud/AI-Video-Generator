#!/bin/bash
# 🚀 AI Video Generator - Container Deployment Script
# Deploys containers to various environments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
REGISTRY="ghcr.io"
NAMESPACE="ai-empower-cloud"
IMAGE_NAME="ai-video-generator"
FULL_IMAGE_NAME="$REGISTRY/$NAMESPACE/$IMAGE_NAME"

echo -e "${BLUE}🚀 AI Video Generator - Container Deployment${NC}"
echo -e "${BLUE}=============================================${NC}"

# Function to deploy locally
deploy_local() {
    echo -e "${BLUE}🏠 Deploying locally with Docker Compose...${NC}"
    
    # Stop existing containers
    docker-compose down 2>/dev/null || true
    
    # Start containers
    docker-compose up -d
    
    echo -e "${GREEN}✅ Local deployment started${NC}"
    echo -e "${BLUE}📋 Services running:${NC}"
    docker-compose ps
    
    echo -e "${BLUE}🌐 Access URLs:${NC}"
    echo -e "  Main App: ${YELLOW}http://localhost:8000${NC}"
    echo -e "  Streamlit: ${YELLOW}http://localhost:8503${NC}"
    echo -e "  Frontend: ${YELLOW}http://localhost:3000${NC}"
}

# Function to deploy to development environment
deploy_dev() {
    echo -e "${BLUE}🧪 Deploying to development environment...${NC}"
    
    # Use development compose file
    docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
    docker-compose -f docker-compose.dev.yml up -d
    
    echo -e "${GREEN}✅ Development deployment started${NC}"
    docker-compose -f docker-compose.dev.yml ps
}

# Function to deploy to production
deploy_prod() {
    echo -e "${BLUE}🏭 Deploying to production environment...${NC}"
    
    # Use production compose file
    docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
    docker-compose -f docker-compose.prod.yml up -d
    
    echo -e "${GREEN}✅ Production deployment started${NC}"
    docker-compose -f docker-compose.prod.yml ps
}

# Function to deploy to cloud (Wasabi/AWS)
deploy_cloud() {
    echo -e "${BLUE}☁️  Deploying to cloud environment...${NC}"
    
    # Check if cloud credentials are available
    if [ -z "$WASABI_ACCESS_KEY" ] || [ -z "$WASABI_SECRET_KEY" ]; then
        echo -e "${YELLOW}⚠️  Cloud credentials not found. Setting up environment...${NC}"
        source ./configure_wasabi_keys.sh
    fi
    
    # Deploy to cloud using Docker Swarm or Kubernetes
    if command -v kubectl &> /dev/null; then
        echo -e "${BLUE}🎛️  Deploying with Kubernetes...${NC}"
        kubectl apply -f k8s/
    elif docker node ls &> /dev/null; then
        echo -e "${BLUE}🐝 Deploying with Docker Swarm...${NC}"
        docker stack deploy -c docker-compose.prod.yml ai-video-stack
    else
        echo -e "${YELLOW}⚠️  No orchestration platform found. Using single node deployment...${NC}"
        deploy_prod
    fi
    
    echo -e "${GREEN}✅ Cloud deployment initiated${NC}"
}

# Function to show status
show_status() {
    echo -e "${BLUE}📊 Container Status${NC}"
    echo -e "${BLUE}==================${NC}"
    
    if docker-compose ps | grep -q "Up"; then
        echo -e "${GREEN}✅ Services are running${NC}"
        docker-compose ps
        
        echo -e "${BLUE}📈 Resource Usage:${NC}"
        docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
    else
        echo -e "${YELLOW}⚠️  No services are currently running${NC}"
    fi
}

# Function to show logs
show_logs() {
    local service=${1:-ai-video-generator}
    echo -e "${BLUE}📋 Showing logs for $service...${NC}"
    docker-compose logs -f --tail=50 "$service"
}

# Function to stop all services
stop_services() {
    echo -e "${BLUE}🛑 Stopping all services...${NC}"
    
    docker-compose down 2>/dev/null || true
    docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
    docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
    
    echo -e "${GREEN}✅ All services stopped${NC}"
}

# Function to update containers
update_containers() {
    echo -e "${BLUE}🔄 Updating containers...${NC}"
    
    # Pull latest images
    docker-compose pull
    
    # Restart with updated images
    docker-compose up -d
    
    echo -e "${GREEN}✅ Containers updated${NC}"
}

# Function to backup data
backup_data() {
    local backup_dir="./backups/$(date +%Y%m%d_%H%M%S)"
    echo -e "${BLUE}💾 Creating backup in $backup_dir...${NC}"
    
    mkdir -p "$backup_dir"
    
    # Backup volumes
    docker run --rm \
        -v "$(pwd)/canvas_projects:/source:ro" \
        -v "$backup_dir:/backup" \
        alpine tar czf /backup/canvas_projects.tar.gz -C /source .
    
    docker run --rm \
        -v "$(pwd)/video_output:/source:ro" \
        -v "$backup_dir:/backup" \
        alpine tar czf /backup/video_output.tar.gz -C /source .
    
    echo -e "${GREEN}✅ Backup created in $backup_dir${NC}"
}

# Function to show help
show_help() {
    echo -e "${BLUE}🎬 AI Video Generator - Container Deployment${NC}"
    echo -e "${BLUE}Usage: $0 [COMMAND]${NC}"
    echo ""
    echo -e "${YELLOW}Commands:${NC}"
    echo -e "  local     Deploy locally with Docker Compose"
    echo -e "  dev       Deploy to development environment"
    echo -e "  prod      Deploy to production environment"
    echo -e "  cloud     Deploy to cloud environment"
    echo -e "  status    Show container status"
    echo -e "  logs      Show container logs [service]"
    echo -e "  stop      Stop all services"
    echo -e "  update    Update containers with latest images"
    echo -e "  backup    Backup container data"
    echo -e "  help      Show this help message"
    echo ""
    echo -e "${BLUE}Examples:${NC}"
    echo -e "  $0 local          # Deploy locally"
    echo -e "  $0 logs api       # Show logs for api service"
    echo -e "  $0 status         # Show current status"
}

# Main execution
case "${1:-local}" in
    local)
        deploy_local
        ;;
    dev)
        deploy_dev
        ;;
    prod)
        deploy_prod
        ;;
    cloud)
        deploy_cloud
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs "${2:-ai-video-generator}"
        ;;
    stop)
        stop_services
        ;;
    update)
        update_containers
        ;;
    backup)
        backup_data
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}❌ Unknown command: $1${NC}"
        show_help
        exit 1
        ;;
esac

echo -e "${GREEN}🎉 Deployment operation completed!${NC}"
