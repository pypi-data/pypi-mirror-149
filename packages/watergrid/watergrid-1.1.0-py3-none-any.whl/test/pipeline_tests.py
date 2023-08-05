import unittest

from watergrid.context import DataContext
from watergrid.pipelines.pipeline import Pipeline
from watergrid.steps import Step


class MockStep(Step):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        self.mock_flag = False

    def run(self, context: DataContext):
        self.mock_flag = True

    def get_flag(self):
        return self.mock_flag


class PipelineTestCase(unittest.TestCase):
    def test_create_pipeline(self):
        pipeline = Pipeline("test_pipeline")
        self.assertIsNotNone(pipeline)

    def test_pipeline_runs_step(self):
        step = MockStep()
        pipeline = Pipeline("test_pipeline")
        pipeline.add_step(step)
        pipeline.run()
        self.assertTrue(step.get_flag())

    def test_pipeline_runs_multiple_steps(self):
        step1 = MockStep()
        step2 = MockStep()
        pipeline = Pipeline("test_pipeline")
        pipeline.add_step(step1)
        pipeline.add_step(step2)
        pipeline.run()
        self.assertTrue(step1.get_flag())
        self.assertTrue(step2.get_flag())


if __name__ == "__main__":
    unittest.main()
