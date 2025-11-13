from telegram import Message
from telegram import Update
from telegram.ext import ContextTypes


async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE, name: str) -> Message:
    """Отправляет изображение пользователю по его имени файла."""
    with open('app/bot/images/' + name + ".jpg", 'rb') as photo:
        return await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
