# 🌐 Complete Hosting Setup Guide
# Durable.co vs Wix Studio for AI Video Generator Platform

## 🎯 **Platform Comparison**

| Feature | Durable.co | Wix Studio |
|---------|------------|------------|
| **Custom HTML** | ✅ Full support | ❌ Limited |
| **GitHub Integration** | ✅ Direct deploy | ⚠️ Manual upload |
| **Monthly Cost** | $5-10 | $13-39 |
| **Setup Time** | 10 minutes | 15-30 minutes |
| **Technical Level** | Medium | Easy |
| **Custom Players** | ✅ Works perfectly | ❌ Need rebuilding |
| **CDN Support** | ✅ Built-in | ✅ Built-in |
| **SSL Certificate** | ✅ Free | ✅ Free |

## 🚀 **Option A: Durable.co Setup (RECOMMENDED)**

### Step 1: Sign Up & Connect GitHub
```bash
# Visit: https://durable.co
# Click "Get Started" → "Import from GitHub"
```

### Step 2: Repository Configuration
```
Repository: AI-Empower-Cloud/AI-Video-Generator
Branch: main
Build Command: (leave empty - static files)
Publish Directory: . (root directory)
Environment Variables: (none needed)
```

### Step 3: Custom Domain (Optional)
```
Domain: your-domain.com
DNS Configuration: Point to Durable's servers
SSL: Automatically provisioned
```

### Step 4: Deploy Settings
```yaml
# durable.yml (auto-generated)
name: ai-video-generator
type: static
build:
  command: ""
  output: "."
deploy:
  files:
    - "*.html"
    - "*.css" 
    - "*.js"
    - "*.json"
    - "*.md"
```

## 🎨 **Option B: Wix Studio Setup**

### Step 1: Create Wix Studio Account
```bash
# Visit: https://www.wix.com/studio
# Sign up for Wix Studio (not regular Wix)
# Choose "Blank Template" or "Developer Mode"
```

### Step 2: Upload Your Files
Since Wix doesn't support custom HTML directly, you'll need to:

1. **Convert HTML to Wix Components**
2. **Manually recreate the interfaces**
3. **Upload media to Wix Media Manager**

### Step 3: Wix Media Manager Setup
```
1. Go to Media Manager
2. Create folders:
   - Audio (for ABC songs, music)
   - Videos (for educational content)
   - Podcasts (for episodes)
   - Interviews (for recordings)
3. Upload files from your Wasabi URLs
```

## 🔧 **Durable.co Detailed Setup Process**

### Prerequisites Completed:
✅ GitHub repository ready
✅ Wasabi deployment completed  
✅ HTML files updated with CDN URLs

### Step-by-Step Process:

#### 1. Account Creation
```bash
# 1. Visit durable.co
# 2. Click "Sign Up"
# 3. Choose "GitHub" authentication
# 4. Authorize Durable to access your repositories
```

#### 2. Import Repository
```bash
# 1. Click "New Project"
# 2. Select "Import Git Repository"
# 3. Choose: AI-Empower-Cloud/AI-Video-Generator
# 4. Branch: main
# 5. Click "Import Project"
```

#### 3. Configure Build Settings
```yaml
# Project Settings:
Framework: Static Site
Build Command: (empty)
Output Directory: .
Install Command: (empty)
Root Directory: (empty)

# Environment Variables: (none needed)
```

#### 4. Deploy & Test
```bash
# 1. Click "Deploy"
# 2. Wait 2-3 minutes for deployment
# 3. Visit your provided URL
# 4. Test all features:
#    - Dashboard loads
#    - Audio player works
#    - Video player works
#    - Podcast player works
#    - All Wasabi CDN links work
```

## 🎯 **Post-Deployment Configuration**

### Update DNS (if using custom domain)
```bash
# For Durable.co:
# Add CNAME record: www.yourdomain.com → your-project.durable.co
# Add A record: yourdomain.com → Durable's IP

# For Wix Studio:  
# Point domain to Wix servers (automatic in Wix dashboard)
```

### Performance Optimization
```html
<!-- Add to <head> of HTML files for better performance -->
<link rel="preconnect" href="https://s3.wasabisys.com">
<link rel="dns-prefetch" href="https://s3.wasabisys.com">

<!-- Enable compression -->
<meta http-equiv="Content-Encoding" content="gzip">
```

## 📊 **Expected Performance**

### Durable.co Performance:
- **Load Time**: 1-2 seconds (with Wasabi CDN)
- **Uptime**: 99.9%
- **Global CDN**: Yes
- **SSL**: Automatic
- **Bandwidth**: Unlimited

### Wix Studio Performance:
- **Load Time**: 2-4 seconds (Wix optimization)
- **Uptime**: 99.9%
- **Global CDN**: Yes
- **SSL**: Automatic  
- **Bandwidth**: Based on plan

## 🚨 **Troubleshooting Guide**

### Common Issues & Solutions:

#### Issue 1: Files not loading from Wasabi
```bash
# Solution: Check CORS settings
# Add to Wasabi bucket policy:
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-bucket/*"
    }
  ]
}
```

#### Issue 2: Audio/Video not playing
```javascript
// Add to your HTML files:
<script>
// Enable CORS for media files
document.addEventListener('DOMContentLoaded', function() {
    const mediaElements = document.querySelectorAll('audio, video');
    mediaElements.forEach(element => {
        element.crossOrigin = 'anonymous';
    });
});
</script>
```

#### Issue 3: Slow loading times
```html
<!-- Optimize by preloading critical resources -->
<link rel="preload" href="https://s3.wasabisys.com/your-bucket/audio/abc_song.wav" as="audio">
<link rel="preload" href="https://s3.wasabisys.com/your-bucket/videos/abc_video.mp4" as="video">
```

## 💡 **Pro Tips**

### For Durable.co:
1. **Use Git Branches** for staging vs production
2. **Enable Analytics** in Durable dashboard
3. **Set up Monitoring** for uptime alerts
4. **Optimize Images** before deployment

### For Wix Studio:
1. **Use Wix Editor** for easy visual editing
2. **Leverage Wix Apps** for additional functionality
3. **Optimize SEO** using Wix SEO tools
4. **Enable Wix Analytics** for visitor tracking

## 🎉 **Final Checklist**

### Before Going Live:
- [ ] All HTML files load correctly
- [ ] Audio players work with Wasabi URLs
- [ ] Video players stream properly
- [ ] Podcast episodes play smoothly  
- [ ] Interview recordings accessible
- [ ] Mobile responsive design works
- [ ] SSL certificate active
- [ ] Custom domain configured (if applicable)
- [ ] Analytics tracking setup
- [ ] SEO metadata added

### Post-Launch:
- [ ] Monitor performance metrics
- [ ] Track user engagement
- [ ] Regular content updates
- [ ] Backup configurations
- [ ] Plan migration strategy (after 6 months)

## 📞 **Support Resources**

### Durable.co:
- Documentation: docs.durable.co
- Support: hello@durable.co
- Community: Discord/Slack

### Wix Studio:
- Help Center: help.wix.com
- Support: Wix Help Center
- Community: Wix Forum

**Your educational platform is ready for professional hosting!** 🚀🎓
