"""
Translations for the bot - English and Russian
"""

TRANSLATIONS = {
    "en": {
        # Language selection
        "select_language": "🌍 Please select your language:",
        "language_selected": "✅ Language set to English",
        
        # Welcome/Start
        "welcome": "👋 Welcome, {name}!\n\n🎬 This bot helps you unicalize (make unique) your videos!\n\nChoose what you want to do:\n• Process 1 Video - Apply modifications to a single video\n• Process 2 Videos - Modify and merge two videos\n\nUse the buttons below to get started!",
        
        # Main menu buttons
        "btn_process_1_video": "🎬 Process 1 Video",
        "btn_process_2_videos": "🎥 Process 2 Videos",
        "btn_statistics": "📊 My Statistics",
        "btn_balance": "💰 Balance",
        "btn_referrals": "👥 Referrals",
        "btn_help": "ℹ️ Help",
        "btn_language": "🌍 Language",
        
        # Help
        "help_text": "🔍 <b>How to use this bot:</b>\n\n<b>Mode 1: Single Video</b>\n1. Click '🎬 Process 1 Video'\n2. Send your video file\n3. Choose modifications (speed, scale, filters, etc.)\n4. Get your unicalized video!\n\n<b>Mode 2: Two Videos</b>\n1. Click '🎥 Process 2 Videos'\n2. Send first video\n3. Send second video\n4. Choose modifications for each\n5. Select merge layout\n6. Get your combined video!\n\n<b>Available Modifications:</b>\n⚡ Speed - Change playback speed\n📐 Scale - Resize video dimensions\n🎨 Filters - Apply visual effects\n✂️ Crop - Cut parts of the video\n🔄 Rotate - Rotate the video\n📝 Text - Add text overlay\n⏱️ Trim - Cut video length\n\nFor support: @YourSupportChannel",
        
        # Statistics
        "statistics_text": "📊 <b>Your Statistics</b>\n\n👤 User ID: {telegram_id}\n📅 Member since: {member_since}\n\n🎬 Total videos: {total_videos}\n✅ Completed: {completed}\n⏳ Processing: {processing}\n⏸️ Pending: {pending}\n\n💰 Balance: ${balance:.2f}",
        
        # Balance
        "balance_text": "💰 <b>Your Balance</b>\n\nCurrent balance: ${balance:.2f}\n\nUse /deposit to add funds\nUse /withdraw to withdraw funds",
        
        # Referrals
        "referral_text": "👥 <b>Referral Program</b>\n\nYour referral link:\n<code>{referral_link}</code>\n\nShare this link with friends and earn bonuses!\n\nTotal referrals: {total_referrals}",
        
        # Mode 1
        "mode1_send_video": "🎬 <b>Mode 1: Single Video Processing</b>\n\nPlease send me the video you want to unicalize.\n\nSupported formats: MP4, AVI, MOV, MKV\nMax size: {max_size}MB",
        
        # Mode 2
        "mode2_send_video1": "🎥 <b>Mode 2: Two Video Processing</b>\n\nPlease send me the <b>first</b> video.\n\nSupported formats: MP4, AVI, MOV, MKV\nMax size: {max_size}MB per video",
        
        # Inline buttons
        "btn_english": "🇬🇧 English",
        "btn_russian": "🇷🇺 Русский",
    },
    "ru": {
        # Language selection
        "select_language": "🌍 Пожалуйста, выберите язык:",
        "language_selected": "✅ Язык установлен на Русский",
        
        # Welcome/Start
        "welcome": "👋 Добро пожаловать, {name}!\n\n🎬 Этот бот помогает вам уникализировать (сделать уникальными) ваши видео!\n\nВыберите, что вы хотите сделать:\n• Обработать 1 видео - Применить изменения к одному видео\n• Обработать 2 видео - Изменить и объединить два видео\n\nИспользуйте кнопки ниже, чтобы начать!",
        
        # Main menu buttons
        "btn_process_1_video": "🎬 Обработать 1 видео",
        "btn_process_2_videos": "🎥 Обработать 2 видео",
        "btn_statistics": "📊 Моя статистика",
        "btn_balance": "💰 Баланс",
        "btn_referrals": "👥 Рефералы",
        "btn_help": "ℹ️ Помощь",
        "btn_language": "🌍 Язык",
        
        # Help
        "help_text": "🔍 <b>Как использовать этого бота:</b>\n\n<b>Режим 1: Одно видео</b>\n1. Нажмите '🎬 Обработать 1 видео'\n2. Отправьте свой видеофайл\n3. Выберите изменения (скорость, масштаб, фильтры и т.д.)\n4. Получите ваше уникализированное видео!\n\n<b>Режим 2: Два видео</b>\n1. Нажмите '🎥 Обработать 2 видео'\n2. Отправьте первое видео\n3. Отправьте второе видео\n4. Выберите изменения для каждого\n5. Выберите макет объединения\n6. Получите ваше комбинированное видео!\n\n<b>Доступные изменения:</b>\n⚡ Скорость - Изменить скорость воспроизведения\n📐 Масштаб - Изменить размер видео\n🎨 Фильтры - Применить визуальные эффекты\n✂️ Обрезка - Вырезать части видео\n🔄 Поворот - Повернуть видео\n📝 Текст - Добавить текстовый оверлей\n⏱️ Обрезка - Обрезать длину видео\n\nДля поддержки: @YourSupportChannel",
        
        # Statistics
        "statistics_text": "📊 <b>Ваша статистика</b>\n\n👤 ID пользователя: {telegram_id}\n📅 Участник с: {member_since}\n\n🎬 Всего видео: {total_videos}\n✅ Завершено: {completed}\n⏳ Обрабатывается: {processing}\n⏸️ Ожидает: {pending}\n\n💰 Баланс: ${balance:.2f}",
        
        # Balance
        "balance_text": "💰 <b>Ваш баланс</b>\n\nТекущий баланс: ${balance:.2f}\n\nИспользуйте /deposit для пополнения\nИспользуйте /withdraw для вывода средств",
        
        # Referrals
        "referral_text": "👥 <b>Реферальная программа</b>\n\nВаша реферальная ссылка:\n<code>{referral_link}</code>\n\nПоделитесь этой ссылкой с друзьями и зарабатывайте бонусы!\n\nВсего рефералов: {total_referrals}",
        
        # Mode 1
        "mode1_send_video": "🎬 <b>Режим 1: Обработка одного видео</b>\n\nПожалуйста, отправьте мне видео, которое вы хотите уникализировать.\n\nПоддерживаемые форматы: MP4, AVI, MOV, MKV\nМаксимальный размер: {max_size}МБ",
        
        # Mode 2
        "mode2_send_video1": "🎥 <b>Режим 2: Обработка двух видео</b>\n\nПожалуйста, отправьте мне <b>первое</b> видео.\n\nПоддерживаемые форматы: MP4, AVI, MOV, MKV\nМаксимальный размер: {max_size}МБ на видео",
        
        # Inline buttons
        "btn_english": "🇬🇧 English",
        "btn_russian": "🇷🇺 Русский",
    }
}


def get_text(language: str, key: str, **kwargs) -> str:
    """
    Get translated text for a given key in the specified language.
    
    Args:
        language: Language code (en, ru)
        key: Translation key
        **kwargs: Format arguments for the text
    
    Returns:
        Translated text with format arguments applied
    """
    # Default to English if language not found
    if language not in TRANSLATIONS:
        language = "en"
    
    # Get the text for the key
    text = TRANSLATIONS[language].get(key, TRANSLATIONS["en"].get(key, key))
    
    # Apply format arguments if provided
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    
    return text
