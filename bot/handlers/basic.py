from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.keyboards import main_menu_keyboard, mode_selection_keyboard
from database.database import async_session_maker
from database.crud import get_or_create_user, get_user_videos, get_statistics
from config import settings

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Handle /start command"""
    await state.clear()
    
    async with async_session_maker() as session:
        user = await get_or_create_user(
            session,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )
    
    welcome_text = (
        f"👋 Welcome, {message.from_user.first_name}!\n\n"
        "🎬 This bot helps you unicalize (make unique) your videos!\n\n"
        "Choose what you want to do:\n"
        "• Process 1 Video - Apply modifications to a single video\n"
        "• Process 2 Videos - Modify and merge two videos\n\n"
        "Use the buttons below to get started!"
    )
    
    await message.answer(welcome_text, reply_markup=main_menu_keyboard())


@router.message(Command("help"))
@router.message(F.text == "ℹ️ Help")
async def cmd_help(message: Message):
    """Handle /help command"""
    help_text = (
        "🔍 <b>How to use this bot:</b>\n\n"
        "<b>Mode 1: Single Video</b>\n"
        "1. Click '🎬 Process 1 Video'\n"
        "2. Send your video file\n"
        "3. Choose modifications (speed, scale, filters, etc.)\n"
        "4. Get your unicalized video!\n\n"
        "<b>Mode 2: Two Videos</b>\n"
        "1. Click '🎥 Process 2 Videos'\n"
        "2. Send first video\n"
        "3. Send second video\n"
        "4. Choose modifications for each\n"
        "5. Select merge layout\n"
        "6. Get your combined video!\n\n"
        "<b>Available Modifications:</b>\n"
        "⚡ Speed - Change playback speed\n"
        "📐 Scale - Resize video dimensions\n"
        "🎨 Filters - Apply visual effects\n"
        "✂️ Crop - Cut parts of the video\n"
        "🔄 Rotate - Rotate the video\n"
        "📝 Text - Add text overlay\n"
        "⏱️ Trim - Cut video length\n\n"
        "For support: @YourSupportChannel"
    )
    
    await message.answer(help_text, parse_mode="HTML")


@router.message(F.text == "📊 My Statistics")
async def show_statistics(message: Message):
    """Show user statistics"""
    async with async_session_maker() as session:
        user = await get_or_create_user(
            session,
            telegram_id=message.from_user.id,
            username=message.from_user.username
        )
        videos = await get_user_videos(session, user.id)
        
        completed_videos = sum(1 for v in videos if v.status == "completed")
        pending_videos = sum(1 for v in videos if v.status == "pending")
        processing_videos = sum(1 for v in videos if v.status == "processing")
    
    stats_text = (
        f"📊 <b>Your Statistics</b>\n\n"
        f"👤 User ID: {user.telegram_id}\n"
        f"📅 Member since: {user.created_at.strftime('%Y-%m-%d')}\n\n"
        f"🎬 Total videos: {len(videos)}\n"
        f"✅ Completed: {completed_videos}\n"
        f"⏳ Processing: {processing_videos}\n"
        f"⏸️ Pending: {pending_videos}\n\n"
        f"💰 Balance: ${user.balance:.2f}"
    )
    
    await message.answer(stats_text, parse_mode="HTML")


@router.message(F.text == "💰 Balance")
async def show_balance(message: Message):
    """Show user balance"""
    async with async_session_maker() as session:
        user = await get_or_create_user(
            session,
            telegram_id=message.from_user.id,
            username=message.from_user.username
        )
    
    balance_text = (
        f"💰 <b>Your Balance</b>\n\n"
        f"Current balance: ${user.balance:.2f}\n\n"
        "Use /deposit to add funds\n"
        "Use /withdraw to withdraw funds"
    )
    
    await message.answer(balance_text, parse_mode="HTML")


@router.message(F.text == "👥 Referrals")
async def show_referrals(message: Message):
    """Show referral information"""
    async with async_session_maker() as session:
        user = await get_or_create_user(
            session,
            telegram_id=message.from_user.id,
            username=message.from_user.username
        )
    
    # Get bot username for referral link
    bot_username = (await message.bot.me()).username
    referral_link = f"https://t.me/{bot_username}?start=ref_{user.telegram_id}"
    
    referral_text = (
        f"👥 <b>Referral Program</b>\n\n"
        f"Your referral link:\n"
        f"<code>{referral_link}</code>\n\n"
        f"Share this link with friends and earn bonuses!\n\n"
        f"Total referrals: {len(user.referrals) if hasattr(user, 'referrals') else 0}"
    )
    
    await message.answer(referral_text, parse_mode="HTML")


@router.message(F.text == "🎬 Process 1 Video")
async def mode_1_handler(message: Message, state: FSMContext):
    """Handle Mode 1: Single video processing"""
    from bot.states import VideoProcessingStates
    await state.set_state(VideoProcessingStates.waiting_for_video_mode1)
    await message.answer(
        "🎬 <b>Mode 1: Single Video Processing</b>\n\n"
        "Please send me the video you want to unicalize.\n\n"
        "Supported formats: MP4, AVI, MOV, MKV\n"
        f"Max size: {settings.MAX_VIDEO_SIZE_MB}MB",
        parse_mode="HTML"
    )


@router.message(F.text == "🎥 Process 2 Videos")
async def mode_2_handler(message: Message, state: FSMContext):
    """Handle Mode 2: Two video processing"""
    from bot.states import VideoProcessingStates
    await state.set_state(VideoProcessingStates.waiting_for_video1_mode2)
    await message.answer(
        "🎥 <b>Mode 2: Two Video Processing</b>\n\n"
        "Please send me the <b>first</b> video.\n\n"
        "Supported formats: MP4, AVI, MOV, MKV\n"
        f"Max size: {settings.MAX_VIDEO_SIZE_MB}MB per video",
        parse_mode="HTML"
    )
