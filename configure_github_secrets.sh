#!/bin/bash
# GitHub Secrets Configuration Helper
# Helps you set up repository secrets for CI/CD

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

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

# Repository information
REPO_OWNER="AI-Empower-Cloud"
REPO_NAME="AI-Video-Generator"
REPO_URL="https://github.com/$REPO_OWNER/$REPO_NAME"

main() {
    print_header "🔐 GitHub Secrets Setup"
    echo "This script will help you configure GitHub repository secrets"
    echo "Repository: $REPO_URL"
    echo ""
    
    # Check if GitHub CLI is available
    if command -v gh >/dev/null 2>&1; then
        print_success "GitHub CLI found"
        
        # Check if authenticated
        if gh auth status >/dev/null 2>&1; then
            print_success "GitHub CLI authenticated"
            setup_secrets_with_cli
        else
            print_warning "GitHub CLI not authenticated"
            print_info "Run: gh auth login"
            setup_secrets_manual
        fi
    else
        print_warning "GitHub CLI not found"
        print_info "Install with: brew install gh (macOS) or apt install gh (Ubuntu)"
        setup_secrets_manual
    fi
}

setup_secrets_with_cli() {
    print_step "🤖 Setting up secrets with GitHub CLI..."
    
    echo ""
    print_info "We'll set up the following secrets:"
    echo "- WASABI_ACCESS_KEY"
    echo "- WASABI_SECRET_KEY" 
    echo "- WASABI_BUCKET"
    echo "- WASABI_REGION"
    echo "- WASABI_ENDPOINT"
    echo ""
    
    read -p "Continue with automated setup? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Load existing values from .env.wasabi if available
        if [[ -f ".env.wasabi" ]]; then
            source .env.wasabi
            print_info "Loading values from .env.wasabi"
        fi
        
        # Prompt for values
        read -p "Wasabi Access Key [$WASABI_ACCESS_KEY]: " access_key
        access_key=${access_key:-$WASABI_ACCESS_KEY}
        
        read -s -p "Wasabi Secret Key [$WASABI_SECRET_KEY]: " secret_key
        secret_key=${secret_key:-$WASABI_SECRET_KEY}
        echo ""
        
        read -p "Wasabi Bucket [$WASABI_BUCKET]: " bucket
        bucket=${bucket:-$WASABI_BUCKET}
        
        read -p "Wasabi Region [$WASABI_REGION]: " region
        region=${region:-$WASABI_REGION}
        
        read -p "Wasabi Endpoint [$WASABI_ENDPOINT]: " endpoint
        endpoint=${endpoint:-$WASABI_ENDPOINT}
        
        # Set secrets
        if [[ -n "$access_key" ]]; then
            echo "$access_key" | gh secret set WASABI_ACCESS_KEY --repo "$REPO_OWNER/$REPO_NAME"
            print_success "Set WASABI_ACCESS_KEY"
        fi
        
        if [[ -n "$secret_key" ]]; then
            echo "$secret_key" | gh secret set WASABI_SECRET_KEY --repo "$REPO_OWNER/$REPO_NAME"
            print_success "Set WASABI_SECRET_KEY"
        fi
        
        if [[ -n "$bucket" ]]; then
            echo "$bucket" | gh secret set WASABI_BUCKET --repo "$REPO_OWNER/$REPO_NAME"
            print_success "Set WASABI_BUCKET"
        fi
        
        if [[ -n "$region" ]]; then
            echo "$region" | gh secret set WASABI_REGION --repo "$REPO_OWNER/$REPO_NAME"
            print_success "Set WASABI_REGION"
        fi
        
        if [[ -n "$endpoint" ]]; then
            echo "$endpoint" | gh secret set WASABI_ENDPOINT --repo "$REPO_OWNER/$REPO_NAME"
            print_success "Set WASABI_ENDPOINT"
        fi
        
        # Generate and set NEXTAUTH_SECRET
        nextauth_secret=$(openssl rand -base64 32 2>/dev/null || echo "$(date | md5sum | head -c 32)")
        echo "$nextauth_secret" | gh secret set NEXTAUTH_SECRET --repo "$REPO_OWNER/$REPO_NAME"
        print_success "Set NEXTAUTH_SECRET"
        
        print_success "All secrets configured!"
        
        # Test the setup
        print_step "🧪 Testing GitHub Actions..."
        echo "You can test your setup by:"
        echo "1. Making a small change and pushing to GitHub"
        echo "2. Checking the Actions tab: $REPO_URL/actions"
        
    else
        setup_secrets_manual
    fi
}

