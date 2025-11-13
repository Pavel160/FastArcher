from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from app.bot.utils.send_photo import send_photo
from app.bot.keyboards import main_menu
from app.bot.api_clients.user_client import api_register_user, api_verify_user


#  Регистрация
async def start_register(update, context):
    """Начинает диалог регистрации и запрашивает имя пользователя."""
    query = update.callback_query
    await query.answer()
    await send_photo(update, context, name="sok_glaz_2")
    await query.message.reply_text("Введите имя пользователя:")
    return "register_username"


async def register_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получает имя пользователя и запрашивает пароль."""
    username = update.message.text.strip()
    if not username:
        await update.message.reply_text("Имя не может быть пустым. Введите снова:")
        return "register_username"

    context.user_data["username"] = username
    await update.message.reply_text("Введите пароль 🔐:")
    return "register_password"


async def register_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получает пароль, вызывает API для регистрации и запрашивает код верификации."""
    password = update.message.text.strip()
    if not password:
        await update.message.reply_text("Пароль не может быть пустым. Введите снова:")
        return "register_password"

    context.user_data["password"] = password
    telegram_id = update.message.from_user.id

    try:
        result = await api_register_user(
        username=context.user_data["username"],
        password=context.user_data["password"],
        telegram_id=telegram_id)

        verification_code = result.get("verification_code")
        await update.message.reply_text(
            f"✅ {result['message']}\n"
            f"Код подтверждения: `{verification_code}`\n\n"
            f"Введите код для активации:",
            parse_mode="Markdown"
        )
        return "register_verify"

    except ValueError as e:
        await update.message.reply_text(f"⚠️ Ошибка регистрации: {e}")
        return ConversationHandler.END


async def register_verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получает код верификации, вызывает API для активации и завершает диалог."""
    username=context.user_data["username"]
    telegram_id = update.message.from_user.id
    code = update.message.text.strip()

    try:
        result = await api_verify_user(
            username=username,
            telegram_id=telegram_id,
            code=code
        )
        await update.message.reply_text(f"✅ {result['message']}", reply_markup=main_menu())
        return ConversationHandler.END
    except ValueError as e:
        await update.message.reply_text(f"⚠️ Ошибка: {e}")
        return "register_verify"
