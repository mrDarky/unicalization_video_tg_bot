from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.states import VideoProcessingStates
from bot.keyboards import (
    merge_layout_keyboard,
    video_modifications_keyboard,
    main_menu_keyboard
)
from database.database import async_session_maker
from database.crud import get_or_create_user, create_video, update_video_status
from utils.video_processing import *
from config import settings
import os
import json

router = Router()


@router.message(VideoProcessingStates.waiting_for_video1_mode2, F.video)
async def handle_video1_mode2(message: Message, state: FSMContext):
    """Handle first video upload for mode 2"""
    video = message.video
    
    if video.file_size > settings.MAX_VIDEO_SIZE_MB * 1024 * 1024:
        await message.answer(
            f"❌ Video is too large! Max size: {settings.MAX_VIDEO_SIZE_MB}MB"
        )
        return
    
    file = await message.bot.get_file(video.file_id)
    filename = generate_filename()
    video_path = os.path.join(settings.TEMP_VIDEO_DIR, filename)
    
    await message.bot.download_file(file.file_path, video_path)
    
    async with async_session_maker() as session:
        user = await get_or_create_user(
            session,
            telegram_id=message.from_user.id,
            username=message.from_user.username
        )
        
        db_video = await create_video(
            session,
            user_id=user.id,
            file_id=video.file_id,
            mode=2,
            original_filename=filename
        )
        
        await state.update_data(
            video1_id=db_video.id,
            video1_path=video_path,
            modifications1=[]
        )
    
    await message.answer(
        "✅ First video received!\n\n"
        "Now send me the <b>second</b> video.",
        parse_mode="HTML"
    )
    await state.set_state(VideoProcessingStates.waiting_for_video2_mode2)


@router.message(VideoProcessingStates.waiting_for_video2_mode2, F.video)
async def handle_video2_mode2(message: Message, state: FSMContext):
    """Handle second video upload for mode 2"""
    video = message.video
    
    if video.file_size > settings.MAX_VIDEO_SIZE_MB * 1024 * 1024:
        await message.answer(
            f"❌ Video is too large! Max size: {settings.MAX_VIDEO_SIZE_MB}MB"
        )
        return
    
    file = await message.bot.get_file(video.file_id)
    filename = generate_filename()
    video_path = os.path.join(settings.TEMP_VIDEO_DIR, filename)
    
    await message.bot.download_file(file.file_path, video_path)
    
    async with async_session_maker() as session:
        user = await get_or_create_user(
            session,
            telegram_id=message.from_user.id,
            username=message.from_user.username
        )
        
        db_video = await create_video(
            session,
            user_id=user.id,
            file_id=video.file_id,
            mode=2,
            original_filename=filename
        )
        
        await state.update_data(
            video2_id=db_video.id,
            video2_path=video_path,
            modifications2=[]
        )
    
    await message.answer(
        "✅ Both videos received!\n\n"
        "Now select how you want to merge them:",
        reply_markup=merge_layout_keyboard()
    )
    await state.set_state(VideoProcessingStates.selecting_merge_layout)


@router.callback_query(VideoProcessingStates.selecting_merge_layout, F.data.startswith("merge_"))
async def handle_merge_layout(callback: CallbackQuery, state: FSMContext):
    """Handle merge layout selection"""
    layout = callback.data.replace("merge_", "")
    await state.update_data(merge_layout=layout)
    
    await callback.message.edit_text(
        "⏳ Processing and merging your videos... Please wait.\n\n"
        "This may take a few minutes."
    )
    await callback.answer()
    
    data = await state.get_data()
    video1_path = data.get('video1_path')
    video2_path = data.get('video2_path')
    video1_id = data.get('video1_id')
    video2_id = data.get('video2_id')
    
    try:
        # Process videos (could add modifications here in the future)
        
        # Merge videos
        final_filename = generate_filename()
        final_path = os.path.join(settings.PROCESSED_VIDEO_DIR, final_filename)
        
        if layout == 'horizontal':
            await merge_videos(video1_path, video2_path, final_path, 'horizontal')
        elif layout == 'vertical':
            await merge_videos(video1_path, video2_path, final_path, 'vertical')
        elif layout == 'sequential':
            await concatenate_videos([video1_path, video2_path], final_path)
        
        # Update database
        async with async_session_maker() as session:
            await update_video_status(
                session,
                video1_id,
                "completed",
                processed_filename=final_filename,
                modifications=json.dumps({'merge_layout': layout, 'position': 'first'})
            )
            await update_video_status(
                session,
                video2_id,
                "completed",
                modifications=json.dumps({'merge_layout': layout, 'position': 'second'})
            )
        
        # Send merged video
        with open(final_path, 'rb') as video_file:
            await callback.message.answer_video(
                video=video_file,
                caption=f"✅ Your merged video is ready! (Layout: {layout})"
            )
        
        # Clean up
        if os.path.exists(video1_path):
            os.remove(video1_path)
        if os.path.exists(video2_path):
            os.remove(video2_path)
        
        await callback.message.answer(
            "🎉 Processing complete!\n\n"
            "Use the menu to process more videos.",
            reply_markup=main_menu_keyboard()
        )
        
    except Exception as e:
        await callback.message.answer(
            f"❌ Error processing videos: {str(e)}\n\n"
            "Please try again.",
            reply_markup=main_menu_keyboard()
        )
        
        async with async_session_maker() as session:
            await update_video_status(session, video1_id, "failed")
            await update_video_status(session, video2_id, "failed")
    
    await state.clear()
