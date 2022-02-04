import telebot
from api import *
import dict

bot = telebot.TeleBot('TELE_TOKEN', parse_mode="HTML")

logger.add("logging.log", format="{time}, {level}, {message}", level="DEBUG", encoding="UTF-8")


@bot.message_handler(commands=['start'])
@logger.catch()
def start_bot(message: telebot.types.Message):
    if message.chat.id in [CHAT_ID, CHAT_ID]:
        bot.send_message(message.chat.id, "Бот запустился, пиши полное название кампании")
        bot.register_next_step_handler(message, get_full_name_campaigns)

@logger.catch()
def get_full_name_campaigns(message: telebot.types.Message):
    campaigns = message.text
    data_campaigns = get_campaings(campaigns)
    bot.send_message(message.chat.id, 'Пиши Id ГЕО')
    bot.register_next_step_handler(message, get_geo, data_campaigns)

@logger.catch()
def get_geo(message, data: dict):
    ge = message.text.split('\n')
    geo = []
    country_dict = dict.country()
    for item in ge:
        flag = True
        for country in country_dict['payload']:
            if item == country['name']:
                geo.append(country['id'])
                flag = False
        if flag:
            bot.send_message(message.chat.id, f'Некорректное название страны: {item}')
    for index in geo:
        data['countryId'] = index
        country = post_create_campaigns(data)
        bot.send_message(message.chat.id, f'Кампания: {country[1]}, Ссылка: {country[0]}')







bot.polling()