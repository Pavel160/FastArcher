from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from app.bot.utils.send_photo import send_photo
from app.bot.keyboards import main_menu
from app.bot.api_clients.user_client import api_logout_user


#  Выход
async def logout_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает выход пользователя из системы (Logout)."""
    query = update.callback_query
    await query.answer()
    await send_photo(update, context, name="sok_glaz_2")
    telegram_id = query.from_user.id

    try:
        result = await api_logout_user(telegram_id)
        await query.message.reply_text(f"✅ {result['message']}", reply_markup=main_menu())
    except ValueError as e:
        await query.message.reply_text(f"⚠️ {e}", reply_markup=main_menu())
    return ConversationHandler.END
