from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler


NAME, EMAIL, WISHLIST, CONFIRM = range(4)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Это обычный start")


def start_player(update: Update, context: CallbackContext):
    # TODO: fetch and use actual game details.
    print(context.args)
    message_text = "Замечательно, ты собираешься участвовать в игре: {game_details}"
    update.message.reply_text(message_text)
    update.message.reply_text(
        """Для начала скажи, как к тебе можно обращаться?
Напиши так, чтобы другие игроки могли тебя узнать"""
    )
    return NAME


def get_name(update: Update, context: CallbackContext):
    context.user_data["name"] = update.message.text
    message_text = "Славно! Теперь напиши свой email"
    update.message.reply_text(message_text)

    return EMAIL


def get_email(update: Update, context: CallbackContext):
    context.user_data["email"] = update.message.text
    message_text = """А сейчас расскажи, что бы ты хотел в подарок :)
Это может быть что-то конкретное или же просто что тебе было бы по душе"""
    update.message.reply_text(message_text)

    return WISHLIST


def get_wishlist(update: Update, context: CallbackContext):
    context.user_data["wishlist"] = update.message.text
    wishlist = update.message.text
    name = context.user_data["name"]
    email = context.user_data["email"]

    message_text = f"""Отлично, давай проверим, что всё верно:
Имя: {name}
Email: {email}
Твои пожелания: {wishlist}

Всё правильно?"""

    keyboard = [
        [InlineKeyboardButton("Да, всё верно", callback_data="participation_correct")],
        [InlineKeyboardButton("Нет, хочу что-то поменять", callback_data="edit_participation")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(message_text, reply_markup=reply_markup)

    return CONFIRM


def confirm_participation(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == "participation_correct":
        # TODO: Create db entry.
        message_text = """Превосходно, ты в игре! \
{game_end_date} мы проведем жеребьевку и ты узнаешь имя и контакты своего тайного друга. \
Ему и нужно будет подарить подарок!"""
        query.message.reply_text(message_text)

    return ConversationHandler.END
