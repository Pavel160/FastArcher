from telegram import (
    InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, KeyboardButton
)


def main_menu():
    """Возвращает объект (Встроенная клавиатурная разметка) для главного меню бота."""
    keyboard = [
        [InlineKeyboardButton("📝 Регистрация", callback_data="menu_register")],
        [InlineKeyboardButton("🔐 Вход в приложение", callback_data="menu_login")],
        [InlineKeyboardButton("🚪 Выйти из системы", callback_data="menu_logout")],
        [InlineKeyboardButton("👤 Мой профиль", callback_data="menu_profile")],
        [InlineKeyboardButton("📂 Послать CSV", callback_data="menu_send_csv")],
        [InlineKeyboardButton("🎯 Статистика", callback_data="menu_stats")],
        [InlineKeyboardButton("❌ Отмена", callback_data="menu_cancel")],
    ]
    return InlineKeyboardMarkup(keyboard)

def home():
    """Возвращает (Кнопка клавиатуры) для кнопки домой🏠."""
    keyboard = [
        [KeyboardButton("🏠 Домой")]
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
