from telegram.ext import Updater
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, CallbackQueryHandler
from telegram.ext import Filters
from environs import Env
import handlers


def main():
    env = Env()
    env.read_env()
    telegram_token = env.str("TELEGRAM_TOKEN")

    updater = Updater(telegram_token)

    dp = updater.dispatcher

    player_signup_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start_player", handlers.start_player)],
        states={
            handlers.NAME: [MessageHandler(Filters.text & ~Filters.command, handlers.get_name)],
            handlers.EMAIL: [MessageHandler(Filters.text & ~Filters.command, handlers.get_email)],
            handlers.WISHLIST: [MessageHandler(Filters.text & ~Filters.command, handlers.get_wishlist)],
            handlers.CONFIRM: [CallbackQueryHandler(handlers.confirm_participation)]
        },
        fallbacks=[],
    )

    dp.add_handler(player_signup_conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
