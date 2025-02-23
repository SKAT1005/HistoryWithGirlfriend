import telebot
import translators as ts

bot = telebot.TeleBot('7171194252:AAH4RfsCaxDNv22yfWoD7kqLwStH1PW7EZk')


def translater(text, language):
    translated_text = ts.translate_text(text, translator='yandex', to_language=language)
    return translated_text