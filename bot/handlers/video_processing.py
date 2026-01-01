from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.states import VideoProcessingStates
from bot.keyboards import (
    video_modifications_keyboard,
    filter_selection_keyboard,
    main_menu_keyboard,
    done_adding_videos_keyboard
)
from database.database import async_session_maker
from database.crud import get_or_create_user, create_video, update_video_status
from utils.video_processing import *
from config import settings
import os
import json

router = Router()


# Mode 1: NEW FLOW - Configure filters first, then add multiple videos
@router.callback_query(VideoProcessingStates.selecting_modifications_mode1, F.data == "mod_speed")
async def handle_speed_modification_mode1(callback: CallbackQuery, state: FSMContext):
    """Handle speed modification"""
    await callback.message.edit_text(
        "⚡ <b>Change Speed</b>\n\n"
        "Enter the speed multiplier (e.g., 1.5 for 1.5x speed, 0.5 for half speed):\n"
        "Range: 0.5 to 2.0",
        parse_mode="HTML"
    )
    await state.set_state(VideoProcessingStates.waiting_for_speed_input)
    await callback.answer()


@router.message(VideoProcessingStates.waiting_for_speed_input)
async def process_speed_input(message: Message, state: FSMContext):
    """Process speed input"""
    try:
        speed = float(message.text)
        if speed < 0.5 or speed > 2.0:
            await message.answer("❌ Speed must be between 0.5 and 2.0")
            return
        
        data = await state.get_data()
        modifications = data.get('modifications', [])
        modifications.append({'type': 'speed', 'value': speed})
        await state.update_data(modifications=modifications)
        
        await message.answer(
            f"✅ Speed set to {speed}x\n\n"
            "Select more modifications or click Done:",
            reply_markup=video_modifications_keyboard()
        )
        await state.set_state(VideoProcessingStates.selecting_modifications_mode1)
    except ValueError:
        await message.answer("❌ Invalid input. Please enter a number.")


