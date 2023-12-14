from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      InputMediaPhoto, Update)
from telegram.ext import CallbackContext, ConversationHandler

INFORMATION_TEXT, INFORMATION_TEXT_2, INFORMATION_TEXT_3, BUTTON_HANDLING, ORDER_FLOWER, CHOOSE_NAME, CHOOSE_SURNAME, CHOOSE_ADDRESS, CHOOSE_DATE, CHOOSE_TIME, CONSULTING, GETTING_NUMBER, CREATE_ORDER = range(
    13)


def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Я готов!", callback_data='next_info')],

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        update.message.photo()
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
            [InlineKeyboardButton("Круто! Погнали!", callback_data='next_info_2')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.callback_query.message.reply_text(
            "Пока все будут собираться в твоей группе и думать, что они хотят получить от своего Санты, уже зарегистрированные смогут поиграть в снежки ☄️ (команда для этого будет в меню [Мои группы]) и порадоваться моим шуткам.\n\n"
            "Когда все соберутся, ты сможешь запустить Распределение подарков и я подберу и разошлю каждому его подопечного 🥷\n\nСанта и подопечный даже смогут анонимно пообщаться, если они захотят уточнить детали или передать привет друг другу.",
            reply_markup=reply_markup)

    return INFORMATION_TEXT_2


def information_text_2(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    last_info = query.data
    if last_info == "next_info_2":

        update.callback_query.message.reply_text(
            "Когда ты создашь группу, я сделаю для тебя волшебную секретную ссылку. Пройдя по ней, твои друзья сразу начнут регистрацию в твоей группе."
            "Что делать дальше?\n\nЕще я создал для тебя внизу экрана кнопки, где ты можешь:\n\n1️⃣ Посмотреть, в каких группах ты состоишь\n\n2️⃣ Управлять твоими созданными группами\n\n3️⃣ Создать свою группу /newgroup\nХорошей игры! 🥳",
            )

    return INFORMATION_TEXT_3