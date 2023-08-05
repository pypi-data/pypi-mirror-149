import unittest

from watergrid.locks import MockPipelineLock


class PipelineLockTests(unittest.TestCase):
    def test_can_acquire_lock(self):
        lock = MockPipelineLock()
        lock.lock()
        self.assertTrue(lock.has_lock())

    def test_can_release_lock(self):
        lock = MockPipelineLock()
        lock.lock()
        lock.unlock()
        self.assertFalse(lock.has_lock())

    def test_cannot_release_missing_lock(self):
        lock = MockPipelineLock()
        with self.assertRaises(RuntimeError):
            lock.unlock()

    def test_cannot_double_lock(self):
        lock = MockPipelineLock()
        lock.lock()
        with self.assertRaises(RuntimeError):
            lock.lock()

    def test_can_ping_acquired_lock(self):
        lock = MockPipelineLock()
        lock.lock()
        lock.ping()

    def test_ping_fails_on_lock_lost(self):
        lock = MockPipelineLock()
        lock.lock()
        lock.manual_lock()
        with self.assertRaises(RuntimeError):
            lock.ping()

    def test_cannot_ping_missing_lock(self):
        lock = MockPipelineLock()
        with self.assertRaises(RuntimeError):
            lock.ping()


if __name__ == "__main__":
    unittest.main()
