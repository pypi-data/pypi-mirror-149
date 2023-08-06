import unittest

from watergrid.context import DataContext
from watergrid.metrics.ConsoleMetricsExporter import ConsoleMetricsExporter
from watergrid.pipelines.pipeline import Pipeline
from watergrid.steps import Step


class MockStep(Step):
    def __init__(self, throw_exception=False):
        self.throw_exception = throw_exception
        super().__init__(self.__class__.__name__)

    def run(self, context: DataContext):
        if self.throw_exception:
            raise Exception("MockStep failed")


class ConsoleMetricsExporterTestCase(unittest.TestCase):
    def test_outputs_pipeline_start(self):
        pipeline = Pipeline("test_pipeline")
        pipeline.add_metrics_exporter(ConsoleMetricsExporter())
        with self.assertLogs() as captured:
            pipeline.run()
        self.assertIn("INFO:root:Starting pipeline: test_pipeline", captured.output)

    def test_outputs_pipeline_end(self):
        pipeline = Pipeline("test_pipeline")
        pipeline.add_metrics_exporter(ConsoleMetricsExporter())
        with self.assertLogs() as captured:
            pipeline.run()
        self.assertIn("INFO:root:Ending pipeline", captured.output)

    def test_outputs_pipeline_end_with_error(self):
        pipeline = Pipeline("test_pipeline")
        pipeline.add_metrics_exporter(ConsoleMetricsExporter())
        pipeline.add_step(MockStep(throw_exception=True))
        with self.assertLogs() as captured:
            pipeline.run()
        self.assertIn("ERROR:root:Exception: MockStep failed", captured.output)

    def test_outputs_step_start(self):
        pipeline = Pipeline("test_pipeline")
        pipeline.add_metrics_exporter(ConsoleMetricsExporter())
        pipeline.add_step(MockStep())
        with self.assertLogs() as captured:
            pipeline.run()
        self.assertIn("INFO:root:Starting step: MockStep", captured.output)

    def test_outputs_step_end(self):
        pipeline = Pipeline("test_pipeline")
        pipeline.add_metrics_exporter(ConsoleMetricsExporter())
        pipeline.add_step(MockStep())
        with self.assertLogs() as captured:
            pipeline.run()
        self.assertIn("INFO:root:Ending step", captured.output)


if __name__ == "__main__":
    unittest.main()
