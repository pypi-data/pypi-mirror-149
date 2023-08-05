from watergrid.locks.PipelineLock import PipelineLock


class MockPipelineLock(PipelineLock):
    def read_key(self, key: str):
        try:
            return self.__key_value[key]
        except KeyError:
            return None

    def write_key(self, key: str, value: str):
        self.__key_value[key] = value

    def __init__(self, lock_timeout: int = 60):
        super().__init__(lock_timeout)
        self.external_lock = False
        self.client_lock = False
        self.__key_value = {}

    def manual_lock(self):
        self.external_lock = True
        self.client_lock = False

    def manual_unlock(self):
        self.external_lock = False

    def acquire(self) -> bool:
        if not self.external_lock:
            self.client_lock = True
            return True
        else:
            return False

    def has_lock(self) -> bool:
        return self.client_lock

    def extend_lease(self):
        pass

    def release(self):
        self.client_lock = False
