import redis
import logging
from dotenv import dotenv_values
from constants.error_message import ErrorMessage


class CacheManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = dotenv_values(".env")
        # self.key_prefix = key_prefix
        self.cache = None
        self.connect()

    def __call__(self, *args, **kwargs):
        return self.cache

    def connect(self):
        try:
            pool = redis.ConnectionPool(host=self.config["REDIS_HOST"], port=self.config["REDIS_PORT"],
                                        )
            self.cache = redis.Redis(connection_pool=pool, decode_responses=True,
                                     password=self.config["REDIS_PASSWORD"])

        except Exception as error:
            self.logger.error(ErrorMessage.REDIS_CONNECTION)
            self.logger.error(error)
            raise Exception

    def hget(self, key: str):
        try:
            value = self.cache.hgetall(key)
        except Exception as error:
            self.logger.error(ErrorMessage.REDIS_GET)
            self.logger.error(error)
            raise Exception
        return value

    def hset(self, key: str, value: dict):
        try:
            return self.cache.hset(key, mapping=value)
        except Exception as error:
            self.logger.error(ErrorMessage.REDIS_SET)
            self.logger.error(error)
            raise Exception

    def delete(self, key):
        try:
            return self.cache.delete(key)
        except Exception as error:
            self.logger.error(ErrorMessage.REDIS_DELETE)
            self.logger.error(error)
            raise Exception
