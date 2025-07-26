#!/usr/bin/env python3
"""
Cloud Storage Module
===================

Handles cloud storage operations with Wasabi/S3 compatible services.
"""

import asyncio
import os
import logging
import tempfile
import uuid
from typing import Optional, List, Dict, Any, Tuple
from pathlib import Path
import json
from datetime import datetime, timedelta
import hashlib

logger = logging.getLogger(__name__)

class CloudStorage:
    """Cloud storage interface for Wasabi/S3 compatible services"""
    
    def __init__(
        self,
        endpoint_url: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        bucket_name: Optional[str] = None,
        region: str = "us-east-1"
    ):
        self.endpoint_url = endpoint_url or os.getenv("WASABI_ENDPOINT_URL")
        self.access_key = access_key or os.getenv("WASABI_ACCESS_KEY")
        self.secret_key = secret_key or os.getenv("WASABI_SECRET_KEY")
        self.bucket_name = bucket_name or os.getenv("WASABI_BUCKET_NAME")
        self.region = region
        
        self.boto3_available = self._check_boto3()
        self.client = None
        
        # Initialize the client
        self._init_client()
        
        logger.info(f"Cloud Storage initialized - Boto3: {self.boto3_available}, Bucket: {self.bucket_name}")
    
    def _check_boto3(self) -> bool:
        """Check if boto3 is available"""
        try:
            import boto3
            return True
        except ImportError:
            return False
    
    def _init_client(self):
        """Initialize S3/Wasabi client"""
        try:
            if not self.boto3_available:
                logger.warning("Boto3 not available for cloud storage")
                return
            
            if not all([self.endpoint_url, self.access_key, self.secret_key, self.bucket_name]):
                logger.warning("Cloud storage credentials not fully configured")
                return
            
            import boto3
            from botocore.config import Config
            
            self.client = boto3.client(
                's3',
                endpoint_url=self.endpoint_url,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region,
                config=Config(
                    retries={'max_attempts': 3},
                    max_pool_connections=50
                )
            )
            
            logger.info("Cloud storage client initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize cloud storage client: {e}")
            self.client = None
    
    async def upload_file(
        self,
        local_path: str,
        remote_key: Optional[str] = None,
        content_type: Optional[str] = None,
        metadata: Optional[Dict] = None,
        public_read: bool = False
    ) -> str:
        """Upload file to cloud storage"""
        
        if not self.client:
            raise RuntimeError("Cloud storage client not available")
        
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Local file not found: {local_path}")
        
        if not remote_key:
            filename = os.path.basename(local_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            remote_key = f"uploads/{timestamp}_{filename}"
        
        logger.info(f"Uploading file to cloud: {local_path} -> {remote_key}")
        
        try:
            # Prepare upload parameters
            extra_args = {}
            
            if content_type:
                extra_args['ContentType'] = content_type
            else:
                extra_args['ContentType'] = self._guess_content_type(local_path)
            
            if metadata:
                extra_args['Metadata'] = metadata
            
            if public_read:
                extra_args['ACL'] = 'public-read'
            
            # Upload file
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.upload_file(
                    local_path,
                    self.bucket_name,
                    remote_key,
                    ExtraArgs=extra_args
                )
            )
            
            # Generate public URL
            if public_read:
                url = f"{self.endpoint_url}/{self.bucket_name}/{remote_key}"
            else:
                url = await self.generate_presigned_url(remote_key)
            
            logger.info(f"File uploaded successfully: {url}")
            return url
            
        except Exception as e:
            logger.error(f"File upload failed: {e}")
            raise
    
    async def download_file(
        self,
        remote_key: str,
        local_path: Optional[str] = None
    ) -> str:
        """Download file from cloud storage"""
        
        if not self.client:
            raise RuntimeError("Cloud storage client not available")
        
        if not local_path:
            filename = os.path.basename(remote_key)
            local_path = os.path.join(tempfile.gettempdir(), f"download_{uuid.uuid4().hex}_{filename}")
        
        logger.info(f"Downloading file from cloud: {remote_key} -> {local_path}")
        
        try:
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.download_file(
                    self.bucket_name,
                    remote_key,
                    local_path
                )
            )
            
            logger.info(f"File downloaded successfully: {local_path}")
            return local_path
            
        except Exception as e:
            logger.error(f"File download failed: {e}")
            raise
    
    async def delete_file(self, remote_key: str) -> bool:
        """Delete file from cloud storage"""
        
        if not self.client:
            raise RuntimeError("Cloud storage client not available")
        
        logger.info(f"Deleting file from cloud: {remote_key}")
        
        try:
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.delete_object(
                    Bucket=self.bucket_name,
                    Key=remote_key
                )
            )
            
            logger.info(f"File deleted successfully: {remote_key}")
            return True
            
        except Exception as e:
            logger.error(f"File deletion failed: {e}")
            raise
    
    async def list_files(
        self,
        prefix: Optional[str] = None,
        max_keys: int = 1000
    ) -> List[Dict]:
        """List files in cloud storage"""
        
        if not self.client:
            raise RuntimeError("Cloud storage client not available")
        
        logger.info(f"Listing files with prefix: {prefix}")
        
        try:
            kwargs = {
                'Bucket': self.bucket_name,
                'MaxKeys': max_keys
            }
            
            if prefix:
                kwargs['Prefix'] = prefix
            
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.list_objects_v2(**kwargs)
            )
            
            files = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    files.append({
                        'key': obj['Key'],
                        'size': obj['Size'],
                        'last_modified': obj['LastModified'],
                        'etag': obj['ETag'].strip('"')
                    })
            
            logger.info(f"Found {len(files)} files")
            return files
            
        except Exception as e:
            logger.error(f"File listing failed: {e}")
            raise
    
    async def generate_presigned_url(
        self,
        remote_key: str,
        expiration: int = 3600,
        method: str = 'get_object'
    ) -> str:
        """Generate presigned URL for file access"""
        
        if not self.client:
            raise RuntimeError("Cloud storage client not available")
        
        logger.info(f"Generating presigned URL for: {remote_key}")
        
        try:
            url = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.generate_presigned_url(
                    method,
                    Params={'Bucket': self.bucket_name, 'Key': remote_key},
                    ExpiresIn=expiration
                )
            )
            
            logger.info(f"Presigned URL generated (expires in {expiration}s)")
            return url
            
        except Exception as e:
            logger.error(f"Presigned URL generation failed: {e}")
            raise
    
    async def file_exists(self, remote_key: str) -> bool:
        """Check if file exists in cloud storage"""
        
        if not self.client:
            raise RuntimeError("Cloud storage client not available")
        
        try:
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.head_object(
                    Bucket=self.bucket_name,
                    Key=remote_key
                )
            )
            return True
            
        except Exception:
            return False
    
    async def get_file_info(self, remote_key: str) -> Dict[str, Any]:
        """Get file information from cloud storage"""
        
        if not self.client:
            raise RuntimeError("Cloud storage client not available")
        
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.head_object(
                    Bucket=self.bucket_name,
                    Key=remote_key
                )
            )
            
            return {
                'key': remote_key,
                'size': response.get('ContentLength', 0),
                'last_modified': response.get('LastModified'),
                'content_type': response.get('ContentType'),
                'etag': response.get('ETag', '').strip('"'),
                'metadata': response.get('Metadata', {})
            }
            
        except Exception as e:
            logger.error(f"Failed to get file info: {e}")
            raise
    
    async def copy_file(
        self,
        source_key: str,
        dest_key: str,
        source_bucket: Optional[str] = None
    ) -> bool:
        """Copy file within cloud storage"""
        
        if not self.client:
            raise RuntimeError("Cloud storage client not available")
        
        source_bucket = source_bucket or self.bucket_name
        copy_source = {'Bucket': source_bucket, 'Key': source_key}
        
        logger.info(f"Copying file: {source_key} -> {dest_key}")
        
        try:
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.copy_object(
                    CopySource=copy_source,
                    Bucket=self.bucket_name,
                    Key=dest_key
                )
            )
            
            logger.info(f"File copied successfully: {dest_key}")
            return True
            
        except Exception as e:
            logger.error(f"File copy failed: {e}")
            raise
    
    async def upload_directory(
        self,
        local_dir: str,
        remote_prefix: str = "",
        exclude_patterns: Optional[List[str]] = None
    ) -> List[str]:
        """Upload entire directory to cloud storage"""
        
        if not os.path.isdir(local_dir):
            raise NotADirectoryError(f"Directory not found: {local_dir}")
        
        exclude_patterns = exclude_patterns or ['.git', '.DS_Store', '__pycache__']
        uploaded_urls = []
        
        logger.info(f"Uploading directory: {local_dir} -> {remote_prefix}")
        
        try:
            for root, dirs, files in os.walk(local_dir):
                # Filter out excluded directories
                dirs[:] = [d for d in dirs if not any(pattern in d for pattern in exclude_patterns)]
                
                for file in files:
                    # Skip excluded files
                    if any(pattern in file for pattern in exclude_patterns):
                        continue
                    
                    local_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_path, local_dir)
                    remote_key = os.path.join(remote_prefix, relative_path).replace('\\', '/')
                    
                    url = await self.upload_file(local_path, remote_key)
                    uploaded_urls.append(url)
            
            logger.info(f"Directory uploaded: {len(uploaded_urls)} files")
            return uploaded_urls
            
        except Exception as e:
            logger.error(f"Directory upload failed: {e}")
            raise
    
    def _guess_content_type(self, file_path: str) -> str:
        """Guess content type from file extension"""
        extension = os.path.splitext(file_path)[1].lower()
        
        content_types = {
            '.mp4': 'video/mp4',
            '.avi': 'video/x-msvideo',
            '.mov': 'video/quicktime',
            '.mkv': 'video/x-matroska',
            '.wav': 'audio/wav',
            '.mp3': 'audio/mpeg',
            '.aac': 'audio/aac',
            '.flac': 'audio/flac',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
            '.srt': 'text/plain',
            '.vtt': 'text/vtt',
            '.txt': 'text/plain',
            '.json': 'application/json',
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript'
        }
        
        return content_types.get(extension, 'application/octet-stream')
    
    def get_public_url(self, remote_key: str) -> str:
        """Get public URL for a file (if bucket allows public access)"""
        if self.endpoint_url and self.bucket_name:
            return f"{self.endpoint_url}/{self.bucket_name}/{remote_key}"
        else:
            raise ValueError("Endpoint URL or bucket name not configured")
    
    async def create_backup(self, files: List[str], backup_name: Optional[str] = None) -> str:
        """Create backup of multiple files"""
        
        if not backup_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}"
        
        backup_urls = []
        
        logger.info(f"Creating backup: {backup_name}")
        
        try:
            for file_path in files:
                if os.path.exists(file_path):
                    filename = os.path.basename(file_path)
                    remote_key = f"backups/{backup_name}/{filename}"
                    url = await self.upload_file(file_path, remote_key)
                    backup_urls.append(url)
            
            # Create backup manifest
            manifest = {
                'backup_name': backup_name,
                'created_at': datetime.now().isoformat(),
                'files': backup_urls,
                'total_files': len(backup_urls)
            }
            
            # Upload manifest
            manifest_path = os.path.join(tempfile.gettempdir(), f"{backup_name}_manifest.json")
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            manifest_url = await self.upload_file(
                manifest_path,
                f"backups/{backup_name}/manifest.json"
            )
            
            os.remove(manifest_path)
            
            logger.info(f"Backup created: {backup_name} ({len(backup_urls)} files)")
            return manifest_url
            
        except Exception as e:
            logger.error(f"Backup creation failed: {e}")
            raise

# Example usage
if __name__ == "__main__":
    async def test_cloud_storage():
        # Initialize with environment variables or provide directly
        storage = CloudStorage(
            endpoint_url="https://s3.wasabisys.com",
            access_key="YOUR_ACCESS_KEY",
            secret_key="YOUR_SECRET_KEY",
            bucket_name="your-bucket-name"
        )
        
        # Test file operations
        test_file = "test.txt"
        
        # Create test file
        with open(test_file, 'w') as f:
            f.write("Hello, Cloud Storage!")
        
        try:
            # Upload file
            url = await storage.upload_file(test_file, public_read=True)
            print(f"File uploaded: {url}")
            
            # List files
            files = await storage.list_files(prefix="uploads/")
            print(f"Found {len(files)} files")
            
            # Generate presigned URL
            presigned_url = await storage.generate_presigned_url("uploads/" + os.path.basename(test_file))
            print(f"Presigned URL: {presigned_url}")
            
        except Exception as e:
            print(f"Cloud storage test failed: {e}")
        finally:
            # Cleanup
            if os.path.exists(test_file):
                os.remove(test_file)
    
    asyncio.run(test_cloud_storage())
