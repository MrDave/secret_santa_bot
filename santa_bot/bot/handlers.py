from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      InputMediaPhoto, KeyboardButton, ReplyKeyboardMarkup,
                      Update)
from telegram.ext import CallbackContext, ConversationHandler

from santa_bot.bot.texts import (ADMIN_BTN_TXT, CREATE_GROUP_BTN_TXT,
                                 MY_GROUPS_BTN_TXT)
from santa_bot.models import Game, Player

NAME, EMAIL, WISHLIST, CONFIRM, EDITING_HANDLING, CHECK_CORRECT, EDIT_RESPONSE = range(7)
INFORMATION_TEXT, INFORMATION_TEXT_2 = range(2)
CREATE_GROUP, DESCRIPTION_GROUP, CHOOSE_DATE = range(3)
CHOSEN_GROUP, IN_GROUP_ACTION, CHANGE_WISHLIST = range(3)


def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Я готов!", callback_data="next_info")],

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        # update.message.photo()
        update.message.reply_text(
            "Привет, я бот-повелитель Тайных Сант. Больше всего на свете я люблю друзей и подарки 🎁")
        update.message.reply_text(
            "С моей помощью ты можешь создать группу и организовать Тайного Санту с друзьями или семьей 👨‍👩‍👧‍👦, на работе 👩‍✈️или в сообществе 🧘, везде, где есть дорогие тебе люди, с кем ты хочешь разделить радость новогодней суеты.\n\nВозглавь новогоднее безумие и стань душой этого праздника ✨",
            reply_markup=reply_markup)

    return INFORMATION_TEXT


def restart(update, context):
    if update.message:
        update.message.reply_text("Бот перезапущен!")
    else:
        update.callback_query.message.reply_text("Бот перезапущен!")
    context.user_data.clear()
    return start(update, context)


