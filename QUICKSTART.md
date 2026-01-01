# Quick Start Guide

## Desktop Application (Easiest!)

### Step 1: Download
Download the pre-built application for your platform:
- **Windows**: `VideoUnicalization.exe`
- **macOS**: `VideoUnicalization.app`
- **Linux**: `VideoUnicalization-x86_64.AppImage`

### Step 2: Install FFmpeg

#### Windows
1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your system PATH

#### macOS
```bash
brew install ffmpeg
```

#### Linux
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch
sudo pacman -S ffmpeg
```

### Step 3: Configure (Optional)
Create a `.env` file next to the executable:
```env
MAX_VIDEO_SIZE_MB=100
TEMP_VIDEO_DIR=./temp_videos
PROCESSED_VIDEO_DIR=./processed_videos
```

### Step 4: Run!

#### Windows
Double-click `VideoUnicalization.exe` or run:
```cmd
VideoUnicalization.exe --mode desktop
```

#### macOS
Double-click `VideoUnicalization.app` or run:
```bash
open VideoUnicalization.app
```

#### Linux
```bash
chmod +x VideoUnicalization-x86_64.AppImage
./VideoUnicalization-x86_64.AppImage --mode desktop
```

### Step 5: Process Videos!
1. Select "Single Video" or "Merge Two Videos"
2. Click "Select Video" to choose your video file
3. Choose modifications (speed, filters, rotation, etc.)
4. Click "Process Video"
5. Wait for processing to complete
6. Find your video in the output directory!

---

## Development Setup (For Developers)

### Prerequisites
- Python 3.9+
- FFmpeg
- Git

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mrDarky/unicalization_video_tg_bot.git
   cd unicalization_video_tg_bot
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**:
   ```bash
   python check_installation.py
   ```

5. **Configure application**:
   ```bash
   cp .env.desktop .env
   # Or for full features:
   cp .env.example .env
   # Edit .env with your settings
   ```

### Running

#### Desktop Mode (GUI)
```bash
python main.py --mode desktop
```

#### Bot Mode (Telegram)
```bash
# Configure BOT_TOKEN in .env first
python main.py --mode bot
```

#### API Mode (Admin Panel)
```bash
python main.py --mode api
# Then open http://localhost:8000/admin
```

#### All Modes (Bot + API)
```bash
./start.sh
```

---

## Building Executables

### Windows
```cmd
build_windows.bat
```
Output: `dist\VideoUnicalization\VideoUnicalization.exe`

### macOS
```bash
./build_macos.sh
```
Output: `dist/VideoUnicalization.app`

### Linux
```bash
./build_linux.sh
```
Output: `VideoUnicalization-x86_64.AppImage`

See [BUILD.md](BUILD.md) for detailed build instructions.

---

## Troubleshooting

### FFmpeg not found
**Error**: "FFmpeg not found in PATH"

**Solution**:
- Make sure FFmpeg is installed
- Verify with: `ffmpeg -version`
- Add FFmpeg to your system PATH

### Application won't start
**Error**: Application crashes on startup

**Solution**:
- Check that `.env` file exists (or use defaults)
- Verify Python 3.9+ is installed
- Run: `python check_installation.py`

### Video processing fails
**Error**: "Error processing video"

**Solution**:
- Check FFmpeg is working: `ffmpeg -version`
- Ensure video file is not corrupted
- Try a smaller video file
- Check available disk space

### Permission denied (Linux/macOS)
**Error**: "Permission denied"

**Solution**:
```bash
chmod +x VideoUnicalization-x86_64.AppImage
# Or
chmod +x build_linux.sh
```

### macOS Gatekeeper blocks app
**Error**: "App can't be opened because it is from an unidentified developer"

**Solution**:
1. Right-click the app
2. Select "Open"
3. Click "Open" in the dialog
4. Or disable Gatekeeper: `sudo spctl --master-disable`

---

## Features

### Single Video Processing
- **Speed**: Change playback speed (0.5x - 2.0x)
- **Scale**: Resize video to different resolutions
- **Filters**: Apply visual effects:
  - Hue adjustment
  - Brightness/Contrast
  - Saturation
  - Blur/Sharpen
  - Grayscale/Sepia
  - Negative
  - Noise
- **Rotate**: 90°, 180°, 270°
- **Text**: Add custom text overlay

### Two Video Merging
- **Horizontal**: Place videos side by side
- **Vertical**: Stack videos top to bottom
- **Sequential**: Play videos one after another

---

## Support

- **Documentation**: See [README.md](README.md)
- **Build Guide**: See [BUILD.md](BUILD.md)
- **Issues**: [GitHub Issues](https://github.com/mrDarky/unicalization_video_tg_bot/issues)

---

## License

MIT License - See [LICENSE](LICENSE) file for details
