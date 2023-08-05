import time
import unittest

from watergrid.context import DataContext
from watergrid.locks import MockPipelineLock
from watergrid.pipelines import HAPipeline
from watergrid.steps import Step


class MockStep(Step):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        self.mock_flag = False

    def run(self, context: DataContext):
        self.mock_flag = True

    def get_flag(self):
        return self.mock_flag


class HAPipelineTestCase(unittest.TestCase):
    def test_pipeline_does_not_runs_without_lock(self):
        step1 = MockStep()
        step2 = MockStep()
        mock_lock = MockPipelineLock()
        pipeline = HAPipeline("test_pipeline", mock_lock)
        pipeline.add_step(step1)
        pipeline.add_step(step2)
        mock_lock.manual_lock()
        pipeline.run()
        self.assertFalse(step1.get_flag())
        self.assertFalse(step2.get_flag())

    def test_pipeline_runs_with_lock(self):
        step1 = MockStep()
        step2 = MockStep()
        mock_lock = MockPipelineLock()
        pipeline = HAPipeline("test_pipeline", mock_lock)
        pipeline.add_step(step1)
        pipeline.add_step(step2)
        pipeline.run()
        self.assertTrue(step1.get_flag())
        self.assertTrue(step2.get_flag())

    def test_pipeline_releases_lock(self):
        step1 = MockStep()
        step2 = MockStep()
        mock_lock = MockPipelineLock()
        pipeline = HAPipeline("test_pipeline", mock_lock)
        pipeline.add_step(step1)
        pipeline.add_step(step2)
        pipeline.run()
        self.assertFalse(mock_lock.has_lock())

    def test_pipeline_calculates_redis_delay(self):
        pipeline = HAPipeline("test_pipeline", MockPipelineLock())
        pipeline._append_timing(10000)
        pipeline._append_timing(20000)
        self.assertEqual(15000, pipeline.get_average_lock_delay())

    def test_pipeline_calculates_job_interval_delay(self):
        pipeline = HAPipeline("test_pipeline", MockPipelineLock())
        self.assertEqual(3000, pipeline._calculate_delay(10))

    def test_pipline_does_not_run_interval_without_lock(self):
        step1 = MockStep()
        pipeline_lcok = MockPipelineLock()
        pipeline = HAPipeline("test_pipeline", pipeline_lcok)
        pipeline.add_step(step1)
        pipeline_lcok.manual_lock()
        pipeline._run_interval_loop(10)
        self.assertFalse(step1.get_flag())

    def test_pipeline_generates_lock_name(self):
        pipeline = HAPipeline("test_pipeline", MockPipelineLock())
        self.assertEqual("test_pipeline_last_run", pipeline._get_pipeline_lock_name())

    def test_pipeline_waits_for_target_time(self):
        step1 = MockStep()
        pipeline_lock = MockPipelineLock()
        pipeline = HAPipeline("test_pipeline", pipeline_lock)
        pipeline.add_step(step1)
        pipeline._set_last_run(time.time() + 30)
        pipeline._run_interval_loop(10)
        self.assertFalse(step1.get_flag())

    def test_pipeline_runs_interval_with_target_time(self):
        step1 = MockStep()
        pipeline_lock = MockPipelineLock()
        pipeline = HAPipeline("test_pipeline", pipeline_lock)
        pipeline.add_step(step1)
        pipeline._set_last_run(time.time() - 20)
        pipeline._run_interval_loop(10)
        self.assertTrue(step1.get_flag())

    def test_pipeline_sets_metadata(self):
        step1 = MockStep()
        pipeline_lock = MockPipelineLock()
        pipeline = HAPipeline("test_pipeline", pipeline_lock)
        pipeline.add_step(step1)
        pipeline._run_interval_loop(10)
        self.assertIsNotNone(pipeline._get_last_run())

    def test_pipeline_locks_with_benchmarking(self):
        pipeline_lock = MockPipelineLock()
        pipeline = HAPipeline("test_pipeline", pipeline_lock)
        pipeline.lock_with_timing()
        self.assertTrue(pipeline_lock.has_lock())
        pipeline.unlock_with_timing()
        self.assertFalse(pipeline_lock.has_lock())
        self.assertNotEqual(0, pipeline.get_average_lock_delay())


if __name__ == "__main__":
    unittest.main()
