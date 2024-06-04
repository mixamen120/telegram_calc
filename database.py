import pymysql

from sql_query import *
class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='LuLuba123!',
            database='telegram_calc',
            cursorclass=pymysql.cursors.DictCursor
        )
    def execute(self,query):
        with self.connection.cursor() as cursor:
            cursor.execute(query)

        self.connection.commit()
        result = cursor.fetchall()
        return result

class Requests:
    def add_person(self, id, name, surname):
        db = Database()
        db.execute(ADD_PERSON.format(id, name, surname))
    def select_person(self):
        db = Database()
        return db.execute(SELECT_PERSON)

    def select_math_functions(self):
        db = Database()
        return db.execute(SELECT_MATH_FUNCTIONS)

    def add_operations(self, id_person, id_func, first_number, second_number, result):
        db = Database()
        db.execute(ADD_OPERATIONS.format(id_person, id_func, first_number, second_number, result))

    def add_operations_nm1(self, id_person, id_func, first_number, result):
        db = Database()
        db.execute(ADD_OPERATIONS_1.format(id_person, id_func, first_number, result))

    def select_math_function_by_id(self, id_func):
        db = Database()
        return db.execute(SELECT_MATH_FUNCTION_BY_ID.format(id_func))