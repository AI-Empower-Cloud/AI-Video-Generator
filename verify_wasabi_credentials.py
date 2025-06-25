#!/usr/bin/env python3
"""
Wasabi Credentials Verification and Troubleshooting
"""

import os
from dotenv import load_dotenv

def verify_credentials():
    """Verify Wasabi credentials are properly configured"""
    print("🔍 Wasabi Credentials Verification")
    print("=" * 40)
    
    # Load environment
    load_dotenv('.env.wasabi')
    
    access_key = os.getenv('WASABI_ACCESS_KEY')
    secret_key = os.getenv('WASABI_SECRET_KEY')
    bucket_name = os.getenv('WASABI_BUCKET')
    
    print(f"📋 Configuration Check:")
    print(f"   Access Key: {'✅ Set' if access_key else '❌ Missing'}")
    print(f"   Secret Key: {'✅ Set' if secret_key else '❌ Missing'}")
    print(f"   Bucket Name: {'✅ Set' if bucket_name else '❌ Missing'}")
    
    if access_key:
        print(f"   Access Key Preview: {access_key[:8]}...{access_key[-4:]}")
    if secret_key:
        print(f"   Secret Key Preview: {secret_key[:8]}...{secret_key[-4:]}")
    if bucket_name:
        print(f"   Bucket Name: {bucket_name}")
    
    print(f"\n🔧 Troubleshooting Tips:")
    print(f"1. ⏰ New keys may take 5-10 minutes to activate")
    print(f"2. 🔄 Try refreshing your Wasabi console")
    print(f"3. 📋 Verify keys were copied exactly (no extra spaces)")
    print(f"4. 🔑 Ensure Root User access key was created")
    print(f"5. 🌐 Check if bucket already exists in Wasabi console")
    
    print(f"\n📝 If issues persist:")
    print(f"1. Go to Wasabi console → Access Keys")
    print(f"2. Delete current key and create new one")
    print(f"3. Copy both keys immediately")
    print(f"4. Run this script again")
    
    # Check file format
    with open('.env.wasabi', 'r') as f:
        content = f.read()
        
    print(f"\n📄 Config file preview:")
    lines = content.split('\n')
    for i, line in enumerate(lines[:10], 1):
        if 'ACCESS_KEY' in line or 'SECRET_KEY' in line:
            # Mask sensitive data
            if '=' in line:
                key, value = line.split('=', 1)
                if value and not value.startswith('your-'):
                    line = f"{key}={value[:8]}...{value[-4:]}"
        print(f"   {i:2d}: {line}")

if __name__ == "__main__":
    verify_credentials()
