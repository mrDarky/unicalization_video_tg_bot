#!/usr/bin/env python3
"""
Verification script to check if the bot is properly configured.
Run this after installation to verify everything is set up correctly.
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python version {version.major}.{version.minor} is too old. Need 3.9+")
        return False

def check_env_file():
    """Check if .env file exists"""
    if Path(".env").exists():
        print("✓ .env file exists")
        return True
    else:
        print("✗ .env file not found. Copy .env.example to .env")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    required = [
        'aiogram',
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'aiosqlite',
        'python-dotenv',
        'jinja2',
        'ffmpeg-python',
        'pydantic_settings'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package} installed")
        except ImportError:
            print(f"✗ {package} not installed")
            missing.append(package)
    
    return len(missing) == 0

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    import subprocess
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✓ FFmpeg installed: {version_line}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("✗ FFmpeg not found. Please install FFmpeg")
    print("  Ubuntu/Debian: sudo apt-get install ffmpeg")
    print("  macOS: brew install ffmpeg")
    return False

def check_directories():
    """Check if required directories exist"""
    dirs = ['temp_videos', 'processed_videos', 'static', 'api/templates', 'bot/handlers']
    all_exist = True
    for dir_path in dirs:
        if Path(dir_path).exists():
            print(f"✓ Directory exists: {dir_path}")
        else:
            print(f"✗ Directory missing: {dir_path}")
            all_exist = False
    return all_exist

def check_bot_token():
    """Check if bot token is configured"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        token = os.getenv('BOT_TOKEN', '')
        if token and token != 'your_bot_token_here':
            print("✓ Bot token is configured")
            return True
        else:
            print("✗ Bot token not configured in .env")
            return False
    except Exception as e:
        print(f"✗ Error checking bot token: {e}")
        return False

def main():
    """Run all checks"""
    print("=" * 60)
    print("Video Unicalization Bot - Installation Verification")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        (".env File", check_env_file),
        ("Python Dependencies", check_dependencies),
        ("FFmpeg", check_ffmpeg),
        ("Directories", check_directories),
        ("Bot Token", check_bot_token),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        results.append(check_func())
    
    print("\n" + "=" * 60)
    if all(results):
        print("✓ All checks passed! You can start the bot with ./start.sh")
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        print("\nQuick fix commands:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Copy .env: cp .env.example .env")
        print("  3. Edit .env with your bot token and settings")
        print("  4. Install FFmpeg (see README.md)")
    print("=" * 60)

if __name__ == "__main__":
    main()
