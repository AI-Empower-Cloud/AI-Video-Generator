# 🌐 Web Service Setup Guide

## Overview
This guide helps you deploy your AI Video Generator as a web service using various platforms and methods.

## 🚀 Deployment Options

### 1. **Heroku (Easiest)**
- Free tier available
- Automatic deployment from Git
- Built-in SSL

### 2. **AWS (Most Scalable)**
- ECS with Fargate
- Lambda for serverless
- EC2 for full control

### 3. **Google Cloud Platform**
- Cloud Run (serverless)
- App Engine
- Compute Engine

### 4. **Digital Ocean**
- App Platform
- Droplets
- Kubernetes

### 5. **Railway (Developer Friendly)**
- Simple deployment
- Auto-scaling
- Built-in database

### 6. **Render (Modern)**
- Free tier
- Auto-deploy from Git
- Built-in SSL

## 📋 Prerequisites

1. **GitHub Repository** ✅ (Already done)
2. **Docker Configuration** ✅ (Already done)
3. **Environment Variables** ✅ (Already done)
4. **Domain Name** (Optional)

## 🎯 Recommended: Railway Deployment

Railway is perfect for your AI Video Generator because:
- ✅ Easy deployment from GitHub
- ✅ Auto-scaling
- ✅ Built-in domains
- ✅ Environment variable management
- ✅ Free tier with good limits

## 🛠️ Next Steps

Choose your preferred deployment method from the options below:

1. **[Railway](#railway-setup)** - Recommended for beginners
2. **[Heroku](#heroku-setup)** - Traditional PaaS
3. **[AWS](#aws-setup)** - Enterprise scale
4. **[Render](#render-setup)** - Modern alternative

---

# Railway Setup

## Step 1: Connect GitHub
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "Deploy from GitHub repo"
4. Select your AI-Video-Generator repository

## Step 2: Configure Service
Railway will automatically:
- Detect your Dockerfile
- Set up the build process
- Deploy your application

## Step 3: Set Environment Variables
Add these variables in Railway dashboard:
```
APP_ENV=production
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
```

## Step 4: Custom Domain (Optional)
- Add your custom domain in Railway settings
- Railway provides a free subdomain automatically

---

# Heroku Setup

## Step 1: Create Heroku App
```bash
# Install Heroku CLI
# Create new app
heroku create your-ai-video-generator

# Set environment variables
heroku config:set APP_ENV=production
heroku config:set PYTHONUNBUFFERED=1
```

## Step 2: Configure for Container Deployment
```bash
# Set stack to container
heroku stack:set container

# Deploy
git push heroku main
```

---

# AWS Setup

## Step 1: Create ECS Service
Use the provided `aws-ecs-task-definition.json`

## Step 2: Set up Load Balancer
Configure Application Load Balancer for HTTPS

## Step 3: Domain Configuration
Use Route 53 for DNS management

---

# Render Setup

## Step 1: Connect Repository
1. Go to [render.com](https://render.com)
2. Connect your GitHub repository
3. Choose "Web Service"

## Step 2: Configure Build
- Build Command: `docker build -t app .`
- Start Command: `docker run -p $PORT:8503 app`

---

# 🔧 Custom VPS Setup

If you want to deploy on your own server:

## Step 1: Server Requirements
- Ubuntu 20.04+ or similar
- 2GB+ RAM
- 20GB+ storage
- Docker installed

## Step 2: Deploy Script
Use the provided deployment scripts in `/deploy` folder

---

# 🌍 Domain and SSL

## Custom Domain Setup
1. **Purchase Domain** (GoDaddy, Namecheap, etc.)
2. **Configure DNS** to point to your service
3. **SSL Certificate** (Let's Encrypt - automatic on most platforms)

## Subdomain Options
- `ai-video.yourdomain.com`
- `video-generator.yourdomain.com`
- `app.yourdomain.com`

---

# 📊 Monitoring and Analytics

## Performance Monitoring
- **Uptime monitoring** with UptimeRobot
- **Error tracking** with Sentry
- **Analytics** with Google Analytics

## Health Checks
Your app includes health check endpoints:
- `/health` - Basic health check
- `/_stcore/health` - Streamlit health check

---

# 🔐 Security Considerations

## Environment Variables
Never commit sensitive data:
- API keys
- Database passwords
- Secret tokens

## HTTPS
All platforms mentioned provide automatic HTTPS

## Rate Limiting
Consider implementing rate limiting for production use

---

# 💰 Cost Estimates

## Free Tiers
- **Railway**: $5/month after free tier
- **Render**: Free for static sites, $7/month for web services
- **Heroku**: $7/month for basic dyno

## Paid Options
- **AWS**: $10-50/month depending on usage
- **Google Cloud**: $10-40/month
- **Digital Ocean**: $5-20/month

---

# 🚀 Quick Start (Railway - Recommended)

1. Go to [railway.app](https://railway.app)
2. Click "Deploy from GitHub repo"
3. Select `AI-Empower-Cloud/AI-Video-Generator`
4. Click "Deploy"
5. Your app will be live in 2-3 minutes!

Your web service will be available at: `https://your-app-name.railway.app`
