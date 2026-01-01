#!/bin/bash
# Build script for macOS .app
# This script creates a standalone macOS application bundle with all dependencies included

set -e  # Exit on error

echo "========================================"
echo "Video Unicalization - macOS Build"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9+ from https://www.python.org/"
    exit 1
fi

echo "[1/6] Creating virtual environment..."
if [ ! -d "build_env" ]; then
    python3 -m venv build_env
fi

echo "[2/6] Activating virtual environment..."
source build_env/bin/activate

echo "[3/6] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[4/6] Building application with PyInstaller..."
pyinstaller --clean VideoUnicalization.spec

echo "[5/6] Checking FFmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    echo ""
    echo "WARNING: FFmpeg is not installed"
    echo "Please install FFmpeg using Homebrew:"
    echo "  brew install ffmpeg"
    echo ""
fi

echo "[6/6] Creating DMG (optional)..."
if command -v create-dmg &> /dev/null; then
    echo "Creating DMG installer..."
    create-dmg \
        --volname "Video Unicalization" \
        --window-pos 200 120 \
        --window-size 800 400 \
        --icon-size 100 \
        --icon "VideoUnicalization.app" 200 190 \
        --hide-extension "VideoUnicalization.app" \
        --app-drop-link 600 185 \
        "VideoUnicalization.dmg" \
        "dist/VideoUnicalization.app" || true
else
    echo "Skipping DMG creation (create-dmg not installed)"
    echo "Install with: brew install create-dmg"
fi

echo ""
echo "========================================"
echo "Build Complete!"
echo "========================================"
echo ""
echo "Application location: dist/VideoUnicalization.app"
echo ""
echo "To run the application:"
echo "  1. Navigate to dist/"
echo "  2. Copy VideoUnicalization.app to your Applications folder"
echo "  3. Create a .env file in ~/.videounicalization/ with your configuration"
echo "  4. Ensure FFmpeg is installed (brew install ffmpeg)"
echo "  5. Open VideoUnicalization.app"
echo ""
echo "Or run from terminal:"
echo "  ./dist/VideoUnicalization.app/Contents/MacOS/VideoUnicalization --mode desktop"
echo ""

deactivate

# Make the app executable
chmod +x dist/VideoUnicalization.app/Contents/MacOS/VideoUnicalization

echo "Done!"
