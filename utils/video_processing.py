import ffmpeg
import os
import random
import string
from typing import Dict, Optional, List, Tuple
from config import settings
import asyncio


def generate_filename(extension: str = "mp4") -> str:
    """Generate random filename"""
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    return f"{random_string}.{extension}"


async def get_video_info(video_path: str) -> Dict:
    """Get video information"""
    try:
        probe = ffmpeg.probe(video_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
        
        info = {
            'duration': float(probe['format']['duration']),
            'size': int(probe['format']['size']),
            'width': int(video_stream['width']) if video_stream else 0,
            'height': int(video_stream['height']) if video_stream else 0,
            'has_audio': audio_stream is not None
        }
        return info
    except Exception as e:
        print(f"Error getting video info: {e}")
        return {}


async def change_video_speed(input_path: str, output_path: str, speed: float = 1.5) -> bool:
    """Change video playback speed"""
    try:
        video_speed = 1.0 / speed
        audio_speed = speed
        
        stream = ffmpeg.input(input_path)
        video = stream.video.filter('setpts', f'{video_speed}*PTS')
        audio = stream.audio.filter('atempo', audio_speed)
        
        output = ffmpeg.output(video, audio, output_path, vcodec='libx264', acodec='aac')
        await asyncio.get_event_loop().run_in_executor(None, output.run)
        return True
    except Exception as e:
        print(f"Error changing video speed: {e}")
        return False


async def scale_video(input_path: str, output_path: str, width: int = 1280, height: int = 720) -> bool:
    """Scale video to specified dimensions"""
    try:
        stream = ffmpeg.input(input_path)
        stream = ffmpeg.filter(stream, 'scale', width, height)
        output = ffmpeg.output(stream, output_path, vcodec='libx264', acodec='aac')
        await asyncio.get_event_loop().run_in_executor(None, output.run)
        return True
    except Exception as e:
        print(f"Error scaling video: {e}")
        return False


async def apply_filter(input_path: str, output_path: str, filter_name: str = 'hue') -> bool:
    """Apply video filter"""
    try:
        stream = ffmpeg.input(input_path)
        
        filters = {
            'hue': 'hue=s=0.5',
            'brightness': 'eq=brightness=0.1',
            'contrast': 'eq=contrast=1.5',
            'saturation': 'eq=saturation=1.5',
            'blur': 'boxblur=2:1',
            'sharpen': 'unsharp=5:5:1.0:5:5:0.0',
            'grayscale': 'hue=s=0',
            'sepia': 'colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131',
            'negative': 'negate',
            'noise': 'noise=alls=20:allf=t+u'
        }
        
        filter_str = filters.get(filter_name, 'hue=s=0.5')
        stream = ffmpeg.filter(stream, 'split').filter(filter_str)
        output = ffmpeg.output(stream, output_path, vcodec='libx264', acodec='aac')
        await asyncio.get_event_loop().run_in_executor(None, output.run)
        return True
    except Exception as e:
        print(f"Error applying filter: {e}")
        return False


async def crop_video(input_path: str, output_path: str, width: int, height: int, x: int = 0, y: int = 0) -> bool:
    """Crop video to specified dimensions"""
    try:
        stream = ffmpeg.input(input_path)
        stream = ffmpeg.crop(stream, x, y, width, height)
        output = ffmpeg.output(stream, output_path, vcodec='libx264', acodec='aac')
        await asyncio.get_event_loop().run_in_executor(None, output.run)
        return True
    except Exception as e:
        print(f"Error cropping video: {e}")
        return False


async def rotate_video(input_path: str, output_path: str, angle: int = 90) -> bool:
    """Rotate video by specified angle"""
    try:
        stream = ffmpeg.input(input_path)
        
        # FFmpeg rotation: 0=90°CCW, 1=90°CW, 2=90°CCW, 3=90°CW+vflip
        rotation_map = {
            90: 1,
            180: 2,
            270: 3,
            -90: 0
        }
        
        transpose = rotation_map.get(angle % 360, 1)
        stream = ffmpeg.filter(stream, 'transpose', transpose)
        output = ffmpeg.output(stream, output_path, vcodec='libx264', acodec='aac')
        await asyncio.get_event_loop().run_in_executor(None, output.run)
        return True
    except Exception as e:
        print(f"Error rotating video: {e}")
        return False


async def add_text_to_video(input_path: str, output_path: str, text: str, 
                           x: int = 10, y: int = 10, fontsize: int = 24, 
                           fontcolor: str = 'white') -> bool:
    """Add text overlay to video"""
    try:
        stream = ffmpeg.input(input_path)
        stream = ffmpeg.drawtext(
            stream,
            text=text,
            x=x,
            y=y,
            fontsize=fontsize,
            fontcolor=fontcolor,
            box=1,
            boxcolor='black@0.5',
            boxborderw=5
        )
        output = ffmpeg.output(stream, output_path, vcodec='libx264', acodec='aac')
        await asyncio.get_event_loop().run_in_executor(None, output.run)
        return True
    except Exception as e:
        print(f"Error adding text to video: {e}")
        return False


async def trim_video(input_path: str, output_path: str, start_time: float = 0, end_time: float = None) -> bool:
    """Trim video to specified time range"""
    try:
        if end_time:
            duration = end_time - start_time
            stream = ffmpeg.input(input_path, ss=start_time, t=duration)
        else:
            stream = ffmpeg.input(input_path, ss=start_time)
        
        output = ffmpeg.output(stream, output_path, vcodec='libx264', acodec='aac')
        await asyncio.get_event_loop().run_in_executor(None, output.run)
        return True
    except Exception as e:
        print(f"Error trimming video: {e}")
        return False


async def merge_videos(input_path1: str, input_path2: str, output_path: str, 
                      layout: str = 'horizontal') -> bool:
    """Merge two videos side by side or vertically"""
    try:
        input1 = ffmpeg.input(input_path1)
        input2 = ffmpeg.input(input_path2)
        
        if layout == 'horizontal':
            # Side by side
            joined = ffmpeg.filter([input1, input2], 'hstack')
        elif layout == 'vertical':
            # One above the other
            joined = ffmpeg.filter([input1, input2], 'vstack')
        else:
            # Concatenate (one after another)
            joined = ffmpeg.concat(input1, input2, v=1, a=1)
        
        output = ffmpeg.output(joined, output_path, vcodec='libx264', acodec='aac')
        await asyncio.get_event_loop().run_in_executor(None, output.run)
        return True
    except Exception as e:
        print(f"Error merging videos: {e}")
        return False


async def concatenate_videos(input_paths: List[str], output_path: str) -> bool:
    """Concatenate multiple videos one after another"""
    try:
        # Create concat file
        concat_file = os.path.join(settings.TEMP_VIDEO_DIR, 'concat_list.txt')
        with open(concat_file, 'w') as f:
            for path in input_paths:
                f.write(f"file '{path}'\n")
        
        # Use concat demuxer
        cmd = f'ffmpeg -f concat -safe 0 -i {concat_file} -c copy {output_path}'
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()
        
        # Clean up
        if os.path.exists(concat_file):
            os.remove(concat_file)
        
        return process.returncode == 0
    except Exception as e:
        print(f"Error concatenating videos: {e}")
        return False
