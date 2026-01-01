from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.states import VideoProcessingStates
from bot.keyboards import (
    merge_layout_keyboard,
    merge_strategy_keyboard,
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


# Mode 2: NEW FLOW - Configure filters for group 1, add videos, configure filters for group 2, add videos, then merge
@router.callback_query(VideoProcessingStates.selecting_modifications_video1, F.data == "mod_speed")
async def handle_speed_modification_video1(callback: CallbackQuery, state: FSMContext):
    """Handle speed modification for video group 1"""
    await callback.message.edit_text(
        "⚡ <b>Change Speed (Group 1)</b>\n\n"
        "Enter the speed multiplier (e.g., 1.5 for 1.5x speed, 0.5 for half speed):\n"
        "Range: 0.5 to 2.0",
        parse_mode="HTML"
    )
    await state.update_data(modification_context='video1')
    await state.set_state(VideoProcessingStates.waiting_for_speed_input)
    await callback.answer()


@router.callback_query(VideoProcessingStates.selecting_modifications_video2, F.data == "mod_speed")
async def handle_speed_modification_video2(callback: CallbackQuery, state: FSMContext):
    """Handle speed modification for video group 2"""
    await callback.message.edit_text(
        "⚡ <b>Change Speed (Group 2)</b>\n\n"
        "Enter the speed multiplier (e.g., 1.5 for 1.5x speed, 0.5 for half speed):\n"
        "Range: 0.5 to 2.0",
        parse_mode="HTML"
    )
    await state.update_data(modification_context='video2')
    await state.set_state(VideoProcessingStates.waiting_for_speed_input)
    await callback.answer()


@router.message(VideoProcessingStates.waiting_for_speed_input)
async def process_speed_input_mode2(message: Message, state: FSMContext):
    """Process speed input for Mode 2"""
    try:
        speed = float(message.text)
        if speed < 0.5 or speed > 2.0:
            await message.answer("❌ Speed must be between 0.5 and 2.0")
            return
        
        data = await state.get_data()
        modification_context = data.get('modification_context', 'video1')
        
        if modification_context == 'video1':
            modifications1 = data.get('modifications1', [])
            modifications1.append({'type': 'speed', 'value': speed})
            await state.update_data(modifications1=modifications1)
            
            await message.answer(
                f"✅ Speed set to {speed}x for Group 1\n\n"
                "Select more modifications or click Done:",
                reply_markup=video_modifications_keyboard()
            )
            await state.set_state(VideoProcessingStates.selecting_modifications_video1)
        else:  # video2
            modifications2 = data.get('modifications2', [])
            modifications2.append({'type': 'speed', 'value': speed})
            await state.update_data(modifications2=modifications2)
            
            await message.answer(
                f"✅ Speed set to {speed}x for Group 2\n\n"
                "Select more modifications or click Done:",
                reply_markup=video_modifications_keyboard()
            )
            await state.set_state(VideoProcessingStates.selecting_modifications_video2)
    except ValueError:
        await message.answer("❌ Invalid input. Please enter a number.")


@router.message(VideoProcessingStates.waiting_for_text_input)
async def process_text_input_mode2(message: Message, state: FSMContext):
    """Process text input for Mode 2"""
    text = message.text
    
    data = await state.get_data()
    modification_context = data.get('modification_context', 'video1')
    
    if modification_context == 'video1':
        modifications1 = data.get('modifications1', [])
        modifications1.append({'type': 'text', 'value': text, 'x': 10, 'y': 10})
        await state.update_data(modifications1=modifications1)
        
        await message.answer(
            f"✅ Text added: '{text}' for Group 1\n\n"
            "Select more modifications or click Done:",
            reply_markup=video_modifications_keyboard()
        )
        await state.set_state(VideoProcessingStates.selecting_modifications_video1)
    else:  # video2
        modifications2 = data.get('modifications2', [])
        modifications2.append({'type': 'text', 'value': text, 'x': 10, 'y': 10})
        await state.update_data(modifications2=modifications2)
        
        await message.answer(
            f"✅ Text added: '{text}' for Group 2\n\n"
            "Select more modifications or click Done:",
            reply_markup=video_modifications_keyboard()
        )
        await state.set_state(VideoProcessingStates.selecting_modifications_video2)



@router.callback_query(VideoProcessingStates.selecting_modifications_video1, F.data == "mod_filter")
async def handle_filter_modification_video1(callback: CallbackQuery, state: FSMContext):
    """Handle filter modification for video group 1"""
    await callback.message.edit_text(
        "🎨 <b>Select Filter (Group 1)</b>\n\n"
        "Choose a filter to apply:",
        reply_markup=filter_selection_keyboard(),
        parse_mode="HTML"
    )
    await state.update_data(modification_context='video1')
    await callback.answer()


@router.callback_query(VideoProcessingStates.selecting_modifications_video2, F.data == "mod_filter")
async def handle_filter_modification_video2(callback: CallbackQuery, state: FSMContext):
    """Handle filter modification for video group 2"""
    await callback.message.edit_text(
        "🎨 <b>Select Filter (Group 2)</b>\n\n"
        "Choose a filter to apply:",
        reply_markup=filter_selection_keyboard(),
        parse_mode="HTML"
    )
    await state.update_data(modification_context='video2')
    await callback.answer()


@router.callback_query(VideoProcessingStates.selecting_modifications_video1, F.data.startswith("filter_"))
async def apply_filter_selection_video1(callback: CallbackQuery, state: FSMContext):
    """Apply selected filter for video group 1"""
    filter_name = callback.data.replace("filter_", "")
    
    data = await state.get_data()
    modifications1 = data.get('modifications1', [])
    modifications1.append({'type': 'filter', 'value': filter_name})
    await state.update_data(modifications1=modifications1)
    
    await callback.message.edit_text(
        f"✅ Filter '{filter_name}' added to Group 1!\n\n"
        "Select more modifications or click Done:",
        reply_markup=video_modifications_keyboard()
    )
    await callback.answer()


@router.callback_query(VideoProcessingStates.selecting_modifications_video2, F.data.startswith("filter_"))
async def apply_filter_selection_video2(callback: CallbackQuery, state: FSMContext):
    """Apply selected filter for video group 2"""
    filter_name = callback.data.replace("filter_", "")
    
    data = await state.get_data()
    modifications2 = data.get('modifications2', [])
    modifications2.append({'type': 'filter', 'value': filter_name})
    await state.update_data(modifications2=modifications2)
    
    await callback.message.edit_text(
        f"✅ Filter '{filter_name}' added to Group 2!\n\n"
        "Select more modifications or click Done:",
        reply_markup=video_modifications_keyboard()
    )
    await callback.answer()


@router.callback_query(VideoProcessingStates.selecting_modifications_video1, F.data == "mod_text")
async def handle_text_modification_video1(callback: CallbackQuery, state: FSMContext):
    """Handle text modification for video group 1"""
    await callback.message.edit_text(
        "📝 <b>Add Text (Group 1)</b>\n\n"
        "Enter the text you want to add:",
        parse_mode="HTML"
    )
    await state.update_data(modification_context='video1')
    await state.set_state(VideoProcessingStates.waiting_for_text_input)
    await callback.answer()


@router.callback_query(VideoProcessingStates.selecting_modifications_video2, F.data == "mod_text")
async def handle_text_modification_video2(callback: CallbackQuery, state: FSMContext):
    """Handle text modification for video group 2"""
    await callback.message.edit_text(
        "📝 <b>Add Text (Group 2)</b>\n\n"
        "Enter the text you want to add:",
        parse_mode="HTML"
    )
    await state.update_data(modification_context='video2')
    await state.set_state(VideoProcessingStates.waiting_for_text_input)
    await callback.answer()


@router.callback_query(VideoProcessingStates.selecting_modifications_video1, F.data == "mod_done")
async def finish_modifications_video1(callback: CallbackQuery, state: FSMContext):
    """Finish setting up modifications for group 1 and proceed to video upload"""
    data = await state.get_data()
    modifications1 = data.get('modifications1', [])
    
    mod_summary = "\n".join([f"• {mod['type'].title()}" for mod in modifications1])
    if not mod_summary:
        mod_summary = "No modifications selected"
    
    await callback.message.edit_text(
        f"✅ <b>Group 1 modifications configured!</b>\n\n"
        f"{mod_summary}\n\n"
        f"Now send me the video(s) for Group 1.\n"
        f"You can send multiple videos.\n\n"
        f"When done, click 'Done'.",
        parse_mode="HTML"
    )
    await callback.answer()
    
    await state.update_data(video_paths1=[], video_ids1=[])
    await state.set_state(VideoProcessingStates.waiting_for_videos_group1)
    
    # Send the done button
    await callback.message.answer(
        "Click 'Done' when you've uploaded all Group 1 videos:",
        reply_markup=done_adding_videos_keyboard()
    )


@router.message(VideoProcessingStates.waiting_for_videos_group1, F.video)
async def handle_videos_group1(message: Message, state: FSMContext):
    """Handle video uploads for group 1"""
    video = message.video
    
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
            mode=2,
            original_filename=filename
        )
        
        data = await state.get_data()
        video_paths1 = data.get('video_paths1', [])
        video_ids1 = data.get('video_ids1', [])
        
        video_paths1.append(video_path)
        video_ids1.append(db_video.id)
        
        await state.update_data(
            video_paths1=video_paths1,
            video_ids1=video_ids1
        )
    
    await message.answer(
        f"✅ Group 1 Video {len(video_paths1)} received!\n\n"
        "Send more videos or click 'Done'."
    )


