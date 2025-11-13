from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler,
    ConversationHandler, filters
)
from app.bot.handlers.stats import (
average_score, best_session, last_practice,
 stats_handler, total_sessions, total_shots
)
from app.bot.handlers.register import (
    register_password, register_username, register_verify, start_register
)
from app.bot.handlers.profile import (
    profile_handler, change_password, change_username,
    new_password, new_username
)
from app.bot.handlers.home import home_handler
from app.core.config import settings
from app.bot.handlers.cancel import cancel
from app.bot.handlers.upload import upload_file, start_upload
from app.bot.handlers.logout import logout_handler
from app.bot.handlers.main_menu import fallback_message, menu_handler, start
from app.bot.handlers.login import login_password, login_username, start_login

TELEGRAM_TOKEN = settings.telegram.TELEGRAM_TOKEN

# Регистрация
register_conv = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(start_register, pattern="^menu_register$")
    ],
    states={
        "register_username": [MessageHandler(filters.TEXT & ~filters.COMMAND, register_username)],
        "register_password": [MessageHandler(filters.TEXT & ~filters.COMMAND, register_password)],
        "register_verify": [MessageHandler(filters.TEXT & ~filters.COMMAND, register_verify)],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
        CallbackQueryHandler(cancel, pattern="^menu_cancel$")
    ],
    allow_reentry=True,
)

# Вход
login_conv = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(start_login, pattern="^menu_login$")
    ],
    states={
        "login_username": [MessageHandler(filters.TEXT & ~filters.COMMAND, login_username)],
        "login_password": [MessageHandler(filters.TEXT & ~filters.COMMAND, login_password)],
        "start_login": [MessageHandler(filters.TEXT & ~filters.COMMAND, start_login)],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
        CallbackQueryHandler(cancel, pattern="^menu_cancel$")
    ],
    allow_reentry=True,
)

# Профиль
profile_conv = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(profile_handler, pattern="^menu_profile$"),
        CallbackQueryHandler(change_username, pattern="^change_name$"), 
        CallbackQueryHandler(change_password, pattern="^change_password$"),
    ],
    states={
        "change_username": [MessageHandler(filters.TEXT & ~filters.COMMAND, new_username)],
        "change_password": [MessageHandler(filters.TEXT & ~filters.COMMAND, new_password)],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
        CallbackQueryHandler(cancel, pattern="^menu_cancel$")
    ],
    allow_reentry=True,
)

# Отправить файл
upload_conv = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(start_upload, pattern="^menu_send_csv$")
    ],
    states={
        "upload_file": [MessageHandler(filters.Document.ALL, upload_file)],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
        CallbackQueryHandler(cancel, pattern="^menu_cancel$")
    ],
    allow_reentry=True,
)

# Статистика
stats_conv = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(stats_handler, pattern="^menu_stats$")
    ],
    states={
        "stats_handler":[
        CallbackQueryHandler(total_sessions, pattern="^total_sessions$"),
        CallbackQueryHandler(average_score, pattern="^average_score$"),
        CallbackQueryHandler(total_shots, pattern="^total_shots$"),
        CallbackQueryHandler(best_session, pattern="^best_session$"),
        CallbackQueryHandler(last_practice, pattern="^last_practice$")
        ]
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
        CallbackQueryHandler(cancel, pattern="^menu_cancel$")
    ],
    allow_reentry=True,
)


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    #  Для возврата в главное меню
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^🏠 Домой$"), home_handler))

    #  Диалоги (ConversationHandler)
    app.add_handler(register_conv)
    app.add_handler(login_conv)
    app.add_handler(profile_conv)
    app.add_handler(upload_conv)
    app.add_handler(stats_conv)

    #  Общие команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(logout_handler, pattern="^menu_logout$"))
    app.add_handler(CallbackQueryHandler(menu_handler, pattern="^menu_"))
    
    #  Для нераспознанного текста
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback_message))
    
    app.run_polling()


if __name__ == "__main__":
    main()
