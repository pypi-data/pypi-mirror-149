import time
import unittest
from time import sleep

from watergrid.locks import RedisPipelineLock


class PipelineTestCase(unittest.TestCase):
    def test_can_connect(self):
        redis_lock = RedisPipelineLock()
        redis_lock.connect()

    def test_can_cycle_lock(self):
        redis_lock = RedisPipelineLock()
        redis_lock.connect()
        redis_lock.lock()
        self.assertTrue(redis_lock.has_lock())
        redis_lock.unlock()

    def test_can_set_host(self):
        redis_lock = RedisPipelineLock()
        redis_lock.set_host("localhost")

    def test_can_set_port(self):
        redis_lock = RedisPipelineLock()
        redis_lock.set_port(6379)

    def test_can_set_db(self):
        redis_lock = RedisPipelineLock()
        redis_lock.set_db(0)

    def test_can_set_password(self):
        redis_lock = RedisPipelineLock()
        redis_lock.set_password("password")

    def test_can_renew_lock(self):
        redis_lock = RedisPipelineLock()
        redis_lock.connect()
        redis_lock.lock()
        redis_lock.extend_lease()
        redis_lock.unlock()

    def test_can_write_keys(self):
        redis_lock = RedisPipelineLock()
        redis_lock.connect()
        redis_lock.write_key("key", "value3")
        self.assertEqual("value3", redis_lock.read_key("key").decode("utf-8"))

    def test_can_write_timestamps(self):
        redis_lock = RedisPipelineLock()
        timestamp = time.time()
        redis_lock.connect()
        redis_lock.write_key("timekey", timestamp)
        self.assertEqual(
            timestamp, float(redis_lock.read_key("timekey").decode("utf-8"))
        )
