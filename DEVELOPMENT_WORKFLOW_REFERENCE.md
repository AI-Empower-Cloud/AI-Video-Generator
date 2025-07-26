# 🚀 Development Workflow Reference

## Git Workflow Management

### Automated Workflow Script
Use the `git_workflow_manager.sh` script for standardized development workflow:

```bash
# Initialize or check workflow status
./git_workflow_manager.sh status

# Create modular commits for different components
./git_workflow_manager.sh commit-modular

# Build and push Docker containers
./git_workflow_manager.sh build-containers

# Deploy to production
./git_workflow_manager.sh deploy

# Create and push new release
./git_workflow_manager.sh release
```

### Manual Git Operations

#### Creating Feature Branches
```bash
# Create and switch to feature branch
git checkout -b feature/new-canvas-tool

# Make your changes...

# Commit with conventional format
git commit -m "feat(canvas): add new drawing tool with pressure sensitivity"

# Push feature branch
git push origin feature/new-canvas-tool
```

#### Modular Commit Strategy
Organize commits by component for better tracking:

```bash
# Core module changes
git add core/
git commit -m "feat(core): enhance element validation system"

# Frontend changes
git add frontend/
git commit -m "feat(ui): add timeline scrubbing functionality"

# Documentation updates
git add *.md
git commit -m "docs: update API reference with new methods"

# CI/CD updates
git add .github/
git commit -m "ci: add automated security scanning"
```

## CI/CD Pipeline Reference

### GitHub Actions Workflow (`.github/workflows/modular-ci-cd.yml`)

#### Triggers
- **Push to main**: Full build, test, and deploy
- **Pull Request**: Build and test only
- **Tag creation**: Release build and deployment
- **Manual dispatch**: Custom deployment options

#### Pipeline Stages

##### 1. Code Quality Check
```yaml
- name: Run linting
  run: |
    flake8 core/ modules/ *.py
    eslint frontend/src/
    
- name: Type checking
  run: |
    mypy core/ modules/
    
- name: Security scan
  run: |
    bandit -r core/ modules/
```

##### 2. Testing
```yaml
- name: Python tests
  run: |
    python -m pytest test_*.py -v --cov=core --cov=modules
    
- name: Frontend tests
  run: |
    cd frontend && npm test -- --coverage
```

##### 3. Build Process
```yaml
- name: Build Docker images
  run: |
    docker build -t ai-video-generator:latest .
    docker build -f Dockerfile.dev -t ai-video-generator:dev .
```

##### 4. Deployment
```yaml
- name: Deploy to Wasabi
  env:
    WASABI_ACCESS_KEY_ID: ${{ secrets.WASABI_ACCESS_KEY_ID }}
    WASABI_SECRET_ACCESS_KEY: ${{ secrets.WASABI_SECRET_ACCESS_KEY }}
  run: |
    ./deploy_to_wasabi.py
```

#### Environment Variables and Secrets

**Required GitHub Secrets:**
- `WASABI_ACCESS_KEY_ID`: Wasabi S3 access key
- `WASABI_SECRET_ACCESS_KEY`: Wasabi S3 secret key
- `DOCKER_HUB_USERNAME`: Docker Hub username (optional)
- `DOCKER_HUB_TOKEN`: Docker Hub access token (optional)

**Environment Variables:**
```bash
# Local development (.env)
WASABI_ENDPOINT_URL=https://s3.wasabisys.com
WASABI_REGION=us-east-1
WASABI_BUCKET_NAME=ai-video-generator

# Production environment
NODE_ENV=production
PYTHONPATH=/app
LOG_LEVEL=info
```

## Docker Development

### Development Container
```bash
# Build development image
docker build -f Dockerfile.dev -t ai-video-generator:dev .

# Run development container with hot reload
docker-compose -f docker-compose.dev.yml up

# Access development container shell
docker exec -it ai-video-generator-dev bash
```

### Production Container
```bash
# Build production image
docker build -t ai-video-generator:latest .

# Run production container
docker-compose up -d

# View logs
docker-compose logs -f
```

### Multi-stage Build Process
The Dockerfile uses multi-stage builds for optimization:

1. **Base Stage**: Common dependencies
2. **Development Stage**: Dev tools and hot reload
3. **Build Stage**: Asset compilation
4. **Production Stage**: Minimal runtime image

## Testing Strategy

### Python Testing
```bash
# Run all tests
python -m pytest test_*.py -v

# Run with coverage
python -m pytest test_*.py --cov=core --cov=modules --cov-report=html

# Run specific test categories
python -m pytest test_core_modules.py -v  # Core functionality
python -m pytest test_wasabi_node_modules.py -v  # Wasabi integration
```

### Frontend Testing
```bash
cd frontend/

# Run unit tests
npm test

# Run with coverage
npm test -- --coverage

# Run integration tests
npm run test:integration

# Run e2e tests
npm run test:e2e
```

