from app.bot.api_clients.stats_client import (
    api_get_average_score, api_get_best_session,
    api_get_last_session_date, api_get_total_sessions,
    api_get_total_shots
)
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from app.bot.utils.send_photo import send_photo
from app.bot.keyboards import main_menu
from app.bot.api_clients.user_client import api_get_user


async def stats_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик для кнопки 🎯 Статистика"""
    query = update.callback_query
    await query.answer()
    await send_photo(update, context, name="sok_glaz_2")

    telegram_id = query.from_user.id

    try:
        user = await api_get_user(telegram_id=telegram_id)
        context.user_data["user_id"] = user["id"]
    except ValueError as e:
        await query.message.reply_text(f"⚠️ Ошибка: {e}", reply_markup=main_menu())
        return ConversationHandler.END

    message = (
        f"🧑‍💻 Профиль пользователя:\n"
        f"ID: {user['id']}\n"
        f"Имя: {user['username']}\n"
        f"Статус: {'✅ Активен' if user['is_active'] else '❌ Не активен'}"
    )

    keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📊 Всего сессий", callback_data="total_sessions")],
            [InlineKeyboardButton("🎯 Средний счёт", callback_data="average_score")],
            [InlineKeyboardButton("🏹 Всего выстрелов", callback_data="total_shots")],
            [InlineKeyboardButton("🥇 Лучшая сессия", callback_data="best_session")],
            [InlineKeyboardButton("📅 Последняя тренировка", callback_data="last_practice")],
        ])

    await query.message.reply_text(message, reply_markup=keyboard)
    return "stats_handler"


async def total_sessions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик для кнопки '📊 Всего сессий'."""
    query = update.callback_query
    await query.answer()
    user_id = context.user_data.get("user_id")

    try:
        data = await api_get_total_sessions(user_id=user_id)
        
        text = (
            f"📊 **ВСЕГО СЕССИЙ**\n"
            f"➖➖➖➖➖➖➖➖➖➖\n"
            f"• Количество тренировочных сессий: **{data['total_sessions']}**\n"
            f"• Количество тренировочных дней: **{data['total_days']}**"
        )
        
        await query.message.reply_text(text, parse_mode='Markdown')

    except ValueError as e:
        await query.message.reply_text(f"❌ Ошибка: {e}")
        return "stats_handler"


async def average_score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик для кнопки '🎯 Средний счёт'."""
    query = update.callback_query
    await query.answer()
    user_id = context.user_data.get("user_id")

    try:
        data = await api_get_average_score(user_id=user_id)
        
        text = (
            f"🎯 **СРЕДНИЙ СЧЁТ**\n"
            f"➖➖➖➖➖➖➖➖➖➖\n"
            f"• Ваш средний счёт: **{data['average_score']:.2f}**"
        )
        await query.message.reply_text(text, parse_mode='Markdown')

    except ValueError as e:
        await query.message.reply_text(f"❌ Ошибка: {e}")
        return "stats_handler"


async def total_shots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик для кнопки '🏹 Всего выстрелов'."""
    query = update.callback_query
    await query.answer()
    user_id = context.user_data.get("user_id")
    try:
        data = await api_get_total_shots(user_id=user_id)
        
        text = (
            f"🏹 **ВСЕГО ВЫСТРЕЛОВ**\n"
            f"➖➖➖➖➖➖➖➖➖➖\n"
            f"• Общее количество выстрелов: **{data['total_shots']:,}**\n"
            f"• Количество дней по выстрелам: **{data['total_days_shots']}**"
        )
        await query.message.reply_text(text, parse_mode='Markdown')

    except ValueError as e:
        await query.message.reply_text(f"❌ Ошибка: {e}")
        return "stats_handler"


async def best_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик для кнопки '🥇 Лучшая сессия'."""
    query = update.callback_query
    await query.answer()
    user_id = context.user_data.get("user_id")
    try:
        data = await api_get_best_session(user_id=user_id)
        
        text = (
            f"🥇 **ЛУЧШАЯ СЕССИЯ**\n"
            f"➖➖➖➖➖➖➖➖➖➖\n"
            f"• Лучший счёт: **{data['best_score']:.2f}**\n"
            f"• Дата: **{data['date']}**"
        )
        await query.message.reply_text(text, parse_mode='Markdown')

    except ValueError as e:
        await query.message.reply_text(f"❌ Ошибка: {e}")
        return "stats_handler"


async def last_practice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик для кнопки '📅 Последняя тренировка'."""
    query = update.callback_query
    await query.answer()
    user_id = context.user_data.get("user_id")

    try:
        data = await api_get_last_session_date(user_id=user_id)
        
        text = (
            f"📅 **ПОСЛЕДНЯЯ ТРЕНИРОВКА**\n"
            f"➖➖➖➖➖➖➖➖➖➖\n"
            f"• Дата последней сессии: **{data['last_session_date']}**"
        )
        await query.message.reply_text(text, parse_mode='Markdown')

    except ValueError as e:
        await query.message.reply_text(f"❌ Ошибка: {e}")
        return "stats_handler"
