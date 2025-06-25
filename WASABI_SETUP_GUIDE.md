# Wasabi Cloud Storage Setup Guide

## 🗄️ Wasabi vs Other Storage Options

| Feature | Wasabi | AWS S3 | Google Cloud | Azure |
|---------|--------|--------|--------------|-------|
| **Cost/TB/month** | $6.99 | $23+ | $20+ | $18+ |
| **Egress fees** | FREE | $90/TB | $120/TB | $87/TB |
| **S3 Compatible** | ✅ Yes | ✅ Native | ❌ No | ❌ No |
| **Global CDN** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |

## 💰 Cost Calculator for Your Platform

**Current Content Size: 288MB**

### Wasabi Pricing:
- **Storage**: $0.002/month (288MB)
- **Bandwidth**: $0 (no egress fees)
- **Total**: ~$0.002/month

### AWS S3 Equivalent:
- **Storage**: $0.007/month  
- **Bandwidth**: $25.9/TB (if high traffic)
- **Total**: $0.007+ per month

## 🚀 Setup Steps

### 1. Create Wasabi Account
```bash
# Visit: https://wasabi.com
# Sign up for free account
# Get access keys from console
```

### 2. Install Dependencies
```bash
pip install boto3 python-dotenv
```

### 3. Environment Setup
```bash
# Create .env file
echo "WASABI_ACCESS_KEY=your-access-key" >> .env
echo "WASABI_SECRET_KEY=your-secret-key" >> .env
echo "WASABI_BUCKET=educational-platform" >> .env
```

### 4. Deploy Your Content
```bash
# Run the deployment script
python wasabi_storage_example.py
```

## 🌐 CDN Integration

### Wasabi + CloudFlare Setup:
```javascript
// Update your HTML players to use CDN URLs
const WASABI_CDN = "https://cdn.yourdomain.com";

// Example: Update video player
function loadVideoFromWasabi(videoKey) {
    const videoUrl = `${WASABI_CDN}/videos/${videoKey}`;
    document.getElementById('video-player').src = videoUrl;
}

// Example: Update audio player  
function loadAudioFromWasabi(audioKey) {
    const audioUrl = `${WASABI_CDN}/audio/${audioKey}`;
    document.getElementById('audio-player').src = audioUrl;
}
```

## 🔒 Security Options

### Public Content:
- Direct bucket access
- CDN caching
- Fast delivery

### Private Content:
- Signed URLs (temporary access)
- User authentication required
- Premium content protection

## 📊 Monitoring & Analytics

```python
# Track usage and costs
def get_storage_stats():
    s3 = boto3.client('s3', endpoint_url='https://s3.wasabisys.com')
    
    # Get bucket size
    response = s3.list_objects_v2(Bucket='your-bucket')
    total_size = sum(obj['Size'] for obj in response.get('Contents', []))
    
    # Calculate monthly cost
    monthly_cost = (total_size / (1024**4)) * 6.99  # $6.99/TB
    
    return {
        'total_size_gb': total_size / (1024**3),
        'monthly_cost_usd': monthly_cost,
        'file_count': response.get('KeyCount', 0)
    }
```

## 🎯 Recommended Architecture

```
Educational Platform Architecture:

┌─────────────────┐    ┌──────────────┐    ┌─────────────┐
│   Your App      │    │   Wasabi     │    │ CloudFlare  │
│   (Codespace)   │───▶│   Storage    │───▶│    CDN      │
│                 │    │              │    │             │
└─────────────────┘    └──────────────┘    └─────────────┘
         │                      │                   │
         │                      │                   │
         ▼                      ▼                   ▼
┌─────────────────┐    ┌──────────────┐    ┌─────────────┐
│   Users         │    │  Backup      │    │   Global    │
│   Access        │    │  & Archive   │    │   Users     │
└─────────────────┘    └──────────────┘    └─────────────┘
```

## ✅ Next Steps

1. **Sign up for Wasabi** (5 minutes)
2. **Run the example script** to test upload
3. **Configure CDN** for better performance  
4. **Update your HTML players** to use Wasabi URLs
5. **Monitor usage** and optimize costs

**Perfect for your educational platform!** 🎓
