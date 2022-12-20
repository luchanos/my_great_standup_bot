import sqlite3
import pytest

TEST_DB_URL = "/Users/nnsviridov/PycharmProjects/ProdProjects/my_great_standup_bot/users.db"


@pytest.fixture(scope="session")  # будет вызвана 1 раз за всё время прогона тестовой сессии
def db_connection():
    """Фикстура для создания соединения с базой"""
    return sqlite3.connect(TEST_DB_URL)


@pytest.fixture(scope="function", autouse=True)  # будет вызываться автоматически перед началом запуска нового теста
def clean_database(db_connection):  # передаем на вход результат работы другой фикстуры
    """Фикстура для очищения базы от данных до прогона теста"""
    db_connection.execute("DELETE FROM users;")
    db_connection.commit()


@pytest.fixture(scope="session")
def create_test_user_in_database_function(db_connection):  # фикстура использует результат работы другой фикстуры
    """Фикстура для создания функции для наполнения базы тестовыми данными"""
    debug_point = 1

    def create_user(user_id: int, username: str, chat_id: int):
        """функция для наполнения базы тестовыми данными"""
        db_connection.execute("""INSERT INTO users (user_id, username, chat_id) VALUES (?, ?, ?);""",
                              (user_id, username, chat_id))
        db_connection.commit()
    return create_user


@pytest.fixture(scope="session")
def create_read_users_from_database_function(db_connection):  # фикстура использует результат работы другой фикстуры
    """Фикстура для создания функции для чтения данных из тестовой базы"""
    debug_point = 1

    def read_users():
        """функция чтения из тестовой базы данных"""
        cursor = db_connection.cursor()
        cursor.execute("""SELECT * FROM users;""")
        return cursor.fetchall()
    return read_users
