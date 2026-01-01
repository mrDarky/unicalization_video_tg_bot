@echo off
REM Build script for Windows .exe
REM This script creates a standalone Windows executable with all dependencies included

echo ========================================
echo Video Unicalization - Windows Build
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
if not exist "build_env" (
    python -m venv build_env
)

echo [2/5] Activating virtual environment...
call build_env\Scripts\activate.bat

echo [3/5] Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo [4/5] Building executable with PyInstaller...
pyinstaller --clean VideoUnicalization.spec

echo [5/5] Checking FFmpeg...
where ffmpeg >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: FFmpeg is not installed or not in PATH
    echo Please download FFmpeg from https://ffmpeg.org/download.html
    echo and add it to your system PATH, or place ffmpeg.exe in the same directory as the executable.
    echo.
)

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Executable location: dist\VideoUnicalization\VideoUnicalization.exe
echo.
echo To run the application:
echo   1. Navigate to dist\VideoUnicalization\
echo   2. Create a .env file with your configuration (see .env.example)
echo   3. Ensure FFmpeg is available in your PATH
echo   4. Run VideoUnicalization.exe --mode desktop
echo.
echo Deactivating virtual environment...
call build_env\Scripts\deactivate

pause
