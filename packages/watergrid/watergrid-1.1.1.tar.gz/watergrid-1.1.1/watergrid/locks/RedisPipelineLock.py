from redis import Redis
from redis.lock import Lock

from watergrid.locks.PipelineLock import PipelineLock


class RedisPipelineLock(PipelineLock):
    def __init__(self, lock_timeout: int = 60):
        super().__init__(lock_timeout=lock_timeout)
        self._lock_key = "pipeline-lock"
        self._redis_host = "localhost"
        self._redis_port = 6379
        self._redis_db = 0
        self._redis_password = None
        self.__redis = None
        self.__lock = None

    def connect(self):
        self.__redis = Redis(
            host=self._redis_host,
            port=self._redis_port,
            db=self._redis_db,
            password=self._redis_password,
        )
        self.__redis.ping()
        self.__lock = Lock(self.__redis, self._lock_key, timeout=self.lock_timeout)

    def set_host(self, host: str):
        self._redis_host = host

    def set_port(self, port: int):
        self._redis_port = port

    def set_db(self, db: int):
        self._redis_db = db

    def set_password(self, password: str):
        self._redis_password = password

    def acquire(self) -> bool:
        return self.__lock.acquire(blocking=False)

    def has_lock(self) -> bool:
        return self.__lock.owned()

    def extend_lease(self):
        self.__lock.extend(self.lock_timeout)

    def release(self):
        self.__lock.release()

    def read_key(self, key: str):
        return self.__redis.get(key)

    def write_key(self, key: str, value: str):
        self.__redis.set(key, value)
