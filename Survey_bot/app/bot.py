'''
Бучминский Якуб, 32 группа
*API_KEY прописан в отдельном файле .env
'''

import telebot, os
from telebot import types
from random import choice
from info import SURVEY, get_data, push_data
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent

load_dotenv(BASE_DIR / '.env')  # take environment variables from .env.
API_KEY = os.getenv('API_KEY')
f = True
data = get_data()
bot = telebot.TeleBot(API_KEY)


def step(call: types.CallbackQuery):
    a = data[str(call.message.from_user.id)]
    if len(a) < 3:
        call.data = a[-1]
        a = a[:-1]
        [survey_second, survey_third][len(a) - 1](call)
    else:
        call.data = ''
        data[str(call.message.from_user.id)] = ''
        push_data(data)
        survey_first(call)


def cont(call: types.CallbackQuery):
    if str(call.message.from_user.id) in list(data.keys()):
        if len(data[str(call.message.from_user.id)]) != 0:
            markup = types.InlineKeyboardMarkup(row_width=1)
            button1 = types.InlineKeyboardButton('Продолжить', callback_data=f'cont')
            button2 = types.InlineKeyboardButton("Заново", callback_data='again')
            markup.add(button1, button2)
            bot.send_message(call.message.chat.id, text='Желаете продолжить незавершённое тестирование или начать заново?', reply_markup=markup)
        else:
            call.data = ''
            survey_first(call)
    else:
        data[str(call.message.from_user.id)] = ''
        call.data = ''
        survey_first(call)


def closer(message, a):
    for i in a:
        i.seek(0)


def check_survey(a: types.CallbackQuery):
    global data, f
    if isinstance(a, types.CallbackQuery):

        if a.data == 'func':
            if f:
                f = False
                return True
            else:
                bot.send_message(a.message.chat.id, 'Пожалуйста, завершите предыдущий тест, прежде чем начать новый!')
                return False


def survey_first(call: types.CallbackQuery):
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.send_message(call.message.chat.id, text='Предлагаем вам пройти анкету ')
    markup = types.InlineKeyboardMarkup(row_width=1)
    text = SURVEY['first']['answers']
    button1 = types.InlineKeyboardButton(text[0], callback_data='1_0')
    button2 = types.InlineKeyboardButton(text[1], callback_data='1_1')
    markup.add(button1, button2)
    bot.send_message(call.message.chat.id, text=f'<b><i>{SURVEY["first"]["question"]}</i></b>', reply_markup=markup, parse_mode='HTML')


def survey_second(call: types.CallbackQuery):
    bot.delete_message(call.message.chat.id, call.message.id)
    data[str(call.message.from_user.id)] += call.data[-1]
    push_data(data)
    markup = types.InlineKeyboardMarkup(row_width=1)
    text = SURVEY['second']['answers']
    button1 = types.InlineKeyboardButton(text[0], callback_data='2_0')
    button2 = types.InlineKeyboardButton(text[1], callback_data='2_1')
    button3 = types.InlineKeyboardButton(text[2], callback_data='2_2')
    markup.add(button1, button2, button3)
    bot.send_message(call.message.chat.id, text=f'<b><i>{SURVEY["second"]["question"]}</i></b>', reply_markup=markup, parse_mode='HTML')


def survey_third(call: types.CallbackQuery):
    bot.delete_message(call.message.chat.id, call.message.id)
    data[str(call.message.from_user.id)] += call.data[-1]
    push_data(data)
    markup = types.InlineKeyboardMarkup(row_width=1)
    text = SURVEY['third']['answers']
    button1 = types.InlineKeyboardButton(text[0], callback_data='3_0')
    button2 = types.InlineKeyboardButton(text[1], callback_data='3_1')
    markup.add(button1, button2)
    bot.send_message(call.message.chat.id, text=f'<b><i>{SURVEY["third"]["question"]}</i></b>', reply_markup=markup, parse_mode='HTML')