def information_text(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    last_info = query.data
    if last_info == "next_info":
        keyboard = [
            [InlineKeyboardButton("Круто! Погнали!", callback_data="next_info_2")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.callback_query.message.reply_text(
            "Пока все будут собираться в твоей группе и думать, что они хотят получить от своего Санты, "
            "уже зарегистрированные смогут поиграть в снежки ☄️ (команда для этого будет в меню [Мои группы]) и "
            "порадоваться моим шуткам.\n\n"
            "Когда все соберутся, ты сможешь запустить Распределение подарков и я подберу и разошлю каждому его "
            "подопечного 🥷\n\nСанта и подопечный даже смогут анонимно пообщаться, если они захотят уточнить детали "
            "или передать привет друг другу.",
            reply_markup=reply_markup)

    return INFORMATION_TEXT_2


def information_text_2(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    last_info = query.data
    if last_info == "next_info_2":
        keyboard = [
            [KeyboardButton(CREATE_GROUP_BTN_TXT)],
            [KeyboardButton(ADMIN_BTN_TXT)],
            [KeyboardButton(MY_GROUPS_BTN_TXT)],
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        update.callback_query.message.reply_text(
            "Когда ты создашь группу, я сделаю для тебя волшебную секретную ссылку. Пройдя по ней, твои друзья сразу "
            "начнут регистрацию в твоей группе."
            "Что делать дальше?\n\nЕще я создал для тебя внизу экрана кнопки, где ты можешь:\n\n1️⃣ Посмотреть, "
            "в каких группах ты состоишь\n\n2️⃣ Управлять твоими созданными группами\n\n3️⃣ Создать свою группу "
            "/newgroup\nХорошей игры! 🥳",
            reply_markup=reply_markup)


# Ветка создания новой группы
def create_group(update: Update, context: CallbackContext):
    message_text = "Самое время создать новую группу, куда ты можешь пригласить своих друзей, коллег или родственников\n\n" \
           "Давай выберем забавное имя для новой группы!"
    update.message.reply_text(message_text)
    return DESCRIPTION_GROUP


def description_group(update: Update, context: CallbackContext):
    context.user_data["group_name"] = update.message.text
    message_text = "Классное название!\n\n" \
                   "А теперь напиши мне короткое  описание вашей группы. Его будут видеть участники при регистрации и на странице группы."
    update.message.reply_text(message_text)
    return CHOOSE_DATE


def choose_date(update: Update, context: CallbackContext):
    pass


# Ветка отображения групп
def my_groups(update: Update, context: CallbackContext):
    groups = ["Достаем", "группы", "из БД"]
    message_text = f"Список групп, где ты участник:\n{', '.join(groups)}\n"
    keyboard = [
        [InlineKeyboardButton(text=group, callback_data=group)] for group in groups
    ]
    print(keyboard)
    update.message.reply_text(text=message_text,
                              reply_markup=InlineKeyboardMarkup(keyboard))
    return CHOSEN_GROUP


def display_about_group(update: Update, context: CallbackContext):
    print('display_about_group')
    query = update.callback_query
    query.answer()
    group_name = query.data
    group = {
        "name": group_name,
        "description": "Куча текста",
        "registration_status": "Открыта",
        "amount_playing_users": 6,
        "players": ['Игрок 1', 'Игрок 2', 'Игрок 3', 'Игрок 4'],
        "present_for": "Игрок 4"
    }

    text = "Название группы: {}\n\n"  \
           "Описание:\n{}\n\n"  \
           "Регистрация в группу {}\n\n"  \
           "Количество участников (через annotate) - {}\n"  \
           "{}\n\n"  \
           "Ты будешь тайным Сантой для {}\n"

    message_text = text.format(group['name'],
                               group['description'],
                               group['registration_status'],
                               group['amount_playing_users'],
                               group['players'],
                               group['present_for'])

    keyboard = [
        [InlineKeyboardButton(text="Назад",
                              callback_data="Назад")],
        [InlineKeyboardButton(text="Покинуть группу",
                              callback_data="Покинуть группу")],
        [InlineKeyboardButton(text="Изменить желание",
                              callback_data="Изменить желание")]
    ]
    query.message.reply_text(
        text=message_text, reply_markup=InlineKeyboardMarkup(keyboard))
    return IN_GROUP_ACTION


def in_group_action(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == 'Назад':
        return CHOSEN_GROUP
    elif query.data == 'Покинуть группу':
        print('Выйти из группу')
        return ConversationHandler.END
    elif query.data == 'Изменить желание':
        query.message.reply_text('Заполните, пожалуйсьа заново вишлист')
        return CHANGE_WISHLIST


# Ветка управления группами
def admin(update: Update, context: CallbackContext):
    pass


# Ветка регистрации игрока
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
    """Collect player's name from text message and ask for email."""
    context.user_data["name"] = update.message.text
    message_text = "Славно! Теперь напиши свой email"
    update.message.reply_text(message_text)

    return EMAIL


def get_email(update: Update, context: CallbackContext):
    """Collect player's email and ask for their wishlist."""
    context.user_data["email"] = update.message.text
    game = context.user_data["current_game"]
    message_text = f"""А сейчас расскажи, что бы ты хотел в подарок :)
Это может быть что-то конкретное или же просто что тебе было бы по душе

Ограничения по подаркам: {game.price_limit}"""
    update.message.reply_text(message_text)

    return WISHLIST


def get_wishlist(update: Update, context: CallbackContext):
    """Collect player's wishlist."""
    context.user_data["wishlist"] = update.message.text
    return check_if_correct(update, context)


def check_if_correct(update: Update, context: CallbackContext):
    """Show summary of the player's info to confirm or edit."""
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
    """Create correct Player entry in db or select field to edit."""
    query = update.callback_query
    query.answer()
    if query.data == "participation_correct":
        game = context.user_data["current_game"]
        wishlist = context.user_data["wishlist"]
        name = context.user_data["name"]
        email = context.user_data["email"]

        Player.objects.create(
            telegram_id=update.effective_user.id,
            game=game,
            name=name,
            email=email,
            wishlist=wishlist
        )
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

def get_edited_response(update: Update, context: CallbackContext):
    key_to_edit = context.user_data.pop("now_editing")
    context.user_data[key_to_edit] = update.message.text

    return check_if_correct(update, context)
def get_edited_response(update: Update, context: CallbackContext):
    key_to_edit = context.user_data.pop("now_editing")
    context.user_data[key_to_edit] = update.message.text

    return check_if_correct(update, context)
