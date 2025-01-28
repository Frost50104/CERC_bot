# в случае ошибки ввода - не возвращается к повторному запросу

from telebot import TeleBot
from telebot import types
from io import StringIO
from datetime import datetime
import requests

import config
import help_message

bot = TeleBot(config.TOKEN)


# Хранение временных данных
user_data = {}
result_message = ''


def ask_for_value(message, chat_id, field, question, next_handler):

    # Универсальная функция для обработки ввода значений.
    # Если значение некорректное, бот повторяет запрос.

    try:
        value = float(message.text)
        user_data[chat_id][field] = value

        if next_handler:  # Проверяем, указан ли следующий шаг
            bot.send_message(chat_id, question)
            bot.register_next_step_handler(message, next_handler)
        else:
            finalize_results(chat_id)  # Завершаем процесс, если нет следующего шага
    except ValueError:
        bot.send_message(chat_id, "Некорректное значение! Попробуйте ещё раз.")
        bot.register_next_step_handler(
            message, lambda msg: ask_for_value(msg, chat_id, field, question, next_handler)
        )


@bot.message_handler(commands=["start"])
def start_handler(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}  # Инициализируем данные пользователя
    bot.send_message(chat_id, "Введите входящую сумму в рублях:")
    bot.register_next_step_handler(
        message,
        lambda msg: ask_for_value(
            msg,
            chat_id,
            "rub_amount",
            "Введите курс RUB > EUR в ЦифраБанке:",
            handle_rub_to_eur,
        ),
    )


def handle_rub_to_eur(message):
    chat_id = message.chat.id
    ask_for_value(
        message,
        chat_id,
        "rub_to_eur",
        "Введите курс RUB > USDT на Bybit:",
        handle_rub_to_usdt,
    )


def handle_rub_to_usdt(message):
    chat_id = message.chat.id
    ask_for_value(
        message,
        chat_id,
        "rub_to_usdt",
        "Введите курс USDT > KZT на Bybit:",
        handle_usdt_to_kzt,
    )


def handle_usdt_to_kzt(message):
    chat_id = message.chat.id
    ask_for_value(
        message,
        chat_id,
        "usdt_to_kzt",
        "Введите курс KZT > EUR в FF Bank:",
        handle_kzt_to_eur,
    )


def handle_kzt_to_eur(message):
    chat_id = message.chat.id
    ask_for_value(
        message,
        chat_id,
        "kzt_to_eur",
        "Введите курс менялы:",
        handle_exchange_rate,
    )


def handle_exchange_rate(message):
    chat_id = message.chat.id
    ask_for_value(
        message,
        chat_id,
        "exchanger_rate",
        "",  # Пустой вопрос, завершаем обработку
        None,
    )


def finalize_results(chat_id):
    global result_message
    # Получение всех данных
    rub_amount = user_data[chat_id]["rub_amount"]
    rub_to_eur = user_data[chat_id]["rub_to_eur"]
    rub_to_usdt = user_data[chat_id]["rub_to_usdt"]
    usdt_to_kzt = user_data[chat_id]["usdt_to_kzt"]
    kzt_to_eur = user_data[chat_id]["kzt_to_eur"]
    exchanger_rate = user_data[chat_id]["exchanger_rate"]

    exit_eur_cifra = round((rub_amount-rub_amount*0.009)/rub_to_eur, 2)
    real_exchanger_rate_cifra = round(rub_amount/exit_eur_cifra, 2)   #ZeroDivisionError: float division by zero

    exit_cash_cifra = round(((rub_amount-rub_amount*0.009)/rub_to_eur)-(((rub_amount-rub_amount*0.009)/rub_to_eur)*0.02+3+5), 2)
    real_exchanger_rate_cifra_cash = round(rub_amount/exit_cash_cifra, 2)

    exit_eur_crypt = round(rub_amount/rub_to_usdt*usdt_to_kzt/kzt_to_eur, 2)
    real_exchanger_rate_eur_cript = round(rub_amount/exit_eur_crypt)

    exit_cash_crypt = round((rub_amount/rub_to_usdt*usdt_to_kzt/kzt_to_eur)-((rub_amount/rub_to_usdt*usdt_to_kzt/kzt_to_eur)*0.02+3+5), 2)
    real_exchanger_rate_crypt_cash = round(rub_amount/exit_cash_crypt, 2)

    exit_man = round(rub_amount/exchanger_rate, 2)




    # Текущая дата
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Формирование итогового сообщения
    result_message = (
        f"📅 Текущая дата: {current_date}\n\n"
        f"💵 Входящая сумма: {rub_amount} RUB\n"
        f"1. Курс RUB > EUR (ЦифраБанк): {rub_to_eur}\n"
        f"2. Курс RUB > USDT (Bybit): {rub_to_usdt}\n"
        f"3. Курс USDT > KZT (Bybit): {usdt_to_kzt}\n"
        f"4. Курс KZT > EUR (FF Bank): {kzt_to_eur}\n"
        f"5. Курс менялы: {exchanger_rate}\n\n"
        f"""Выход в евро Цифра: {exit_eur_cifra}
Курс Цифра: {real_exchanger_rate_cifra}

Выход в евро наличные через цифру: {exit_cash_cifra}
Курс наличных через цифру: {real_exchanger_rate_cifra_cash}
        
Выход евро через крипту: {exit_eur_crypt}
Курс Крипта: {real_exchanger_rate_eur_cript}
        
Выход в евро наличные через крипту: {exit_cash_crypt}
Курс наличных через крипту: {real_exchanger_rate_crypt_cash}
        
Выход в евро меняла: {exit_man}
Курс меняла: {exchanger_rate}
        """
    )

    # Отправка результата
    bot.send_message(
        chat_id = chat_id,
        text=result_message
    )

    # Предложение повторного запуска
    bot.send_message(
        chat_id= chat_id,
        text="""Введите /start, чтобы начать заново.
        \n
Введите /fix чтобы зафиксировать результат в специальном чате
        """
    )


@bot.message_handler(commands=['fix'])
def fix(message: types.Message):
    bot.send_message(
        chat_id=-4696327476,
        text=result_message
    )
    bot.send_message(
        chat_id=message.chat.id,
        text='Результа зафиксирован в чате\nВведите /start, чтобы начать заново.'
    )

#  Возвращает курс EUR к RUB по API
@bot.message_handler(commands=['api'])
def get_eur_to_rub_ratio(message: types.Message):
    from_currency = 'eur'
    to_currency = 'rub'
    response = requests.get(config.API_EXCHANGE_RATE)
    if response.status_code != 200:
        ratio_result = -1
    json_data = response.json()
    ratio_result = json_data[from_currency][to_currency]
    bot.send_message(
        chat_id=message.chat.id,
        text=f'Примерный курс евро: {ratio_result}'
    )



# Запуск бота
if __name__ == "__main__":
    print("Бот запущен!")
    bot.polling(none_stop=True)