### Integration Testing
```bash
# Test complete workflow
python integration_test.py

# Test canvas editor functionality
python test_canvas_integration.py

# Test export pipeline
python test_export_pipeline.py
```

## Release Management

### Versioning Strategy
Follow Semantic Versioning (SemVer):
- **Major**: Breaking changes (v2.0.0 → v3.0.0)
- **Minor**: New features (v2.0.0 → v2.1.0)
- **Patch**: Bug fixes (v2.0.0 → v2.0.1)

### Release Process
```bash
# 1. Prepare release
./git_workflow_manager.sh prepare-release 2.1.0

# 2. Update CHANGELOG.md
# 3. Test thoroughly

# 4. Create and push release
./git_workflow_manager.sh release 2.1.0

# 5. Deploy to production
./git_workflow_manager.sh deploy-production
```

### Changelog Management
Follow Keep a Changelog format in `CHANGELOG.md`:

```markdown
## [2.1.0] - 2025-01-15

### Added
- New animation timeline editor
- Batch export functionality
- WebM export support

### Changed
- Improved memory usage for large projects
- Updated UI component library

### Fixed
- Fixed audio sync issues in exports
- Resolved canvas scaling problems

### Security
- Updated dependencies with security patches
```

## Deployment Strategies

### Development Deployment
```bash
# Deploy to development environment
./deploy-containers.sh dev

# Update frontend only
./deploy_frontend_to_wasabi.py --env=dev

# Quick development deploy
docker-compose -f docker-compose.dev.yml up --build -d
```

### Staging Deployment
```bash
# Deploy to staging
./deploy-containers.sh staging

# Run staging tests
npm run test:staging

# Validate deployment
curl https://staging.ai-video-generator.com/health
```

### Production Deployment
```bash
# Deploy to production (requires approval)
./deploy-containers.sh production

# Blue-green deployment
./deploy-containers.sh production --strategy=blue-green

# Rollback if needed
./deploy-containers.sh rollback
```

## Monitoring and Maintenance

### Health Checks
```bash
# Application health
curl http://localhost:8000/health

# Container health
docker-compose ps

# Resource usage
docker stats ai-video-generator
```

### Log Management
```bash
# View application logs
docker-compose logs -f app

# View specific service logs
docker-compose logs -f frontend

# Export logs for analysis
docker-compose logs --no-color > deployment.log
```

### Backup and Recovery
```bash
# Backup projects to Wasabi
./wasabi_node_modules.sh backup

# Restore from backup
./wasabi_node_modules.sh restore

# Database backup (future)
pg_dump ai_video_generator > backup.sql
```

## Performance Optimization

### Development Optimization
```bash
# Profile Python code
python -m cProfile -o profile.stats modular_canvas_editor.py

# Analyze memory usage
mprof run modular_canvas_editor.py
mprof plot

# Frontend bundle analysis
cd frontend && npm run analyze
```

### Production Optimization
```bash
# Optimize Docker images
docker system prune -a

# Update production dependencies
pip-audit --fix

# Monitor resource usage
htop
iotop
```

## Troubleshooting Commands

### Common Issues
```bash
# Clear Docker cache
docker system prune -a

# Restart services
docker-compose restart

# Reset development environment
docker-compose down -v && docker-compose up --build

# Check Wasabi connectivity
python test_wasabi_connection.py

# Validate project structure
python comprehensive_status_check.py
```

### Debug Mode
```bash
# Run in debug mode
DEBUG=true python modular_canvas_editor.py

# Enable verbose logging
LOG_LEVEL=debug docker-compose up

# Run tests in debug mode
python -m pytest test_*.py -v -s --pdb
```

## Code Quality Standards

### Python Standards
```python
# Follow PEP 8 style guide
# Use type hints for all functions
def create_element(name: str, x: float, y: float) -> CanvasElement:
    """Create a new canvas element with specified position."""
    pass

# Use dataclasses for data structures
@dataclass
class VideoSettings:
    width: int
    height: int
    fps: int = 30
```

### TypeScript Standards
```typescript
// Use strict TypeScript configuration
// Define interfaces for all data structures
interface CanvasElement {
  id: string;
  type: 'text' | 'image' | 'video';
  position: { x: number; y: number };
}

// Use proper error handling
try {
  await exportVideo(project);
} catch (error) {
  logger.error('Export failed:', error);
  throw new ExportError('Failed to export video');
}
```

### Documentation Standards
- All public functions must have docstrings
- API changes require documentation updates
- README files for each major component
- Inline comments for complex logic

---

*This reference guide covers the complete development workflow for the AI Video Generator project. Keep it updated as processes evolve.*

**Last Updated**: July 2025  
**Version**: 2.0.0
