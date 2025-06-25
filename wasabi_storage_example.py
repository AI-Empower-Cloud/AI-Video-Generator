#!/usr/bin/env python3
"""
Wasabi Cloud Storage Integration Example
For Educational Video/Audio Platform
"""

import boto3
import os
from pathlib import Path
import mimetypes

class WasabiStorage:
    def __init__(self):
        # Wasabi S3-compatible endpoint
        self.endpoint = "https://s3.wasabisys.com"
        self.region = "us-east-1"  # or your preferred region
        
        # Initialize S3 client for Wasabi
        self.s3_client = boto3.client(
            's3',
            endpoint_url=self.endpoint,
            aws_access_key_id=os.getenv('WASABI_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('WASABI_SECRET_KEY'),
            region_name=self.region
        )
        
        self.bucket_name = "educational-platform-content"
    
    def upload_file(self, local_file_path, remote_key):
        """Upload file to Wasabi storage"""
        try:
            # Detect content type
            content_type, _ = mimetypes.guess_type(local_file_path)
            if not content_type:
                content_type = 'application/octet-stream'
            
            # Upload with proper content type
            self.s3_client.upload_file(
                local_file_path, 
                self.bucket_name, 
                remote_key,
                ExtraArgs={'ContentType': content_type}
            )
            
            # Generate public URL
            url = f"{self.endpoint}/{self.bucket_name}/{remote_key}"
            print(f"✅ Uploaded: {local_file_path} -> {url}")
            return url
            
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            return None
    
    def upload_directory(self, local_dir, remote_prefix=""):
        """Upload entire directory to Wasabi"""
        local_path = Path(local_dir)
        uploaded_files = []
        
        for file_path in local_path.rglob("*"):
            if file_path.is_file():
                # Create remote key
                relative_path = file_path.relative_to(local_path)
                remote_key = f"{remote_prefix}/{relative_path}".lstrip("/")
                
                # Upload file
                url = self.upload_file(str(file_path), remote_key)
                if url:
                    uploaded_files.append({
                        'local': str(file_path),
                        'remote': remote_key,
                        'url': url
                    })
        
        return uploaded_files
    
    def generate_signed_url(self, remote_key, expiration=3600):
        """Generate signed URL for private content"""
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': remote_key},
                ExpiresIn=expiration
            )
            return url
        except Exception as e:
            print(f"❌ Failed to generate signed URL: {e}")
            return None

def deploy_content_to_wasabi():
    """Deploy all educational content to Wasabi storage"""
    wasabi = WasabiStorage()
    
    # Upload directories
    content_dirs = [
        ('audio_output', 'audio'),
        ('video_output', 'videos'), 
        ('podcast_output', 'podcasts'),
        ('interview_output', 'interviews')
    ]
    
    all_uploaded = {}
    
    for local_dir, remote_prefix in content_dirs:
        if os.path.exists(local_dir):
            print(f"\n📁 Uploading {local_dir}...")
            files = wasabi.upload_directory(local_dir, remote_prefix)
            all_uploaded[remote_prefix] = files
            print(f"✅ Uploaded {len(files)} files from {local_dir}")
    
    # Generate content manifest
    manifest = {
        'platform': 'Educational Video/Audio Platform',
        'upload_date': '2025-06-25',
        'total_files': sum(len(files) for files in all_uploaded.values()),
        'content': all_uploaded
    }
    
    return manifest

if __name__ == "__main__":
    # Example usage
    print("🚀 Wasabi Storage Integration for Educational Platform")
    print("=" * 50)
    
    # Set environment variables first:
    # export WASABI_ACCESS_KEY="your-access-key" 
    # export WASABI_SECRET_KEY="your-secret-key"
    
    if not os.getenv('WASABI_ACCESS_KEY'):
        print("⚠️  Please set WASABI_ACCESS_KEY and WASABI_SECRET_KEY environment variables")
        print("\nExample setup:")
        print("export WASABI_ACCESS_KEY='your-access-key'")
        print("export WASABI_SECRET_KEY='your-secret-key'")
    else:
        manifest = deploy_content_to_wasabi()
        print(f"\n🎉 Deployment complete! {manifest['total_files']} files uploaded")
