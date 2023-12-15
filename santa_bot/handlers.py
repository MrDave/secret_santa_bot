from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from santa_bot.models import Game


NAME, EMAIL, WISHLIST, CONFIRM, EDITING_HANDLING, CHECK_CORRECT, EDIT_RESPONSE = range(7)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Это обычный start")


def start_player(update: Update, context: CallbackContext):
    """Reached through deep-link with game ID."""
    game_id = context.args[0]
    game = Game.objects.get(id=game_id)
    message_text = f"""Замечательно, ты собираешься участвовать в игре: {game.name}
Игра проходит с {game.start_date} по {game.end_date}.
Краткое описание от организатора:
{game.description}"""
    update.message.reply_text(message_text)
    update.message.reply_text(
        """Для начала скажи, как к тебе можно обращаться?
Напиши так, чтобы другие игроки могли тебя узнать"""
    )
    context.user_data["current_game"] = game
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
    return check_if_correct(update, context)


def check_if_correct(update: Update, context: CallbackContext):
    wishlist = context.user_data["wishlist"]
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
    if update.message:
        update.message.reply_text(message_text, reply_markup=reply_markup)
    elif update.callback_query:
        update.callback_query.answer()
        update.callback_query.message.reply_text(message_text, reply_markup=reply_markup)

    return CONFIRM


def confirm_participation(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == "participation_correct":
        game = context.user_data["current_game"]
        # TODO: Create db entry.
        message_text = f"""Превосходно, ты в игре! \
{game.end_date} мы проведем жеребьевку и ты узнаешь имя и контакты своего тайного друга. \
Ему и нужно будет подарить подарок!"""
        query.message.reply_text(message_text)
        return ConversationHandler.END
    elif query.data == "edit_participation":
        message_text = "Окей, что надо изменить?"
        keyboard = [
            [
                InlineKeyboardButton("Имя", callback_data="edit_name"),
                InlineKeyboardButton("Email", callback_data="edit_email"),
                InlineKeyboardButton("Пожелания", callback_data="edit_wishlist")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(message_text, reply_markup=reply_markup)
        return EDITING_HANDLING


def handle_participation_editing(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "edit_name":
        message_text = "Напиши, как к тебе обращаться (чтобы другие игроки тебя могли узнать)"
        context.user_data["now_editing"] = "name"
    elif query.data == "edit_email":
        message_text = "Напиши, свой email"
        context.user_data["now_editing"] = "email"
    elif query.data == "edit_wishlist":
        message_text = "Напиши, что ты хочешь получить в подарок"
        context.user_data["now_editing"] = "wishlist"

    query.message.reply_text(message_text)
    return EDIT_RESPONSE


def get_edited_response(update: Update, context: CallbackContext):
    key_to_edit = context.user_data.pop("now_editing")
    context.user_data[key_to_edit] = update.message.text

    return check_if_correct(update, context)

