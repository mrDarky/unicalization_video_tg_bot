"""
Test script for multi-language support
This simulates the basic flow of language selection
"""
import asyncio
from unittest.mock import AsyncMock, MagicMock
from bot.handlers.basic import cmd_start, process_language_selection
from bot.keyboards import language_selection_keyboard, main_menu_keyboard
from locales import get_text


def test_translations():
    """Test that translations work correctly"""
    print("Testing translations...")
    
    # Test English
    en_welcome = get_text('en', 'welcome', name='John')
    assert 'Welcome, John!' in en_welcome
    assert 'unicalize' in en_welcome
    
    # Test Russian
    ru_welcome = get_text('ru', 'welcome', name='Иван')
    assert 'Добро пожаловать, Иван!' in ru_welcome
    assert 'уникализировать' in ru_welcome
    
    # Test all keys exist in both languages
    from locales.translations import TRANSLATIONS
    en_keys = set(TRANSLATIONS['en'].keys())
    ru_keys = set(TRANSLATIONS['ru'].keys())
    
    missing_in_ru = en_keys - ru_keys
    missing_in_en = ru_keys - en_keys
    
    if missing_in_ru:
        print(f"⚠️  Keys missing in Russian: {missing_in_ru}")
    if missing_in_en:
        print(f"⚠️  Keys missing in English: {missing_in_en}")
    
    assert en_keys == ru_keys, "Language keys must match"
    
    print("✅ All translation tests passed!")


def test_keyboards():
    """Test that keyboards are created correctly"""
    print("Testing keyboards...")
    
    # Test language selection keyboard
    lang_kb = language_selection_keyboard()
    assert len(lang_kb.inline_keyboard) == 2  # English and Russian buttons
    
    # Test main menu keyboard with English
    en_kb = main_menu_keyboard('en')
    assert len(en_kb.keyboard) == 4  # 4 rows of buttons
    en_text = str(en_kb.keyboard)
    assert 'Process 1 Video' in en_text
    
    # Test main menu keyboard with Russian
    ru_kb = main_menu_keyboard('ru')
    assert len(ru_kb.keyboard) == 4  # 4 rows of buttons
    ru_text = str(ru_kb.keyboard)
    assert 'Обработать 1 видео' in ru_text
    
    print("✅ All keyboard tests passed!")


def test_database_model():
    """Test that User model has language field"""
    print("Testing database model...")
    
    from database.models import User
    from sqlalchemy import inspect
    
    # Get columns
    mapper = inspect(User)
    columns = [col.key for col in mapper.columns]
    
    assert 'language' in columns, "User model must have 'language' column"
    
    # Check default value
    language_col = mapper.columns['language']
    assert language_col.default is not None or language_col.server_default is not None
    
    print("✅ Database model test passed!")


def test_crud_functions():
    """Test that CRUD functions exist"""
    print("Testing CRUD functions...")
    
    from database.crud import update_user_language, get_or_create_user
    
    # Just check they exist and are callable
    assert callable(update_user_language)
    assert callable(get_or_create_user)
    
    print("✅ CRUD functions test passed!")


def test_states():
    """Test that language selection state exists"""
    print("Testing states...")
    
    from bot.states import LanguageSelectionStates
    
    assert hasattr(LanguageSelectionStates, 'selecting_language')
    
    print("✅ States test passed!")


if __name__ == "__main__":
    print("=" * 50)
    print("Multi-Language Support Test Suite")
    print("=" * 50)
    print()
    
    try:
        test_translations()
        print()
        test_keyboards()
        print()
        test_database_model()
        print()
        test_crud_functions()
        print()
        test_states()
        print()
        print("=" * 50)
        print("✅ ALL TESTS PASSED!")
        print("=" * 50)
    except AssertionError as e:
        print()
        print("=" * 50)
        print(f"❌ TEST FAILED: {e}")
        print("=" * 50)
        exit(1)
    except Exception as e:
        print()
        print("=" * 50)
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("=" * 50)
        exit(1)
