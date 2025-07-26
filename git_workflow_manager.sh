#!/bin/bash

# 🚀 AI Video Generator - Git Workflow Manager
# =============================================
# 
# This script helps manage the Git workflow for the modular AI Video Generator.
# It creates small, focused commits and manages tags for releases.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="https://github.com/your-username/AI-Video-Generator.git"
MAIN_BRANCH="main"
DEVELOP_BRANCH="develop"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if we're in a git repository
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not a git repository. Please run 'git init' first."
        exit 1
    fi
}

# Function to initialize Git repository if needed
init_git_repo() {
    if [ ! -d ".git" ]; then
        print_status "Initializing Git repository..."
        git init
        git branch -M $MAIN_BRANCH
        
        if [ -n "$REPO_URL" ]; then
            git remote add origin $REPO_URL
            print_success "Added remote origin: $REPO_URL"
        fi
    fi
}

# Function to create and push small focused commits
commit_module() {
    local module_name="$1"
    local description="$2"
    local files=("${@:3}")
    
    if [ ${#files[@]} -eq 0 ]; then
        print_error "No files specified for module: $module_name"
        return 1
    fi
    
    print_status "Committing module: $module_name"
    
    # Add files
    for file in "${files[@]}"; do
        if [ -f "$file" ] || [ -d "$file" ]; then
            git add "$file"
            print_status "Added: $file"
        else
            print_warning "File not found: $file"
        fi
    done
    
    # Create commit
    local commit_message="🧩 Add $module_name module

$description

Components:
$(printf "- %s\n" "${files[@]}")

Type: feature
Scope: $module_name"
    
    git commit -m "$commit_message"
    print_success "Committed: $module_name"
}

# Function to create a release tag
create_release_tag() {
    local version="$1"
    local description="$2"
    
    if [ -z "$version" ]; then
        print_error "Version number required"
        echo "Usage: create_release_tag <version> [description]"
        return 1
    fi
    
    # Ensure version starts with 'v'
    if [[ ! "$version" =~ ^v ]]; then
        version="v$version"
    fi
    
    print_status "Creating release tag: $version"
    
    # Create annotated tag
    local tag_message="🏷️ Release $version

${description:-"Release $version of AI Video Generator"}

## Features
- Modular architecture with core components
- Advanced canvas editor
- React frontend with Next.js
- Automated CI/CD pipeline

## Components
- Core data models and managers
- Canvas editor engine
- Frontend UI components
- GitHub workflows"
    
    git tag -a "$version" -m "$tag_message"
    print_success "Created tag: $version"
}

# Function to push changes to GitHub
push_to_github() {
    local branch="${1:-$MAIN_BRANCH}"
    local push_tags="${2:-false}"
    
    print_status "Pushing to GitHub..."
    
    # Check if remote exists
    if ! git remote get-url origin > /dev/null 2>&1; then
        print_error "No remote 'origin' configured. Please add it first:"
        echo "git remote add origin <your-repo-url>"
        return 1
    fi
    
    # Push branch
    git push origin "$branch"
    print_success "Pushed branch: $branch"
    
    # Push tags if requested
    if [ "$push_tags" = "true" ]; then
        git push origin --tags
        print_success "Pushed tags"
    fi
}

# Function to build and push Docker containers
build_and_push_containers() {
    print_step "Building and pushing Docker containers"
    
    # Check if Docker is available
    if ! command -v docker &> /dev/null; then
        print_warning "Docker not found. Skipping container build."
        return 0
    fi
    
    # Check if docker-build.sh exists
    if [ ! -f "./docker-build.sh" ]; then
        print_warning "docker-build.sh not found. Skipping container build."
        return 0
    fi
    
    print_info "Building Docker containers..."
    
    # Make sure script is executable
    chmod +x ./docker-build.sh
    
    # Run the Docker build script
    if ./docker-build.sh; then
        print_success "Docker containers built successfully"
        return 0
    else
        print_error "Docker build failed"
        return 1
    fi
}

# Function to create container deployment
create_container_deployment() {
    local version=$1
    local environment=${2:-production}
    
    print_step "Creating container deployment for $environment"
    
    # Check if deploy script exists
    if [ ! -f "./deploy-containers.sh" ]; then
        print_warning "deploy-containers.sh not found. Skipping deployment."
        return 0
    fi
    
    # Make sure script is executable
    chmod +x ./deploy-containers.sh
    
    case $environment in
        "production"|"prod")
            print_info "Deploying to production environment..."
            ./deploy-containers.sh prod
            ;;
        "staging"|"stage")
            print_info "Deploying to staging environment..."
            ./deploy-containers.sh dev
            ;;
        "local")
            print_info "Deploying locally..."
            ./deploy-containers.sh local
            ;;
        *)
            print_info "Deploying to $environment..."
            ./deploy-containers.sh "$environment"
            ;;
    esac
    
    print_success "Container deployment completed"
}

