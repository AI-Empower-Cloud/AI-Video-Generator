#!/usr/bin/env python3
"""
Wasabi Deployment Script for Educational Platform
Simple, fast deployment of all content to Wasabi storage
"""

import os
import boto3
import json
from pathlib import Path
from dotenv import load_dotenv
import mimetypes
from datetime import datetime

class WasabiDeployer:
    def __init__(self):
        # Load environment variables
        load_dotenv('.env.wasabi')
        
        self.access_key = os.getenv('WASABI_ACCESS_KEY')
        self.secret_key = os.getenv('WASABI_SECRET_KEY')
        self.bucket_name = os.getenv('WASABI_BUCKET', 'educational-platform-content')
        self.region = os.getenv('WASABI_REGION', 'us-east-1')
        self.endpoint = os.getenv('WASABI_ENDPOINT', 'https://s3.wasabisys.com')
        
        if not self.access_key or not self.secret_key:
            print("❌ Error: WASABI_ACCESS_KEY and WASABI_SECRET_KEY must be set in .env.wasabi")
            print("\n📝 Please edit .env.wasabi with your Wasabi credentials")
            exit(1)
        
        # Initialize S3 client
        self.s3 = boto3.client(
            's3',
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region
        )
        
        print(f"🚀 Connected to Wasabi bucket: {self.bucket_name}")
    
    def create_bucket_if_not_exists(self):
        """Create bucket if it doesn't exist"""
        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
            print(f"✅ Bucket '{self.bucket_name}' exists")
        except:
            try:
                self.s3.create_bucket(Bucket=self.bucket_name)
                print(f"✅ Created bucket '{self.bucket_name}'")
            except Exception as e:
                print(f"❌ Failed to create bucket: {e}")
                return False
        return True
    
    def upload_file(self, local_path, remote_key):
        """Upload single file to Wasabi"""
        try:
            # Detect content type
            content_type, _ = mimetypes.guess_type(local_path)
            if not content_type:
                if local_path.endswith('.mp4'):
                    content_type = 'video/mp4'
                elif local_path.endswith('.wav'):
                    content_type = 'audio/wav'
                elif local_path.endswith('.mp3'):
                    content_type = 'audio/mpeg'
                else:
                    content_type = 'application/octet-stream'
            
            # Upload with proper content type and public read access
            self.s3.upload_file(
                local_path,
                self.bucket_name,
                remote_key,
                ExtraArgs={
                    'ContentType': content_type,
                    'ACL': 'public-read'  # Make files publicly accessible
                }
            )
            
            # Generate public URL
            public_url = f"{self.endpoint}/{self.bucket_name}/{remote_key}"
            return public_url
            
        except Exception as e:
            print(f"❌ Upload failed for {local_path}: {e}")
            return None
    
    def deploy_directory(self, local_dir, remote_prefix):
        """Deploy entire directory to Wasabi"""
        if not os.path.exists(local_dir):
            print(f"⚠️  Directory {local_dir} not found, skipping...")
            return []
        
        local_path = Path(local_dir)
        uploaded_files = []
        
        print(f"\n📁 Deploying {local_dir} to {remote_prefix}/...")
        
        for file_path in local_path.rglob("*"):
            if file_path.is_file():
                # Create remote key
                relative_path = file_path.relative_to(local_path)
                remote_key = f"{remote_prefix}/{relative_path}".replace("\\", "/")
                
                # Upload file
                public_url = self.upload_file(str(file_path), remote_key)
                
                if public_url:
                    uploaded_files.append({
                        'filename': file_path.name,
                        'local_path': str(file_path),
                        'remote_key': remote_key,
                        'public_url': public_url,
                        'size_mb': round(file_path.stat().st_size / (1024*1024), 2)
                    })
                    print(f"  ✅ {file_path.name} ({uploaded_files[-1]['size_mb']} MB)")
        
        print(f"📊 Uploaded {len(uploaded_files)} files from {local_dir}")
        return uploaded_files
    
    def deploy_all_content(self):
        """Deploy all educational content to Wasabi"""
        print("🚀 Starting Educational Platform Deployment to Wasabi")
        print("=" * 60)
        
        # Create bucket if needed
        if not self.create_bucket_if_not_exists():
            return None
        
        # Define content directories
        content_dirs = [
            ('audio_output', 'audio'),
            ('video_output', 'videos'),
            ('podcast_output', 'podcasts'),
            ('interview_output', 'interviews')
        ]
        
        deployment_manifest = {
            'platform': 'Educational Video/Audio Generation Platform',
            'deployment_date': datetime.now().isoformat(),
            'bucket': self.bucket_name,
            'endpoint': self.endpoint,
            'content': {},
            'stats': {
                'total_files': 0,
                'total_size_mb': 0
            }
        }
        
        # Deploy each directory
        for local_dir, remote_prefix in content_dirs:
            files = self.deploy_directory(local_dir, remote_prefix)
            if files:
                deployment_manifest['content'][remote_prefix] = files
                deployment_manifest['stats']['total_files'] += len(files)
                deployment_manifest['stats']['total_size_mb'] += sum(f['size_mb'] for f in files)
        
        # Save deployment manifest
        manifest_path = 'wasabi_deployment_manifest.json'
        with open(manifest_path, 'w') as f:
            json.dump(deployment_manifest, f, indent=2)
        
        # Upload manifest to Wasabi
        manifest_url = self.upload_file(manifest_path, 'deployment_manifest.json')
        
        print("\n🎉 Deployment Complete!")
        print("=" * 60)
        print(f"📊 Total Files: {deployment_manifest['stats']['total_files']}")
        print(f"📊 Total Size: {deployment_manifest['stats']['total_size_mb']:.1f} MB")
        print(f"🌐 Bucket: {self.bucket_name}")
        print(f"📋 Manifest: {manifest_url}")
        
        return deployment_manifest

def main():
    """Main deployment function"""
    print("🗄️  Wasabi Educational Platform Deployer")
    print("=" * 50)
    
    # Check if .env.wasabi exists
    if not os.path.exists('.env.wasabi'):
        print("❌ .env.wasabi file not found!")
        print("📝 Please create .env.wasabi with your Wasabi credentials")
        print("\nExample:")
        print("WASABI_ACCESS_KEY=your-access-key")
        print("WASABI_SECRET_KEY=your-secret-key")
        print("WASABI_BUCKET=educational-platform-content")
        return
    
    try:
        deployer = WasabiDeployer()
        manifest = deployer.deploy_all_content()
        
        if manifest:
            print(f"\n✅ All content deployed successfully!")
            print(f"📱 Access your content at: {deployer.endpoint}/{deployer.bucket_name}/")
            
            # Show some example URLs
            if 'audio' in manifest['content'] and manifest['content']['audio']:
                print(f"🎵 Example Audio: {manifest['content']['audio'][0]['public_url']}")
            if 'videos' in manifest['content'] and manifest['content']['videos']:
                print(f"🎬 Example Video: {manifest['content']['videos'][0]['public_url']}")
    
    except Exception as e:
        print(f"❌ Deployment failed: {e}")

if __name__ == "__main__":
    main()
