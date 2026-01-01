from aiogram.fsm.state import State, StatesGroup


class LanguageSelectionStates(StatesGroup):
    """States for language selection"""
    selecting_language = State()


class VideoProcessingStates(StatesGroup):
    """States for video processing"""
    # Mode 1: Single video - NEW FLOW (filters first, then multiple videos)
    selecting_modifications_mode1 = State()
    waiting_for_videos_mode1 = State()
    
    # Mode 2: Two video groups - NEW FLOW (filters per group, then multiple videos per group)
    selecting_modifications_video1 = State()
    waiting_for_videos_group1 = State()
    selecting_modifications_video2 = State()
    waiting_for_videos_group2 = State()
    selecting_merge_strategy = State()
    selecting_merge_layout = State()
    
    # Mode N: Multiple video groups - NEW FLOW (n groups with filters)
    selecting_num_groups = State()
    selecting_modifications_group = State()
    waiting_for_videos_group = State()
    selecting_combine_strategy = State()
    
    # Common states
    processing = State()
    waiting_for_text_input = State()
    waiting_for_speed_input = State()
    waiting_for_scale_input = State()
    waiting_for_crop_input = State()
    waiting_for_rotate_input = State()
    waiting_for_trim_input = State()