# Function to create workflow for modular commits
create_modular_commits() {
    print_status "Creating modular commits for AI Video Generator..."
    
    # Core module commit
    commit_module "Core" \
        "Core data models and base classes for the modular architecture" \
        "core/" \
        "core/__init__.py" \
        "core/models.py" \
        "core/base.py"
    
    # Modular editor commit  
    commit_module "Modular-Canvas-Editor" \
        "Modular canvas editor built with composition pattern" \
        "modular_canvas_editor.py"
    
    # Frontend commit
    if [ -d "frontend" ]; then
        commit_module "Frontend" \
            "Modern React frontend with Next.js and Tailwind CSS" \
            "frontend/"
    fi
    
    # Workflows commit
    commit_module "CI-CD-Workflows" \
        "GitHub Actions workflows for testing, building, and deployment" \
        ".github/workflows/modular-ci-cd.yml" \
        "git_workflow_manager.sh"
    
    # Documentation commit
    if [ -f "README.md" ]; then
        commit_module "Documentation" \
            "Project documentation and setup guides" \
            "README.md" \
            "CHANGELOG.md"
    fi
    
    print_success "All modular commits created!"
}

# Function to sync node_modules with Wasabi
sync_node_modules() {
    print_status "🔄 Syncing node_modules with Wasabi..."
    
    # Check if Wasabi is configured
    if [[ ! -f ".env.wasabi" ]]; then
        print_warning "Wasabi not configured - skipping node_modules sync"
        print_info "Run ./configure_wasabi_keys.sh to set up Wasabi"
        return 0
    fi
    
    # Check if wasabi node modules manager exists
    if [[ ! -f "./wasabi_node_modules.sh" ]]; then
        print_warning "Wasabi node_modules manager not found - skipping sync"
        return 0
    fi
    
    # Sync all Node.js projects
    ./wasabi_node_modules.sh sync --all || {
        print_warning "Some node_modules sync operations failed"
        return 0  # Don't fail the workflow
    }
    
    print_success "Node modules synced with Wasabi"
}

# Function to display help
show_help() {
    echo "🚀 AI Video Generator - Git Workflow Manager"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  init                          Initialize Git repository"
    echo "  commit-modules               Create modular commits"
    echo "  tag <version> [description]  Create release tag"
    echo "  push [branch] [--tags]       Push to GitHub"
    echo "  release <version> [env]      Create tag, build containers, and push"
    echo "  containers                   Build and push Docker containers"
    echo "  deploy <version> [env]       Deploy containers to environment"
    echo "  setup                        Complete setup (init + commits + optional containers)"
    echo "  help                         Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 setup                     # Complete setup with optional containers"
    echo "  $0 tag v1.0.0               # Create v1.0.0 tag"
    echo "  $0 containers                # Build and push Docker containers"
    echo "  $0 release v1.1.0 prod      # Create v1.1.0, build containers, and deploy to prod"
    echo "  $0 deploy v1.0.0 local      # Deploy v1.0.0 to local environment"
}

# Main script logic
main() {
    case "${1:-help}" in
        "init")
            init_git_repo
            ;;
        "commit-modules")
            check_git_repo
            create_modular_commits
            ;;
        "tag")
            check_git_repo
            create_release_tag "$2" "$3"
            ;;
        "push")
            check_git_repo
            local push_tags_flag="false"
            if [ "$3" = "--tags" ]; then
                push_tags_flag="true"
            fi
            push_to_github "$2" "$push_tags_flag"
            ;;
        "release")
            if [ -z "$2" ]; then
                print_error "Version required for release"
                echo "Usage: $0 release <version> [environment]"
                exit 1
            fi
            check_git_repo
            create_release_tag "$2" "Official release $2"
            
            # Sync node_modules before release
            sync_node_modules
            
            # Build and push containers
            print_step "Building containers for release $2"
            if build_and_push_containers; then
                print_success "Containers built and pushed"
            else
                print_warning "Container build failed, continuing with git push"
            fi
            
            push_to_github "$MAIN_BRANCH" "true"
            
            # Optional deployment
            if [ -n "$3" ]; then
                create_container_deployment "$2" "$3"
            fi
            ;;
        "setup")
            print_status "🚀 Setting up AI Video Generator Git workflow..."
            init_git_repo
            create_modular_commits
            
            # Sync node_modules with Wasabi
            sync_node_modules
            
            # Ask if user wants to build containers
            read -p "🐳 Build Docker containers? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                build_and_push_containers
            fi
            
            print_status "Ready to push! Run: $0 push main --tags"
            ;;
        "containers")
            build_and_push_containers
            ;;
        "deploy")
            create_container_deployment "${2:-v1.0.0}" "${3:-local}"
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Run main function with all arguments
main "$@"
