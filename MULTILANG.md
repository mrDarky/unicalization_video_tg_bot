# Multi-Language Support

This bot now supports multiple languages (English and Russian).

## Features

- Language selection at first bot start
- Ability to change language anytime via the "🌍 Language" button
- Main menu buttons and core messages translated
- Language preference stored in database

## Supported Languages

- 🇬🇧 English (`en`)
- 🇷🇺 Russian (`ru`)

## How to Add More Languages

1. Open `locales/translations.py`
2. Add a new language code to the `TRANSLATIONS` dictionary (e.g., `"es"` for Spanish)
3. Copy the structure from `"en"` or `"ru"` and translate all strings
4. The language will automatically be available

Example:
```python
TRANSLATIONS = {
    "en": { ... },
    "ru": { ... },
    "es": {  # Spanish
        "select_language": "🌍 Por favor, seleccione su idioma:",
        "welcome": "👋 ¡Bienvenido, {name}!...",
        # ... more translations
    }
}
```

5. Update `language_selection_keyboard()` in `bot/keyboards/__init__.py` to include the new language button:
```python
[InlineKeyboardButton(text="🇪🇸 Español", callback_data="lang_es")]
```

## Usage

When a user starts the bot for the first time:
1. They see a language selection menu
2. They choose their preferred language
3. All subsequent interactions use their selected language

Users can change their language at any time by clicking the "🌍 Language" button in the main menu.

## Database Migration

If you have an existing database, run the migration script to add the language column:

```bash
python migrate_language.py
```

This will:
- Add the `language` column to the `users` table
- Set default language to English for existing users

## Files Modified

- `database/models.py` - Added `language` field to User model
- `database/crud.py` - Added `update_user_language()` function
- `locales/translations.py` - New file with all translations
- `bot/handlers/basic.py` - Updated to use translations
- `bot/keyboards/__init__.py` - Updated to support multiple languages
- `bot/states.py` - Added `LanguageSelectionStates`

## Future Improvements

The following areas can be enhanced with translations in the future:
- Video processing messages (error messages, confirmations)
- Modification selection menus
- Filter names and descriptions
- Admin panel messages
