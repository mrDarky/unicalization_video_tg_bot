#!/usr/bin/env python3
"""
Installation Verification Script
Checks if all dependencies are properly installed for different modes
"""

import sys
import subprocess
from typing import Dict, List, Tuple

def check_python_version() -> bool:
    """Check if Python version is 3.9+"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (requires 3.9+)")
        return False

def check_ffmpeg() -> bool:
    """Check if FFmpeg is installed"""
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✓ {version_line}")
            return True
        else:
            print("✗ FFmpeg not working properly")
            return False
    except FileNotFoundError:
        print("✗ FFmpeg not found in PATH")
        return False
    except Exception as e:
        print(f"✗ Error checking FFmpeg: {e}")
        return False

def check_module(module_name: str, package_name: str = None) -> bool:
    """Check if a Python module can be imported"""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        print(f"✓ {package_name}")
        return True
    except ImportError:
        print(f"✗ {package_name}")
        return False

def main():
    print("=" * 60)
    print("Video Unicalization - Installation Verification")
    print("=" * 60)
    print()
    
    # Check Python version
    print("Checking Python version...")
    python_ok = check_python_version()
    print()
    
    # Check FFmpeg
    print("Checking FFmpeg...")
    ffmpeg_ok = check_ffmpeg()
    print()
    
    # Check core dependencies
    print("Checking core dependencies...")
    core_deps = [
        ('pydantic', 'pydantic'),
        ('pydantic_settings', 'pydantic-settings'),
        ('dotenv', 'python-dotenv'),
        ('ffmpeg', 'ffmpeg-python'),
    ]
    
    core_ok = all(check_module(mod, pkg) for mod, pkg in core_deps)
    print()
    
    # Check bot dependencies
    print("Checking bot mode dependencies...")
    bot_deps = [
        ('aiogram', 'aiogram'),
        ('aiosqlite', 'aiosqlite'),
        ('sqlalchemy', 'sqlalchemy'),
    ]
    
    bot_ok = all(check_module(mod, pkg) for mod, pkg in bot_deps)
    print()
    
    # Check desktop dependencies
    print("Checking desktop mode dependencies...")
    desktop_deps = [
        ('kivy', 'kivy'),
    ]
    
    desktop_ok = all(check_module(mod, pkg) for mod, pkg in desktop_deps)
    print()
    
    # Check API dependencies
    print("Checking API mode dependencies...")
    api_deps = [
        ('fastapi', 'fastapi'),
        ('uvicorn', 'uvicorn'),
        ('jinja2', 'jinja2'),
    ]
    
    api_ok = all(check_module(mod, pkg) for mod, pkg in api_deps)
    print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print()
    
    modes_available = []
    modes_unavailable = []
    
    if python_ok and core_ok and ffmpeg_ok:
        if desktop_ok:
            modes_available.append("Desktop Mode (GUI)")
        else:
            modes_unavailable.append("Desktop Mode (missing: kivy)")
        
        if bot_ok:
            modes_available.append("Bot Mode (Telegram)")
        else:
            modes_unavailable.append("Bot Mode (missing: aiogram, aiosqlite, sqlalchemy)")
        
        if api_ok:
            modes_available.append("API Mode (Admin Panel)")
        else:
            modes_unavailable.append("API Mode (missing: fastapi, uvicorn, jinja2)")
    else:
        print("⚠️  Core requirements not met:")
        if not python_ok:
            print("   - Python 3.9+ required")
        if not core_ok:
            print("   - Core Python packages missing")
        if not ffmpeg_ok:
            print("   - FFmpeg not installed or not in PATH")
        print()
    
    if modes_available:
        print("✓ Available modes:")
        for mode in modes_available:
            print(f"  - {mode}")
        print()
    
    if modes_unavailable:
        print("✗ Unavailable modes:")
        for mode in modes_unavailable:
            print(f"  - {mode}")
        print()
        print("To install all dependencies, run:")
        print("  pip install -r requirements.txt")
        print()
    
    # Installation instructions
    if not ffmpeg_ok:
        print("=" * 60)
        print("FFmpeg Installation Instructions")
        print("=" * 60)
        print()
        print("Windows:")
        print("  1. Download from https://ffmpeg.org/download.html")
        print("  2. Extract to C:\\ffmpeg")
        print("  3. Add C:\\ffmpeg\\bin to system PATH")
        print()
        print("macOS:")
        print("  brew install ffmpeg")
        print()
        print("Linux (Ubuntu/Debian):")
        print("  sudo apt-get update && sudo apt-get install ffmpeg")
        print()
    
    # Exit with appropriate code
    if python_ok and core_ok and ffmpeg_ok and (desktop_ok or bot_ok or api_ok):
        print("✅ System is ready! You can run the application.")
        print()
        print("Quick start:")
        if desktop_ok:
            print("  python main.py --mode desktop")
        elif bot_ok:
            print("  python main.py --mode bot")
        elif api_ok:
            print("  python main.py --mode api")
        return 0
    else:
        print("❌ System is not ready. Please install missing dependencies.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
