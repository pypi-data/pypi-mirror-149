import time
from abc import ABC, abstractmethod


class PipelineLock(ABC):
    def __init__(self, lock_timeout: int = 60):
        self.lock_timeout = lock_timeout
        self.__start_time = None
        self.__has_lock = False

    def lock(self) -> bool:
        if self.has_lock():
            raise RuntimeError("Lock already acquired")
        if self.acquire():
            self.__start_time = time.perf_counter()
            self.__has_lock = True
            return True
        return False

    def ping(self):
        if not self.has_lock():
            raise RuntimeError("Lock not acquired")
        if not self.has_lock():
            raise RuntimeError("Lock was lost")
        lock_time = time.perf_counter() - self.__start_time
        if lock_time > (self.lock_timeout * 0.9):
            self.extend_lease()

    def unlock(self):
        if not self.has_lock():
            raise RuntimeError("Lock not acquired")
        self.release()
        self.__has_lock = False

    @abstractmethod
    def acquire(self) -> bool:
        pass

    @abstractmethod
    def has_lock(self) -> bool:
        pass

    @abstractmethod
    def extend_lease(self):
        pass

    @abstractmethod
    def release(self):
        pass

    @abstractmethod
    def read_key(self, key: str):
        pass

    @abstractmethod
    def write_key(self, key: str, value):
        pass
