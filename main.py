import base64
import os
from io import BytesIO

import django
from const import translater, bot

import buttons
from neuro_api import generate_text

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HistoryWithGirlfriend.settings')
django.setup()

from app.models import User, Character, History


def menu(chat_id, user):
    language = user.language
    text = translater('Выберите персонажа', language)
    bot.send_message(chat_id=chat_id, text=text, reply_markup=buttons.choose_character(language))


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user, _ = User.objects.get_or_create(chat_id=chat_id)
    user.choose_history = None
    user.save(update_fields=['choose_history'])
    user.history_message.all().delete()
    if _:
        bot.send_message(chat_id=chat_id, text='Выбери язык', reply_markup=buttons.choose_language())
    else:
        menu(chat_id, user)


@bot.message_handler(content_types=['text'])
def text(message):
    chat_id = message.chat.id
    user, _ = User.objects.get_or_create(chat_id=chat_id)
    if user.choose_history:
        text, photo = generate_text(user, message.text)
        if photo:
            image_data = base64.b64decode(photo)  # Декодируем base64 строку
            image = BytesIO(image_data)
            bot.send_photo(chat_id=chat_id, photo=image, caption=text)
        else:
            bot.send_message(chat_id=chat_id, text=text)
    else:
        menu(chat_id=chat_id, user=user)


def history_detail(chat_id, user, character_id, history_id, language):
    history = History.objects.get(id=history_id)
    text = f'Название истории: {history.name}\n' \
           f'Сюжет: {history.description}'
    bot.send_message(chat_id=chat_id, text=translater(text, language),
                     reply_markup=buttons.history_detail_button(character_id=character_id, history_id=history_id,
                                                                language=language))


def character_detail(chat_id, user, character_id, language):
    chatacter = Character.objects.get(id=character_id)
    text = f'Имя персонажа: {chatacter.name}\n' \
           f'Характер персонажа: {chatacter.personality}'
    try:
        bot.send_photo(chat_id=chat_id, photo=chatacter.photo, caption=translater(text, language),
                       reply_markup=buttons.choose_history(character_id, language))
    except Exception:
        bot.send_message(chat_id=chat_id, text=translater(text, language),
                         reply_markup=buttons.choose_history(character_id, language))


def choose_history(chat_id, user, history_id, language):
    history = History.objects.get(id=history_id)
    user.choose_history = history
    user.save(update_fields=['choose_history'])
    bot.send_message(chat_id=chat_id, text='💡 ПОДСКАЗКА: Нажмите /start, чтобы выбрать новую историю')
    try:
        bot.send_photo(chat_id=chat_id, photo=history.photo, caption=translater(history.start_text, language))
    except Exception:
        bot.send_message(chat_id=chat_id, text=translater(history.start_text, language))


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    chat_id = call.message.chat.id
    user, _ = User.objects.get_or_create(chat_id=chat_id)
    language = user.language
    if call.message:
        data = call.data.split('|')
        bot.clear_step_handler_by_chat_id(chat_id=chat_id)
        if data[0] != 'chat':
            bot.delete_message(chat_id=chat_id, message_id=call.message.id)
        if data[0] == 'menu':
            menu(chat_id=chat_id, user=user)
        elif data[0] == 'language':
            user.language = data[1]
            user.save()
            menu(chat_id=chat_id, user=user)
        elif data[0] == 'character':
            character_detail(chat_id=chat_id, user=user, character_id=data[1], language=language)
        elif data[0] == 'history':
            history_detail(chat_id=chat_id, user=user, character_id=data[1], history_id=data[2], language=language)
        elif data[0] == 'choose_history':
            choose_history(chat_id=chat_id, user=user, history_id=data[1], language=language)

bot.infinity_polling(timeout=50, long_polling_timeout = 25)