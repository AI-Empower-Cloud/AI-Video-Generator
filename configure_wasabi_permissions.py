#!/usr/bin/env python3
"""
Wasabi Bucket Permissions & Tags Configuration
Configure proper permissions and tags for ai-video-generator-content bucket
"""

import boto3
import json
import os
from dotenv import load_dotenv

def configure_bucket_permissions_and_tags():
    """Configure Wasabi bucket with proper permissions and tags"""
    
    # Load environment variables
    load_dotenv('.env.wasabi')
    
    access_key = os.getenv('WASABI_ACCESS_KEY')
    secret_key = os.getenv('WASABI_SECRET_KEY')
    bucket_name = os.getenv('WASABI_BUCKET', 'ai-video-generator-content')
    endpoint = os.getenv('WASABI_ENDPOINT', 'https://s3.wasabisys.com')
    
    if not access_key or not secret_key:
        print("❌ Please configure your Wasabi credentials first!")
        print("Run: ./configure_wasabi_keys.sh")
        return False
    
    try:
        # Initialize S3 client for Wasabi
        s3 = boto3.client(
            's3',
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name='us-east-1'
        )
        
        print(f"🔧 Configuring bucket: {bucket_name}")
        
        # 1. Configure CORS for web access
        print("🌐 Setting up CORS for web access...")
        cors_configuration = {
            'CORSRules': [
                {
                    'AllowedHeaders': ['*'],
                    'AllowedMethods': ['GET', 'HEAD'],
                    'AllowedOrigins': ['*'],
                    'ExposeHeaders': ['ETag'],
                    'MaxAgeSeconds': 3000
                }
            ]
        }
        
        s3.put_bucket_cors(
            Bucket=bucket_name,
            CORSConfiguration=cors_configuration
        )
        print("✅ CORS configured for web access")
        
        # 2. Set bucket policy for public read access
        print("🔓 Setting public read access policy...")
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }
        
        s3.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps(bucket_policy)
        )
        print("✅ Public read access configured")
        
        # 3. Configure bucket tags
        print("🏷️  Setting bucket tags...")
        bucket_tags = {
            'TagSet': [
                {'Key': 'Project', 'Value': 'AI-Video-Generator'},
                {'Key': 'Platform', 'Value': 'EmpowerHub360'},
                {'Key': 'Environment', 'Value': 'Production'},
                {'Key': 'Purpose', 'Value': 'Educational-Content'},
                {'Key': 'Owner', 'Value': 'admin@empowerhub360.org'},
                {'Key': 'CostCenter', 'Value': 'AI-Tools'},
                {'Key': 'Backup', 'Value': 'Required'},
                {'Key': 'ContentType', 'Value': 'Audio-Video-Podcasts'},
                {'Key': 'AccessLevel', 'Value': 'Public'},
                {'Key': 'CreatedBy', 'Value': 'AI-Assistant'},
                {'Key': 'Version', 'Value': 'v1.0'},
                {'Key': 'LastUpdated', 'Value': '2025-06-25'}
            ]
        }
        
        s3.put_bucket_tagging(
            Bucket=bucket_name,
            Tagging=bucket_tags
        )
        print("✅ Bucket tags configured")
        
        # 4. Enable versioning (optional but recommended)
        print("📝 Enabling bucket versioning...")
        s3.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={'Status': 'Enabled'}
        )
        print("✅ Bucket versioning enabled")
        
        # 5. Test configuration
        print("\n🧪 Testing bucket configuration...")
        
        # Test CORS
        try:
            cors = s3.get_bucket_cors(Bucket=bucket_name)
            print("✅ CORS configuration verified")
        except Exception as e:
            print(f"⚠️  CORS test failed: {e}")
        
        # Test policy
        try:
            policy = s3.get_bucket_policy(Bucket=bucket_name)
            print("✅ Bucket policy verified")
        except Exception as e:
            print(f"⚠️  Policy test failed: {e}")
        
        # Test tags
        try:
            tags = s3.get_bucket_tagging(Bucket=bucket_name)
            print("✅ Bucket tags verified")
        except Exception as e:
            print(f"⚠️  Tags test failed: {e}")
        
        print(f"\n🎉 Bucket {bucket_name} configured successfully!")
        print("📋 Configuration summary:")
        print("   ✅ CORS enabled for web access")
        print("   ✅ Public read access policy set")
        print("   ✅ Comprehensive tags applied")
        print("   ✅ Versioning enabled")
        print("   ✅ Ready for content deployment")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Wasabi Bucket Configuration Tool")
    print("=" * 40)
    configure_bucket_permissions_and_tags()
