import os

from django.conf import settings
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler,
                          Updater)

from santa_bot.bot import handlers


def main():
    updater = Updater(settings.TELEGRAM_TOKEN)

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

    dp.add_handler(conv_handler)
    dp.add_handler(conv_handler_create_group)
    dp.add_handler(conv_handler_my_groups)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