@router.callback_query(VideoProcessingStates.selecting_modifications_mode1, F.data == "mod_filter")
async def handle_filter_modification_mode1(callback: CallbackQuery, state: FSMContext):
    """Handle filter modification"""
    await callback.message.edit_text(
        "🎨 <b>Select Filter</b>\n\n"
        "Choose a filter to apply to your video:",
        reply_markup=filter_selection_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(VideoProcessingStates.selecting_modifications_mode1, F.data.startswith("filter_"))
async def apply_filter_selection_mode1(callback: CallbackQuery, state: FSMContext):
    """Apply selected filter"""
    filter_name = callback.data.replace("filter_", "")
    
    data = await state.get_data()
    modifications = data.get('modifications', [])
    modifications.append({'type': 'filter', 'value': filter_name})
    await state.update_data(modifications=modifications)
    
    await callback.message.edit_text(
        f"✅ Filter '{filter_name}' added!\n\n"
        "Select more modifications or click Done:",
        reply_markup=video_modifications_keyboard()
    )
    await callback.answer()


@router.callback_query(VideoProcessingStates.selecting_modifications_mode1, F.data == "mod_scale")
async def handle_scale_modification_mode1(callback: CallbackQuery, state: FSMContext):
    """Handle scale modification"""
    await callback.message.edit_text(
        "📐 <b>Scale Video</b>\n\n"
        "Enter dimensions in format: width height\n"
        "Example: 1280 720\n\n"
        "Common sizes:\n"
        "• 1920 1080 (Full HD)\n"
        "• 1280 720 (HD)\n"
        "• 854 480 (SD)",
        parse_mode="HTML"
    )
    await state.set_state(VideoProcessingStates.waiting_for_scale_input)
    await callback.answer()


@router.message(VideoProcessingStates.waiting_for_scale_input)
async def process_scale_input(message: Message, state: FSMContext):
    """Process scale input"""
    try:
        parts = message.text.split()
        if len(parts) != 2:
            await message.answer("❌ Please enter width and height separated by space")
            return
        
        width, height = int(parts[0]), int(parts[1])
        
        data = await state.get_data()
        modifications = data.get('modifications', [])
        modifications.append({'type': 'scale', 'width': width, 'height': height})
        await state.update_data(modifications=modifications)
        
        await message.answer(
            f"✅ Scale set to {width}x{height}\n\n"
            "Select more modifications or click Done:",
            reply_markup=video_modifications_keyboard()
        )
        await state.set_state(VideoProcessingStates.selecting_modifications_mode1)
    except ValueError:
        await message.answer("❌ Invalid input. Please enter valid numbers.")


@router.callback_query(VideoProcessingStates.selecting_modifications_mode1, F.data == "mod_rotate")
async def handle_rotate_modification_mode1(callback: CallbackQuery, state: FSMContext):
    """Handle rotate modification"""
    await callback.message.edit_text(
        "🔄 <b>Rotate Video</b>\n\n"
        "Enter rotation angle:\n"
        "• 90 - Rotate 90° clockwise\n"
        "• 180 - Rotate 180°\n"
        "• 270 - Rotate 270° clockwise\n"
        "• -90 - Rotate 90° counter-clockwise",
        parse_mode="HTML"
    )
    await state.set_state(VideoProcessingStates.waiting_for_rotate_input)
    await callback.answer()


@router.message(VideoProcessingStates.waiting_for_rotate_input)
async def process_rotate_input(message: Message, state: FSMContext):
    """Process rotate input"""
    try:
        angle = int(message.text)
        if angle not in [90, 180, 270, -90]:
            await message.answer("❌ Please enter 90, 180, 270, or -90")
            return
        
        data = await state.get_data()
        modifications = data.get('modifications', [])
        modifications.append({'type': 'rotate', 'angle': angle})
        await state.update_data(modifications=modifications)
        
        await message.answer(
            f"✅ Rotation set to {angle}°\n\n"
            "Select more modifications or click Done:",
            reply_markup=video_modifications_keyboard()
        )
        await state.set_state(VideoProcessingStates.selecting_modifications_mode1)
    except ValueError:
        await message.answer("❌ Invalid input. Please enter a valid angle.")


@router.callback_query(VideoProcessingStates.selecting_modifications_mode1, F.data == "mod_text")
async def handle_text_modification_mode1(callback: CallbackQuery, state: FSMContext):
    """Handle text modification"""
    await callback.message.edit_text(
        "📝 <b>Add Text</b>\n\n"
        "Enter the text you want to add to the video:",
        parse_mode="HTML"
    )
    await state.set_state(VideoProcessingStates.waiting_for_text_input)
    await callback.answer()


@router.message(VideoProcessingStates.waiting_for_text_input)
async def process_text_input(message: Message, state: FSMContext):
    """Process text input"""
    text = message.text
    
    data = await state.get_data()
    modifications = data.get('modifications', [])
    modifications.append({'type': 'text', 'value': text, 'x': 10, 'y': 10})
    await state.update_data(modifications=modifications)
    
    await message.answer(
        f"✅ Text added: '{text}'\n\n"
        "Select more modifications or click Done:",
        reply_markup=video_modifications_keyboard()
    )
    await state.set_state(VideoProcessingStates.selecting_modifications_mode1)


@router.callback_query(VideoProcessingStates.selecting_modifications_mode1, F.data == "mod_done")
async def finish_modifications_mode1(callback: CallbackQuery, state: FSMContext):
    """Finish setting up modifications and proceed to video upload"""
    data = await state.get_data()
    modifications = data.get('modifications', [])
    
    mod_summary = "\n".join([f"• {mod['type'].title()}" for mod in modifications])
    if not mod_summary:
        mod_summary = "No modifications selected"
    
    await callback.message.edit_text(
        f"✅ <b>Modifications configured!</b>\n\n"
        f"{mod_summary}\n\n"
        f"Now send me the video(s) you want to process.\n"
        f"You can send multiple videos and they will all be processed with these settings.\n\n"
        f"When done uploading videos, click the 'Done' button.",
        parse_mode="HTML"
    )
    await callback.answer()
    
    await state.update_data(video_paths=[], video_ids=[])
    await state.set_state(VideoProcessingStates.waiting_for_videos_mode1)
    
    # Send the done button
    await callback.message.answer(
        "Click 'Done' when you've uploaded all videos:",
        reply_markup=done_adding_videos_keyboard()
    )


@router.message(VideoProcessingStates.waiting_for_videos_mode1, F.video)
async def handle_videos_mode1(message: Message, state: FSMContext):
    """Handle video uploads for mode 1"""
    video = message.video
    
    # Check file size
    if video.file_size > settings.MAX_VIDEO_SIZE_MB * 1024 * 1024:
        await message.answer(
            f"❌ Video is too large! Max size: {settings.MAX_VIDEO_SIZE_MB}MB"
        )
        return
    
    # Download video
    file = await message.bot.get_file(video.file_id)
    filename = generate_filename()
    video_path = os.path.join(settings.TEMP_VIDEO_DIR, filename)
    
    await message.bot.download_file(file.file_path, video_path)
    
    # Save video to database
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
            mode=1,
            original_filename=filename
        )
        
        data = await state.get_data()
        video_paths = data.get('video_paths', [])
        video_ids = data.get('video_ids', [])
        
        video_paths.append(video_path)
        video_ids.append(db_video.id)
        
        video_count = len(video_paths)
        
        await state.update_data(
            video_paths=video_paths,
            video_ids=video_ids
        )
    
    await message.answer(
        f"✅ Video {video_count} received!\n\n"
        "Send more videos or click 'Done' to start processing."
    )


