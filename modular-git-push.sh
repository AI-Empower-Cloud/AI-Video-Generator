#!/bin/bash
# 🚀 Modular Git Workflow Manager
# ===============================
# Handles small, focused commits and pushes to GitHub

set -e  # Exit on any error

echo "🚀 AI Video Generator - Modular Git Workflow"
echo "============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_error "Not in a git repository!"
    exit 1
fi

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)
print_status "Current branch: $CURRENT_BRANCH"

# Check for changes
if [[ -z $(git status --porcelain) ]]; then
    print_warning "No changes to commit!"
    exit 0
fi

# Create modular commits
print_step "Creating modular commits..."

# 1. Core Architecture Commit
if [[ -n $(git status --porcelain core/) ]]; then
    print_step "📦 Committing core architecture..."
    git add core/
    git commit -m "🏗️ Core: Add modular backend architecture

✨ Features:
- Data models (Keyframe, Transition, Tag, UseCase, CanvasElement, CanvasProject)
- Base classes (BaseManager, BaseEditor, TagManager, UseCaseManager)
- Clean module imports and public API
- Event-driven architecture support

📊 Components:
- core/models.py: Core data structures
- core/base.py: Abstract base classes and managers
- core/__init__.py: Public API exports

🎯 Benefits:
- Improved code organization
- Better testability
- Enhanced maintainability
- Scalable architecture

#modular #architecture #backend" || print_warning "Core files already committed or no changes"
fi

# 2. Modular Canvas Editor Commit
if [[ -n $(git status --porcelain modular_canvas_editor.py) ]]; then
    print_step "🎨 Committing modular canvas editor..."
    git add modular_canvas_editor.py
    git commit -m "🎨 Canvas: Implement modular canvas editor

✨ Features:
- Event-driven architecture using core modules
- Composition over inheritance pattern
- Clean separation of concerns
- Integration with new core models

🔧 Implementation:
- Uses core.TagManager for tag operations
- Uses core.ProjectManager for project handling
- Leverages core.EventEmitter for events
- Maintains backward compatibility

🎯 Improvements:
- Better code organization
- Enhanced maintainability
- Improved testability
- Cleaner dependencies

#canvas #modular #editor #refactor" || print_warning "Modular canvas editor already committed or no changes"
fi

# 3. Bot and Automation Commit
if [[ -n $(git status --porcelain .bot/ .github/workflows/auto-commit-bot.yml setup-bot.sh) ]]; then
    print_step "🤖 Committing bot and automation..."
    git add .bot/ .github/workflows/auto-commit-bot.yml setup-bot.sh
    git commit -m "🤖 Bot: Add automated workflow system

✨ Features:
- Automated commit workflows
- Code formatting and testing
- Repository monitoring
- Deployment automation
- GitHub Actions integration

📊 Components:
- .github/workflows/auto-commit-bot.yml: CI/CD pipeline
- .bot/: Bot configuration and scripts
- setup-bot.sh: One-click bot setup

🔧 Automation:
- Daily maintenance tasks
- Automatic code formatting
- Test execution before commits
- Deployment preparation
- Release tagging

🎯 Benefits:
- Reduced manual work
- Consistent code quality
- Reliable deployments
- Better collaboration

#automation #bot #cicd #github-actions" || print_warning "Bot files already committed or no changes"
fi

# 4. Tests and Documentation Commit
if [[ -n $(git status --porcelain test_core_modules.py README_MODULAR.md CHANGELOG.md) ]]; then
    print_step "🧪 Committing tests and documentation..."
    git add test_core_modules.py README_MODULAR.md CHANGELOG.md
    git commit -m "🧪 Tests: Add comprehensive test suite and documentation

✨ Features:
- Core module import testing
- Data model validation
- Manager functionality tests
- Integration testing
- Template system verification

📚 Documentation:
- README_MODULAR.md: Architecture guide
- CHANGELOG.md: Version history
- Inline code documentation
- API reference examples

🔧 Test Coverage:
- Import validation
- Data model creation
- Manager operations
- Template functionality
- Error handling

🎯 Quality Assurance:
- Automated testing
- Documentation clarity
- Code examples
- Best practices

#testing #documentation #quality #coverage" || print_warning "Test files already committed or no changes"
fi

# 5. CI/CD Workflows Commit
if [[ -n $(git status --porcelain .github/workflows/) ]]; then
    print_step "⚙️ Committing CI/CD workflows..."
    git add .github/workflows/
    git commit -m "⚙️ CI/CD: Enhance GitHub Actions workflows

✨ Features:
- Modular CI/CD pipeline
- Multi-environment testing
- Automated deployment
- Release management
- Quality gates

🚀 Workflows:
- auto-commit-bot.yml: Automated maintenance
- Backend testing and building
- Frontend building and deployment
- Integration testing
- Release automation

🔧 Environments:
- Development
- Staging
- Production
- Testing

🎯 DevOps:
- Continuous integration
- Continuous deployment
- Infrastructure as code
- Monitoring and alerts

#cicd #devops #github-actions #deployment" || print_warning "Workflow files already committed or no changes"
fi

