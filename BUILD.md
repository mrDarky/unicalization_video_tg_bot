# Building Desktop Applications

This document explains how to build standalone desktop applications for Windows, macOS, and Linux.

## Overview

The Video Unicalization tool can run in three modes:
- **Bot mode**: Telegram bot for remote video processing
- **Desktop mode**: Standalone GUI application using Kivy
- **API mode**: Web-based admin panel

This guide focuses on building the desktop application as a standalone executable.

## Prerequisites

### All Platforms
- Python 3.9 or higher
- FFmpeg installed and in system PATH
- Git (for cloning the repository)

### Platform-Specific Requirements

#### Windows
- Windows 7 or later
- Visual C++ Redistributable (usually included with Python)

#### macOS
- macOS 10.13 (High Sierra) or later
- Xcode Command Line Tools: `xcode-select --install`
- Homebrew (recommended): `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

#### Linux
- Ubuntu 18.04+ / Debian 10+ / Fedora 30+ or equivalent
- Build essentials: `sudo apt-get install build-essential` (Ubuntu/Debian)

## Building Instructions

### Windows (.exe)

1. Open Command Prompt or PowerShell in the project directory

2. Run the build script:
   ```cmd
   build_windows.bat
   ```

3. The executable will be created in `dist\VideoUnicalization\`

4. To distribute:
   - Copy the entire `dist\VideoUnicalization\` folder
   - Include a `.env` file with configuration (see Configuration section)
   - Ensure FFmpeg is available (bundle it or instruct users to install)

**File size**: Approximately 150-300 MB (includes all Python dependencies)

### macOS (.app)

1. Open Terminal in the project directory

2. Run the build script:
   ```bash
   ./build_macos.sh
   ```

3. The application bundle will be created in `dist/VideoUnicalization.app`

4. Optional: Create a DMG installer (requires `create-dmg`):
   ```bash
   brew install create-dmg
   ./build_macos.sh
   ```

5. To distribute:
   - Copy `VideoUnicalization.app` to Applications folder
   - Or distribute the DMG file if created
   - Include instructions for FFmpeg installation: `brew install ffmpeg`

**Note**: macOS may require notarization for distribution outside the App Store. See [Apple's documentation](https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution).

**File size**: Approximately 150-300 MB

### Linux (AppImage)

1. Open Terminal in the project directory

2. Run the build script:
   ```bash
   ./build_linux.sh
   ```

3. The AppImage will be created as `VideoUnicalization-x86_64.AppImage`

4. To run:
   ```bash
   chmod +x VideoUnicalization-x86_64.AppImage
   ./VideoUnicalization-x86_64.AppImage --mode desktop
   ```

5. To distribute:
   - Share the single AppImage file
   - Include instructions for FFmpeg installation

**File size**: Approximately 150-300 MB

**Alternative**: If AppImageTool is not available, you can distribute the `VideoUnicalization.AppDir` folder and users can run `./AppRun --mode desktop`

## Configuration

### Creating a Configuration File

Before running the application, create a `.env` file in the same directory as the executable:

```env
# For Desktop Mode (optional, only if you want to use bot features)
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_IDS=123456789

# Video Processing Settings
MAX_VIDEO_SIZE_MB=100
TEMP_VIDEO_DIR=./temp_videos
PROCESSED_VIDEO_DIR=./processed_videos

