import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def information(message: telebot.types.Message):
    text = ('Инструкция по применению:\n'
            '\n'
            'Чтобы начать работу введите следующую команду - \n'
            '<имя валюты, цену которой вы хочете узнать> \n'
            '<имя валюты, в которой надо узнать цену первой валюты> \n'
            '<количество первой валюты>. \n'
            '\n'
            'Чтобы увидеть список доступных валют введите: /values \n' 
            'Чтобы получить инструкцию введите: /help')

    bot.reply_to(message, text)


@bot.message_handler(commands=['values',])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text',])
def conversion(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Некорректное количество параметров')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()