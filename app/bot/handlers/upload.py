from app.bot.utils.send_photo import send_photo
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from app.bot.keyboards import main_menu
from app.bot.api_clients.uploud_client import api_upload_csv


#  Загрузка CSV
async def start_upload(update, context):
    """
    Начинает диалог загрузки CSV, запрашивая у пользователя файл.
    """
    query = update.callback_query
    await query.answer()
    await send_photo(update, context, name="sok_glaz_2")
    await query.message.reply_text("📄 Отправьте CSV-файл для загрузки:")
    return "upload_file"


async def upload_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Получает файл, проверяет его, аутентифицирует пользователя и отправляет
    данные в API для обработки.
    """
    document = update.message.document
    telegram_id = update.effective_user.id

    if not document or not document.file_name.endswith(".csv"):
        await update.message.reply_text("❌ Пожалуйста, отправьте CSV-файл.")
        return "upload_file"

    file = await document.get_file()
    file_data = await file.download_as_bytearray()

    try:
        result = await api_upload_csv(
            file_data=file_data,
            filename=document.file_name,
            telegram_id=telegram_id
        )
        await update.message.reply_text(
            result.get("message", "✅ Файл успешно загружен!"),reply_markup=main_menu())
        return ConversationHandler.END
    except ValueError as e:
        await update.message.reply_text(f"⚠️ Ошибка: {e}")
        return "upload_file"
