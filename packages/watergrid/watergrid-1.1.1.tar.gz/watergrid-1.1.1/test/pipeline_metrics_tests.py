import unittest

from watergrid.context import DataContext
from watergrid.metrics.MetricsExporter import MetricsExporter
from watergrid.pipelines.pipeline import Pipeline
from watergrid.steps import Step


class MockMetricsExporter(MetricsExporter):
    def start_pipeline(self, pipeline_name):
        self.__pipeline_start = True

    def end_pipeline(self):
        self.__pipeline_end = True

    def start_step(self, step_name):
        self.__step_start += 1

    def end_step(self):
        self.__step_end += 1

    def get_pipeline_start(self):
        return self.__pipeline_start

    def get_pipeline_end(self):
        return self.__pipeline_end

    def get_step_start(self):
        return self.__step_start

    def get_step_end(self):
        return self.__step_end

    def get_excpetion_raised(self):
        return self.__exception_raised

    def capture_exception(self, exception: Exception):
        self.__exception_raised = True

    def __init__(self, step_count):
        self.__pipeline_start = False
        self.__pipeline_end = False
        self.__step_start = 0
        self.__step_end = 0
        self.__step_count = step_count
        self.__exception_raised = False
        super().__init__()


class MockStep(Step):
    def __init__(self, throw_exception=False):
        super().__init__(self.__class__.__name__)
        self.mock_flag = False
        self.throw_exception = throw_exception

    def run(self, context: DataContext):
        self.mock_flag = True
        if self.throw_exception:
            raise Exception("Mock exception")

    def get_flag(self):
        return self.mock_flag


class PipelineMetricsTestCase(unittest.TestCase):
    def test_pipeline_accepts_metrics(self):
        pipeline = Pipeline("test_pipeline")
        exporter = MockMetricsExporter(1)
        pipeline.add_metrics_exporter(exporter)
        step1 = MockStep()
        pipeline.add_step(step1)
        pipeline.run()
        self.assertTrue(step1.get_flag())
        self.assertTrue(exporter.get_pipeline_start())
        self.assertTrue(exporter.get_pipeline_end())
        self.assertEqual(1, exporter.get_step_start())
        self.assertEqual(1, exporter.get_step_end())
        self.assertFalse(exporter.get_excpetion_raised())

    def test_pipeline_measures_two_steps(self):
        pipeline = Pipeline("test_pipeline")
        exporter = MockMetricsExporter(2)
        pipeline.add_metrics_exporter(exporter)
        step1 = MockStep()
        step2 = MockStep()
        pipeline.add_step(step1)
        pipeline.add_step(step2)
        pipeline.run()
        self.assertTrue(step1.get_flag())
        self.assertTrue(step2.get_flag())
        self.assertTrue(exporter.get_pipeline_start())
        self.assertTrue(exporter.get_pipeline_end())
        self.assertEqual(2, exporter.get_step_start())
        self.assertEqual(2, exporter.get_step_end())
        self.assertFalse(exporter.get_excpetion_raised())

    def test_metrics_captures_exception(self):
        pipeline = Pipeline("test_pipeline")
        exporter = MockMetricsExporter(1)
        pipeline.add_metrics_exporter(exporter)
        step1 = MockStep(True)
        pipeline.add_step(step1)
        pipeline.run()
        self.assertTrue(step1.get_flag())
        self.assertTrue(exporter.get_pipeline_start())
        self.assertTrue(exporter.get_pipeline_end())
        self.assertEqual(1, exporter.get_step_start())
        self.assertEqual(1, exporter.get_step_end())
        self.assertTrue(exporter.get_excpetion_raised())


if __name__ == "__main__":
    unittest.main()