@router.callback_query(VideoProcessingStates.waiting_for_videos_group1, F.data == "videos_done")
async def proceed_to_group2(callback: CallbackQuery, state: FSMContext):
    """Proceed to configure group 2 after finishing group 1"""
    data = await state.get_data()
    video_paths1 = data.get('video_paths1', [])
    
    if not video_paths1:
        await callback.message.edit_text(
            "❌ No videos were uploaded for Group 1. Please upload at least one video."
        )
        return
    
    await callback.message.edit_text(
        f"✅ <b>Group 1 complete!</b> ({len(video_paths1)} video(s))\n\n"
        f"Now configure modifications for <b>Group 2</b>:",
        parse_mode="HTML",
        reply_markup=video_modifications_keyboard()
    )
    await callback.answer()
    
    await state.update_data(modifications2=[])
    await state.set_state(VideoProcessingStates.selecting_modifications_video2)


@router.callback_query(VideoProcessingStates.selecting_modifications_video2, F.data == "mod_done")
async def finish_modifications_video2(callback: CallbackQuery, state: FSMContext):
    """Finish setting up modifications for group 2 and proceed to video upload"""
    data = await state.get_data()
    modifications2 = data.get('modifications2', [])
    
    mod_summary = "\n".join([f"• {mod['type'].title()}" for mod in modifications2])
    if not mod_summary:
        mod_summary = "No modifications selected"
    
    await callback.message.edit_text(
        f"✅ <b>Group 2 modifications configured!</b>\n\n"
        f"{mod_summary}\n\n"
        f"Now send me the video(s) for Group 2.\n"
        f"You can send multiple videos.\n\n"
        f"When done, click 'Done'.",
        parse_mode="HTML"
    )
    await callback.answer()
    
    await state.update_data(video_paths2=[], video_ids2=[])
    await state.set_state(VideoProcessingStates.waiting_for_videos_group2)
    
    # Send the done button
    await callback.message.answer(
        "Click 'Done' when you've uploaded all Group 2 videos:",
        reply_markup=done_adding_videos_keyboard()
    )


