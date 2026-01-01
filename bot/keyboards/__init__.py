from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from locales import get_text


def language_selection_keyboard() -> InlineKeyboardMarkup:
    """Language selection keyboard"""
    keyboard = [
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def main_menu_keyboard(language: str = "en") -> ReplyKeyboardMarkup:
    """Main menu keyboard"""
    keyboard = [
        [KeyboardButton(text=get_text(language, "btn_process_1_video")), 
         KeyboardButton(text=get_text(language, "btn_process_2_videos"))],
        [KeyboardButton(text=get_text(language, "btn_statistics")), 
         KeyboardButton(text=get_text(language, "btn_balance"))],
        [KeyboardButton(text=get_text(language, "btn_referrals")), 
         KeyboardButton(text=get_text(language, "btn_help"))],
        [KeyboardButton(text=get_text(language, "btn_language"))]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def mode_selection_keyboard() -> InlineKeyboardMarkup:
    """Mode selection keyboard"""
    keyboard = [
        [InlineKeyboardButton(text="Mode 1: Single Video", callback_data="mode_1")],
        [InlineKeyboardButton(text="Mode 2: Two Videos", callback_data="mode_2")],
        [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def video_modifications_keyboard() -> InlineKeyboardMarkup:
    """Video modification options keyboard"""
    keyboard = [
        [InlineKeyboardButton(text="⚡ Change Speed", callback_data="mod_speed")],
        [InlineKeyboardButton(text="📐 Scale/Resize", callback_data="mod_scale")],
        [InlineKeyboardButton(text="🎨 Apply Filter", callback_data="mod_filter")],
        [InlineKeyboardButton(text="✂️ Crop", callback_data="mod_crop")],
        [InlineKeyboardButton(text="🔄 Rotate", callback_data="mod_rotate")],
        [InlineKeyboardButton(text="📝 Add Text", callback_data="mod_text")],
        [InlineKeyboardButton(text="⏱️ Trim/Cut", callback_data="mod_trim")],
        [InlineKeyboardButton(text="✅ Done", callback_data="mod_done")],
        [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def filter_selection_keyboard() -> InlineKeyboardMarkup:
    """Filter selection keyboard"""
    keyboard = [
        [InlineKeyboardButton(text="🌈 Hue", callback_data="filter_hue")],
        [InlineKeyboardButton(text="☀️ Brightness", callback_data="filter_brightness")],
        [InlineKeyboardButton(text="🔆 Contrast", callback_data="filter_contrast")],
        [InlineKeyboardButton(text="🎨 Saturation", callback_data="filter_saturation")],
        [InlineKeyboardButton(text="💫 Blur", callback_data="filter_blur")],
        [InlineKeyboardButton(text="✨ Sharpen", callback_data="filter_sharpen")],
        [InlineKeyboardButton(text="⚫ Grayscale", callback_data="filter_grayscale")],
        [InlineKeyboardButton(text="📜 Sepia", callback_data="filter_sepia")],
        [InlineKeyboardButton(text="🔄 Negative", callback_data="filter_negative")],
        [InlineKeyboardButton(text="📺 Noise", callback_data="filter_noise")],
        [InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_mods")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def merge_layout_keyboard() -> InlineKeyboardMarkup:
    """Merge layout selection keyboard"""
    keyboard = [
        [InlineKeyboardButton(text="➡️ Horizontal (Side by Side)", callback_data="merge_horizontal")],
        [InlineKeyboardButton(text="⬇️ Vertical (Top to Bottom)", callback_data="merge_vertical")],
        [InlineKeyboardButton(text="▶️ Sequential (One after Another)", callback_data="merge_sequential")],
        [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def confirm_keyboard() -> InlineKeyboardMarkup:
    """Confirmation keyboard"""
    keyboard = [
        [InlineKeyboardButton(text="✅ Yes", callback_data="confirm_yes")],
        [InlineKeyboardButton(text="❌ No", callback_data="confirm_no")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def cancel_keyboard() -> InlineKeyboardMarkup:
    """Cancel keyboard"""
    keyboard = [
        [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
