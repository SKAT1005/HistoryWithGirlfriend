import telebot
import translators as ts

bot = telebot.TeleBot('7195501588:AAFNEF48b0wNeIqUTVxdq5KZ3K8Ur4e9rz0')


def translater(text, language):
    translated_text = ts.translate_text(text, translator='yandex', to_language=language)
    return translated_text