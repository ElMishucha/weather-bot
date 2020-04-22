import telebot

from telebot import types

import pyowm

BOT_TOKEN = open("BOT_API.txt", "r").read()
OWM_API = open("OWM_API.txt", "r").read()
COMMANDS = (
    "temperature",
    "wind",
    "humidity",
    "clouds"
)
owm = pyowm.OWM(OWM_API)
bot = telebot.TeleBot(BOT_TOKEN)

observation = owm.weather_at_place('Kharkiv, UA')

def create_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=len(COMMANDS))
    buttons = [types.InlineKeyboardButton(text=c, callback_data=c) for c in COMMANDS]
    keyboard.add(*buttons)
    return keyboard
@bot.callback_query_handler(func = lambda x: True)
def callback_hangler(callback_query):
    message = callback_query.message
    text = callback_query.data
    if text == 'wind':
        global wi
        
        ang_wind = str(wi['deg'])
        speed_wind = wi['speed']
        bot.send_message(message.chat.id, f"Направление ветра: {ang_wind}° от севера. Скорость: {speed_wind} м/с.")
    elif text == 'temperature':
        global c
 
        celsius = c['temp']
        max_temp = c['temp_max']
        min_temp = c['temp_min']
        # bot.send_message(553053278, f"{message.from_user.first_name} {message.from_user.last_name}")
        bot.send_message(message.chat.id, f'Сейчас в твоем городе: {celsius}° C. А максимальная температура сегодня была: {max_temp}° C, а минимальная: {min_temp}° C.')
        if celsius > 10:
            bot.send_message(message.chat.id, f'Сегодня стоило бы одеться полегче.')
        elif celsius > 20:
            bot.send_message(message.chat.id, f"Ухх, сегодня выходи в майке и трусах ))")
        elif celsius < 0:
            bot.send_message(message.chat.id, f"Брррр, одева..аай ш..шшубу..уу, скк..корей")
        elif celsius < 10:
            bot.send_message(message.chat.id, f"Шапку не забудь!")
    elif text == 'clouds':
        global cl
        bot.send_message(message.chat.id, f"Облачность составляет {cl}%.")
    elif text == 'humidity':  
        global h 
        bot.send_message(message.chat.id, f"Влажность составляет {h}%.")
@bot.message_handler(commands = ['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}. Я твой бот, который поможет с погодой. Для большей информации напишите /help.")
@bot.message_handler(commands = ['help'])
def send_help(message):
    keyboard = create_keyboard()
    bot.send_message(message.chat.id, f'Что тебя интересует?', reply_markup=keyboard)       

observation = owm.weather_at_place('Kharkiv, UA')
w = observation.get_weather()
cl = w.get_clouds() 
c = w.get_temperature('celsius')
wi = w.get_wind()
h = w.get_humidity() 
bot.polling()