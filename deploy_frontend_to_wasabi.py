#!/usr/bin/env python3
"""
Enhanced Wasabi Deployment Script for AI Video Generator Platform
Deploys both backend content and frontend static files to Wasabi
"""

import os
import boto3
import json
import subprocess
import shutil
from pathlib import Path
from dotenv import load_dotenv
import mimetypes
from datetime import datetime

class WasabiFrontendDeployer:
    def __init__(self):
        # Load environment variables
        load_dotenv('.env.wasabi')
        
        self.access_key = os.getenv('WASABI_ACCESS_KEY')
        self.secret_key = os.getenv('WASABI_SECRET_KEY')
        self.bucket_name = os.getenv('WASABI_BUCKET', 'ai-video-generator-content')
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
                
                # Configure bucket for static website hosting
                self.configure_static_website()
            except Exception as e:
                print(f"❌ Error creating bucket: {e}")
                return False
        return True
    
    def configure_static_website(self):
        """Configure bucket for static website hosting"""
        try:
            website_config = {
                'IndexDocument': {'Suffix': 'index.html'},
                'ErrorDocument': {'Key': 'error.html'}
            }
            
            self.s3.put_bucket_website(
                Bucket=self.bucket_name,
                WebsiteConfiguration=website_config
            )
            
            # Set bucket policy for public read access
            bucket_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "PublicReadGetObject",
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": "s3:GetObject",
                        "Resource": f"arn:aws:s3:::{self.bucket_name}/*"
                    }
                ]
            }
            
            self.s3.put_bucket_policy(
                Bucket=self.bucket_name,
                Policy=json.dumps(bucket_policy)
            )
            
            print(f"✅ Configured bucket for static website hosting")
            print(f"🌐 Website URL: https://{self.bucket_name}.s3-website.{self.region}.wasabisys.com")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not configure static website hosting: {e}")
    
    def build_frontend(self):
        """Build the Next.js frontend"""
        print("🔨 Building Next.js frontend...")
        
        frontend_dir = Path("frontend")
        if not frontend_dir.exists():
            print("❌ Frontend directory not found!")
            return False
        
        try:
            # Change to frontend directory and build
            os.chdir(frontend_dir)
            
            # Install dependencies if node_modules doesn't exist
            if not Path("node_modules").exists():
                print("📦 Installing dependencies...")
                subprocess.run(["npm", "install"], check=True)
            
            # Build the project
            print("🔨 Building project...")
            subprocess.run(["npm", "run", "build"], check=True)
            
            # Export static files
            print("📤 Exporting static files...")
            subprocess.run(["npm", "run", "export"], check=True, capture_output=True)
            
            os.chdir("..")  # Return to root directory
            print("✅ Frontend build completed!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Build failed: {e}")
            os.chdir("..")  # Return to root directory
            return False
        except Exception as e:
            print(f"❌ Unexpected error during build: {e}")
            os.chdir("..")  # Return to root directory
            return False
    
    def upload_frontend(self):
        """Upload frontend static files to Wasabi"""
        print("🚀 Uploading frontend to Wasabi...")
        
        # Check for built frontend files
        build_dir = Path("frontend/out")  # Next.js export output
        if not build_dir.exists():
            build_dir = Path("frontend/.next")  # Fallback to .next
            if not build_dir.exists():
                print("❌ No built frontend files found!")
                return False
        
        uploaded_files = []
        
        try:
            for file_path in build_dir.rglob("*"):
                if file_path.is_file():
                    # Calculate relative path from build directory
                    relative_path = file_path.relative_to(build_dir)
                    
                    # Skip certain files
                    if any(skip in str(relative_path) for skip in ['.DS_Store', 'Thumbs.db', '.git']):
                        continue
                    
                    # Determine S3 key (remote path)
                    s3_key = f"frontend/{relative_path}".replace("\\", "/")
                    
                    # Special handling for index.html at root
                    if relative_path.name == "index.html" and str(relative_path) == "index.html":
                        # Also upload as root index
                        self.upload_file(file_path, "index.html")
                        uploaded_files.append(("index.html", file_path))
                    
                    # Upload file
                    self.upload_file(file_path, s3_key)
                    uploaded_files.append((s3_key, file_path))
                    
            print(f"✅ Uploaded {len(uploaded_files)} frontend files")
            return True
            
        except Exception as e:
            print(f"❌ Error uploading frontend: {e}")
            return False
    
    def upload_file(self, local_path, s3_key):
        """Upload a single file to S3"""
        try:
            # Determine content type
            content_type, _ = mimetypes.guess_type(str(local_path))
            if content_type is None:
                content_type = 'application/octet-stream'
            
            # Special content types for web files
            if str(local_path).endswith('.js'):
                content_type = 'application/javascript'
            elif str(local_path).endswith('.css'):
                content_type = 'text/css'
            elif str(local_path).endswith('.html'):
                content_type = 'text/html'
            elif str(local_path).endswith('.json'):
                content_type = 'application/json'
            
            # Upload with proper content type and cache headers
            extra_args = {
                'ContentType': content_type,
                'ACL': 'public-read'
            }
            
            # Add cache headers for static assets
            if any(ext in str(local_path) for ext in ['.js', '.css', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg']):
                extra_args['CacheControl'] = 'public, max-age=31536000'  # 1 year
            elif str(local_path).endswith('.html'):
                extra_args['CacheControl'] = 'public, max-age=0, must-revalidate'  # No cache for HTML
            
            self.s3.upload_file(
                str(local_path),
                self.bucket_name,
                s3_key,
                ExtraArgs=extra_args
            )
            
            print(f"📤 {s3_key}")
            
        except Exception as e:
            print(f"❌ Error uploading {local_path}: {e}")
    
    def upload_backend_content(self):
        """Upload backend content (audio, video, etc.)"""
        print("🎵 Uploading backend content...")
        
        content_dirs = {
            'audio_output': 'audio',
            'video_output': 'video',
            'podcast_output': 'podcast',
            'interview_output': 'interview',
            'output': 'generated'
        }
        
        total_uploaded = 0
        
        for local_dir, remote_prefix in content_dirs.items():
            local_path = Path(local_dir)
            if local_path.exists():
                print(f"📁 Uploading {local_dir}...")
                for file_path in local_path.rglob("*"):
                    if file_path.is_file():
                        relative_path = file_path.relative_to(local_path)
                        s3_key = f"{remote_prefix}/{relative_path}".replace("\\", "/")
                        self.upload_file(file_path, s3_key)
                        total_uploaded += 1
        
        print(f"✅ Uploaded {total_uploaded} backend content files")
        return total_uploaded > 0
    
    def create_deployment_manifest(self):
        """Create a deployment manifest"""
        manifest = {
            "platform": "AI Video Generator Platform",
            "deployment_date": datetime.now().isoformat(),
            "bucket": self.bucket_name,
            "endpoint": self.endpoint,
            "website_url": f"https://{self.bucket_name}.s3-website.{self.region}.wasabisys.com",
            "api_base_url": f"{self.endpoint}/{self.bucket_name}",
            "features": {
                "frontend_spa": True,
                "static_hosting": True,
                "api_content": True,
                "cdn_ready": True
            },
            "deployment_info": {
                "frontend_built": True,
                "backend_content": True,
                "total_files": "calculated_during_deployment"
            }
        }
        
        # Save manifest locally
        with open("deployment_manifest.json", "w") as f:
            json.dump(manifest, f, indent=2)
        
        # Upload manifest to Wasabi
        self.upload_file("deployment_manifest.json", "deployment_manifest.json")
        
        print(f"📄 Created deployment manifest")
        return manifest
    
    def deploy_all(self):
        """Deploy everything to Wasabi"""
        print("🚀 Starting full deployment to Wasabi...")
        print("=" * 50)
        
        # Create bucket if needed
        if not self.create_bucket_if_not_exists():
            return False
        
        # Build and upload frontend
        if self.build_frontend():
            if not self.upload_frontend():
                print("⚠️  Frontend upload failed, continuing with backend...")
        else:
            print("⚠️  Frontend build failed, continuing with backend...")
        
        # Upload backend content
        self.upload_backend_content()
        
        # Create deployment manifest
        manifest = self.create_deployment_manifest()
        
        print("=" * 50)
        print("🎉 Deployment completed!")
        print(f"🌐 Website: {manifest['website_url']}")
        print(f"📡 API Base: {manifest['api_base_url']}")
        print(f"💾 Bucket: {self.bucket_name}")
        
        return True

def main():
    """Main deployment function"""
    print("🚀 AI Video Generator - Wasabi Deployment")
    print("=" * 50)
    
    deployer = WasabiFrontendDeployer()
    
    try:
        success = deployer.deploy_all()
        if success:
            print("\n✅ Deployment successful!")
            exit(0)
        else:
            print("\n❌ Deployment failed!")
            exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Deployment cancelled by user")
        exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
