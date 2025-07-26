#!/bin/bash
# GitHub Environment Setup Script for AI Video Generator
# This script helps set up your local development environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Print colored output
print_header() {
    echo -e "${PURPLE}================================${NC}"
    echo -e "${PURPLE}$1${NC}"
    echo -e "${PURPLE}================================${NC}"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
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

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Main setup function
main() {
    print_header "🚀 GitHub Environment Setup"
    echo "Setting up AI Video Generator for development"
    echo ""
    
    # Step 1: Check prerequisites
    print_step "1️⃣ Checking prerequisites..."
    
    if ! command_exists git; then
        print_error "Git is not installed!"
        exit 1
    fi
    
    if ! command_exists python3; then
        print_error "Python 3 is not installed!"
        exit 1
    fi
    
    if ! command_exists node; then
        print_warning "Node.js not found - frontend features may not work"
    fi
    
    if ! command_exists docker; then
        print_warning "Docker not found - containerization features disabled"
    fi
    
    print_success "Prerequisites checked"
    
    # Step 2: Check Git configuration
    print_step "2️⃣ Checking Git configuration..."
    
    USER_NAME=$(git config user.name 2>/dev/null || echo "")
    USER_EMAIL=$(git config user.email 2>/dev/null || echo "")
    
    if [[ -z "$USER_NAME" || -z "$USER_EMAIL" ]]; then
        print_warning "Git user not configured"
        read -p "Enter your name: " name
        read -p "Enter your email: " email
        
        git config --global user.name "$name"
        git config --global user.email "$email"
        print_success "Git user configured"
    else
        print_info "Git user: $USER_NAME <$USER_EMAIL>"
    fi
    
    # Step 3: Check repository connection
    print_step "3️⃣ Checking repository connection..."
    
    if git remote get-url origin >/dev/null 2>&1; then
        REPO_URL=$(git remote get-url origin)
        print_info "Repository: $REPO_URL"
        
        if [[ "$REPO_URL" == *"AI-Empower-Cloud/AI-Video-Generator"* ]]; then
            print_success "Connected to correct repository"
        else
            print_warning "Repository URL seems different"
        fi
    else
        print_error "No Git repository found!"
        print_info "Run: git clone https://github.com/AI-Empower-Cloud/AI-Video-Generator.git"
        exit 1
    fi
    
    # Step 4: Set up environment files
    print_step "4️⃣ Setting up environment files..."
    
    # Create .env.wasabi template
    if [[ ! -f ".env.wasabi" ]]; then
        cat > .env.wasabi << EOF
# Wasabi Cloud Storage Configuration
WASABI_ACCESS_KEY=your-access-key-here
WASABI_SECRET_KEY=your-secret-key-here
WASABI_BUCKET=ai-video-generator-content
WASABI_REGION=us-east-1
WASABI_ENDPOINT=https://s3.wasabisys.com
EOF
        print_success "Created .env.wasabi template"
        print_warning "Please edit .env.wasabi with your actual Wasabi credentials"
    else
        print_info ".env.wasabi already exists"
    fi
    
    # Create frontend .env.local template
    if [[ -d "frontend" && ! -f "frontend/.env.local" ]]; then
        cat > frontend/.env.local << EOF
# Frontend Environment Configuration
NEXTAUTH_SECRET=$(openssl rand -base64 32 2>/dev/null || echo "your-nextauth-secret-here")
NEXTAUTH_URL=http://localhost:3000
NODE_ENV=development

# Optional: Database
# DATABASE_URL=postgresql://username:password@localhost:5432/database

# Optional: External APIs
# OPENAI_API_KEY=your-openai-key
# ELEVENLABS_API_KEY=your-elevenlabs-key
EOF
        print_success "Created frontend/.env.local"
    fi
    
    # Step 5: Check Python dependencies
    print_step "5️⃣ Checking Python dependencies..."
    
    if python3 -c "import boto3" 2>/dev/null; then
        print_success "boto3 available"
    else
        print_warning "boto3 not found"
        read -p "Install Python dependencies? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            pip3 install boto3 python-dotenv
            print_success "Python dependencies installed"
        fi
    fi
    
    # Step 6: Check Node.js dependencies
    if [[ -d "frontend" ]]; then
        print_step "6️⃣ Checking Node.js dependencies..."
        
        cd frontend
        if [[ -f "package.json" ]]; then
            if [[ -d "node_modules" ]]; then
                print_success "Node modules found"
            else
                print_warning "Node modules not found"
                read -p "Install Node.js dependencies? (y/N): " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    if command_exists npm; then
                        npm install
                        print_success "Node dependencies installed"
                    elif command_exists yarn; then
                        yarn install
                        print_success "Node dependencies installed"
                    else
                        print_error "Neither npm nor yarn found"
                    fi
                fi
            fi
        fi
        cd ..
    fi
    
    # Step 7: Make scripts executable
    print_step "7️⃣ Making scripts executable..."
    
    chmod +x *.sh 2>/dev/null || true
    chmod +x *.py 2>/dev/null || true
    print_success "Scripts made executable"
    
    # Step 8: Test Wasabi connection
    print_step "8️⃣ Testing Wasabi connection..."
    
    if [[ -f ".env.wasabi" ]]; then
        source .env.wasabi
        if [[ "$WASABI_ACCESS_KEY" != "your-access-key-here" && -n "$WASABI_ACCESS_KEY" ]]; then
            if python3 -c "
import boto3
import os
from dotenv import load_dotenv
load_dotenv('.env.wasabi')
try:
    s3 = boto3.client('s3', 
        endpoint_url=os.getenv('WASABI_ENDPOINT'),
        aws_access_key_id=os.getenv('WASABI_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('WASABI_SECRET_KEY')
    )
    s3.list_buckets()
    print('SUCCESS')
except Exception as e:
    print(f'ERROR: {e}')
" 2>/dev/null | grep -q "SUCCESS"; then
                print_success "Wasabi connection successful"
            else
                print_warning "Wasabi connection failed - check credentials"
            fi
        else
            print_warning "Wasabi not configured - edit .env.wasabi"
        fi
    fi
    
    # Step 9: Summary and next steps
    print_step "9️⃣ Setup Summary"
    
    echo ""
    print_header "✅ Setup Complete!"
    echo ""
    print_info "Next steps:"
    echo "1. 🔐 Set up GitHub Secrets (see GITHUB_SETUP_GUIDE.md)"
    echo "2. ✏️  Edit .env.wasabi with your Wasabi credentials"
    echo "3. 🧪 Test the setup:"
    echo "   ./wasabi_node_modules.sh status"
    echo "4. 🚀 Create your first commit:"
    echo "   ./git_workflow_manager.sh setup"
    echo ""
    
    print_info "GitHub Repository: https://github.com/AI-Empower-Cloud/AI-Video-Generator"
    print_info "Documentation: GITHUB_SETUP_GUIDE.md"
    print_info "Wasabi Guide: WASABI_NODE_MODULES_GUIDE.md"
    
    echo ""
    print_success "Happy coding! 🎉"
}

# Run setup if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
