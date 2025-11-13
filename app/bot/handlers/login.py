from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from app.bot.utils.send_photo import send_photo
from app.bot.keyboards import main_menu
from app.bot.api_clients.user_client import api_login_user


#  Вход
async def start_login(update, context):
    """Начинает диалог входа и запрашивает имя пользователя."""
    query = update.callback_query
    await query.answer()
    await send_photo(update, context, name="sok_glaz_2")
    await query.message.reply_text("Введите имя пользователя:")
    return "login_username"


async def login_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получает имя пользователя и запрашивает пароль."""
    username = update.message.text.strip()
    if not username:
        await update.message.reply_text("Имя не может быть пустым. Введите снова:")
        return "login_username"

    context.user_data["username"] = username
    await update.message.reply_text("Введите пароль 🔐:")
    return "login_password"


async def login_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получает пароль, вызывает API для входа и завершает диалог или возвращает к началу."""
    password = update.message.text.strip()
    context.user_data["password"] = password
    telegram_id = update.message.from_user.id

    try:
        result = await api_login_user(
            username=context.user_data["username"],
            password=context.user_data["password"],
            telegram_id=telegram_id)

        await update.message.reply_text(f"✅ {result['message']}", reply_markup=main_menu())
        return ConversationHandler.END
    except ValueError as e:
        await update.message.reply_text(f"⚠️ Ошибка: {e}")
        return "login_username"
