#!/bin/bash
# 🐳 AI Video Generator - Docker Build & Push Script
# Builds and pushes Docker images with proper tagging

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

# Get version from git tag or use timestamp
VERSION=$(git describe --tags --exact-match 2>/dev/null || echo "v$(date +%Y%m%d_%H%M%S)")
COMMIT_SHA=$(git rev-parse --short HEAD)
BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)

echo -e "${BLUE}🐳 AI Video Generator Docker Build & Push${NC}"
echo -e "${BLUE}=======================================${NC}"
echo -e "Registry: ${YELLOW}$REGISTRY${NC}"
echo -e "Image: ${YELLOW}$FULL_IMAGE_NAME${NC}"
echo -e "Version: ${YELLOW}$VERSION${NC}"
echo -e "Commit: ${YELLOW}$COMMIT_SHA${NC}"
echo -e "Branch: ${YELLOW}$BRANCH_NAME${NC}"
echo ""

# Function to build and tag image
build_image() {
    local dockerfile=$1
    local tag_suffix=$2
    local description=$3
    
    echo -e "${BLUE}📦 Building $description...${NC}"
    
    docker build \
        -f "$dockerfile" \
        -t "$FULL_IMAGE_NAME:$tag_suffix" \
        -t "$FULL_IMAGE_NAME:$tag_suffix-$COMMIT_SHA" \
        --build-arg VERSION="$VERSION" \
        --build-arg COMMIT_SHA="$COMMIT_SHA" \
        --build-arg BUILD_DATE="$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
        .
    
    echo -e "${GREEN}✅ Built $description successfully${NC}"
}

# Function to push image
push_image() {
    local tag=$1
    local description=$2
    
    echo -e "${BLUE}🚀 Pushing $description...${NC}"
    docker push "$FULL_IMAGE_NAME:$tag"
    echo -e "${GREEN}✅ Pushed $description successfully${NC}"
}

# Main execution
main() {
    # Check if Docker is running
    if ! docker info >/dev/null 2>&1; then
        echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
        exit 1
    fi
    
    # Build production image
    echo -e "${BLUE}🏗️  Building Production Image${NC}"
    build_image "Dockerfile" "latest" "Production Image"
    build_image "Dockerfile" "$VERSION" "Production Image (Tagged)"
    
    # Build development image
    echo -e "${BLUE}🏗️  Building Development Image${NC}"
    build_image "Dockerfile.dev" "dev" "Development Image"
    build_image "Dockerfile.dev" "dev-$COMMIT_SHA" "Development Image (Tagged)"
    
    # Tag with branch name if not main
    if [ "$BRANCH_NAME" != "main" ] && [ "$BRANCH_NAME" != "master" ]; then
        docker tag "$FULL_IMAGE_NAME:latest" "$FULL_IMAGE_NAME:$BRANCH_NAME"
        echo -e "${GREEN}✅ Tagged with branch name: $BRANCH_NAME${NC}"
    fi
    
    # Show built images
    echo -e "${BLUE}📋 Built Images:${NC}"
    docker images "$FULL_IMAGE_NAME" --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
    
    # Ask for push confirmation
    echo ""
    read -p "🤔 Do you want to push images to registry? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}🔐 Logging into GitHub Container Registry...${NC}"
        echo "$GITHUB_TOKEN" | docker login ghcr.io -u "$GITHUB_USERNAME" --password-stdin
        
        # Push all tags
        push_image "latest" "Latest Production"
        push_image "$VERSION" "Version $VERSION"
        push_image "dev" "Latest Development"
        push_image "dev-$COMMIT_SHA" "Development $COMMIT_SHA"
        
        if [ "$BRANCH_NAME" != "main" ] && [ "$BRANCH_NAME" != "master" ]; then
            push_image "$BRANCH_NAME" "Branch $BRANCH_NAME"
        fi
        
        echo -e "${GREEN}🎉 All images pushed successfully!${NC}"
        echo -e "${BLUE}📦 Images available at:${NC}"
        echo -e "  Production: ${YELLOW}$FULL_IMAGE_NAME:latest${NC}"
        echo -e "  Version: ${YELLOW}$FULL_IMAGE_NAME:$VERSION${NC}"
        echo -e "  Development: ${YELLOW}$FULL_IMAGE_NAME:dev${NC}"
    else
        echo -e "${YELLOW}⏭️  Skipping push to registry${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}🎬 Docker build process completed!${NC}"
    echo -e "${BLUE}💡 To run locally:${NC}"
    echo -e "  Production: ${YELLOW}docker run -p 8000:8000 $FULL_IMAGE_NAME:latest${NC}"
    echo -e "  Development: ${YELLOW}docker run -p 8000:8000 $FULL_IMAGE_NAME:dev${NC}"
    echo -e "  With compose: ${YELLOW}docker-compose up${NC}"
}

# Cleanup function
cleanup() {
    echo -e "${BLUE}🧹 Cleaning up...${NC}"
    docker system prune -f
    echo -e "${GREEN}✅ Cleanup completed${NC}"
}

# Handle script arguments
case "${1:-}" in
    --clean)
        cleanup
        ;;
    --push-only)
        # Push existing images
        push_image "latest" "Latest Production"
        push_image "dev" "Latest Development"
        ;;
    *)
        main
        ;;
esac
