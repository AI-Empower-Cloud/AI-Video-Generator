# Deployment Guide

This guide covers deploying the AI Video Generator in different environments.

## Environment Setup

The project supports multiple environments with different configurations:

### Development Environment
- **File**: `.env.example` → copy to `.env`
- **Features**: Debug mode, reduced limits, local storage
- **Setup**: `bash scripts/setup_dev.sh`

### Testing Environment  
- **File**: `.env.testing`
- **Features**: Minimal resources, fast execution, cleanup
- **Setup**: `bash scripts/run_tests.sh`

### Production Environment
- **File**: `.env.production`
- **Features**: High performance, security, monitoring
- **Setup**: `bash scripts/deploy_prod.sh`

## Quick Start

### Local Development
```bash
# 1. Clone repository
git clone <your-repo-url>
cd AI-Video-Generator

# 2. Set up development environment
bash scripts/setup_dev.sh

# 3. Activate environment
source venv/bin/activate

# 4. Configure settings
cp .env.example .env
# Edit .env with your settings

# 5. Run application
streamlit run streamlit_app.py
```

### Docker Deployment
```bash
# Single container
docker build -t ai-video-generator .
docker run -p 8503:8503 ai-video-generator

# With Docker Compose (recommended)
docker-compose up -d
```

## Environment Variables

### Core Settings
- `APP_ENV`: Environment name (development/testing/production)
- `DEBUG`: Enable debug mode (true/false)
- `HOST`: Server host (0.0.0.0 for Docker, localhost for dev)
- `PORT`: Server port (default: 8503)

### Video Generation
- `MAX_VIDEO_DURATION`: Maximum video length in seconds
- `MAX_VIDEO_RESOLUTION`: Maximum resolution (e.g., "1920x1080")
- `DEFAULT_FPS`: Default frames per second

### Audio & Animation
- `ENABLE_AUDIO`: Enable audio generation (true/false)
- `ENABLE_BACKGROUND_MUSIC`: Enable background music (true/false)
- `ENABLE_ADVANCED_ANIMATION`: Enable advanced animations (true/false)

### Storage
- `OUTPUT_DIRECTORY`: Where to save generated videos
- `TEMP_DIRECTORY`: Temporary files directory
- `CLEANUP_TEMP_FILES`: Auto-cleanup temporary files (true/false)

### Security
- `ENABLE_RATE_LIMITING`: Enable API rate limiting (true/false)
- `REQUESTS_PER_MINUTE`: Max requests per minute per IP

## Deployment Options

### 1. Local Development
```bash
# Set up development environment
bash scripts/setup_dev.sh
source venv/bin/activate
streamlit run streamlit_app.py
```

### 2. Docker (Single Container)
```dockerfile
# Build image
docker build -t ai-video-generator .

# Run container
docker run -d \
  --name ai-video-gen \
  -p 8503:8503 \
  -v $(pwd)/generated_videos:/app/generated_videos \
  ai-video-generator
```

### 3. Docker Compose (Recommended)
```bash
# Production deployment with Redis
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f ai-video-generator
```

### 4. Cloud Deployment

#### Heroku
```bash
# Install Heroku CLI
# Set environment variables
heroku config:set APP_ENV=production
heroku config:set DEBUG=false
# Deploy
git push heroku main
```

#### AWS/GCP/Azure
- Use Docker image with container services
- Set environment variables in cloud console
- Configure load balancer and auto-scaling

## Production Checklist

### Before Deployment
- [ ] Environment variables configured
- [ ] SSL certificates installed (if using HTTPS)
- [ ] Database migrations run (if applicable)
- [ ] Storage volumes mounted
- [ ] Monitoring configured

### Security
- [ ] Rate limiting enabled
- [ ] File scanning enabled
- [ ] Debug mode disabled
- [ ] Secure secrets management
- [ ] Network security configured

### Performance
- [ ] GPU support configured (if available)
- [ ] Caching enabled (Redis)
- [ ] File cleanup scheduled
- [ ] Resource limits set

### Monitoring
- [ ] Health checks configured
- [ ] Log aggregation set up
- [ ] Error tracking enabled
- [ ] Performance monitoring active

## Troubleshooting

### Common Issues

#### "Module not found" errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m coreferee install en
```

#### "Permission denied" errors
```bash
# Fix directory permissions
chmod 755 generated_videos temp logs
chown -R appuser:appuser /app  # In Docker
```

#### "Out of memory" errors
- Reduce MAX_CONCURRENT_GENERATIONS
- Lower video resolution/duration limits
- Add swap space or increase RAM

#### "Audio/Animation not working"
- Check system dependencies (ffmpeg, etc.)
- Verify audio libraries installed
- Check environment variables

### Performance Optimization

#### CPU Optimization
- Set optimal worker count
- Enable multiprocessing where possible
- Use efficient video codecs

#### Memory Optimization
- Enable cleanup of temporary files
- Set reasonable video duration limits
- Use streaming for large files

#### Storage Optimization
- Configure automatic file cleanup
- Use compression for stored videos
- Implement file rotation

## Scaling

### Horizontal Scaling
- Use load balancer (nginx/ALB)
- Deploy multiple app instances
- Shared storage for generated videos
- Redis for session/cache sharing

### Vertical Scaling
- Increase CPU/RAM allocation
- Add GPU support for AI processing
- Use faster storage (SSD)

## Backup & Recovery

### Data Backup
- Generated videos (if retention needed)
- Configuration files
- User data (if applicable)
- Logs for debugging

### Recovery Procedures
- Container restart procedures
- Database recovery (if applicable)
- File system recovery
- Rollback procedures

## Monitoring & Maintenance

### Health Checks
- Application health endpoint: `/_stcore/health`
- Database connectivity (if applicable)
- Storage space monitoring
- Memory/CPU usage

### Log Management
- Application logs: `/app/logs/`
- Error tracking and alerting
- Performance metrics
- User analytics (if applicable)

### Regular Maintenance
- Update dependencies regularly
- Clean up old files
- Monitor and optimize performance
- Security updates and patches
