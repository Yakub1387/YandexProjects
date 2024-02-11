'''
Бучминский Якуб, Beta-группа
*API_KEY прописан в отдельном файле .env
'''

import telebot, os, json
from telebot import types
from random import choice
from info import get_data, push_data
from pathlib import Path
from dotenv import load_dotenv
from random import choice

BASE_DIR = Path(__file__).parent.parent

load_dotenv(BASE_DIR / '.env')
API_KEY = os.getenv('API_KEY')
data = get_data()
bot = telebot.TeleBot(API_KEY)

with open('quest.json', encoding='utf-8') as f: QUEST = json.load(f)


def closer(a):
    for i in a:
        i.close()


def tracker(call: types.CallbackQuery):
    bot.delete_message(call.message.chat.id, call.message.id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton('Продолжить', callback_data=f'cont')
    button2 = types.InlineKeyboardButton("Заново", callback_data='again')
    markup.add(button1, button2)
    bot.send_message(call.message.chat.id, text='Желаете продолжить незавершённый квест или начать заново?', reply_markup=markup)


def cont(call: types.CallbackQuery):
    call.data = data[str(call.from_user.id)][0]
    quest(call)


def again(call: types.CallbackQuery):
    call.data = 'Forest'
    quest(call)


def check_quest(a: types.CallbackQuery):
    if isinstance(a, types.CallbackQuery):
        if a.data == 'quest':
            if str(a.from_user.id) not in data.keys():
                data[str(a.from_user.id)] = ('Forest', False)
                push_data(data)
                return True
            elif data[str(a.from_user.id)][1]:
                data[str(a.from_user.id)] = (data[str(a.from_user.id)][0], False)
                push_data(data)
                return True
            else:
                markup = types.InlineKeyboardMarkup(row_width=1)
                button1 = types.InlineKeyboardButton('Заново', callback_data='again')
                markup.add(button1)
                bot.send_message(a.message.chat.id, 'Пожалуйста, завершите предыдущий квест или начните новый!', reply_markup=markup)
                return False


def quest_handler(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton('Начать', callback_data='quest')
    button2 = types.InlineKeyboardButton('Назад', callback_data='back')
    markup.add(button1, button2)
    bot.send_message(message.chat.id,
                     text='<i>Вы застряли в густом, непроходимом лесу без каких-либо средств к выживанию и воспоминаний о том, как сюда попали...</i>\n<b>Ваши действия?</b>', reply_markup=markup, parse_mode='HTML')


def quest(call: types.CallbackQuery):
    bot.delete_message(call.message.chat.id, call.message.id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    img = QUEST[call.data]['img']
    if not isinstance(img, list):
        img = [img, ]
    img = [open(i, 'rb') for i in img]
    if not call.data == 'Forest':
        data[str(call.from_user.id)] = (call.data, False)
        push_data(data)
        img = [choice(img), ]
    to_send = [types.InputMediaPhoto(i) for i in img]
    if 'options' in QUEST[call.data].keys():
        for i in QUEST[call.data]['options']:
            if isinstance(i['calling'], list):
                cb = choice(i['calling'])
            else:
                cb = i['calling']
            markup.add(types.InlineKeyboardButton(i['description'], callback_data=cb))
        bot.send_media_group(call.message.chat.id, to_send)
        bot.send_message(call.message.chat.id, text=QUEST[call.data]['text'], reply_markup=markup)
        closer(img)
    else:
        img = choice(img)
        bot.send_media_group(call.message.chat.id, to_send)
        button1 = types.InlineKeyboardButton('Вернуться в меню', callback_data='back')
        button2 = types.InlineKeyboardButton('Начать заново', callback_data='Forest')
        markup.add(button1, button2)
        bot.send_message(call.message.chat.id, text=QUEST[call.data]['text'], reply_markup=markup)
        bot.send_message(call.message.chat.id, text=QUEST[call.data]['ending'])
        closer(img)
        data[str(call.from_user.id)] = (call.data, True)
        push_data(data)


def begin_handler(call: types.CallbackQuery, bot: telebot.TeleBot):
    if isinstance(call, types.CallbackQuery):
        bot.delete_message(call.message.chat.id, call.message.id)
        call = call.message
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.InlineKeyboardButton("👋")
    button3 = types.InlineKeyboardButton("На что ты способен???")
    button4 = types.InlineKeyboardButton("/help")
    button5 = types.InlineKeyboardButton('/quest')
    markup.add(button1, button3, button4, button5)
    if call.from_user.is_bot:
        bot.send_message(call.chat.id, text="Здравствуйте! Я просто бот", reply_markup=markup)
    else:
        bot.send_message(call.chat.id, text="Здравствуйте, {}! Я просто бот".format(call.from_user.full_name), reply_markup=markup)


def helping_handler(message: types.Message, bot: telebot.TeleBot):
    bot.send_message(message.chat.id, text='В Вашем распоряжении данный <i>бот</i> и кнопки, на которых прописаны всевозможные действия (включая квест), то есть ввод с клавиатуры <b>не требуется</b>; можете отправить голосовое сообщение, я его запишу в файл.', parse_mode="HTML")


def what_handler(message: types.Message, bot: telebot.TeleBot):
    var = ['Ну даже не знаю, что ответить...', "Просто без слов", "Без понятия", "Да-да...", "Почему?", "Наверно",
           "Я не местный", "Это не ко мне", "На то есть GPT...", "???", "Я очень прямолинейный", "Дайте подумать...",
           "Это случайная фраза", "Число 'пи' ≈ 3,1415926535", 'Нет', "Не знаю", "Ничем не могу помочь...", "Я не умею думать, если что"]
    bot.send_message(message.chat.id, text=choice(var))


def get_voice_handler(message: types.Message, bot: telebot.TeleBot):
    voice = bot.get_file(message.voice.file_id)
    file = bot.download_file(voice.file_path)
    with open('media/the_voices.ogg', 'wb') as new_file:
        new_file.write(file)


def main_handler(message: types.Message, bot: telebot.TeleBot):
    if (message.text == "👋"):
        bot.send_message(message.chat.id, text="Привееет, {}".format(message.from_user.first_name))

    elif (message.text.lower() == "на что ты способен???"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.InlineKeyboardButton("Ты кто?")
        btn2 = types.InlineKeyboardButton("Что ты можешь?")
        back = types.InlineKeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Задайте мне вопрос", reply_markup=markup)
    elif (message.text.lower() == "ты кто?"):
        img = open('media/tree.jpg', 'rb')
        bot.send_photo(message.chat.id, photo=img, caption='А вот и я')
        bot.send_message(message.chat.id, "Мистическое дерево, <b>мудрый дуб</b> из 'Войны и мира' и тд - у меня много имён", parse_mode='HTML')
        img.close()


    elif message.text.lower() == "что ты можешь?":
        bot.send_message(message.chat.id, text="ВСЁ")

    elif (message.text.lower() == "вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.InlineKeyboardButton("👋")
        button3 = types.InlineKeyboardButton("На что ты способен???")
        button4 = types.InlineKeyboardButton("/help")
        button5 = types.InlineKeyboardButton('/quest')
        markup.add(button1, button3, button4, button5)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню.", reply_markup=markup)

    else:
        what_handler(message, bot)


def register_handlers(bot: telebot.TeleBot):
    """Функуция регестрирует хенделы"""
    bot.register_callback_query_handler(begin_handler, func=lambda call: call.data == 'back', pass_bot=True)
    bot.register_message_handler(begin_handler, content_types=['text'], commands=['start'], pass_bot=True)
    bot.register_message_handler(helping_handler, content_types=['text'], commands=['help'], pass_bot=True)
    bot.register_message_handler(quest_handler, content_types=['text'], commands=['quest'])
    bot.register_callback_query_handler(tracker, func=check_quest)
    bot.register_callback_query_handler(cont, func=lambda call: call.data == 'cont')
    bot.register_callback_query_handler(again, func=lambda call: call.data == 'again')
    bot.register_callback_query_handler(quest, func=lambda call: call.data in QUEST.keys())
    bot.register_message_handler(get_voice_handler, content_types=['voice'], pass_bot=True)
    bot.register_message_handler(main_handler, content_types=['text'], pass_bot=True)


register_handlers(bot)
bot.polling()