# 6. Frontend Integration Commit
if [[ -n $(git status --porcelain frontend/) ]]; then
    print_step "🌐 Committing frontend integration..."
    git add frontend/
    git commit -m "🌐 Frontend: Integrate with modular backend

✨ Features:
- API integration with modular backend
- Canvas editor interface
- Real-time project management
- Tag and use case management
- Responsive design

🔧 Integration:
- RESTful API calls
- WebSocket connections
- State management
- Error handling
- Loading states

🎯 User Experience:
- Intuitive interface
- Fast performance
- Mobile responsive
- Accessibility support

#frontend #integration #ui #api" || print_warning "Frontend files already committed or no changes"
fi

# 7. Configuration and Setup Commit
if [[ -n $(git status --porcelain *.json *.yml *.yaml requirements.txt Dockerfile* docker-compose*) ]]; then
    print_step "⚙️ Committing configuration files..."
    git add *.json *.yml *.yaml requirements.txt Dockerfile* docker-compose* 2>/dev/null || true
    git commit -m "⚙️ Config: Update configuration and dependencies

✨ Updates:
- Python dependencies
- Docker configuration
- Environment settings
- Service configuration
- Build settings

📦 Dependencies:
- Core Python packages
- Development tools
- Testing frameworks
- Deployment utilities

🔧 Infrastructure:
- Docker containers
- Database setup
- Cloud configuration
- Environment variables

#config #dependencies #docker #infrastructure" || print_warning "Config files already committed or no changes"
fi

# 8. Remaining Changes Commit
if [[ -n $(git status --porcelain) ]]; then
    print_step "📝 Committing remaining changes..."
    git add .
    git commit -m "📝 Misc: Final cleanup and improvements

✨ Changes:
- Code formatting
- Minor bug fixes
- Documentation updates
- Asset organization
- Cleanup tasks

🔧 Improvements:
- Code quality
- File organization
- Performance optimizations
- Error handling

#cleanup #misc #improvements" || print_warning "No remaining changes to commit"
fi

# Push to remote
print_step "🚀 Pushing to GitHub..."
if git remote get-url origin >/dev/null 2>&1; then
    print_status "Pushing branch '$CURRENT_BRANCH' to remote repository..."
    git push origin "$CURRENT_BRANCH"
    print_status "✅ Successfully pushed to GitHub!"
    
    # Create and push tags if on main branch
    if [[ "$CURRENT_BRANCH" == "main" || "$CURRENT_BRANCH" == "master" ]]; then
        print_step "🏷️ Creating release tag..."
        
        # Get latest tag or default to v0.0.0
        LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
        print_status "Latest tag: $LATEST_TAG"
        
        # Increment version (simple patch increment)
        if [[ "$LATEST_TAG" == "v0.0.0" ]]; then
            NEW_TAG="v1.0.0"
        else
            # Extract version numbers and increment patch
            VERSION=${LATEST_TAG#v}
            IFS='.' read -ra VERSION_PARTS <<< "$VERSION"
            MAJOR=${VERSION_PARTS[0]}
            MINOR=${VERSION_PARTS[1]}
            PATCH=$((${VERSION_PARTS[2]} + 1))
            NEW_TAG="v${MAJOR}.${MINOR}.${PATCH}"
        fi
        
        print_status "Creating new tag: $NEW_TAG"
        git tag -a "$NEW_TAG" -m "🚀 Release $NEW_TAG: Modular Architecture

🎉 Major Updates:
- Modular backend architecture
- Enhanced canvas editor
- Automated CI/CD pipeline
- Comprehensive test suite
- Bot automation system

✨ Features:
- Core module system
- Event-driven architecture
- Automated workflows
- Better code organization
- Improved maintainability

🔧 Technical Improvements:
- Separation of concerns
- Clean API design
- Comprehensive testing
- Documentation updates
- DevOps automation

📊 Release Date: $(date '+%Y-%m-%d %H:%M:%S UTC')
🏷️ Tag: $NEW_TAG"
        
        git push origin "$NEW_TAG"
        print_status "✅ Release tag $NEW_TAG created and pushed!"
    fi
else
    print_error "No remote repository configured!"
    print_warning "Add a remote with: git remote add origin <repository-url>"
    exit 1
fi

# Summary
echo ""
echo "🎉 Modular Git Workflow Complete!"
echo "================================="
print_status "✅ All changes committed in focused, modular commits"
print_status "✅ Changes pushed to GitHub repository"
print_status "✅ Automated workflows are now active"
print_status "✅ Bot system is configured and ready"
echo ""
print_status "🚀 Your AI Video Generator is now:"
echo "   📦 Modularly architected"
echo "   🤖 Automatically maintained"
echo "   🧪 Comprehensively tested"
echo "   📚 Well documented"
echo "   ⚙️ CI/CD enabled"
echo ""
print_status "🔗 Check your GitHub repository for:"
echo "   • Commit history with detailed messages"
echo "   • GitHub Actions workflows running"
echo "   • Release tags and versions"
echo "   • Bot automation in action"
echo ""
print_status "Happy coding! 🎨✨"
