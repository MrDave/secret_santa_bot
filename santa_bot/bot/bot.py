from environs import Env
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler,
                          Updater)

from santa_bot.bot import handlers
from santa_bot.bot.texts import (ADMIN_BTN_TXT, CREATE_GROUP_BTN_TXT,
                                 MY_GROUPS_BTN_TXT)

FALLBACKS = [
    CommandHandler('restart', handlers.restart),
    MessageHandler(Filters.regex(CREATE_GROUP_BTN_TXT),
                   handlers.create_group),
    MessageHandler(Filters.regex(MY_GROUPS_BTN_TXT),
                   handlers.my_groups),
    MessageHandler(Filters.regex(ADMIN_BTN_TXT),
                   handlers.admin)
]


def main():
    env = Env()
    env.read_env()

    updater = Updater(token=env.str("TELEGRAM_TOKEN"))
    dp = updater.dispatcher

    organizer_start_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', handlers.start),
                      CommandHandler('restart', handlers.restart)],
        states={
            handlers.INFORMATION_TEXT: [CallbackQueryHandler(
                                        handlers.information_text)],
            handlers.INFORMATION_TEXT_2: [CallbackQueryHandler(
                                          handlers.information_text_2)],
        },
        fallbacks=FALLBACKS,
    )

    my_groups_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(MY_GROUPS_BTN_TXT),
                                     handlers.my_groups)],
        states={
            handlers.CHOSEN_GROUP: [CallbackQueryHandler(handlers.display_about_group)],
            handlers.IN_GROUP_ACTION: [CallbackQueryHandler(handlers.in_group_action)],
            handlers.CHANGE_WISHLIST: [],
        },
        fallbacks=FALLBACKS
    )

    create_group_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(CREATE_GROUP_BTN_TXT),
                                     handlers.create_group)],
        states={
            handlers.CREATE_GROUP: [CallbackQueryHandler(
                                    handlers.create_group)],
            handlers.DESCRIPTION_GROUP: [CallbackQueryHandler(
                                         handlers.description_group)],
            handlers.CHOOSE_DATE: [CallbackQueryHandler(handlers.choose_date)],
        },
        fallbacks=FALLBACKS
    )

    admin_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(ADMIN_BTN_TXT),
                                     handlers.admin)],
        states={},
        fallbacks=FALLBACKS
    )

    player_signup_conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", handlers.start_player, Filters.regex("\d"))
        ],
        states={
            handlers.NAME: [MessageHandler(Filters.text & ~Filters.command,
                                           handlers.get_name)],
            handlers.EMAIL: [MessageHandler(Filters.text & ~Filters.command,
                                            handlers.get_email)],
            handlers.WISHLIST: [MessageHandler(Filters.text & ~Filters.command,
                                               handlers.get_wishlist)],
            handlers.CONFIRM: [
                CallbackQueryHandler(handlers.confirm_participation)
            ],
            handlers.EDITING_HANDLING: [
                CallbackQueryHandler(handlers.handle_participation_editing)
            ],
            handlers.EDIT_RESPONSE: [
                MessageHandler(Filters.text & ~Filters.command,
                               handlers.get_edited_response)
            ],
        },
        fallbacks=[],
    )

    dp.add_handler(player_signup_conv_handler)
    dp.add_handler(organizer_start_conv_handler)
    dp.add_handler(create_group_conv_handler)
    dp.add_handler(my_groups_conv_handler)
    dp.add_handler(admin_conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()


if __name__ == '__main__':
    main()
