
import sqlite3

# Подключаемся к базе данных или создаем новую базу данных, если ее нет
conn = sqlite3.connect('users.db')

# Создаем таблицу для хранения информации о пользователях
conn.execute('''CREATE TABLE IF NOT EXISTS users
             (numberid INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT,
             usersurname TEXT,
             course TEXT,
             userage INTEGER,
             pay BLOB)''')

# Запрашиваем у пользователя ввод информации и добавляем ее в таблицу "users"

username = input("Введите ваше имя: ")
usersurname = input("Введите вашу фамилию: ")
course = input("Введите ваш курс: ")
userage = int(input("Введите ваш возраст: "))
pay = int(input("Введите вашу зарплату: "))

conn.execute("INSERT INTO users (username, usersurname, course, userage, pay) VALUES (?, ?, ?, ?, ?)",
             (username, usersurname, course, userage, pay))
conn.commit()

# Закрываем соединение с базой данных
conn.close()
