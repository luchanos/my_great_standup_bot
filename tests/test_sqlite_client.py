from clients.sqlite3_client import SQLiteClient
from tests.conftest import TEST_DB_URL


def test_write_to_db_by_command(create_read_users_from_database_function):
    COMMAND = """
    INSERT INTO users (user_id, username, chat_id) VALUES (?, ?, ?);
    """
    user_id = 1
    username = "luchanos"
    chat_id = 123123
    client = SQLiteClient(TEST_DB_URL)
    client.create_conn()
    client.execute_command(COMMAND, (user_id, username, chat_id))
    users = create_read_users_from_database_function()
    assert len(users) == 1
    user = users[0]
    assert user[0] == user_id
    assert user[1] == username
    assert user[2] == chat_id


def test_read_from_db_by_client(create_test_user_in_database_function):  # передаем фикстуру, как параметр тестовой функции
    user_id = 1
    username = "luchanos"
    chat_id = 123123
    create_test_user_in_database_function(user_id, username, chat_id)
    COMMAND = """
    SELECT * FROM users;
    """
    client = SQLiteClient(TEST_DB_URL)
    client.create_conn()
    users = client.execute_select_command(COMMAND)
    assert len(users) == 1
    user = users[0]
    assert user[0] == user_id
    assert user[1] == username
    assert user[2] == chat_id
