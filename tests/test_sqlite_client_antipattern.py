import sqlite3

from clients.sqlite3_client import SQLiteClient
from tests.conftest import TEST_DB_URL

# запрос для создания таблицы
CREATE_USER_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS users (
user_id serial NOT NULL,
username varchar NOT NULL,
chat_id integer NOT NULL
);
"""

# запрос для спиливания таблиц
DROP_USER_TABLE_QUERY = """
DROP TABLE users;
"""


def test_write_to_db_by_command():
    # для начала создаём для тестирования этого отдельный коннект к БД, чтобы всё было независимо.
    # запускаем команду для создания таблиц
    db_connection = sqlite3.connect(TEST_DB_URL)
    cursor = db_connection.cursor()
    db_connection.execute(CREATE_USER_TABLE_QUERY)
    db_connection.commit()

    # команда, которая будет использоваться для тестирования клиента
    command = """
    INSERT INTO users (user_id, username, chat_id) VALUES (?, ?, ?);
    """

    # тестовые данные
    user_id = 1
    username = "luchanos"
    chat_id = 123123

    # создаём клиент, который мы будем тестировать
    client = SQLiteClient(TEST_DB_URL)
    client.create_conn()

    # запускаем команду на запись в базу
    client.execute_command(command, (user_id, username, chat_id))

    # после этого ожидается, что в базе отобразится записанная строка и нам надо в этом убедиться.
    # запускаем команду на чтение строк из базы
    cursor.execute("""SELECT * FROM users;""")
    users = cursor.fetchall()

    # проверяем, что в базу действительно всё прописалось
    assert len(users) == 1
    user = users[0]
    assert user[0] == user_id
    assert user[1] == username
    assert user[2] == chat_id

    # удаляем таблицу
    db_connection.execute(DROP_USER_TABLE_QUERY)
    db_connection.commit()


def test_read_from_db_by_client():
    # для начала создаём для тестирования этого отдельный коннект к БД, чтобы всё было независимо.
    # запускаем команду для создания таблиц
    db_connection = sqlite3.connect(TEST_DB_URL)
    db_connection.execute(CREATE_USER_TABLE_QUERY)
    db_connection.commit()

    # тестовые данные
    user_id = 1
    username = "luchanos"
    chat_id = 123123

    # создадим в базе строку, которую потом будем читать с помощью тестируемого клиента
    db_connection = sqlite3.connect(TEST_DB_URL)
    db_connection.execute("""INSERT INTO users (user_id, username, chat_id) VALUES (?, ?, ?);""",
                          (user_id, username, chat_id))
    db_connection.commit()

    # команда для передачи в клиент, который мы будем тестировать
    command = """
    SELECT * FROM users;
    """

    # создаем клиент, который будем тестировать
    client = SQLiteClient(TEST_DB_URL)
    client.create_conn()
    users = client.execute_select_command(command)

    # проверяем, что достали из базы желаемые значения
    assert len(users) == 1
    user = users[0]
    assert user[0] == user_id
    assert user[1] == username
    assert user[2] == chat_id

    # удаляем таблицу
    db_connection.execute(DROP_USER_TABLE_QUERY)
    db_connection.commit()


# какие проблемы есть сейчас в коде?
# 1. ОЧЕНЬ МНОГО КОПИПАСТЫ!
# 2. Код паршиво читается
# 3. Код паршиво поддерживается


# Что делаем? Давайте для начала распилим всё на функции:
# 1. Функция для создания таблицы
# 2. Функция для удаления таблицы
# 3. Функция для записи тестовых данных о пользователе в базу
# 4. Функция для чтения тестовых данных о пользователе из базы
DB_CONNECTION = sqlite3.connect(TEST_DB_URL)


def create_user(user_id: int, username: str, chat_id: int):
    """функция для наполнения базы тестовыми данными"""
    DB_CONNECTION.execute("""INSERT INTO users (user_id, username, chat_id) VALUES (?, ?, ?);""",
                          (user_id, username, chat_id))
    DB_CONNECTION.commit()


def read_users():
    """функция чтения из тестовой базы данных"""
    cursor = DB_CONNECTION.cursor()
    cursor.execute("""SELECT * FROM users;""")
    return cursor.fetchall()

def create_tables():
    cursor = DB_CONNECTION.cursor()
    cursor.execute(CREATE_USER_TABLE_QUERY)


def drop_tables():
    cursor = DB_CONNECTION.cursor()
    cursor.execute(DROP_USER_TABLE_QUERY)


def test_write_to_db_by_command_refactored():
    # запускаем команду для создания таблиц
    create_tables()

    # команда, которая будет использоваться для тестирования клиента
    command = """
    INSERT INTO users (user_id, username, chat_id) VALUES (?, ?, ?);
    """

    # тестовые данные
    user_id = 1
    username = "luchanos"
    chat_id = 123123

    # создаём клиент, который мы будем тестировать
    client = SQLiteClient(TEST_DB_URL)
    client.create_conn()

    # запускаем команду на запись в базу
    client.execute_command(command, (user_id, username, chat_id))

    # после этого ожидается, что в базе отобразится записанная строка и нам надо в этом убедиться.
    # используем функцию для чтения
    users = read_users()

    # проверяем, что в базу действительно всё прописалось
    assert len(users) == 1
    user = users[0]
    assert user[0] == user_id
    assert user[1] == username
    assert user[2] == chat_id

    # удаляем таблицу
    drop_tables()


def test_read_from_db_by_client_refactored():
    # запускаем команду для создания таблиц
    create_tables()

    # тестовые данные
    user_id = 1
    username = "luchanos"
    chat_id = 123123

    # создадим в базе строку с помощью функции, которую потом будем читать с помощью тестируемого клиента
    create_user(user_id, username, chat_id)

    # команда для передачи в клиент, который мы будем тестировать
    command = """
    SELECT * FROM users;
    """

    # создаем клиент, который будем тестировать
    client = SQLiteClient(TEST_DB_URL)
    client.create_conn()
    users = client.execute_select_command(command)

    # проверяем, что достали из базы желаемые значения
    assert len(users) == 1
    user = users[0]
    assert user[0] == user_id
    assert user[1] == username
    assert user[2] == chat_id

    # удаляем таблицу
    drop_tables()


# Что тут плохо?
# Всё ещё очень много лишних движений)
