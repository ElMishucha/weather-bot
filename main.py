import telebot

import pyowm

BOT_TOKEN = open("BOT_API.txt", "r").read()
OWM_API = open("OWM_API.txt", "r").read()
COMMANDS = (
    "help",
    "temperature",
    "wind",
    "humidity"
)
owm = pyowm.OWM(OWM_API)
bot = telebot.TeleBot(BOT_TOKEN)

observation = owm.weather_at_place('Kharkiv, UA')


w = observation.get_weather()
c = w.get_temperature('celsius')
wi = w.get_wind()
h = w.get_humidity() 

celsius = c['temp']
ang_wind = str(wi['deg'])
speed_wind = wi['speed']

@bot.message_handler(commands = ['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Привет. Я твой бот, который поможет с погодой. Для большей информации напишите /help.")
    print(message.from_user.first_name)
@bot.message_handler(commands = ['help'])
def send_help(message):
    bot.send_message(message.chat.id, f'Можешь мне сказать сделать:')
    s = ''
    for mes in COMMANDS:
        s += '/'
        s += mes
        s += '\n'
    bot.send_message(message.chat.id, f"{s}")        
    print(message.from_user.first_name)
@bot.message_handler(commands = ['temp', 'temperature'])
def temp(message):
    bot.send_message(message.chat.id, f'Сейчас в твоем городе: {celsius}° C.')
    if celsius > 10:
        bot.send_message(message.chat.id, f'Сегодня стоило бы одеться потеплее.')
    elif celsius > 20:
        bot.send_message(message.chat.id, f"Ухх, сегодня выходи в майке и трусах ))")
    elif celsius < 10:
        bot.send_message(message.chat.id, f"Брррр, одева..аай ш..шшубу..уу, скк..корей")
    print(message.from_user.first_name)
@bot.message_handler(commands = ['wind'])
def wind(message):
    global ang_wind
    if int(ang_wind) % 8 == [0 or 1]:
        ang_wind = 'N'
    elif int(ang_wind) % 8 == [2 or 3]:
        ang_wind = 'E'
    elif int(ang_wind) % 8 == [4 or 5]:
        ang_wind = 'S'
    elif int(ang_wind) % 8 == [6 or 7]:
        ang_wind = 'W'
    bot.send_message(message.chat.id, f"Направление ветра: {ang_wind} от севера. Скорость: {speed_wind} м/с.")
    print(message.from_user.first_name)
@bot.message_handler(commands = ['humidity'])
def humidity(message):
    bot.send_message(message.chat.id, f"Влажность составляет {h}%.")
bot.polling()