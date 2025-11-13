from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from app.bot.utils.send_photo import send_photo
from app.bot.keyboards import main_menu
from app.bot.api_clients.user_client import api_get_user, api_update_password, api_update_username


#  Профиль
async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Показывает текущий профиль пользователя и предлагает опции изменения.
    """
    query = update.callback_query
    await query.answer()
    await send_photo(update, context, name="sok_glaz_2")

    telegram_id = query.from_user.id

    try:
        user = await api_get_user(telegram_id=telegram_id)
    except ValueError as e:
        await query.message.reply_text(
            f"⚠️ Ошибка: {e}", reply_markup=main_menu()
        )
        return ConversationHandler.END


    message = (
        f"🧑‍💻 Профиль пользователя:\n"
        f"ID: {user['id']}\n"
        f"Имя: {user['username']}\n"
        f"Статус: {'✅ Активен' if user['is_active'] else '❌ Не активен'}"
    )

    keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✏️ Изменить имя", callback_data="change_name")],
            [InlineKeyboardButton("🔑 Изменить пароль", callback_data="change_password")],
        ])

    await query.message.reply_text(message, reply_markup=keyboard)
    return ConversationHandler.END


#  Изменение имени
async def change_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начинает поддиалог изменения имени пользователя."""
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Введите новое имя пользователя:")
    return "change_username"


async def new_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Принимает новое имя пользователя и вызывает API для его обновления."""
    new_username = update.message.text.strip()
    telegram_id = update.message.from_user.id

    try:
        result = await api_update_username(
            telegram_id=telegram_id,
            new_username=new_username
        )
        context.user_data["active_username"] = new_username
        await update.message.reply_text(
            f"✅ Имя изменено на: {result['username']}",
            reply_markup=main_menu()
        )
        return ConversationHandler.END
    except ValueError as e:
        await update.message.reply_text(f"⚠️ Ошибка: {e}")
        return "change_username"

#  Смена пароля
async def change_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начинает поддиалог смены пароля."""
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Введите новый пароль:")
    return "change_password"

async def new_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Принимает новый пароль и вызывает API для его обновления."""
    new_password = update.message.text.strip()
    telegram_id = update.message.from_user.id

    try:
        await api_update_password(
            telegram_id=telegram_id,
            new_password=new_password
        )
        await update.message.reply_text(
            "✅ Пароль успешно изменён",
            reply_markup=main_menu()
        )
        return ConversationHandler.END
    except ValueError as e:
        await update.message.reply_text(f"⚠️ Ошибка: {e}")
        return "change_password"

