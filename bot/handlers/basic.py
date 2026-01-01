from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.keyboards import main_menu_keyboard, mode_selection_keyboard, language_selection_keyboard, video_modifications_keyboard, num_groups_keyboard
from database.database import async_session_maker
from database.crud import get_or_create_user, get_user_videos, get_statistics, update_user_language, get_user_by_telegram_id, get_user_referrals_count
from config import settings
from locales import get_text
from bot.states import LanguageSelectionStates

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Handle /start command"""
    await state.clear()
    
    async with async_session_maker() as session:
        user_before = await get_user_by_telegram_id(session, message.from_user.id)
        is_new_user = user_before is None
        
        user = await get_or_create_user(
            session,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )
    
    # Show language selection only for new users
    if is_new_user:
        await state.set_state(LanguageSelectionStates.selecting_language)
        await message.answer(
            get_text("en", "select_language"),
            reply_markup=language_selection_keyboard()
        )
    else:
        # Show welcome message with user's language
        welcome_text = get_text(user.language, "welcome", name=message.from_user.first_name)
        await message.answer(welcome_text, reply_markup=main_menu_keyboard(user.language))


@router.callback_query(F.data.startswith("lang_"))
async def process_language_selection(callback: CallbackQuery, state: FSMContext):
    """Handle language selection"""
    language = callback.data.split("_")[1]  # Extract 'en' or 'ru' from 'lang_en' or 'lang_ru'
    
    async with async_session_maker() as session:
        await update_user_language(session, callback.from_user.id, language)
        user = await get_or_create_user(
            session,
            telegram_id=callback.from_user.id,
            username=callback.from_user.username
        )
    
    await state.clear()
    
    # Send confirmation
    await callback.message.edit_text(get_text(language, "language_selected"))
    
    # Show welcome message
    welcome_text = get_text(language, "welcome", name=callback.from_user.first_name)
    await callback.message.answer(welcome_text, reply_markup=main_menu_keyboard(language))
    
    await callback.answer()


@router.message(F.text.in_(["🌍 Language", "🌍 Язык"]))
async def change_language(message: Message, state: FSMContext):
    """Handle language change request"""
    await state.set_state(LanguageSelectionStates.selecting_language)
    await message.answer(
        get_text("en", "select_language"),
        reply_markup=language_selection_keyboard()
    )


@router.message(Command("help"))
@router.message(F.text.in_(["ℹ️ Help", "ℹ️ Помощь"]))
async def cmd_help(message: Message):
    """Handle /help command"""
    async with async_session_maker() as session:
        user = await get_or_create_user(
            session,
            telegram_id=message.from_user.id,
            username=message.from_user.username
        )
    
    help_text = get_text(user.language, "help_text")
    await message.answer(help_text, parse_mode="HTML")


@router.message(F.text.in_(["📊 My Statistics", "📊 Моя статистика"]))
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
    
    stats_text = get_text(
        user.language,
        "statistics_text",
        telegram_id=user.telegram_id,
        member_since=user.created_at.strftime('%Y-%m-%d'),
        total_videos=len(videos),
        completed=completed_videos,
        processing=processing_videos,
        pending=pending_videos,
        balance=user.balance
    )
    
    await message.answer(stats_text, parse_mode="HTML")


@router.message(F.text.in_(["💰 Balance", "💰 Баланс"]))
async def show_balance(message: Message):
    """Show user balance"""
    async with async_session_maker() as session:
        user = await get_or_create_user(
            session,
            telegram_id=message.from_user.id,
            username=message.from_user.username
        )
    
    balance_text = get_text(user.language, "balance_text", balance=user.balance)
    await message.answer(balance_text, parse_mode="HTML")


@router.message(F.text.in_(["👥 Referrals", "👥 Рефералы"]))
async def show_referrals(message: Message):
    """Show referral information"""
    async with async_session_maker() as session:
        user = await get_or_create_user(
            session,
            telegram_id=message.from_user.id,
            username=message.from_user.username
        )
        
        # Get referrals count within the session context
        total_referrals = await get_user_referrals_count(session, user.id)
        language = user.language
        telegram_id = user.telegram_id
    
    # Get bot username for referral link
    bot_username = (await message.bot.me()).username
    referral_link = f"https://t.me/{bot_username}?start=ref_{telegram_id}"
    
    referral_text = get_text(
        language,
        "referral_text",
        referral_link=referral_link,
        total_referrals=total_referrals
    )
    
    await message.answer(referral_text, parse_mode="HTML")


@router.message(F.text.in_(["🎬 Process 1 Video", "🎬 Обработать 1 видео"]))
async def mode_1_handler(message: Message, state: FSMContext):
    """Handle Mode 1: Single video processing - NEW FLOW"""
    from bot.states import VideoProcessingStates
    
    async with async_session_maker() as session:
        user = await get_or_create_user(
            session,
            telegram_id=message.from_user.id,
            username=message.from_user.username
        )
    
    await state.update_data(mode='mode1', modifications=[])
    await state.set_state(VideoProcessingStates.selecting_modifications_mode1)
    
    mode1_text = get_text(user.language, "mode1_configure_filters")
    if mode1_text == "mode1_configure_filters":  # Fallback if translation missing
        mode1_text = (
            "🎬 <b>Mode 1: Process Multiple Videos with Same Settings</b>\n\n"
            "<b>Step 1:</b> Configure the modifications/filters you want to apply.\n"
            "<b>Step 2:</b> Upload one or more videos.\n"
            "All videos will be processed with the same settings!\n\n"
            "Let's start by selecting the modifications:"
        )
    
    await message.answer(
        mode1_text,
        parse_mode="HTML",
        reply_markup=video_modifications_keyboard()
    )


@router.message(F.text.in_(["🎥 Process 2 Videos", "🎥 Обработать 2 видео"]))
async def mode_2_handler(message: Message, state: FSMContext):
    """Handle Mode 2: Two video groups processing - NEW FLOW"""
    from bot.states import VideoProcessingStates
    
    async with async_session_maker() as session:
        user = await get_or_create_user(
            session,
            telegram_id=message.from_user.id,
            username=message.from_user.username
        )
    
    await state.update_data(mode='mode2', modifications1=[], modifications2=[])
    await state.set_state(VideoProcessingStates.selecting_modifications_video1)
    
    mode2_text = get_text(user.language, "mode2_configure_filters")
    if mode2_text == "mode2_configure_filters":  # Fallback if translation missing
        mode2_text = (
            "🎥 <b>Mode 2: Process Two Video Groups and Merge</b>\n\n"
            "<b>Step 1:</b> Configure modifications for Group 1 videos\n"
            "<b>Step 2:</b> Upload one or more videos for Group 1\n"
            "<b>Step 3:</b> Configure modifications for Group 2 videos\n"
            "<b>Step 4:</b> Upload one or more videos for Group 2\n"
            "<b>Step 5:</b> Choose how to combine them (first-with-first, all-with-all, sequential)\n"
            "<b>Step 6:</b> Select layout (horizontal, vertical, sequential)\n\n"
            "Let's start by configuring <b>Group 1</b> modifications:"
        )
    
    await message.answer(
        mode2_text,
        parse_mode="HTML",
        reply_markup=video_modifications_keyboard()
    )


@router.message(F.text == "🎞️ Process N Videos")
async def mode_n_handler(message: Message, state: FSMContext):
    """Handle Mode N: Multiple video groups processing - NEW"""
    from bot.states import VideoProcessingStates
    
    async with async_session_maker() as session:
        user = await get_or_create_user(
            session,
            telegram_id=message.from_user.id,
            username=message.from_user.username
        )
    
    await state.set_state(VideoProcessingStates.selecting_num_groups)
    
    await message.answer(
        "🎞️ <b>Mode N: Process Multiple Video Groups</b>\n\n"
        "This mode allows you to process 3, 4, or 5 video groups, "
        "each with its own modifications/filters and multiple videos.\n\n"
        "Then you can combine them using various strategies!\n\n"
        "How many video groups do you want to create?",
        parse_mode="HTML",
        reply_markup=num_groups_keyboard()
    )
