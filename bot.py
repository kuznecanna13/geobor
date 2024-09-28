import telebot
from config import *
from logic import *
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, """Доступные команды:

/help - список команд
                     
/remember_city название города - сохранить город
                     
/show_city название города - показать город на карте
                     
/show_city color название цвета название города - показать город на карте с указанием цвета
                     
/show_my_cities - показать сохранённые города

/show_my_cities color название цвета - показать сохранённые города  с указанием цвета""")
    


@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    text = message.text.split()
    if 'color' in text:
        color = text[2]
        cities = text[3:]
    else:
        color = 'blue'
        cities = text[1:]
    user_id = message.chat.id
    path = f"users_images/img{user_id}.png"
    manager.create_grapf(path, cities, color)
    bot.send_photo(user_id, photo=open(path, 'rb'))


@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    city_name = message.text.split()[-1]
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    cities = manager.select_cities(message.chat.id)
    user_id = message.chat.id
    text = message.text.split()
    if 'color' in text:
        color = text[2]
    else:
        color = 'blue'
    path = f"users_images/img{user_id}.png"
    manager.create_grapf(path, cities, color)
    bot.send_photo(user_id, photo=open(path, 'rb'))



if __name__=="__main__":
    manager = DB_Map(DATABASE)
    bot.polling()
