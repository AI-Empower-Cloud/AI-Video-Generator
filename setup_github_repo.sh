#!/bin/bash
# GitHub Repository Setup Script for AI-Empower-Cloud/AI-Video-Generator

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  AI Video Generator GitHub Setup${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

check_git_config() {
    echo "🔍 Checking Git configuration..."
    
    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not in a Git repository!"
        exit 1
    fi
    
    # Check remote URL
    remote_url=$(git remote get-url origin 2>/dev/null || echo "")
    if [[ "$remote_url" == *"AI-Empower-Cloud/AI-Video-Generator"* ]]; then
        print_success "Connected to AI-Empower-Cloud/AI-Video-Generator"
    else
        print_warning "Remote URL: $remote_url"
        print_warning "Expected: https://github.com/AI-Empower-Cloud/AI-Video-Generator"
    fi
    
    # Check user configuration
    user_name=$(git config user.name 2>/dev/null || echo "Not set")
    user_email=$(git config user.email 2>/dev/null || echo "Not set")
    
    echo "📧 Git User: $user_name <$user_email>"
    
    if [[ "$user_name" == "Not set" ]] || [[ "$user_email" == "Not set" ]]; then
        print_warning "Git user not configured!"
        configure_git_user
    fi
}

configure_git_user() {
    echo ""
    echo "🔧 Let's configure your Git user information:"
    
    read -p "Enter your name: " git_name
    read -p "Enter your email: " git_email
    
    git config user.name "$git_name"
    git config user.email "$git_email"
    
    print_success "Git user configured: $git_name <$git_email>"
}

check_wasabi_config() {
    echo ""
    echo "🔍 Checking Wasabi configuration..."
    
    if [[ -f ".env.wasabi" ]]; then
        print_success "Local .env.wasabi file found"
        
        # Check if all required vars are present
        if grep -q "WASABI_ACCESS_KEY" .env.wasabi && \
           grep -q "WASABI_SECRET_KEY" .env.wasabi; then
            print_success "Wasabi credentials configured"
        else
            print_warning "Wasabi credentials incomplete"
            setup_wasabi_local
        fi
    else
        print_warning "Local .env.wasabi file not found"
        setup_wasabi_local
    fi
}

setup_wasabi_local() {
    echo ""
    read -p "🤔 Do you want to set up Wasabi credentials now? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ./configure_wasabi_keys.sh
    else
        print_info "You can set up Wasabi later with: ./configure_wasabi_keys.sh"
    fi
}

show_github_secrets_instructions() {
    echo ""
    echo "🔐 GitHub Secrets Setup Required"
    echo "================================="
    echo ""
    print_info "To enable CI/CD and Wasabi integration, add these secrets to GitHub:"
    echo ""
    echo "1. Go to: https://github.com/AI-Empower-Cloud/AI-Video-Generator/settings/secrets/actions"
    echo "2. Click 'New repository secret' for each:"
    echo ""
    
    if [[ -f ".env.wasabi" ]]; then
        echo "   📋 Copy these values from your .env.wasabi file:"
        echo ""
        while IFS= read -r line; do
            if [[ $line == WASABI_* ]] && [[ $line == *"="* ]]; then
                key=$(echo "$line" | cut -d'=' -f1)
                echo "   🔑 Secret Name: $key"
            fi
        done < .env.wasabi
    else
        echo "   🔑 WASABI_ACCESS_KEY"
        echo "   🔑 WASABI_SECRET_KEY"
        echo "   🔑 WASABI_BUCKET"
        echo "   🔑 WASABI_REGION"
        echo "   🔑 WASABI_ENDPOINT"
    fi
    
    echo ""
    echo "3. Optional secrets for enhanced features:"
    echo "   🔑 DOCKER_USERNAME (for container registry)"
    echo "   🔑 DOCKER_PASSWORD (for container registry)"
    echo "   🔑 OPENAI_API_KEY (for AI features)"
    echo ""
    print_info "See GITHUB_SECRETS_SETUP.md for detailed instructions"
}

test_github_connection() {
    echo ""
    echo "🧪 Testing GitHub connection..."
    
    # Test if we can fetch from remote
    if git fetch origin --dry-run > /dev/null 2>&1; then
        print_success "GitHub connection working"
    else
        print_warning "GitHub connection issues - you may need to authenticate"
        echo ""
        print_info "Try: gh auth login"
        print_info "Or set up SSH keys: https://docs.github.com/en/authentication/connecting-to-github-with-ssh"
    fi
}

show_next_steps() {
    echo ""
    echo "🚀 Next Steps"
    echo "============="
    echo ""
    echo "1. 🔐 Set up GitHub Secrets (see instructions above)"
    echo "2. 🧪 Test your setup:"
    echo "   ./wasabi_node_modules.sh status"
    echo "   ./git_workflow_manager.sh setup"
    echo ""
    echo "3. 📦 Initialize frontend for Wasabi:"
    echo "   ./wasabi_node_modules.sh init ./frontend"
    echo ""
    echo "4. 🔄 Test the complete workflow:"
    echo "   git add ."
    echo "   git commit -m 'feat: setup GitHub integration'"
    echo "   git push origin main"
    echo ""
    echo "5. 🎯 Check GitHub Actions:"
    echo "   https://github.com/AI-Empower-Cloud/AI-Video-Generator/actions"
    echo ""
    print_success "Your repository is ready for collaborative development!"
}

main() {
    print_header
    
    check_git_config
    check_wasabi_config
    test_github_connection
    show_github_secrets_instructions
    show_next_steps
    
    echo ""
    print_success "GitHub setup complete! 🎉"
}

# Run main function
main