@router.message(VideoProcessingStates.waiting_for_videos_group2, F.video)
async def handle_videos_group2(message: Message, state: FSMContext):
    """Handle video uploads for group 2"""
    video = message.video
    
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
            mode=2,
            original_filename=filename
        )
        
        data = await state.get_data()
        video_paths2 = data.get('video_paths2', [])
        video_ids2 = data.get('video_ids2', [])
        
        video_paths2.append(video_path)
        video_ids2.append(db_video.id)
        
        await state.update_data(
            video_paths2=video_paths2,
            video_ids2=video_ids2
        )
    
    await message.answer(
        f"✅ Group 2 Video {len(video_paths2)} received!\n\n"
        "Send more videos or click 'Done'."
    )


@router.callback_query(VideoProcessingStates.waiting_for_videos_group2, F.data == "videos_done")
async def select_merge_strategy(callback: CallbackQuery, state: FSMContext):
    """Select merge strategy after both groups are ready"""
    data = await state.get_data()
    video_paths2 = data.get('video_paths2', [])
    video_paths1 = data.get('video_paths1', [])
    
    if not video_paths2:
        await callback.message.edit_text(
            "❌ No videos were uploaded for Group 2. Please upload at least one video."
        )
        return
    
    await callback.message.edit_text(
        f"✅ <b>Both groups complete!</b>\n\n"
        f"Group 1: {len(video_paths1)} video(s)\n"
        f"Group 2: {len(video_paths2)} video(s)\n\n"
        f"How do you want to combine them?",
        parse_mode="HTML",
        reply_markup=merge_strategy_keyboard()
    )
    await callback.answer()
    
    await state.set_state(VideoProcessingStates.selecting_merge_strategy)


