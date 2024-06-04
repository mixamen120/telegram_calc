CREATE DATABASE telegram_calc;
USE telegram_calc;

CREATE TABLE persons (
id_person INT NOT NULL PRIMARY KEY,
name VARCHAR(20) NOT NULL,
surname VARCHAR(20) NOT NULL
);

CREATE TABLE math_functions (
id_func INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
symbol VARCHAR(5) NOT NULL,
name VARCHAR(20) NOT NULL,
count_of_numbers INT NOT NULL
);

CREATE TABLE operations (
id_operation INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
id_person INT NOT NULL,
id_func INT NOT NULL,
first_number INT NOT NULL,
second_number INT,
result INT NOT NULL,
FOREIGN KEY (id_person) REFERENCES persons (id_person) ON DELETE CASCADE,
FOREIGN KEY (id_func) REFERENCES math_functions (id_func) ON DELETE CASCADE
);

INSERT INTO math_functions
(symbol, name, count_of_numbers)
VALUES
('| |','модуль', 1),
('sin','синус', 1),
('cos','косинус', 1),
('tg','тангенс', 1),
('/', 'деление', 2),
('+','сложение', 2),
('-','вычитание', 2),
('*','умножение', 2),
('√','квадратный корень', 2);

