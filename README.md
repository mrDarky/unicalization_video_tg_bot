# Video Unicalization - Bot & Desktop Application

A powerful video processing and unicalization tool that runs as:
- **Telegram Bot** - Remote video processing via Telegram
- **Desktop Application** - Standalone GUI app for Windows, macOS, and Linux
- **Admin Panel** - Web-based management interface

## Features

### Desktop Application (NEW! 🎉)
Cross-platform GUI application with:
- **Standalone executable** - No Python installation required
- **All dependencies included** - Ready to run out of the box
- **User-friendly interface** - Built with Kivy framework
- **Single Video Processing** - Apply modifications to one video
- **Two Video Merging** - Combine videos in different layouts
- **Real-time progress** - Visual feedback during processing
- **File browser** - Easy video selection

### Telegram Bot
- **Mode 1: Single Video Processing**
  - Change playback speed
  - Scale/resize video
  - Apply filters (hue, brightness, contrast, saturation, blur, sharpen, grayscale, sepia, negative, noise)
  - Crop video
  - Rotate video (90°, 180°, 270°)
  - Add text overlay
  - Trim/cut video

- **Mode 2: Two Video Processing**
  - Process two videos separately
  - Merge videos in different layouts:
    - Horizontal (side by side)
    - Vertical (top to bottom)
    - Sequential (one after another)

- **User Features**
  - User statistics
  - Balance management
  - Referral system
  - Transaction history

### Admin Panel
Modern Bootstrap 5-based admin interface with:
- **Dashboard** - Overview statistics
- **Users Management** - View, edit, delete users
- **Videos Management** - Monitor video processing
- **Deposits Management** - Handle deposits
- **Withdrawals Management** - Process withdrawals
- **Settings Management** - Configure bot settings
- **Statistics** - Comprehensive analytics

## Technology Stack

- **Python 3.9+**
- **Kivy 2.3** - Cross-platform UI framework
- **aiogram 3.3** - Telegram Bot framework
- **FastAPI** - Admin panel backend
- **SQLite** - Database with async support (aiosqlite)
- **SQLAlchemy 2.0** - ORM
- **FFmpeg** - Video processing
- **PyInstaller** - Application packaging
- **Bootstrap 5** - Frontend UI
- **Jinja2** - Template engine

## Quick Start

### Desktop Application (Recommended for End Users)

The easiest way to use the video processing features without any setup:

1. **Download** the pre-built executable for your platform:
   - Windows: `VideoUnicalization.exe`
   - macOS: `VideoUnicalization.app`
   - Linux: `VideoUnicalization-x86_64.AppImage`

2. **Install FFmpeg** (one-time setup):
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt-get install ffmpeg` (Ubuntu/Debian)

3. **Run the application**:
   ```bash
   # Windows: Double-click VideoUnicalization.exe
   # macOS: Double-click VideoUnicalization.app
   # Linux:
   chmod +x VideoUnicalization-x86_64.AppImage
   ./VideoUnicalization-x86_64.AppImage --mode desktop
   ```

4. **Start processing videos!** 🎬

See [BUILD.md](BUILD.md) for building from source.

## Installation (For Developers)

### Prerequisites
- Python 3.9 or higher
- FFmpeg installed on your system
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))

### Setup

1. Clone the repository:
```bash
git clone https://github.com/mrDarky/unicalization_video_tg_bot.git
cd unicalization_video_tg_bot
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install FFmpeg (if not already installed):

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

5. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` file with your settings:
```env
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_IDS=123456789,987654321
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password
SECRET_KEY=your_secret_key_here
```

6. Start the services:

**Option 1: Desktop Mode (GUI Application)**
```bash
python main.py --mode desktop
```

**Option 2: Bot Mode (Telegram Bot)**
```bash
python main.py --mode bot
```

**Option 3: API Mode (Admin Panel)**
```bash
python main.py --mode api
```

**Option 4: Use the startup script (runs both bot and API)**
```bash
./start.sh
```

Or start services manually:
```bash
# Terminal 1 - Start API server
python api_main.py

