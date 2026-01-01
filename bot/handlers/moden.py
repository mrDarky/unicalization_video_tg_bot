from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.states import VideoProcessingStates
from bot.keyboards import (
    num_groups_keyboard,
    next_group_keyboard,
    merge_strategy_keyboard,
    merge_layout_keyboard,
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


# Mode N: Process N video groups
@router.callback_query(VideoProcessingStates.selecting_num_groups, F.data.startswith("groups_"))
async def handle_num_groups(callback: CallbackQuery, state: FSMContext):
    """Handle number of groups selection"""
    num_groups = int(callback.data.replace("groups_", ""))
    
    await state.update_data(
        num_groups=num_groups,
        current_group=1,
        groups_data={}
    )
    
    await callback.message.edit_text(
        f"✅ <b>{num_groups} groups selected!</b>\n\n"
        f"Now configure modifications for <b>Group 1/{num_groups}</b>:",
        parse_mode="HTML",
        reply_markup=video_modifications_keyboard()
    )
    await callback.answer()
    
    await state.set_state(VideoProcessingStates.selecting_modifications_group)


@router.callback_query(VideoProcessingStates.selecting_modifications_group, F.data == "mod_speed")
async def handle_speed_modification_group(callback: CallbackQuery, state: FSMContext):
    """Handle speed modification for current group"""
    data = await state.get_data()
    current_group = data.get('current_group', 1)
    
    await callback.message.edit_text(
        f"⚡ <b>Change Speed (Group {current_group})</b>\n\n"
        "Enter the speed multiplier (e.g., 1.5 for 1.5x speed, 0.5 for half speed):\n"
        "Range: 0.5 to 2.0",
        parse_mode="HTML"
    )
    await state.set_state(VideoProcessingStates.waiting_for_speed_input)
    await callback.answer()


@router.callback_query(VideoProcessingStates.selecting_modifications_group, F.data == "mod_filter")
async def handle_filter_modification_group(callback: CallbackQuery, state: FSMContext):
    """Handle filter modification for current group"""
    data = await state.get_data()
    current_group = data.get('current_group', 1)
    
    await callback.message.edit_text(
        f"🎨 <b>Select Filter (Group {current_group})</b>\n\n"
        "Choose a filter to apply:",
        reply_markup=filter_selection_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(VideoProcessingStates.selecting_modifications_group, F.data.startswith("filter_"))
async def apply_filter_selection_group(callback: CallbackQuery, state: FSMContext):
    """Apply selected filter for current group"""
    filter_name = callback.data.replace("filter_", "")
    
    data = await state.get_data()
    current_group = data.get('current_group', 1)
    modifications = data.get('modifications', [])
    modifications.append({'type': 'filter', 'value': filter_name})
    await state.update_data(modifications=modifications)
    
    await callback.message.edit_text(
        f"✅ Filter '{filter_name}' added to Group {current_group}!\n\n"
        "Select more modifications or click Done:",
        reply_markup=video_modifications_keyboard()
    )
    await callback.answer()


@router.callback_query(VideoProcessingStates.selecting_modifications_group, F.data == "mod_text")
async def handle_text_modification_group(callback: CallbackQuery, state: FSMContext):
    """Handle text modification for current group"""
    data = await state.get_data()
    current_group = data.get('current_group', 1)
    
    await callback.message.edit_text(
        f"📝 <b>Add Text (Group {current_group})</b>\n\n"
        "Enter the text you want to add:",
        parse_mode="HTML"
    )
    await state.set_state(VideoProcessingStates.waiting_for_text_input)
    await callback.answer()


@router.callback_query(VideoProcessingStates.selecting_modifications_group, F.data == "mod_done")
async def finish_modifications_group(callback: CallbackQuery, state: FSMContext):
    """Finish setting up modifications for current group and proceed to video upload"""
    data = await state.get_data()
    current_group = data.get('current_group', 1)
    modifications = data.get('modifications', [])
    
    mod_summary = "\n".join([f"• {mod['type'].title()}" for mod in modifications])
    if not mod_summary:
        mod_summary = "No modifications selected"
    
    await callback.message.edit_text(
        f"✅ <b>Group {current_group} modifications configured!</b>\n\n"
        f"{mod_summary}\n\n"
        f"Now send me the video(s) for Group {current_group}.\n"
        f"You can send multiple videos.\n\n"
        f"When done, click 'Done'.",
        parse_mode="HTML"
    )
    await callback.answer()
    
    # Store modifications for this group
    groups_data = data.get('groups_data', {})
    groups_data[f'group_{current_group}'] = {
        'modifications': modifications,
        'video_paths': [],
        'video_ids': []
    }
    await state.update_data(groups_data=groups_data, modifications=[])
    await state.set_state(VideoProcessingStates.waiting_for_videos_group)
    
    # Send the done button
    await callback.message.answer(
        f"Click 'Done' when you've uploaded all Group {current_group} videos:",
        reply_markup=done_adding_videos_keyboard()
    )


@router.message(VideoProcessingStates.waiting_for_videos_group, F.video)
async def handle_videos_group(message: Message, state: FSMContext):
    """Handle video uploads for current group"""
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
            mode=3,  # Mode N
            original_filename=filename
        )
        
        data = await state.get_data()
        current_group = data.get('current_group', 1)
        groups_data = data.get('groups_data', {})
        
        group_key = f'group_{current_group}'
        if group_key not in groups_data:
            groups_data[group_key] = {'modifications': [], 'video_paths': [], 'video_ids': []}
        
        groups_data[group_key]['video_paths'].append(video_path)
        groups_data[group_key]['video_ids'].append(db_video.id)
        
        await state.update_data(groups_data=groups_data)
        
        video_count = len(groups_data[group_key]['video_paths'])
    
    await message.answer(
        f"✅ Group {current_group} Video {video_count} received!\n\n"
        "Send more videos or click 'Done'."
    )


@router.callback_query(VideoProcessingStates.waiting_for_videos_group, F.data == "videos_done")
async def proceed_to_next_group(callback: CallbackQuery, state: FSMContext):
    """Proceed to next group or to merge strategy if all groups are done"""
    data = await state.get_data()
    current_group = data.get('current_group', 1)
    num_groups = data.get('num_groups', 3)
    groups_data = data.get('groups_data', {})
    
    group_key = f'group_{current_group}'
    if not groups_data.get(group_key, {}).get('video_paths'):
        await callback.message.edit_text(
            f"❌ No videos were uploaded for Group {current_group}. Please upload at least one video."
        )
        return
    
    if current_group < num_groups:
        # Move to next group
        next_group = current_group + 1
        await state.update_data(current_group=next_group, modifications=[])
        
        await callback.message.edit_text(
            f"✅ <b>Group {current_group} complete!</b>\n\n"
            f"Now configure modifications for <b>Group {next_group}/{num_groups}</b>:",
            parse_mode="HTML",
            reply_markup=video_modifications_keyboard()
        )
        await callback.answer()
        
        await state.set_state(VideoProcessingStates.selecting_modifications_group)
    else:
        # All groups done, select combine strategy
        summary = "\n".join([
            f"Group {i+1}: {len(groups_data.get(f'group_{i+1}', {}).get('video_paths', []))} video(s)"
            for i in range(num_groups)
        ])
        
        await callback.message.edit_text(
            f"✅ <b>All groups complete!</b>\n\n"
            f"{summary}\n\n"
            f"How do you want to combine them?",
            parse_mode="HTML",
            reply_markup=merge_strategy_keyboard()
        )
        await callback.answer()
        
        await state.set_state(VideoProcessingStates.selecting_combine_strategy)


@router.callback_query(VideoProcessingStates.selecting_combine_strategy, F.data.startswith("strategy_"))
async def handle_combine_strategy(callback: CallbackQuery, state: FSMContext):
    """Handle combine strategy selection for mode N"""
    strategy = callback.data.replace("strategy_", "")
    await state.update_data(combine_strategy=strategy)
    
    await callback.message.edit_text(
        f"✅ Strategy selected: {strategy.replace('_', ' ').title()}\n\n"
        f"Now select the layout for combining:",
        parse_mode="HTML",
        reply_markup=merge_layout_keyboard()
    )
    await callback.answer()
    
    await state.set_state(VideoProcessingStates.selecting_merge_layout)


@router.callback_query(VideoProcessingStates.selecting_combine_strategy, F.data.startswith("merge_"))
async def handle_merge_layout_moden(callback: CallbackQuery, state: FSMContext):
    """Handle merge layout selection and process videos for mode N"""
    layout = callback.data.replace("merge_", "")
    
    await callback.message.edit_text(
        "⏳ Processing and combining your videos... Please wait.\n\n"
        "This may take several minutes."
    )
    await callback.answer()
    
    data = await state.get_data()
    num_groups = data.get('num_groups', 3)
    groups_data = data.get('groups_data', {})
    combine_strategy = data.get('combine_strategy', 'sequential')
    
    try:
        # First, apply modifications to all videos in all groups
        all_processed = {}
        all_ids = []
        
        for i in range(1, num_groups + 1):
            group_key = f'group_{i}'
            group_info = groups_data.get(group_key, {})
            video_paths = group_info.get('video_paths', [])
            modifications = group_info.get('modifications', [])
            video_ids = group_info.get('video_ids', [])
            
            all_ids.extend(video_ids)
            processed_paths = []
            
            for idx, video_path in enumerate(video_paths):
                current_path = video_path
                
                for j, mod in enumerate(modifications):
                    output_path = os.path.join(settings.TEMP_VIDEO_DIR, f"temp_g{i}_{idx}_{j}_{generate_filename()}")
                    
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
                
                processed_paths.append(current_path)
            
            all_processed[group_key] = processed_paths
        
        # Now combine based on strategy
        combined_count = 0
        
        if combine_strategy == 'sequential':
            # Concatenate all videos sequentially: all from group 1, then group 2, etc.
            all_videos = []
            for i in range(1, num_groups + 1):
                all_videos.extend(all_processed.get(f'group_{i}', []))
            
            if all_videos:
                final_filename = generate_filename()
                final_path = os.path.join(settings.PROCESSED_VIDEO_DIR, final_filename)
                await concatenate_videos(all_videos, final_path)
                
                with open(final_path, 'rb') as video_file:
                    await callback.message.answer_video(
                        video=video_file,
                        caption=f"✅ All videos merged sequentially!"
                    )
                combined_count = 1
        
        elif combine_strategy == 'first_with_first':
            # Take first video from each group and combine, then second from each group, etc.
            max_videos = max(len(all_processed.get(f'group_{i}', [])) for i in range(1, num_groups + 1))
            
            for vid_idx in range(max_videos):
                videos_to_merge = []
                for i in range(1, num_groups + 1):
                    group_videos = all_processed.get(f'group_{i}', [])
                    if vid_idx < len(group_videos):
                        videos_to_merge.append(group_videos[vid_idx])
                
                if len(videos_to_merge) >= 2:
                    final_filename = generate_filename()
                    final_path = os.path.join(settings.PROCESSED_VIDEO_DIR, final_filename)
                    
                    if layout == 'sequential':
                        await concatenate_videos(videos_to_merge, final_path)
                    else:
                        # For horizontal/vertical, merge first two, then add third, etc.
                        temp_path = videos_to_merge[0]
                        for j in range(1, len(videos_to_merge)):
                            if j == len(videos_to_merge) - 1:
                                output = final_path
                            else:
                                output = os.path.join(settings.TEMP_VIDEO_DIR, f"merge_temp_{j}_{generate_filename()}")
                            
                            if layout == 'horizontal':
                                await merge_videos(temp_path, videos_to_merge[j], output, 'horizontal')
                            elif layout == 'vertical':
                                await merge_videos(temp_path, videos_to_merge[j], output, 'vertical')
                            
                            if temp_path != videos_to_merge[0] and os.path.exists(temp_path):
                                os.remove(temp_path)
                            temp_path = output
                    
                    with open(final_path, 'rb') as video_file:
                        await callback.message.answer_video(
                            video=video_file,
                            caption=f"✅ Combined video {vid_idx + 1}/{max_videos}"
                        )
                    combined_count += 1
        
        elif combine_strategy == 'all_with_all':
            # Cartesian product of all groups
            import itertools
            
            group_lists = [all_processed.get(f'group_{i}', []) for i in range(1, num_groups + 1)]
            combinations = list(itertools.product(*group_lists))
            
            for combo_idx, combo in enumerate(combinations[:100]):  # Limit to 100 combinations
                final_filename = generate_filename()
                final_path = os.path.join(settings.PROCESSED_VIDEO_DIR, final_filename)
                
                if layout == 'sequential':
                    await concatenate_videos(list(combo), final_path)
                else:
                    # For horizontal/vertical, merge progressively
                    temp_path = combo[0]
                    for j in range(1, len(combo)):
                        if j == len(combo) - 1:
                            output = final_path
                        else:
                            output = os.path.join(settings.TEMP_VIDEO_DIR, f"combo_{combo_idx}_{j}_{generate_filename()}")
                        
                        if layout == 'horizontal':
                            await merge_videos(temp_path, combo[j], output, 'horizontal')
                        elif layout == 'vertical':
                            await merge_videos(temp_path, combo[j], output, 'vertical')
                        
                        if temp_path != combo[0] and os.path.exists(temp_path):
                            os.remove(temp_path)
                        temp_path = output
                
                with open(final_path, 'rb') as video_file:
                    await callback.message.answer_video(
                        video=video_file,
                        caption=f"✅ Combination {combo_idx + 1}"
                    )
                combined_count += 1
        
        # Update database
        async with async_session_maker() as session:
            for video_id in all_ids:
                await update_video_status(
                    session,
                    video_id,
                    "completed",
                    modifications=json.dumps({'mode': 'n', 'strategy': combine_strategy, 'layout': layout})
                )
        
        # Clean up all temporary files
        for group_key in all_processed:
            for path in all_processed[group_key]:
                if os.path.exists(path):
                    os.remove(path)
        
        for i in range(1, num_groups + 1):
            group_info = groups_data.get(f'group_{i}', {})
            for path in group_info.get('video_paths', []):
                if os.path.exists(path):
                    os.remove(path)
        
        await callback.message.answer(
            f"🎉 Processing complete!\n\n"
            f"Created {combined_count} combined video(s).\n\n"
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
            for video_id in all_ids:
                await update_video_status(session, video_id, "failed")
    
    await state.clear()