@router.callback_query(VideoProcessingStates.waiting_for_videos_mode1, F.data == "videos_done")
async def process_all_videos_mode1(callback: CallbackQuery, state: FSMContext):
    """Process all uploaded videos with the configured modifications"""
    await callback.message.edit_text("⏳ Processing your videos... Please wait.")
    await callback.answer()
    
    data = await state.get_data()
    video_paths = data.get('video_paths', [])
    video_ids = data.get('video_ids', [])
    modifications = data.get('modifications', [])
    
    if not video_paths:
        await callback.message.answer(
            "❌ No videos were uploaded. Please try again.",
            reply_markup=main_menu_keyboard()
        )
        await state.clear()
        return
    
    processed_count = 0
    failed_count = 0
    
    for idx, (video_path, video_id) in enumerate(zip(video_paths, video_ids)):
        try:
            # Process video with modifications
            current_path = video_path
            
            for i, mod in enumerate(modifications):
                output_path = os.path.join(settings.TEMP_VIDEO_DIR, f"temp_{idx}_{i}_{generate_filename()}")
                
                if mod['type'] == 'speed':
                    await change_video_speed(current_path, output_path, mod['value'])
                elif mod['type'] == 'filter':
                    await apply_filter(current_path, output_path, mod['value'])
                elif mod['type'] == 'scale':
                    await scale_video(current_path, output_path, mod['width'], mod['height'])
                elif mod['type'] == 'rotate':
                    await rotate_video(current_path, output_path, mod['angle'])
                elif mod['type'] == 'text':
                    await add_text_to_video(current_path, output_path, mod['value'], mod['x'], mod['y'])
                
                # Clean up previous temp file
                if current_path != video_path and os.path.exists(current_path):
                    os.remove(current_path)
                
                current_path = output_path
            
            # Save final video
            final_filename = generate_filename()
            final_path = os.path.join(settings.PROCESSED_VIDEO_DIR, final_filename)
            
            if current_path != video_path:
                os.rename(current_path, final_path)
            else:
                import shutil
                shutil.copy(video_path, final_path)
            
            # Update database
            async with async_session_maker() as session:
                await update_video_status(
                    session,
                    video_id,
                    "completed",
                    processed_filename=final_filename,
                    modifications=json.dumps(modifications)
                )
            
            # Send processed video
            with open(final_path, 'rb') as video_file:
                await callback.message.answer_video(
                    video=video_file,
                    caption=f"✅ Video {idx + 1}/{len(video_paths)} is ready!"
                )
            
            # Clean up
            if os.path.exists(video_path):
                os.remove(video_path)
            
            processed_count += 1
            
        except Exception as e:
            failed_count += 1
            await callback.message.answer(
                f"❌ Error processing video {idx + 1}: {str(e)}"
            )
            
            # Update database
            async with async_session_maker() as session:
                await update_video_status(session, video_id, "failed")
    
    await callback.message.answer(
        f"🎉 Processing complete!\n\n"
        f"✅ Successful: {processed_count}\n"
        f"❌ Failed: {failed_count}\n\n"
        "Use the menu to process more videos.",
        reply_markup=main_menu_keyboard()
    )
    
    await state.clear()


@router.callback_query(F.data == "cancel")
async def cancel_processing(callback: CallbackQuery, state: FSMContext):
    """Cancel processing"""
    await state.clear()
    await callback.message.edit_text(
        "❌ Cancelled. Use the menu to start over.",
    )
    await callback.answer()


@router.callback_query(VideoProcessingStates.selecting_modifications_mode1, F.data == "back_to_mods")
async def back_to_modifications(callback: CallbackQuery, state: FSMContext):
    """Go back to modifications menu"""
    await callback.message.edit_text(
        "Select modifications:",
        reply_markup=video_modifications_keyboard()
    )
    await callback.answer()
