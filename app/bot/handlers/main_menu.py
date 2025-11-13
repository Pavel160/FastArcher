from app.bot.handlers.cancel import cancel
from app.bot.utils.send_photo import send_photo
from telegram import Update
from telegram.ext import ContextTypes
from app.bot.keyboards import home, main_menu

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главное меню. Устанавливает Reply Keyboard и показывает Inline Menu."""
    text = (
        "👋 Привет! Добро пожаловать в бот для тренировок с луком.\n"
        "Выберите действие ниже:"
    )
    
    await send_photo(update, context, name="sok_glaz_1")
    await update.message.reply_text(
        text,
        reply_markup=home()
    )
    await update.message.reply_text(
        "Используйте кнопки для навигации:",
        reply_markup=main_menu()
    )


async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает кнопки главного меню"""
    query = update.callback_query
    await query.answer()
    data = query.data.replace("menu_", "")

    if data == "cancel":
        return await cancel(update, context)


async def fallback_message(update, context):
    """Отвечает, если сообщение не относится к активному диалогу."""
    await update.message.reply_text(
        "🤔 Я не понял ваше сообщение.\n"
        "Пожалуйста, используйте кнопки меню ниже 👇",
        reply_markup=main_menu()
    )
