from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from app.bot.utils.send_photo import send_photo
from app.bot.keyboards import main_menu


#  Отмена
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик отмены.
    Завершает текущий диалог и возвращает пользователя в главное меню.
    """
    if update.callback_query:
        await update.callback_query.answer()
        await send_photo(update, context, name="sok_glaz_3")
        await update.callback_query.message.reply_text("❌ Действие отменено.", reply_markup=main_menu())
    elif update.message:
        await update.message.reply_text("❌ Действие отменено.", reply_markup=main_menu())
    return ConversationHandler.END
