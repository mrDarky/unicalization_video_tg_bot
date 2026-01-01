"""
Demo script showing the multi-language flow
This demonstrates how language selection works in the bot
"""
from locales import get_text
from bot.keyboards import language_selection_keyboard, main_menu_keyboard


def demo_language_flow():
    """Demonstrate the language selection flow"""
    print("=" * 70)
    print("MULTI-LANGUAGE BOT FLOW DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Step 1: User starts bot
    print("📱 USER ACTION: /start")
    print("-" * 70)
    print()
    print("🤖 BOT RESPONSE:")
    print(get_text("en", "select_language"))
    print()
    lang_kb = language_selection_keyboard()
    print("   Inline Keyboard:")
    for row in lang_kb.inline_keyboard:
        for btn in row:
            print(f"   [{btn.text}]  (callback: {btn.callback_data})")
    print()
    
    # Step 2a: User selects English
    print("=" * 70)
    print("📱 USER ACTION: Clicks '🇬🇧 English'")
    print("-" * 70)
    print()
    print("🤖 BOT RESPONSE:")
    print(get_text("en", "language_selected"))
    print()
    print(get_text("en", "welcome", name="John"))
    print()
    en_kb = main_menu_keyboard("en")
    print("   Main Menu Keyboard:")
    for row in en_kb.keyboard:
        row_text = " | ".join([btn.text for btn in row])
        print(f"   {row_text}")
    print()
    
    # Step 2b: Alternative - User selects Russian
    print("=" * 70)
    print("📱 ALTERNATIVE: User clicks '🇷🇺 Русский'")
    print("-" * 70)
    print()
    print("🤖 BOT RESPONSE:")
    print(get_text("ru", "language_selected"))
    print()
    print(get_text("ru", "welcome", name="Иван"))
    print()
    ru_kb = main_menu_keyboard("ru")
    print("   Main Menu Keyboard:")
    for row in ru_kb.keyboard:
        row_text = " | ".join([btn.text for btn in row])
        print(f"   {row_text}")
    print()
    
    # Step 3: Show language change
    print("=" * 70)
    print("📱 USER ACTION: Later clicks '🌍 Language' button")
    print("-" * 70)
    print()
    print("🤖 BOT RESPONSE:")
    print(get_text("en", "select_language"))
    print()
    print("   User can now switch to another language anytime!")
    print()
    
    # Step 4: Show other translated features
    print("=" * 70)
    print("EXAMPLES OF TRANSLATED MESSAGES")
    print("=" * 70)
    print()
    
    print("📊 Statistics (English):")
    print("-" * 70)
    print(get_text("en", "statistics_text",
                  telegram_id=123456,
                  member_since="2024-01-01",
                  total_videos=10,
                  completed=8,
                  processing=1,
                  pending=1,
                  balance=25.50))
    print()
    
    print("📊 Statistics (Russian):")
    print("-" * 70)
    print(get_text("ru", "statistics_text",
                  telegram_id=123456,
                  member_since="2024-01-01",
                  total_videos=10,
                  completed=8,
                  processing=1,
                  pending=1,
                  balance=25.50))
    print()
    
    print("🎬 Mode 1 Instructions (English):")
    print("-" * 70)
    print(get_text("en", "mode1_send_video", max_size=100))
    print()
    
    print("🎬 Mode 1 Instructions (Russian):")
    print("-" * 70)
    print(get_text("ru", "mode1_send_video", max_size=100))
    print()
    
    print("=" * 70)
    print("✅ DEMONSTRATION COMPLETE")
    print("=" * 70)
    print()
    print("Summary:")
    print("  • Users can select language on first /start")
    print("  • Language preference is saved to database")
    print("  • All main menu items are translated")
    print("  • Users can change language anytime via 🌍 button")
    print("  • Both English and Russian fully supported")
    print("  • Easy to add more languages (see MULTILANG.md)")
    print()


if __name__ == "__main__":
    demo_language_flow()
