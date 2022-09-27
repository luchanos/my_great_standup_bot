# import requests
#
#
# class TelegramClient:
#     def __init__(self, token: str, base_url: str):
#         self.token = token
#         self.base_url = base_url
#
#     def prepare_url(self, method: str):
#         result_url = f"{self.base_url}/bot{self.token}/"
#         if method is not None:
#             result_url += method
#         return result_url
#
#     def post(self, method: str = None, params: dict = None, body: dict = None):
#         url = self.prepare_url(method)
#         resp = requests.post(url, params=params, data=body)
#         return resp.json()
#
#
# token = "5200212331:AAH5oY0ZR5B8f0JkS8ckU6w6GMVHE-sOEcI"
# telegram_client = TelegramClient(token=token, base_url="https://api.telegram.org")
# my_params = {"chat_id": 362857450, "text": "sczxcvzxcvzxcvzx"}
# print(telegram_client.post(method="sendMessage", params=my_params))

import sqlite3

# conn = sqlite3.connect("users.db")
#
# CREATE_QUERY = """
#     CREATE TABLE IF NOT EXISTS users (
#         user_id int PRIMARY KEY,
#         username text,
#         chat_id int
#     );
# """
# conn.execute(CREATE_QUERY)
#
# conn.execute("""INSERT INTO users (user_id, username, chat_id) VALUES (1, 'luchanos', 123);""")
#
# conn.commit()


class SQLiteClient:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.conn = None

    def create_conn(self):
        self.conn = sqlite3.connect(self.filepath, check_same_thread=False)

    def execute_command(self, command: str, params: tuple):
        if self.conn is not None:
            self.conn.execute(command, params)
            self.conn.commit()
        else:
            raise ConnectionError("you need to create connection to database!")

    def execute_select_command(self, command: str):
        if self.conn is not None:
            cur = self.conn.cursor()
            cur.execute(command)
            return cur.fetchall()
        else:
            raise ConnectionError("you need to create connection to database!")


class UserActioner:
    GET_USER = """
    SELECT user_id, username, chat_id FROM users WHERE user_id = %s;
    """

    CREATE_USER = """
    INSERT INTO users (user_id, username, chat_id) VALUES (?, ?, ?);
    """

    def __init__(self, database_client: SQLiteClient):
        self.database_client = database_client

    def setup(self):
        self.database_client.create_conn()

    def get_user(self, user_id: str):
        user = self.database_client.execute_select_command(self.GET_USER % user_id)
        return user[0] if user else user

    def create_user(self, user_id: str, username: str, chat_id: int):
        self.database_client.execute_command(self.CREATE_USER, (user_id, username, chat_id))



