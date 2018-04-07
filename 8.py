import sys
import requests
import pygame
import json
import random
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove


def go(bot, updater, user_data):
    if user_data['current'] < len(user_data['english_words']):
        static_api_request = "https://www.googleapis.com/customsearch/v1?q=" + user_data['english_words'][user_data[
            'current']] + "&key=AIzaSyBLxDLnQQJbB6Ps0oEcqUK5w-0Tg3rhLVI&searchType=image&cx=005680010173931685076:cdr_fpoqyvm"
        req = requests.get(static_api_request).json()['items'][2]['link']
        req2 = requests.get(static_api_request).json()['items'][3]['link']
        user_data['links'].append(req2)
        user_data['links2'].append(req)
        try:
            bot.sendPhoto(
                updater.message.chat.id,
                req,
                caption="Что же это такое?"
            )
            user_data['current'] += 1
        except:
            user_data['current'] += 1
            go(bot, updater, user_data)
    else:
        stop(bot, updater, user_data)


def analiz(bot, updater, user_data):
    text = updater.message.text
    if text.lower() == user_data['english_words'][user_data['current'] - 1].lower():
        try:
            bot.sendPhoto(
                updater.message.chat.id,
                user_data['links'][user_data['current'] - 1],
                caption="Верно! Это " + user_data['english_words'][user_data['current'] - 1]
            )
        except:
            bot.sendPhoto(
                updater.message.chat.id,
                user_data['links2'][user_data['current'] - 1],
                caption="Верно! Это " + user_data['english_words'][user_data['current'] - 1])
        user_data['balls'] += 1

    else:
        try:
            bot.sendPhoto(
                updater.message.chat.id,
                user_data['links'][user_data['current'] - 1],
                caption="Неверно, это " + user_data['english_words'][user_data['current'] - 1]
            )
        except:
            bot.sendPhoto(
                updater.message.chat.id,
                user_data['links2'][user_data['current'] - 1],
                caption="Неверно, это " + user_data['english_words'][user_data['current'] - 1]

            )
        user_data['notballs'] += 1
    go(bot, updater, user_data)


def slova(bot, updater, args, user_data):
    user_data['russian_words'] = args
    user_data['english_words'] = []
    for i in user_data['russian_words']:
        translator_uri = "https://translate.yandex.net/api/v1.5/tr.json/translate"
        response = requests.get(
            translator_uri,
            params={
                "key":
                    "trnsl.1.1.20180328T165618Z.c5cc9a2fa0ef1df4.06dc14ab8d26ee1d740068a7fc369c444174b019",
                "lang": 'ru-en',
                "text": i
            })
        text = response.json()["text"][0]
        user_data['english_words'].append(text)
    go(bot, updater, user_data)


def start(bot, update, user_data):
    user_data['notballs'] = 0
    user_data[
        'russian_words'] = "кот друзья платье юбка кофта кружка абрикос яблоко груша вишня торт пакет зеркало мебель глаза мяч брови уши цирк свадьба орел ножницы закат солнце футбол стопа кисть ракетка круг птица гора небо зима".split(
        " ")
    user_data['english_words'] = []
    for i in user_data['russian_words']:
        try:
            translator_uri = "https://translate.yandex.net/api/v1.5/tr.json/translate"
            response = requests.get(
                translator_uri,
                params={
                    "key":
                        "trnsl.1.1.20180328T165618Z.c5cc9a2fa0ef1df4.06dc14ab8d26ee1d740068a7fc369c444174b019",
                    "lang": 'ru-en',
                    "text": i
                })
            text = response.json()["text"][0]
            user_data['english_words'].append(text)
        except:
            pass
    user_data['current'] = 0
    user_data['balls'] = 0
    user_data['links'] = []
    user_data['links2'] = []
    update.message.reply_text("Добрый день. Я бот, который помогает выучить английские слова.")
def stop(bot, update, user_data):
    update.message.reply_text(
        str(user_data['balls']) + " правильных ответа и " + str(user_data['notballs']) + " неправильных.")
    user_data['current'] = 0
    user_data['balls'] = 0
    user_data['notballs'] = 0
    user_data['english_words'] = []
    user_data['links'] = []
    user_data['links2'] = []
    return ConversationHandler.END


def main():
    updater = Updater("575881493:AAE0ArgHDSPIhboGgdv8z9q4QGMLObEmD7E")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start, pass_user_data=True))
    dp.add_handler(CommandHandler('go', go, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, analiz, pass_user_data=True))
    dp.add_handler(CommandHandler('stop', stop, pass_user_data=True))
    dp.add_handler(CommandHandler('slova', slova, pass_args=True, pass_user_data=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()