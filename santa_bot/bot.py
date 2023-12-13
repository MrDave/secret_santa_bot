import os

import handlers
from dotenv import load_dotenv
from telegram.ext import CommandHandler, CallbackContext, Updater, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters


def main():
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    updater = Updater(telegram_token)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', handlers.start)],
        states={
            handlers.INFORMATION_TEXT: [CallbackQueryHandler(handlers.information_text)],
            handlers.INFORMATION_TEXT_2: [CallbackQueryHandler(handlers.information_text_2)],
        #     handlers.CUSTOM_OCCASION_TEXT: [
        #         MessageHandler(Filters.text & ~Filters.command, handlers.custom_occasion_text)
        #     ],
        #     handlers.CHOOSE_BUDGET: [CallbackQueryHandler(handlers.choose_budget)],
        #     handlers.BUTTON_HANDLING: [CallbackQueryHandler(handlers.button_handling)],
        #     handlers.CHOOSE_NAME: [MessageHandler(Filters.text & ~Filters.command, handlers.ask_name)],
        #     handlers.CHOOSE_SURNAME: [MessageHandler(Filters.text & ~Filters.command, handlers.ask_surname)],
        #     handlers.CHOOSE_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, handlers.ask_address)],
        #     handlers.CHOOSE_DATE: [MessageHandler(Filters.text & ~Filters.command, handlers.ask_date)],
        #     handlers.CHOOSE_TIME: [MessageHandler(Filters.text & ~Filters.command, handlers.ask_time)],
        #     handlers.ORDER_FLOWER: [MessageHandler(Filters.text & ~Filters.command, handlers.get_order)],
        #     handlers.GETTING_NUMBER: [MessageHandler(Filters.text & ~Filters.command, handlers.get_number_to_florist)],
        #     handlers.CREATE_ORDER: [CallbackQueryHandler(handlers.create_order, pattern='^confirm_order$')],
        },
        fallbacks=[CommandHandler('restart', handlers.restart)],
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