@router.callback_query(VideoProcessingStates.selecting_merge_strategy, F.data.startswith("strategy_"))
async def handle_merge_strategy(callback: CallbackQuery, state: FSMContext):
    """Handle merge strategy selection"""
    strategy = callback.data.replace("strategy_", "")
    await state.update_data(merge_strategy=strategy)
    
    await callback.message.edit_text(
        f"✅ Strategy selected: {strategy.replace('_', ' ').title()}\n\n"
        f"Now select the layout for merging:",
        parse_mode="HTML",
        reply_markup=merge_layout_keyboard()
    )
    await callback.answer()
    
    await state.set_state(VideoProcessingStates.selecting_merge_layout)


@router.callback_query(VideoProcessingStates.selecting_merge_layout, F.data.startswith("merge_"))
async def handle_merge_layout_mode2(callback: CallbackQuery, state: FSMContext):
    """Handle merge layout selection and process videos"""
    layout = callback.data.replace("merge_", "")
    await state.update_data(merge_layout=layout)
    
    data = await state.get_data()
    video_paths1 = data.get('video_paths1', [])
    video_paths2 = data.get('video_paths2', [])
    video_ids1 = data.get('video_ids1', [])
    video_ids2 = data.get('video_ids2', [])
    modifications1 = data.get('modifications1', [])
    modifications2 = data.get('modifications2', [])
    merge_strategy = data.get('merge_strategy', 'first_with_first')
    
    # Calculate total number of output videos based on merge strategy
    if merge_strategy == 'first_with_first':
        total_output_videos = min(len(video_paths1), len(video_paths2))
    elif merge_strategy == 'all_with_all':
        total_output_videos = len(video_paths1) * len(video_paths2)
    else:
        total_output_videos = max(len(video_paths1), len(video_paths2))
    
    # Check video limits
    async with async_session_maker() as session:
        from database.crud import check_user_can_process_videos, get_or_create_user
        user = await get_or_create_user(
            session,
            telegram_id=callback.from_user.id,
            username=callback.from_user.username
        )
        
        can_process, error_message = await check_user_can_process_videos(
            session, user.id, total_output_videos
        )
        
        if not can_process:
            await callback.message.edit_text(
                f"❌ {error_message}\n\n"
                "Please try again later or upgrade your plan.",
                reply_markup=main_menu_keyboard()
            )
            await state.clear()
            return
    
    await callback.message.edit_text(
        "⏳ Processing and merging your videos... Please wait.\n\n"
        "This may take a few minutes."
    )
    await callback.answer()
    
    try:
        # First, apply modifications to all videos in both groups
        processed_paths1 = []
        for idx, video_path in enumerate(video_paths1):
            current_path = video_path
            
            for i, mod in enumerate(modifications1):
                output_path = os.path.join(settings.TEMP_VIDEO_DIR, f"temp_g1_{idx}_{i}_{generate_filename()}")
                
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
                
                if current_path != video_path and os.path.exists(current_path):
                    os.remove(current_path)
                
                current_path = output_path
            
            processed_paths1.append(current_path)
        
        processed_paths2 = []
        for idx, video_path in enumerate(video_paths2):
            current_path = video_path
            
            for i, mod in enumerate(modifications2):
                output_path = os.path.join(settings.TEMP_VIDEO_DIR, f"temp_g2_{idx}_{i}_{generate_filename()}")
                
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
                
                if current_path != video_path and os.path.exists(current_path):
                    os.remove(current_path)
                
                current_path = output_path
            
            processed_paths2.append(current_path)
        
        # Now merge based on strategy
        merged_count = 0
        
        if merge_strategy == 'first_with_first':
            # Pair first with first, second with second, etc.
            pairs = min(len(processed_paths1), len(processed_paths2))
            for i in range(pairs):
                final_filename = generate_filename()
                final_path = os.path.join(settings.PROCESSED_VIDEO_DIR, final_filename)
                
                if layout == 'horizontal':
                    await merge_videos(processed_paths1[i], processed_paths2[i], final_path, 'horizontal')
                elif layout == 'vertical':
                    await merge_videos(processed_paths1[i], processed_paths2[i], final_path, 'vertical')
                elif layout == 'sequential':
                    await concatenate_videos([processed_paths1[i], processed_paths2[i]], final_path)
                
                # Send merged video
                with open(final_path, 'rb') as video_file:
                    await callback.message.answer_video(
                        video=video_file,
                        caption=f"✅ Merged video {i + 1}/{pairs} is ready!"
                    )
                merged_count += 1
        
        elif merge_strategy == 'all_with_all':
            # Cartesian product - every video from group 1 with every video from group 2
            for i, path1 in enumerate(processed_paths1):
                for j, path2 in enumerate(processed_paths2):
                    final_filename = generate_filename()
                    final_path = os.path.join(settings.PROCESSED_VIDEO_DIR, final_filename)
                    
                    if layout == 'horizontal':
                        await merge_videos(path1, path2, final_path, 'horizontal')
                    elif layout == 'vertical':
                        await merge_videos(path1, path2, final_path, 'vertical')
                    elif layout == 'sequential':
                        await concatenate_videos([path1, path2], final_path)
                    
                    # Send merged video
                    with open(final_path, 'rb') as video_file:
                        await callback.message.answer_video(
                            video=video_file,
                            caption=f"✅ Merged: G1[{i+1}] + G2[{j+1}]"
                        )
                    merged_count += 1
        
        elif merge_strategy == 'sequential':
            # All from group 1, then all from group 2
            final_filename = generate_filename()
            final_path = os.path.join(settings.PROCESSED_VIDEO_DIR, final_filename)
            
            all_videos = processed_paths1 + processed_paths2
            await concatenate_videos(all_videos, final_path)
            
            # Send merged video
            with open(final_path, 'rb') as video_file:
                await callback.message.answer_video(
                    video=video_file,
                    caption=f"✅ All videos merged sequentially!"
                )
            merged_count = 1
        
        # Update database
        async with async_session_maker() as session:
            for video_id in video_ids1:
                await update_video_status(
                    session,
                    video_id,
                    "completed",
                    modifications=json.dumps({'group': 1, 'modifications': modifications1, 'strategy': merge_strategy, 'layout': layout})
                )
            for video_id in video_ids2:
                await update_video_status(
                    session,
                    video_id,
                    "completed",
                    modifications=json.dumps({'group': 2, 'modifications': modifications2, 'strategy': merge_strategy, 'layout': layout})
                )
        
        # Clean up
        for path in video_paths1 + video_paths2 + processed_paths1 + processed_paths2:
            if os.path.exists(path):
                os.remove(path)
        
        # Increment daily usage for successfully processed videos
        async with async_session_maker() as session:
            from database.crud import increment_daily_usage, get_or_create_user
            user = await get_or_create_user(
                session,
                telegram_id=callback.from_user.id,
                username=callback.from_user.username
            )
            await increment_daily_usage(session, user.id, merged_count)
        
        await callback.message.answer(
            f"🎉 Processing complete!\n\n"
            f"Created {merged_count} merged video(s).\n\n"
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
            for video_id in video_ids1 + video_ids2:
                await update_video_status(session, video_id, "failed")
    
    await state.clear()
