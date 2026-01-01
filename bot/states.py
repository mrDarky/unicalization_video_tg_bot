from aiogram.fsm.state import State, StatesGroup


class LanguageSelectionStates(StatesGroup):
    """States for language selection"""
    selecting_language = State()


class VideoProcessingStates(StatesGroup):
    """States for video processing"""
    # Mode 1: Single video
    waiting_for_video_mode1 = State()
    selecting_modifications_mode1 = State()
    waiting_for_modification_params = State()
    
    # Mode 2: Two videos
    waiting_for_video1_mode2 = State()
    waiting_for_video2_mode2 = State()
    selecting_modifications_video1 = State()
    selecting_modifications_video2 = State()
    selecting_merge_layout = State()
    
    # Common states
    processing = State()
    waiting_for_text_input = State()
    waiting_for_speed_input = State()
    waiting_for_scale_input = State()
    waiting_for_crop_input = State()
    waiting_for_rotate_input = State()
    waiting_for_trim_input = State()
