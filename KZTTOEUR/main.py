import telebot
from config import TOKEN # импортируем токен бота из файла конфига
from extensions import APIException, CurrencyConverter # классы в файле extensions.py

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help']) # Обработчик команды /start и /help
def send_welcome(message):
    text = 'Привет! Я бот-обменник, который поможет посчитать сколько ' \
           'тенге в долларах, в евро, в юанях, в золоте, ' \
           'сколько долларов в евро, в золоте, в тенге, в юанях и наоборот. ' \
           'Чтобы начать, напишите, а для удобства нажмите /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values']) # Обработчик команды /values
def send_currencies(message):
    currencies = [
        'KZT - тенге',
        'USD - доллар США',
        'EUR - евро',
        'CNY - юань',
        'XAU - золото',
        'Напишите в формате: USD KZT 100'
    ]
    text = '\n'.join(currencies)
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: True) # Обработчик текстовых сообщений
def get_price(message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException('Неверный формат ввода. Напишите /values для получения списка поддерживаемых валют')

        valid_currencies = ['KZT', 'USD', 'EUR', 'CNY', 'XAU']
        if values[0].upper() not in valid_currencies or values[1].upper() not in valid_currencies:
            raise APIException(f'Неправильно указаны валюты. Например: CNY USD 400')

        base, quote, amount = values

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Некорректное число: {amount}. Введите число, например, 100')

        if base.upper() == quote.upper():
            raise APIException(f'Вы указали одинаковые валюты: {base} {quote}')

        total = CurrencyConverter.get_price(base, quote, float(amount))
        text = f'{amount} {base.upper()} = {total} {quote.upper()}'
        bot.send_message(message.chat.id, text)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка: {str(e)}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {str(e)}')

bot.polling(none_stop=True)