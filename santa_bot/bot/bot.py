from telegram.ext import Updater
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, CallbackQueryHandler
from telegram.ext import Filters
from environs import Env
from santa_bot import handlers


def main():
    env = Env()
    env.read_env()
    telegram_token = env.str("TELEGRAM_TOKEN")

    updater = Updater(telegram_token)

    dp = updater.dispatcher
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', handlers.start),
                      CommandHandler('restart', handlers.restart)],
        states={
            handlers.INFORMATION_TEXT: [CallbackQueryHandler(handlers.information_text)],
            handlers.INFORMATION_TEXT_2: [CallbackQueryHandler(handlers.information_text_2)],
            # handlers.BUTTON_HANDLING: [MessageHandler(Filters.regex('Мои группы'), handlers.button_handling)],
        },
        fallbacks=[CommandHandler('restart', handlers.restart)],
    )
    conv_handler_my_groups = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Мои группы'), handlers.button_handling)],
        states={
            handlers.CHOSEN_GROUP: [CallbackQueryHandler(handlers.display_about_group)]
        },
        fallbacks=[
            CommandHandler('restart', handlers.restart),
            MessageHandler(Filters.regex('Создание новой группы'),
                           handlers.button_handling)
        ]
    )


    conv_handler_create_group = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Создание новой группы'),
                                     handlers.button_handling)],
        states={
            handlers.CREATE_GROUP: [CallbackQueryHandler(handlers.create_group)],
            handlers.DESCRIPTION_GROUP: [CallbackQueryHandler(handlers.description_group)],
            handlers.CHOOSE_DATE: [CallbackQueryHandler(handlers.choose_date)],
        },
        fallbacks=[
            CommandHandler('restart', handlers.restart),
            MessageHandler(Filters.regex('Мои группы'), handlers.button_handling)
        ]
    )

    player_signup_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", handlers.start_player, Filters.regex("\d"))],
        states={
            handlers.NAME: [MessageHandler(Filters.text & ~Filters.command, handlers.get_name)],
            handlers.EMAIL: [MessageHandler(Filters.text & ~Filters.command, handlers.get_email)],
            handlers.WISHLIST: [MessageHandler(Filters.text & ~Filters.command, handlers.get_wishlist)],
            handlers.CONFIRM: [CallbackQueryHandler(handlers.confirm_participation)],
            handlers.EDITING_HANDLING: [CallbackQueryHandler(handlers.handle_participation_editing)],
            handlers.EDIT_RESPONSE: [MessageHandler(Filters.text & ~Filters.command, handlers.get_edited_response)],
        },
        fallbacks=[],
    )
    
    dp.add_handler(conv_handler)
    dp.add_handler(conv_handler_create_group)
    dp.add_handler(conv_handler_my_groups)
    dp.add_handler(player_signup_conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
