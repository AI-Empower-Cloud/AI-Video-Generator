# 🚀 Quick Wasabi Setup & Deployment Guide

## 1️⃣ **Get Wasabi Account** (2 minutes)
```bash
# Visit: https://wasabi.com
# Sign up for free account (30-day trial)
# Go to: Access Keys → Generate New Key
# Copy: Access Key ID & Secret Access Key
```

## 2️⃣ **Configure Credentials** (1 minute)
```bash
# Edit .env.wasabi file:
nano .env.wasabi

# Add your credentials:
WASABI_ACCESS_KEY=your-actual-access-key-here
WASABI_SECRET_KEY=your-actual-secret-key-here
WASABI_BUCKET=educational-platform-content
```

## 3️⃣ **Deploy Your Content** (30 seconds)
```bash
# Run the deployment script:
python deploy_to_wasabi.py
```

## 4️⃣ **Test Your Deployment** (Optional)
```bash
# Test a sample file:
python test_wasabi_deployment.py
```

## 📊 **What Gets Deployed:**
- ✅ **Audio Files** (47 files, ~66MB): ABC songs, music tracks
- ✅ **Video Files** (48 files, ~165MB): Educational videos  
- ✅ **Podcast Files** (10 files, ~6.5MB): Educational podcasts
- ✅ **Interview Files** (12 files, ~47MB): Live interviews

## 💰 **Expected Costs:**
- **Storage**: ~$0.002/month (288MB total)
- **Bandwidth**: $0 (no egress fees)
- **Total**: Under $0.01/month

## 🌐 **After Deployment:**
Your files will be accessible at:
```
https://s3.wasabisys.com/educational-platform-content/audio/[filename]
https://s3.wasabisys.com/educational-platform-content/videos/[filename]
https://s3.wasabisys.com/educational-platform-content/podcasts/[filename]
https://s3.wasabisys.com/educational-platform-content/interviews/[filename]
```

## 🔄 **Update Your Web Players:**
The deployment script will generate a manifest with all public URLs that you can use to update your HTML players automatically.

## ⚡ **Total Setup Time: 3-4 minutes**
