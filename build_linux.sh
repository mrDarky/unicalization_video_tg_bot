#!/bin/bash
# Build script for Linux AppImage
# This script creates a standalone Linux application with all dependencies included

set -e  # Exit on error

echo "========================================"
echo "Video Unicalization - Linux Build"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9+ using your package manager"
    exit 1
fi

echo "[1/7] Creating virtual environment..."
if [ ! -d "build_env" ]; then
    python3 -m venv build_env
fi

echo "[2/7] Activating virtual environment..."
source build_env/bin/activate

echo "[3/7] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[4/7] Building application with PyInstaller..."
pyinstaller --clean VideoUnicalization.spec

echo "[5/7] Checking FFmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    echo ""
    echo "WARNING: FFmpeg is not installed"
    echo "Please install FFmpeg:"
    echo "  Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "  Fedora: sudo dnf install ffmpeg"
    echo "  Arch: sudo pacman -S ffmpeg"
    echo ""
fi

echo "[6/7] Creating AppImage structure..."
APP_DIR="VideoUnicalization.AppDir"
rm -rf "$APP_DIR"
mkdir -p "$APP_DIR/usr/bin"
mkdir -p "$APP_DIR/usr/lib"
mkdir -p "$APP_DIR/usr/share/applications"
mkdir -p "$APP_DIR/usr/share/icons/hicolor/256x256/apps"

# Copy the application
cp -r dist/VideoUnicalization/* "$APP_DIR/usr/bin/"

# Create desktop entry
cat > "$APP_DIR/usr/share/applications/videounicalization.desktop" << EOF
[Desktop Entry]
Type=Application
Name=Video Unicalization
Comment=Video processing and unicalization tool
Exec=VideoUnicalization --mode desktop
Icon=videounicalization
Categories=AudioVideo;Video;
Terminal=false
EOF

# Create AppRun script
cat > "$APP_DIR/AppRun" << 'EOF'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH}"
cd "${HERE}/usr/bin"
exec "${HERE}/usr/bin/VideoUnicalization" "$@"
EOF

chmod +x "$APP_DIR/AppRun"

# Create a simple icon (placeholder)
cat > "$APP_DIR/videounicalization.desktop" << EOF
[Desktop Entry]
Type=Application
Name=Video Unicalization
Comment=Video processing and unicalization tool
Exec=VideoUnicalization
Icon=videounicalization
Categories=AudioVideo;Video;
Terminal=false
EOF

# Create a placeholder icon
cat > "$APP_DIR/.DirIcon" << EOF
# Placeholder icon
# Replace with actual icon file
EOF

echo "[7/7] Creating AppImage..."
if command -v appimagetool &> /dev/null; then
    appimagetool "$APP_DIR" VideoUnicalization-x86_64.AppImage
    chmod +x VideoUnicalization-x86_64.AppImage
    echo "AppImage created: VideoUnicalization-x86_64.AppImage"
else
    echo ""
    echo "WARNING: appimagetool is not installed"
    echo "Please install it from: https://github.com/AppImage/AppImageKit/releases"
    echo ""
    echo "Download appimagetool-x86_64.AppImage and run:"
    echo "  chmod +x appimagetool-x86_64.AppImage"
    echo "  ./appimagetool-x86_64.AppImage $APP_DIR VideoUnicalization-x86_64.AppImage"
    echo ""
    echo "Alternatively, you can run the application directly from:"
    echo "  $APP_DIR/AppRun"
fi

echo ""
echo "========================================"
echo "Build Complete!"
echo "========================================"
echo ""
echo "Application directory: $APP_DIR"
if [ -f "VideoUnicalization-x86_64.AppImage" ]; then
    echo "AppImage: VideoUnicalization-x86_64.AppImage"
fi
echo ""
echo "To run the application:"
if [ -f "VideoUnicalization-x86_64.AppImage" ]; then
    echo "  1. Make sure FFmpeg is installed"
    echo "  2. Create a .env file with your configuration"
    echo "  3. Run: ./VideoUnicalization-x86_64.AppImage --mode desktop"
else
    echo "  1. Make sure FFmpeg is installed"
    echo "  2. Create a .env file with your configuration"
    echo "  3. Run: ./$APP_DIR/AppRun --mode desktop"
fi
echo ""
echo "Or run from the dist directory:"
echo "  cd dist/VideoUnicalization && ./VideoUnicalization --mode desktop"
echo ""

deactivate

echo "Done!"
