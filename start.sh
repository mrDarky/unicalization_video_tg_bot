#!/bin/bash

# Start both bot and API server

echo "Starting Video Unicalization Bot..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please copy .env.example to .env and configure it."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "Warning: FFmpeg is not installed!"
    echo "Please install FFmpeg to process videos."
    echo "Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "macOS: brew install ffmpeg"
    echo ""
fi

# Start API server in background
echo "Starting API server..."
python api_main.py &
API_PID=$!

# Wait a bit for API to start
sleep 2

# Start bot
echo "Starting Telegram bot..."
python bot_main.py &
BOT_PID=$!

echo ""
echo "================================"
echo "Services started successfully!"
echo "================================"
echo "API Server: http://localhost:8000"
echo "Admin Panel: http://localhost:8000/admin"
echo "Bot is running..."
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for Ctrl+C
trap "kill $API_PID $BOT_PID; exit" INT
wait