def survey_ending(call: types.CallbackQuery):
    global f
    bot.delete_message(call.message.chat.id, call.message.id)
    data[str(call.message.from_user.id)] += call.data[-1]
    staff = SURVEY['choose'][data[str(call.message.from_user.id)]]
    to_send = [types.InputMediaPhoto(staff[i]) if i != (len(staff) - 1) else types.InputMediaPhoto(staff[i], f'<i>{staff[0]}</i>', parse_mode='HTML') for i in range(1, len(staff))]
    bot.send_media_group(call.message.chat.id, to_send)
    f = True
    data[str(call.message.from_user.id)] = ''
    push_data(data)
    closer(call.message, staff[1:])


def begin_handler(call: types.CallbackQuery, bot: telebot.TeleBot):
    if isinstance(call, types.CallbackQuery):
        bot.delete_message(call.message.chat.id, call.message.id)
        call = call.message
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.InlineKeyboardButton("👋")
    button2 = types.InlineKeyboardButton('Анкета')
    button3 = types.InlineKeyboardButton("На что ты способен???")
    button4 = types.InlineKeyboardButton("/help")
    markup.add(button1, button2, button3, button4)
    bot.send_message(call.chat.id,
                     text="Здравствуйте, {}! Я просто бот".format(
                         call.from_user.full_name), reply_markup=markup)


def helping_handler(message: types.Message, bot: telebot.TeleBot):
    bot.send_message(message.chat.id, text='В Вашем распоряжении данный <i>бот</i> и кнопки, на которых прописаны всевозможные действия, то есть ввод с клавиатуры <b>не требуется</b>; можете отправить голосовое сообщение, я его запишу в файл.', parse_mode="HTML")


def what_handler(message: types.Message, bot: telebot.TeleBot):
    var = ['Ну даже не знаю, что ответить...', "Просто без слов", "Без понятия", "Да-да...", "Почему?", "Наверно",
           "Я не местный", "Это не ко мне", "На то есть GPT...", "???", "Я очень прямолинейный", "Дайте подумать...",
           "Это случайная фраза", "Число 'пи' ≈ 3,1415926535", 'Нет', "Не знаю", "Ничем не могу помочь..."]
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
        bot.send_photo(message.chat.id, photo=open('media/tree.jpg', 'rb'), caption='А вот и я')
        bot.send_message(message.chat.id, "Мистическое дерево, <b>мудрый дуб</b> из 'Войны и мира' и тд - у меня много имён", parse_mode='HTML')

    elif message.text.lower() == "что ты можешь?":
        bot.send_message(message.chat.id, text="ВСЁ")

    elif (message.text.lower() == "вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.InlineKeyboardButton("👋")
        button2 = types.InlineKeyboardButton('Анкета')
        button3 = types.InlineKeyboardButton("На что ты способен???")
        button4 = types.InlineKeyboardButton("/help")
        markup.add(button1, button2, button3, button4)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню.", reply_markup=markup)
    elif (message.text.lower() == 'анкета'):
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Продолжить', callback_data='func')
        button2 = types.InlineKeyboardButton('Вернуться в главное меню⬅️', callback_data='back')
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text='Данный бот предлагает возможность поучаствовать в тесте,\nкоторый предложит Вам страну для комфортабельного проживания по некоторым критериям', reply_markup=markup)
    else:
        what_handler(message, bot)


def register_handlers(bot: telebot.TeleBot):
    """Функуция регестрирует хенделы"""
    bot.register_callback_query_handler(begin_handler, func=lambda call: call.data == 'back', pass_bot=True)
    bot.register_callback_query_handler(cont, func=check_survey)
    bot.register_callback_query_handler(step, func=lambda call: call.data == 'cont')
    bot.register_callback_query_handler(survey_first, func=lambda call: call.data == 'again')
    bot.register_callback_query_handler(survey_second, func=lambda call: call.data[0] == '1')
    bot.register_callback_query_handler(survey_third, func=lambda call: call.data[0] == '2')
    bot.register_callback_query_handler(survey_ending, func=lambda call: call.data[0] == '3')
    bot.register_message_handler(begin_handler, content_types=['text'], commands=['start'], pass_bot=True)
    bot.register_message_handler(helping_handler, content_types=['text'], commands=['help'], pass_bot=True)
    bot.register_message_handler(get_voice_handler, content_types=['voice'], pass_bot=True)
    bot.register_message_handler(main_handler, content_types=['text'], pass_bot=True)



register_handlers(bot)
bot.polling()
