import os

import django
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from const import translater

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HistoryWithGirlfriend.settings')
django.setup()
from app.models import Character, History


def choose_language():
    markup = InlineKeyboardMarkup(row_width=1)
    ru = InlineKeyboardButton('🇷🇺Русский🇷🇺', callback_data='language|ru')
    en = InlineKeyboardButton('🇺🇸English🇺🇸', callback_data='language|en')
    markup.add(ru, en)
    return markup


def choose_character(language):
    markup = InlineKeyboardMarkup(row_width=1)
    for character in Character.objects.all():
        btn = InlineKeyboardButton(translater(character.name, language), callback_data=f'character|{character.id}')
        markup.add(btn)
    return markup


def choose_history(character_id, language):
    markup = InlineKeyboardMarkup(row_width=1)
    back = InlineKeyboardButton(translater('Назад', language), callback_data='menu')
    for history in History.objects.filter(character_id=character_id):
        btn = InlineKeyboardButton(translater(history.name, language),
                                   callback_data=f'history|{character_id}|{history.id}')
        markup.add(btn, back)
    return markup


def history_detail_button(character_id, history_id, language):
    markup = InlineKeyboardMarkup(row_width=1)
    back = InlineKeyboardButton(translater('Назад', language), callback_data=f'character|{character_id}')
    choose = InlineKeyboardButton(translater('Выбрать историю', language), callback_data=f'choose_history|{history_id}')
    markup.add(choose, back)
    return markup