# Terminal 2 - Start Telegram bot
python bot_main.py
```

## Usage

### Desktop Application

1. Launch the application:
   ```bash
   python main.py --mode desktop
   # Or use the standalone executable
   ```

2. Select processing mode:
   - **Single Video** - Process one video with modifications
   - **Merge Two Videos** - Combine two videos

3. Choose your video file(s) using the file browser

4. Select modifications:
   - Speed: 0.5x to 2.0x
   - Scale: Various resolutions
   - Filters: Hue, brightness, contrast, blur, etc.
   - Rotation: 90°, 180°, 270°
   - Text overlay: Add custom text

5. Click "Process Video" and wait for completion

6. Find your processed video in the output directory!

### Telegram Bot
1. Start the bot: `/start`
2. Choose processing mode:
   - **🎬 Process 1 Video** - Single video unicalization
   - **🎥 Process 2 Videos** - Merge two videos
3. Upload your video(s)
4. Select modifications
5. Get your processed video!

### Admin Panel
1. Open browser: `http://localhost:8000/admin`
2. Navigate through different sections
3. Manage users, videos, deposits, withdrawals, and settings
4. Monitor statistics and activity

## Project Structure

```
unicalization_video_tg_bot/
├── bot/                        # Telegram bot
│   ├── handlers/              # Message and callback handlers
│   │   ├── basic.py           # Basic commands
│   │   ├── video_processing.py # Mode 1 processing
│   │   └── mode2.py           # Mode 2 processing
│   ├── keyboards/             # Keyboard layouts
│   └── states.py              # FSM states
├── api/                       # FastAPI admin panel
│   ├── routes/                # API endpoints
│   │   ├── users.py
│   │   ├── videos.py
│   │   ├── deposits.py
│   │   ├── withdrawals.py
│   │   ├── settings.py
│   │   └── statistics.py
│   └── templates/             # HTML templates
├── database/                  # Database layer
│   ├── models.py              # SQLAlchemy models
│   ├── database.py            # Database connection
│   └── crud.py                # CRUD operations
├── utils/                     # Utilities
│   └── video_processing.py    # Video processing functions
├── static/                    # Static files (CSS, JS)
├── config.py                  # Configuration
├── main.py                    # Main launcher (NEW!)
├── desktop_app.py             # Desktop GUI (NEW!)
├── bot_main.py                # Bot entry point
├── api_main.py                # API entry point
├── start.sh                   # Startup script
├── requirements.txt           # Python dependencies
├── VideoUnicalization.spec    # PyInstaller spec (NEW!)
├── build_windows.bat          # Windows build script (NEW!)
├── build_macos.sh             # macOS build script (NEW!)
├── build_linux.sh             # Linux build script (NEW!)
├── BUILD.md                   # Build documentation (NEW!)
└── README.md                  # This file
```

## Building Standalone Applications

To create standalone executables that include all dependencies:

### Windows
```cmd
build_windows.bat
```
Creates: `dist\VideoUnicalization\VideoUnicalization.exe`

### macOS
```bash
./build_macos.sh
```
Creates: `dist/VideoUnicalization.app`

### Linux
```bash
./build_linux.sh
```
Creates: `VideoUnicalization-x86_64.AppImage`

**See [BUILD.md](BUILD.md) for detailed build instructions and distribution guide.**

## API Documentation

Once the API server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

### Adding New Video Filters
Add new filters in `utils/video_processing.py`:
```python
async def apply_custom_filter(input_path: str, output_path: str) -> bool:
    # Your filter implementation
    pass
```

### Adding New Bot Handlers
Create handlers in `bot/handlers/` and register them in `bot_main.py`

### Adding New API Endpoints
Create routes in `api/routes/` and include them in `api_main.py`

## Configuration

Key configuration options in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `BOT_TOKEN` | Telegram Bot Token | Required |
| `ADMIN_IDS` | Admin user IDs (comma-separated) | - |
| `API_HOST` | API server host | 0.0.0.0 |
| `API_PORT` | API server port | 8000 |
| `ADMIN_USERNAME` | Admin panel username | admin |
| `ADMIN_PASSWORD` | Admin panel password | admin123 |
| `MAX_VIDEO_SIZE_MB` | Max video size | 100 |
| `DATABASE_URL` | Database connection string | sqlite:///./bot_database.db |

## Troubleshooting

### FFmpeg not found
Make sure FFmpeg is installed and in your system PATH.

### Database errors
Delete `bot_database.db` and restart to create a fresh database.

### Bot not responding
Check that your `BOT_TOKEN` is correct in the `.env` file.

### Video processing fails
Ensure FFmpeg is properly installed and videos are in supported formats.

## Future Enhancements

- [ ] Payment gateway integration
- [ ] More video effects and filters
- [ ] Batch video processing
- [ ] Video templates
- [ ] Advanced merging options
- [ ] Cloud storage integration
- [ ] Multi-language support
- [ ] Mobile-responsive admin panel improvements

## License

MIT License

## Support

For issues and questions:
- Create an issue on GitHub
- Contact: @YourSupportChannel

## Credits

Developed with ❤️ using Python, aiogram, FastAPI, and Bootstrap 5