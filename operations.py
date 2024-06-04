import math
from email import message
from database import Requests
from math import sqrt, sin, cos, tan
import telebot
import database


class Math_func:
    def __init__(self, id_func):
        self.id_func = id_func
        request =  Requests().select_math_function_by_id(id_func)[0]
        self.name = request['name']
        self.count_of_numbers = request['count_of_numbers']
    def plus(self, x, y):
        return x + y
    def difference(self, x, y):
        return x - y
    def multiplication(self, x, y):
        return x * y
    def division(self, x, y):
        return x / y
    def square_root(self, x):
        return sqrt(x)
    def abs(self, x):
        return abs(x)
    def sin(self,x):
        return math.sin(x)
    def cos(self, x):
        return math.cos(x)
    def tan(self, x):
        return math.tan(x)
    def get_function(self):
        if self.name == "деление":
            return self.division
        elif self.name == "сложение":
            return self.plus
        elif self.name == "вычитание":
            return self.difference
        elif self.name == 'умножение':
            return self.multiplication
        elif self.name == 'квадратный корень':
            return self.square_root
        elif self.name == 'модуль':
            return self.abs
        elif self.name == 'синус':
            return self.sin
        elif self.name == 'косинус':
            return self.cos
        elif self.name == 'тангенс':
            return self.tan
    @staticmethod
    def get_id_func_by_symbol(symbol):
        funcs = Requests().select_math_functions()
        for func in funcs:
            if func['symbol'] == symbol:
                return func['id_func']
class Operations:
    def __init__(self, first_number, id_person, id_func, second_number=None):
        self.first_number = first_number
        self.second_number = second_number
        self.id_person = id_person
        self.func = Math_func(id_func)

    def calculate(self):
        '''
            Расчитываем значение выражения по first_number и second_number (если необходимо)
        '''
        if self.func.count_of_numbers == 2:
            func = self.func.get_function()
            self.result = func(self.first_number, self.second_number)
        elif self.func.count_of_numbers == 1:
            func = self.func.get_function()
            self.result = func(self.first_number)
        else:
            raise ValueError("В базе данных некорректное количество чисел для функции")

    def get_result(self):
        '''
            Вернуть результат пользователю. Тип возращаемого значения: float
        '''
        return self.result

    def setup_to_database(self):
        '''
            Отправка результата в таблицу функцией add_operations
        '''
        if self.second_number is None:
            Requests().add_operations_nm1(self.id_person, self.func.id_func, self.first_number, self.result)
        else:
            Requests().add_operations(self.id_person, self.func.id_func, self.first_number, self.second_number, self.result)
