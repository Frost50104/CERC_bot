from telebot import TeleBot
from telebot import types
from io import StringIO
import datetime

import config
import help_message

bot = TeleBot(config.TOKEN)

value = None
exchange_cifra = None
exchange_bybit_usdt = None
exchange_bybit_kzt = None
exchange_eur_ff = None
exchange_man = None

@bot.message_handler(commands=['start'])
def start(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text='Добро пожаловать в калькулятор курса обмена',
    )
    bot.send_message(
        chat_id=message.chat.id,
        text='Укажите сумму для обмена (RUB)',
    )
    bot.register_next_step_handler(message, handle_value)  # запуск следующего обработчика




@bot.message_handler()
def handle_value(message: types.Message):
    global value
    try:
        # Пробуем преобразовать сообщение в целое число
        value = int(message.text)
        bot.send_message(
            chat_id=message.chat.id,
            text=f"Меняем {value} руб"
        )
    except ValueError:
        # Если введено не число, отправляем сообщение об ошибке
        bot.send_message(
            chat_id=message.chat.id,
            text="Пожалуйста, введите корректное целое число"
        )
    print('Входящая сумма: ', value)
    bot.send_message(
        chat_id=message.chat.id,
        text='Введите курс RUB > EUR в ЦифраБанке',
    )
    bot.register_next_step_handler(message, handle_cifra) # запуск следующего обработчика

@bot.message_handler()
def handle_cifra(message: types.Message):
    global exchange_cifra
    try:
        # Пробуем преобразовать сообщение в целое число
        exchange_cifra = int(message.text)
        bot.send_message(
            chat_id=message.chat.id,
            text=f"Курс в Цифре: {exchange_cifra} евро"
        )
    except ValueError:
        # Если введено не число, отправляем сообщение об ошибке
        bot.send_message(
            chat_id=message.chat.id,
            text="Пожалуйста, введите корректное целое число"
        )
    print('Курс Цифра: ', exchange_cifra)
    bot.send_message(
        chat_id=message.chat.id,
        text='Введите курс RUB > USDT на ByBit',
    )
    bot.register_next_step_handler(message, handle_usdt_bybit)  # запуск следующего обработчика

@bot.message_handler()
def handle_usdt_bybit(message: types.Message):
    global exchange_bybit_usdt
    try:
        # Пробуем преобразовать сообщение в целое число
        exchange_bybit_usdt = int(message.text)
        bot.send_message(
            chat_id=message.chat.id,
            text=f"Курс USDT: {exchange_bybit_usdt} руб"
        )
    except ValueError:
        # Если введено не число, отправляем сообщение об ошибке
        bot.send_message(
            chat_id=message.chat.id,
            text="Пожалуйста, введите корректное целое число"
        )
    print('Курс USDT: ', exchange_bybit_usdt)
    bot.send_message(
        chat_id=message.chat.id,
        text='Введите курс USDT > KZT на ByBit',
    )
    bot.register_next_step_handler(message, handle_kzt_bybit)  # запуск следующего обработчика

@bot.message_handler()
def handle_kzt_bybit(message: types.Message):
    global exchange_bybit_kzt
    try:
        # Пробуем преобразовать сообщение в целое число
        exchange_bybit_kzt = int(message.text)
        bot.send_message(
            chat_id=message.chat.id,
            text=f"Курс KZT: {exchange_bybit_kzt} USDT"
        )
    except ValueError:
        # Если введено не число, отправляем сообщение об ошибке
        bot.send_message(
            chat_id=message.chat.id,
            text="Пожалуйста, введите корректное целое число"
        )
    print('Курс KZT: ', exchange_bybit_kzt)
    bot.send_message(
        chat_id=message.chat.id,
        text='Введите курс KZT > EUR в FF bank',
    )
    bot.register_next_step_handler(message, handle_eur_ff)

@bot.message_handler()
def handle_eur_ff(message: types.Message):
    global exchange_eur_ff
    try:
        # Пробуем преобразовать сообщение в целое число
        exchange_eur_ff = int(message.text)
        bot.send_message(
            chat_id=message.chat.id,
            text=f"Курс EUR: {exchange_eur_ff} KZT"
        )
    except ValueError:
        # Если введено не число, отправляем сообщение об ошибке
        bot.send_message(
            chat_id=message.chat.id,
            text="Пожалуйста, введите корректное целое число"
        )
    print('Курс EUR: ', exchange_eur_ff)
    bot.send_message(
        chat_id=message.chat.id,
        text='Введите курс менялы',
    )
    bot.register_next_step_handler(message, handle_man)

@bot.message_handler()
def handle_man(message: types.Message):
    global exchange_man
    try:
        # Пробуем преобразовать сообщение в целое число
        exchange_man = int(message.text)
        bot.send_message(
            chat_id=message.chat.id,
            text=f"Курс EUR у менялы: {exchange_man} RUB"
        )
    except ValueError:
        # Если введено не число, отправляем сообщение об ошибке
        bot.send_message(
            chat_id=message.chat.id,
            text="Пожалуйста, введите корректное целое число"
        )
    print('Курс EUR у менялы: ', exchange_man)
    bot.send_message(
        chat_id=message.chat.id,
        text=f""" <b>{datetime.date.today()}</b>
        
Входящая сумма: {value}   
Курс Цифра: {exchange_cifra}
Курс USDT: {exchange_bybit_usdt}
Курс KZT: {exchange_bybit_kzt}
Курс EUR: {exchange_eur_ff}
Курс EUR у менялы: {exchange_man}
        
Выход в евро Цифра: {(value-value*0.009)/exchange_cifra}
Курс Цифра: {value/((value-value*0.009)/exchange_cifra)}

Выход в евро наличные через цифру: {((value-value*0.009)/exchange_cifra)-(((value-value*0.009)/exchange_cifra)*0.02+3+5)}
Курс наличных через цифру: {value/(((value-value*0.009)/exchange_cifra)-(((value-value*0.009)/exchange_cifra)*0.02+3+5))}
        
Выход евро через крипту: 
Курс Крипта:
        
Выход в евро наличные через крипту:
Курс наличных через крипту:
        
Выход в евро меняла:
Курс меняла:
        """,
        parse_mode='HTML'
    )


if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)