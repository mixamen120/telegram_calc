import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

from database import Requests
from operations import Math_func, Operations
from persons import Person
from handlers import is_float_digit

bot = telebot.TeleBot(token="6753365422:AAFyeVKBU_4-lMQjvMWgoBMuza2apRTeN18")
numbers = '0123456789'

@bot.message_handler(commands=["start"])
def welcome(message: Message):
    person = Person(message.from_user.id)
    person.authorize()
    if person.is_authorized == True:
        bot.send_message(chat_id=message.chat.id, text=f"Привет, {person.name}!")
        menu(message, person)
    else:
        registration(message, person)
@bot.message_handler(commands=["menu"])
def menu(message: Message, person=None):
    if person is None:
        person = init_person(message)
    keyboard = ReplyKeyboardMarkup()
    button_calculator = KeyboardButton(text="Калькулятор")
    button_how_are_you = KeyboardButton(text="Поговорить")
    keyboard.add(button_calculator, button_how_are_you)
    msg = bot.send_message(chat_id=message.chat.id, text=f"{person.name}, выберите функцию!", reply_markup=keyboard)
    bot.register_next_step_handler(msg, define_action_for_menu, person)

def define_action_for_menu(message: Message, person):
    if message.text.lower() == 'калькулятор':
        calculate(message, person)
    elif message.text.lower() == 'поговорить':
        how_are_you(message, person)

def init_person(message: Message):
    person = Person(message.from_user.id)
    person.authorize()
    if person.is_authorized == False:
        registration(message,person)
    return person

def registration(message: Message, person):
    msg = bot.send_message(chat_id=message.chat.id, text="Привет, Вы не зарегистированы! Введите имя и фамилию, через пробел, в одной строке.")
    bot.register_next_step_handler(msg, define_persons_name_and_surname, person)

def define_persons_name_and_surname(message: Message, person):
    name_surname = message.text.lower().split()
    if len(name_surname) == 2:
        name = name_surname[0]
        surname = name_surname[1]
        person.registration(name, surname)
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Вы успешно зарегистрированы!")
    else:
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Запись не правильная")
        bot.register_next_step_handler(msg, registration, person)


@bot.message_handler(commands=["how_are_you"])
def how_are_you(message: Message, person):
    keyboard = ReplyKeyboardMarkup()
    button1 = KeyboardButton(text="Хорошо")
    button2 = KeyboardButton(text="Плохо")
    keyboard.add(button1, button2)
    msg = bot.send_message(chat_id=message.chat.id, text="Хорошо, а у тебя?", reply_markup=keyboard)
    bot.register_next_step_handler(msg, define_answer_for_how_are_you)

def define_answer_for_how_are_you(message: Message):
    if message.text.lower() == "хорошо":
        bot.send_message(chat_id=message.chat.id, text="Супер!")
    elif message.text.lower() == "плохо":
        bot.send_message(chat_id=message.chat.id, text="Не супер")
    else:
        bot.send_message(chat_id=message.chat.id, text="Не понимаю")


@bot.message_handler(commands=["calculate"])
def calculate(message: Message, person=None):
    if person is None:
       person = init_person(message)
    keyboard = ReplyKeyboardMarkup(row_width=4)
    math_funcs = Requests().select_math_functions()
    for math_func in math_funcs:
        button = KeyboardButton(text=math_func['symbol'])
        keyboard.add(button)
    msg = bot.send_message(chat_id=message.chat.id, text="Выберите операцию.", reply_markup=keyboard)
    bot.register_next_step_handler(msg, define_number1, person)


def define_number1(message: Message, person):
    operation = message.text
    msg = bot.send_message(chat_id=message.chat.id, text="Введите первое число")
    id_function = Math_func.get_id_func_by_symbol(operation)
    if Math_func(id_function).count_of_numbers == 1:
        bot.register_next_step_handler(msg, calculator, operation, person)
    else:
        bot.register_next_step_handler(msg, define_number2, operation, person)

def define_number2(message: Message, operation, person):
    if message.text.isdigit():
        num1 = int(message.text)
    else:
        bot.send_message(chat_id=message.chat.id, text="Вы ввели не число, попробуйте еще раз запустить команду")
        return
    msg = bot.send_message(chat_id=message.chat.id, text="Введите второе число")
    bot.register_next_step_handler(msg, calculator, operation, person, num1)

def calculator(message: Message, symbol, person,  num1=None):
    if num1 is not None:
        if is_float_digit(message.text):
            num2 = float(message.text)
        else:
            bot.send_message(chat_id=person.ID,
                             text='Вы ввели неккоректное число')
            return

    else:
        if is_float_digit(message.text):
            num1 = float(message.text)
            num2 = None
        else:
            bot.send_message(chat_id=person.ID,
                             text='Вы ввели неккоректное число')
            return

    id_func = Math_func.get_id_func_by_symbol(symbol)
    operation = Operations(id_func=id_func, id_person=person.ID, first_number=num1, second_number=num2)
    operation.calculate()
    operation.setup_to_database()
    bot.send_message(chat_id=person.ID, text=f'Результат математической операции {round(operation.get_result(), 4)}')



bot.polling()