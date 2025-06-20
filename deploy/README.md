# 🚀 Deployment Guide

This guide covers deployment options for the AI Video Generator project.

## 📋 Prerequisites

- Docker and Docker Compose
- Git
- Minimum 4GB RAM
- 10GB free disk space

## 🐳 Docker Deployment Options

### 1. Development Environment

Quick setup for development:

```bash
# Clone repository
git clone https://github.com/yourusername/AI-Video-Generator.git
cd AI-Video-Generator

# Start development environment
./deploy/dev.sh setup

# Access application
open http://localhost:8503
```

### 2. Production Deployment

Full production setup with Nginx:

```bash
# Production deployment
./deploy/deploy.sh

# Or manually
docker-compose -f docker-compose.prod.yml up -d

# Access application
open http://localhost
```

### 3. Docker Hub Deployment

```bash
# Pull from Docker Hub
docker pull yourusername/ai-video-generator:latest

# Run container
docker run -d \
  --name ai-video-generator \
  -p 8503:8503 \
  -v $(pwd)/generated_videos:/app/generated_videos \
  yourusername/ai-video-generator:latest
```

## ☁️ Cloud Deployment

### AWS Deployment

1. **EC2 Instance**:
   ```bash
   # Launch EC2 instance (t3.medium or larger)
   # Install Docker
   sudo yum update -y
   sudo amazon-linux-extras install docker
   sudo service docker start
   sudo usermod -a -G docker ec2-user
   
   # Deploy application
   git clone https://github.com/yourusername/AI-Video-Generator.git
   cd AI-Video-Generator
   ./deploy/deploy.sh
   ```

2. **ECS Deployment**:
   ```yaml
   # task-definition.json
   {
     "family": "ai-video-generator",
     "networkMode": "awsvpc",
     "requiresCompatibilities": ["FARGATE"],
     "cpu": "2048",
     "memory": "4096",
     "containerDefinitions": [
       {
         "name": "ai-video-generator",
         "image": "yourusername/ai-video-generator:latest",
         "portMappings": [
           {
             "containerPort": 8503,
             "protocol": "tcp"
           }
         ]
       }
     ]
   }
   ```

### Google Cloud Platform

```bash
# Deploy to Cloud Run
gcloud run deploy ai-video-generator \
  --image=gcr.io/your-project/ai-video-generator \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated \
  --memory=4Gi \
  --cpu=2
```

### Azure Container Instances

```bash
# Deploy to Azure
az container create \
  --resource-group myResourceGroup \
  --name ai-video-generator \
  --image yourusername/ai-video-generator:latest \
  --dns-name-label ai-video-gen \
  --ports 8503 \
  --memory 4 \
  --cpu 2
```

## 🔧 Configuration

### Environment Variables

Create `.env` file:

```bash
# Application
APP_ENV=production
DEBUG=false
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql://user:pass@localhost/dbname

# External APIs
YOUTUBE_API_KEY=your-youtube-api-key
OPENAI_API_KEY=your-openai-api-key

# Storage
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
S3_BUCKET=your-s3-bucket

# Monitoring
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=INFO
```

### SSL Configuration

For production with SSL:

1. Obtain SSL certificates
2. Update `nginx/nginx.conf`
3. Mount certificates in docker-compose

```yaml
volumes:
  - ./ssl:/etc/nginx/ssl:ro
```

## 📊 Monitoring & Logging

### Health Checks

```bash
# Application health
curl http://localhost:8503/_stcore/health

# Nginx health
curl http://localhost/health

# Container health
docker ps --filter "name=ai-video-generator"
```

### Log Monitoring

```bash
# Application logs
docker-compose logs -f ai-video-generator

# Nginx logs
docker-compose logs -f nginx

# System monitoring
./deploy/docker-utils.sh logs
```

## 🔒 Security

### Production Security Checklist

- [ ] Use strong passwords/secrets
- [ ] Enable SSL/TLS
- [ ] Configure firewall rules
- [ ] Set up rate limiting
- [ ] Enable container security scanning
- [ ] Use non-root user in containers
- [ ] Regularly update dependencies

### Network Security

```yaml
# docker-compose.prod.yml
networks:
  ai-video-net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

## 🚀 CI/CD Pipeline

### GitHub Actions

The project includes automated CI/CD:

- **Test**: Runs on every push/PR
- **Build**: Creates Docker images
- **Deploy**: Pushes to container registry
- **Docs**: Updates GitHub Pages

### Manual Deployment

```bash
# Build and push
./deploy/docker-utils.sh build latest

# Deploy to production
./deploy/docker-utils.sh prod

# Monitor deployment
./deploy/docker-utils.sh health
```

## 📈 Scaling

### Horizontal Scaling

```bash
# Scale application containers
docker-compose -f docker-compose.prod.yml up -d --scale ai-video-generator=3

# Load balancer configuration
# Update nginx upstream configuration
```

### Vertical Scaling

```yaml
# docker-compose.prod.yml
services:
  ai-video-generator:
    deploy:
      resources:
        limits:
          memory: 8G
          cpus: '4'
```

## 🛠️ Troubleshooting

### Common Issues

1. **Out of Memory**:
   ```bash
   # Increase memory limits
   docker-compose down
   # Edit docker-compose.yml memory limits
   docker-compose up -d
   ```

2. **Permission Issues**:
   ```bash
   # Fix file permissions
   sudo chown -R 1000:1000 generated_videos logs
   ```

3. **Port Conflicts**:
   ```bash
   # Check port usage
   netstat -tulpn | grep :8503
   # Change port in docker-compose.yml
   ```

### Log Analysis

```bash
# Application errors
docker-compose logs ai-video-generator | grep ERROR

# Performance metrics
docker stats ai-video-generator

# Container inspection
docker inspect ai-video-generator
```

## 🔄 Backup & Recovery

### Automated Backups

```bash
# Create backup
./deploy/docker-utils.sh backup

# Restore from backup
./deploy/docker-utils.sh restore /path/to/backup
```

### Data Persistence

Ensure these directories are persistent:
- `./generated_videos`
- `./logs`
- `./data` (if using database)

## 📞 Support

For deployment issues:

1. Check logs: `./deploy/docker-utils.sh logs`
2. Run health checks: `./deploy/docker-utils.sh health`
3. Create GitHub issue with logs
4. Contact support team

---

**Next**: [User Guide](USER_GUIDE.md) | [API Reference](API_REFERENCE.md)