# API Settings (if using API mode)
API_HOST=0.0.0.0
API_PORT=8000
ADMIN_USERNAME=admin
ADMIN_PASSWORD=change_this_password
```

**For desktop-only usage**, you can use a minimal `.env`:
```env
MAX_VIDEO_SIZE_MB=100
TEMP_VIDEO_DIR=./temp_videos
PROCESSED_VIDEO_DIR=./processed_videos
```

### Configuration Locations

- **Windows**: Place `.env` next to `VideoUnicalization.exe`
- **macOS**: Place `.env` next to the `.app` bundle or in `~/.videounicalization/`
- **Linux**: Place `.env` next to the AppImage or in `~/.videounicalization/`

## Running the Application

### Desktop Mode (GUI)

This is the default mode and provides a graphical user interface.

**Windows**:
```cmd
VideoUnicalization.exe --mode desktop
```
Or simply double-click `VideoUnicalization.exe`

**macOS**:
```bash
./VideoUnicalization.app/Contents/MacOS/VideoUnicalization --mode desktop
```
Or double-click `VideoUnicalization.app` in Finder

**Linux**:
```bash
./VideoUnicalization-x86_64.AppImage --mode desktop
```

### Bot Mode

Runs as a Telegram bot (requires BOT_TOKEN in .env):

**Windows**:
```cmd
VideoUnicalization.exe --mode bot
```

**macOS/Linux**:
```bash
./VideoUnicalization --mode bot
```

### API Mode

Runs the web-based admin panel:

**Windows**:
```cmd
VideoUnicalization.exe --mode api
```

**macOS/Linux**:
```bash
./VideoUnicalization --mode api
```

## Features in Desktop Mode

The desktop application provides:

1. **Single Video Processing**
   - Change playback speed
   - Resize/scale video
   - Apply filters (hue, brightness, contrast, etc.)
   - Rotate video
   - Add text overlay
   - And more!

2. **Two Video Merging**
   - Merge videos horizontally (side by side)
   - Merge videos vertically (top to bottom)
   - Concatenate videos sequentially

3. **User-Friendly Interface**
   - File browser for easy video selection
   - Real-time progress indicators
   - Preview of selected modifications
   - Cross-platform native look and feel

## FFmpeg Installation

FFmpeg is required for video processing. Install it before using the application:

### Windows
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to system PATH

**Or bundle with your application**:
Copy `ffmpeg.exe` to the same directory as `VideoUnicalization.exe`

### macOS
```bash
brew install ffmpeg
```

### Linux

**Ubuntu/Debian**:
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Fedora**:
```bash
sudo dnf install ffmpeg
```

**Arch Linux**:
```bash
sudo pacman -S ffmpeg
```

## Troubleshooting

### "FFmpeg not found"
- Make sure FFmpeg is installed and in your system PATH
- On Windows, try placing `ffmpeg.exe` next to the executable
- Test FFmpeg: `ffmpeg -version`

### Application won't start
- Check that `.env` file is present and properly formatted
- Ensure you have write permissions for `TEMP_VIDEO_DIR` and `PROCESSED_VIDEO_DIR`
- On macOS, if blocked by Gatekeeper: Right-click app → Open → Open anyway

### "Module not found" errors
- Ensure you built with all dependencies: `pip install -r requirements.txt`
- Try rebuilding with `--clean` flag

### Video processing fails
- Check FFmpeg installation: `ffmpeg -version`
- Ensure input video file is not corrupted
- Check available disk space
- Try with a smaller video file first

### Large file size
The standalone executables are large because they include:
- Python interpreter
- All Python packages (Kivy, FFmpeg bindings, etc.)
- Required system libraries

To reduce size:
- Use UPX compression (enabled by default)
- Remove unused features before building
- Consider distributing as a Python package instead

## Advanced Build Options

### Custom Icons

To add custom icons, edit `VideoUnicalization.spec`:

```python
exe = EXE(
    ...
    icon='path/to/your/icon.ico',  # Windows
    ...
)

# For macOS
app = BUNDLE(
    ...
    icon='path/to/your/icon.icns',  # macOS
    ...
)
```

### Windowed Mode (No Console)

To hide the console window on Windows, edit `VideoUnicalization.spec`:

```python
exe = EXE(
    ...
    console=False,  # Change from True to False
    ...
)
```

### Debug Build

For debugging, create a debug build:

```bash
pyinstaller --debug all VideoUnicalization.spec
```

### One-File Mode

To create a single executable file (slower startup):

Edit `VideoUnicalization.spec`:

```python
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,    # Add these
    a.zipfiles,    # Add these
    a.datas,       # Add these
    [],
    name='VideoUnicalization',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    one_file=True,  # Add this
)
```

Then remove the `COLLECT` section.

## Distribution Checklist

Before distributing your application:

- [ ] Test on a clean system without Python installed
- [ ] Include README with FFmpeg installation instructions
- [ ] Provide sample `.env` file (`.env.example`)
- [ ] Test all video processing features
- [ ] Verify file paths work correctly
- [ ] Check antivirus doesn't flag the executable
- [ ] Include license information
- [ ] Provide support/contact information

## Size Optimization Tips

1. **Remove unused packages**: Before building, uninstall packages you don't need
2. **Use virtual environment**: Build in a clean venv with only required packages
3. **Exclude development dependencies**: Remove testing/linting tools
4. **Use UPX compression**: Already enabled in spec file
5. **Exclude unused Kivy backends**: Configure Kivy to only include needed modules

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: [Repository Issues](https://github.com/mrDarky/unicalization_video_tg_bot/issues)
- Documentation: See main README.md

## Credits

Built with:
- Python 3.9+
- Kivy (UI framework)
- PyInstaller (packaging)
- FFmpeg (video processing)
