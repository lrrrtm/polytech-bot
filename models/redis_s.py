from os import getenv

import redis as redis_server
from dotenv import load_dotenv

load_dotenv()

class Redis:
    def __init__(self):
        self.connection = None

    def reconnect(self):
        self.connection = redis_server.StrictRedis(
            host=getenv('REDIS_HOST'),
            port=getenv('REDIS_PORT'),
            db=getenv('REDIS_DB'),
        )

    def set_value(self, key: str, value):
        self.reconnect()
        self.connection.set(key, value, 10)

    def get_value(self, key: str):
        self.reconnect()
        return self.connection.get(key)

    # def set_user_settings_token(self, user_id: int, token: str):
    #     self.set_value(str(user_id), token, ttl=30)