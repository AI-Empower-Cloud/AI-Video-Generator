# GitHub Repository Setup Guide for AI Video Generator

This guide will help you set up your GitHub repository with proper environment variables, secrets, and CI/CD workflows.

## 📋 Repository Information
- **Repository**: https://github.com/AI-Empower-Cloud/AI-Video-Generator
- **Account**: AI-Empower-Cloud
- **Email**: admin@empowerhub360.org

## 🔐 GitHub Secrets Setup

### Required Secrets for CI/CD

Go to your GitHub repository: **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these secrets:

#### Wasabi Cloud Storage
- `WASABI_ACCESS_KEY` - Your Wasabi access key
- `WASABI_SECRET_KEY` - Your Wasabi secret key  
- `WASABI_BUCKET` - Your bucket name (e.g., `ai-video-generator-content`)
- `WASABI_REGION` - Region (e.g., `us-east-1`)
- `WASABI_ENDPOINT` - Endpoint URL (e.g., `https://s3.wasabisys.com`)

#### Docker Hub (Optional)
- `DOCKER_USERNAME` - Your Docker Hub username
- `DOCKER_PASSWORD` - Your Docker Hub password/token

#### Other Environment Variables
- `NODE_ENV` - Set to `production` for production builds
- `NEXTAUTH_SECRET` - Random string for NextAuth.js (generate with `openssl rand -base64 32`)
- `NEXTAUTH_URL` - Your production URL (e.g., `https://your-domain.com`)

## 🚀 Quick Setup Commands

```bash
# Clone repository (if needed)
git clone https://github.com/AI-Empower-Cloud/AI-Video-Generator.git
cd AI-Video-Generator

# Set up local environment
./setup_github_environment.sh

# Configure Wasabi credentials
./configure_wasabi_keys.sh

# Initialize frontend project for node_modules caching
./wasabi_node_modules.sh init ./frontend

# Run the complete setup workflow
./git_workflow_manager.sh setup
```

## 📁 Local Environment Files

### 1. Create `.env.wasabi` (for local development)
```bash
WASABI_ACCESS_KEY=your-access-key-here
WASABI_SECRET_KEY=your-secret-key-here
WASABI_BUCKET=ai-video-generator-content
WASABI_REGION=us-east-1
WASABI_ENDPOINT=https://s3.wasabisys.com
```

### 2. Create `.env.local` (for frontend)
```bash
NEXTAUTH_SECRET=your-nextauth-secret-here
NEXTAUTH_URL=http://localhost:3000
NODE_ENV=development
```

## 🔄 GitHub Actions Workflows

Your repository includes these automated workflows:

### 1. **Modular CI/CD** (`.github/workflows/modular-ci-cd.yml`)
- Tests core modules
- Tests Wasabi node_modules functionality
- Builds frontend and backend
- Runs Docker builds
- Creates releases

### 2. **Triggers**
- **Push** to `main`, `develop`, `feature/*` branches
- **Pull requests** to `main`
- **Tags** starting with `v*`

## 📦 Node Modules Management with Wasabi

### Commands
```bash
# Upload node_modules to Wasabi
./wasabi_node_modules.sh upload ./frontend

# Download node_modules from Wasabi
./wasabi_node_modules.sh download ./frontend

# Smart sync (auto upload/download)
./wasabi_node_modules.sh sync ./frontend

# Process all Node.js projects
./wasabi_node_modules.sh sync --all

# List cached modules
./wasabi_node_modules.sh list

# Check status
./wasabi_node_modules.sh status --all
```

### NPM Scripts (after init)
```bash
npm run wasabi:upload
npm run wasabi:download
npm run wasabi:sync
```

## 🐳 Docker & Containerization

### Build and Deploy
```bash
# Build containers
./docker-build.sh

# Deploy containers
./deploy-containers.sh

# Full workflow with containers
./git_workflow_manager.sh release v1.0.0 production
```

## 🏷️ Release Management

### Create a Release
```bash
# Create and push a new release
./git_workflow_manager.sh release v2.1.0

# Create release with deployment
./git_workflow_manager.sh release v2.1.0 production
```

### Version Tagging
- Use semantic versioning: `v1.0.0`, `v1.1.0`, etc.
- Tags trigger automated builds and deployments
- GitHub Actions automatically creates releases

## 🔧 Development Workflow

### 1. **Feature Development**
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "✨ Add new feature"

# Push to GitHub
git push origin feature/new-feature

# Create Pull Request on GitHub
```

### 2. **Modular Commits**
```bash
# Use the modular commit system
./git_workflow_manager.sh commit "feature-name" "Description" file1.py file2.py

# Or use regular git
git add specific-files
git commit -m "🧩 Add feature-name module"
```

### 3. **Sync Dependencies**
```bash
# Before working on frontend
./wasabi_node_modules.sh download ./frontend

# After adding dependencies
npm install
./wasabi_node_modules.sh upload ./frontend
```

## 📊 Monitoring & Analytics

### Check Repository Status
```bash
# Check all projects
./wasabi_node_modules.sh status --all

# Check git status
git status

# Check CI/CD workflows
# Go to: https://github.com/AI-Empower-Cloud/AI-Video-Generator/actions
```

### View Logs
- **GitHub Actions**: Repository → Actions tab
- **Wasabi Storage**: Use AWS CLI or Wasabi console
- **Docker Containers**: `docker logs container-name`

## 🔒 Security Best Practices

### 1. **Never Commit Secrets**
- All `.env*` files are in `.gitignore`
- Use GitHub Secrets for CI/CD
- Use environment variables in production

### 2. **Repository Access**
- Set up branch protection rules
- Require PR reviews for main branch
- Enable automated security updates

### 3. **Dependency Management**
- Regular dependency updates
- Security scanning with GitHub Dependabot
- Node modules cached in Wasabi (not in Git)

## 🆘 Troubleshooting

### Common Issues

1. **"Wasabi not configured"**
   ```bash
   ./configure_wasabi_keys.sh
   ```

2. **"Permission denied"**
   ```bash
   chmod +x *.sh
   ```

3. **"GitHub push failed"**
   ```bash
   git remote -v
   git config --list | grep user
   ```

4. **"CI/CD workflow failed"**
   - Check GitHub Secrets are properly set
   - Verify workflow file syntax
   - Check Actions tab for detailed logs

## 📞 Support

- **Repository Issues**: https://github.com/AI-Empower-Cloud/AI-Video-Generator/issues
- **Wasabi Support**: https://wasabi.com/support/
- **GitHub Support**: https://support.github.com/

## 🎯 Next Steps

1. ✅ **Set up GitHub Secrets** (see above)
2. ✅ **Configure local environment files**
3. ✅ **Test Wasabi integration**
4. ✅ **Run first deployment**
5. ✅ **Set up branch protection rules**
6. ✅ **Invite team members** (if applicable)

---

**Happy coding! 🚀**