setup_secrets_manual() {
    print_step "📝 Manual secrets setup..."
    
    echo ""
    print_info "To set up GitHub secrets manually:"
    echo ""
    echo "1. Go to: $REPO_URL/settings/secrets/actions"
    echo "2. Click 'New repository secret'"
    echo "3. Add each of these secrets:"
    echo ""
    
    # Show current values from .env.wasabi if available
    if [[ -f ".env.wasabi" ]]; then
        source .env.wasabi
        echo "📋 Current values from .env.wasabi:"
        echo ""
        echo "Secret Name: WASABI_ACCESS_KEY"
        echo "Value: $WASABI_ACCESS_KEY"
        echo ""
        echo "Secret Name: WASABI_SECRET_KEY"
        echo "Value: $WASABI_SECRET_KEY"
        echo ""
        echo "Secret Name: WASABI_BUCKET"
        echo "Value: $WASABI_BUCKET"
        echo ""
        echo "Secret Name: WASABI_REGION"
        echo "Value: $WASABI_REGION"
        echo ""
        echo "Secret Name: WASABI_ENDPOINT"
        echo "Value: $WASABI_ENDPOINT"
        echo ""
    else
        echo "Required secrets:"
        echo ""
        echo "Secret Name: WASABI_ACCESS_KEY"
        echo "Value: your-wasabi-access-key"
        echo ""
        echo "Secret Name: WASABI_SECRET_KEY"
        echo "Value: your-wasabi-secret-key"
        echo ""
        echo "Secret Name: WASABI_BUCKET"
        echo "Value: ai-video-generator-content"
        echo ""
        echo "Secret Name: WASABI_REGION"
        echo "Value: us-east-1"
        echo ""
        echo "Secret Name: WASABI_ENDPOINT"
        echo "Value: https://s3.wasabisys.com"
        echo ""
    fi
    
    # Generate NEXTAUTH_SECRET
    nextauth_secret=$(openssl rand -base64 32 2>/dev/null || echo "$(date | md5sum | head -c 32)")
    echo "Secret Name: NEXTAUTH_SECRET"
    echo "Value: $nextauth_secret"
    echo ""
    
    print_info "Optional secrets (for advanced features):"
    echo ""
    echo "Secret Name: DOCKER_USERNAME"
    echo "Value: your-docker-hub-username"
    echo ""
    echo "Secret Name: DOCKER_PASSWORD"
    echo "Value: your-docker-hub-password"
    echo ""
    echo "Secret Name: OPENAI_API_KEY"
    echo "Value: your-openai-api-key"
    echo ""
    
    print_warning "⚠️  Never commit these values to your repository!"
    print_info "✅ After adding secrets, your CI/CD workflows will have access to them"
}

show_status() {
    print_step "📊 Current Setup Status"
    
    echo ""
    print_info "Repository: $REPO_URL"
    
    if [[ -f ".env.wasabi" ]]; then
        source .env.wasabi
        if [[ "$WASABI_ACCESS_KEY" != "your-access-key-here" && -n "$WASABI_ACCESS_KEY" ]]; then
            print_success "✅ Wasabi configured locally"
        else
            print_warning "⚠️ Wasabi not configured locally"
        fi
    else
        print_warning "⚠️ .env.wasabi not found"
    fi
    
    if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
        print_success "✅ GitHub CLI authenticated"
        
        # Try to list secrets (requires admin access)
        if gh secret list --repo "$REPO_OWNER/$REPO_NAME" >/dev/null 2>&1; then
            echo ""
            print_info "Repository secrets:"
            gh secret list --repo "$REPO_OWNER/$REPO_NAME" | head -10
        fi
    else
        print_warning "⚠️ GitHub CLI not available/authenticated"
    fi
    
    echo ""
    print_info "Next steps:"
    echo "- Configure secrets (if not done)"
    echo "- Test with: git push origin main"
    echo "- Check Actions: $REPO_URL/actions"
}

# Parse command line arguments
case "${1:-setup}" in
    "setup")
        main
        ;;
    "status")
        show_status
        ;;
    "help"|"--help"|"-h")
        echo "Usage: $0 [setup|status|help]"
        echo ""
        echo "Commands:"
        echo "  setup   - Set up GitHub repository secrets"
        echo "  status  - Show current setup status"
        echo "  help    - Show this help message"
        ;;
    *)
        print_error "Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac
