ADD_PERSON="""
INSERT INTO persons
(id_person, name, surname)
VALUES
({0}, '{1}', '{2}');
"""
SELECT_PERSON="""
SELECT * FROM persons
"""
SELECT_MATH_FUNCTIONS = """
SELECT * FROM math_functions
"""
ADD_OPERATIONS = """
INSERT INTO operations
(id_person, id_func, first_number, second_number, result)
VALUES
({0},{1},{2},{3},{4})
"""
SELECT_MATH_FUNCTION_BY_ID = """
SELECT * FROM math_functions
WHERE id_func = {0};
"""
ADD_OPERATIONS_1 = """
INSERT INTO operations
(id_person, id_func, first_number, result)
VALUES
({0},{1},{2},{3})
"""