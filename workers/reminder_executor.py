from logging import getLogger, StreamHandler

from clients.sqlite3_client import SQLiteClient
from clients.telegram_client import TelegramClient
from workers.reminder import Reminder
import datetime
import time
from envparse import Env

logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel("INFO")
env = Env()
TOKEN = env.str("TOKEN")
FROM_TIME = env.str("FROM_TIME")
TO_TIME = env.str("TO_TIME")

database_client = SQLiteClient("/Users/nnsviridov/PycharmProjects/ProdProjects/my_great_standup_bot/users.db")
telegram_client = TelegramClient(token=TOKEN,
                                 base_url="https://api.telegram.org")
reminder = Reminder(database_client=database_client, telegram_client=telegram_client)
reminder.setup()
reminder()

start_time = datetime.datetime.strptime(FROM_TIME, '%H:%M').time()
end_time = datetime.datetime.strptime(TO_TIME, '%H:%M').time()
while True:
    now_time = datetime.datetime.now().time()
    if start_time <= now_time <= end_time:
        reminder()
        time.sleep(3600)
    else:
        time.sleep(3600_0)
