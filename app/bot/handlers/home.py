from app.bot.keyboards import main_menu
from app.bot.utils.send_photo import send_photo
from telegram import Update
from telegram.ext import ContextTypes


async def home_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает кнопку 'Домой'"""
    text = ("👋 Вы вернулись в главное меню. Выберите, что вас интересует:")
    await send_photo(update, context, name="sok_glaz_1")
    await update.message.reply_text(text, reply_markup=main_menu())
