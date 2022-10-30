from datetime import date

from clients.sqlite3_client import SQLiteClient


class UserActioner:
    GET_USER = """
    SELECT user_id, username, chat_id FROM users WHERE user_id = %s;
    """

    CREATE_USER = """
    INSERT INTO users (user_id, username, chat_id) VALUES (?, ?, ?);
    """

    UPDATE_LAST_DATE = """
    UPDATE users SET last_updated_date = ? WHERE user_id = ?;
    """

    def __init__(self, database_client: SQLiteClient):
        self.database_client = database_client

    def setup(self):
        self.database_client.create_conn()

    def shutdown(self):
        self.database_client.close_conn()

    def get_user(self, user_id: str):
        user = self.database_client.execute_select_command(self.GET_USER % user_id)
        return user[0] if user else []

    def create_user(self, user_id: str, username: str, chat_id: int):
        self.database_client.execute_command(self.CREATE_USER, (user_id, username, chat_id))

    def update_date(self, user_id: str, updated_date: date):
        self.database_client.execute_command(self.UPDATE_LAST_DATE, (updated_date, user_id))
